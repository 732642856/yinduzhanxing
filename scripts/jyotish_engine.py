#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
印度占星统一引擎 v3.7.0 (Jyotish Unified Engine)
整合所有计算能力为单一CLI入口，供Skill调用

子命令:
  chart        计算完整星盘（基于Swiss Ephemeris）
  dasha        计算Vimshottari Dasha大运时间线
  yoga         Yoga格局识别
  predict      三层验证法事件预测（优先EventPredictionModel规则引擎）
  varga        分盘计算（D9/D10）
  varga-full   BPHS十六分盘完整计算（D2-D60）（v3.7新增）
  aspects      度数精确相位系统（v3.7新增）
  jaimini      Jaimini系统（Chara Karaka/Chara Dasha/Karakamsha）（v3.7新增）
  nakshatra-adv 高级Nakshatra分析（Tara Bala/Sub-Lord/兼容性）（v3.7新增）
  argala       Argala门闩系统（v3.7新增）
  tajika       Tajika/Varshaphala年运盘（v3.7新增）
  synastry     合盘分析（Ashta Koota 36分制+Mangal Dosha）（v3.7新增）
  celebrity    名人案例查询（15,807条数据+SQLite验证库）
  db-stats     验证数据库统计
  transit      行星过境查询
  shadbala     六重力量计算（v3.4新增）
  ashtakavarga 八分法计算（v3.5升级BPHS完整表，SAV=337）
  memory       Hermes记忆系统（v3.4新增）
  validate     R1-R10数学验证（v3.5新增，含R2b BAV列→SAV校验）
  audit        P1-P12行星审计管线（v3.6升级含P3仓库耦合+P8年龄状态+冲突仲裁）
  report       MD→HTML报告生成（v3.6新增，羊皮纸主题）

用法示例:
  python3 jyotish_engine.py chart --year 1993 --month 4 --day 17 --hour 14 --minute 45 --lat 36.6 --lon 114.5 --tz 8
  python3 jyotish_engine.py shadbala --year 1993 --month 4 --day 17 --hour 14 --minute 45 --lat 36.6 --lon 114.5 --tz 8
  python3 jyotish_engine.py ashtakavarga --year 1993 --month 4 --day 17 --hour 14 --minute 45 --lat 36.6 --lon 114.5 --tz 8
  python3 jyotish_engine.py memory --action store --content "测试记忆"
"""

import argparse
import json
import sys
import os
import csv
import math
import sqlite3
from datetime import datetime, timedelta
from typing import Dict

# ============================================================================
# 路径常量
# ============================================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HOME_DIR = os.path.expanduser('~')
CLAW_DIR = os.path.join(HOME_DIR, 'WorkBuddy', 'Claw')
DB_PATH = os.path.join(CLAW_DIR, 'vedic_astrology_validation.db')
PERSON_CSV = os.path.join(CLAW_DIR, 'vedastro_data', 'PersonList-15k.csv')
TRANSIT_JSON = os.path.join(CLAW_DIR, '月运过境配置-2026-2028.json')

try:
    import swisseph as swe
    HAS_SWE = True
except ImportError:
    HAS_SWE = False

# ============================================================================
# 常量
# ============================================================================
NAKSHATRA_LIST = [
    ("Ashwini", "Ketu", 7), ("Bharani", "Venus", 20), ("Krittika", "Sun", 6),
    ("Rohini", "Moon", 10), ("Mrigashira", "Mars", 7), ("Ardra", "Rahu", 18),
    ("Punarvasu", "Jupiter", 16), ("Pushya", "Saturn", 19), ("Ashlesha", "Mercury", 17),
    ("Magha", "Ketu", 7), ("Purva Phalguni", "Venus", 20), ("Uttara Phalguni", "Sun", 6),
    ("Hasta", "Moon", 10), ("Chitra", "Mars", 7), ("Swati", "Rahu", 18),
    ("Vishakha", "Jupiter", 16), ("Anuradha", "Saturn", 19), ("Jyeshtha", "Mercury", 17),
    ("Mula", "Ketu", 7), ("Purva Ashadha", "Venus", 20), ("Uttara Ashadha", "Sun", 6),
    ("Shravana", "Moon", 10), ("Dhanishta", "Mars", 7), ("Shatabhisha", "Rahu", 18),
    ("Purva Bhadrapada", "Jupiter", 16), ("Uttara Bhadrapada", "Saturn", 19), ("Revati", "Mercury", 17),
]
DASHA_ORDER = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
DASHA_YEARS = {"Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7, "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17}
SIGNS = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
SIGNS_CN = {'Aries': '白羊座', 'Taurus': '金牛座', 'Gemini': '双子座', 'Cancer': '巨蟹座', 'Leo': '狮子座', 'Virgo': '处女座', 'Libra': '天秤座', 'Scorpio': '天蝎座', 'Sagittarius': '射手座', 'Capricorn': '摩羯座', 'Aquarius': '水瓶座', 'Pisces': '双鱼座'}
SIGN_LORDS = {'Aries': 'Mars', 'Taurus': 'Venus', 'Gemini': 'Mercury', 'Cancer': 'Moon', 'Leo': 'Sun', 'Virgo': 'Mercury', 'Libra': 'Venus', 'Scorpio': 'Mars', 'Sagittarius': 'Jupiter', 'Capricorn': 'Saturn', 'Aquarius': 'Saturn', 'Pisces': 'Jupiter'}
EXALTATION = {'Sun': 'Aries', 'Moon': 'Taurus', 'Mars': 'Capricorn', 'Mercury': 'Virgo', 'Jupiter': 'Cancer', 'Venus': 'Pisces', 'Saturn': 'Libra'}
DEBILITATION = {'Sun': 'Libra', 'Moon': 'Scorpio', 'Mars': 'Cancer', 'Mercury': 'Pisces', 'Jupiter': 'Capricorn', 'Venus': 'Virgo', 'Saturn': 'Aries'}
PLANET_CN = {"Ketu": "南交点Ketu", "Venus": "金星Venus", "Sun": "太阳Sun", "Moon": "月亮Moon", "Mars": "火星Mars", "Rahu": "北交点Rahu", "Jupiter": "木星Jupiter", "Saturn": "土星Saturn", "Mercury": "水星Mercury"}
PLANETS_SWE = {'Sun': swe.SUN, 'Moon': swe.MOON, 'Mars': swe.MARS, 'Mercury': swe.MERCURY, 'Jupiter': swe.JUPITER, 'Venus': swe.VENUS, 'Saturn': swe.SATURN, 'Rahu': swe.MEAN_NODE} if HAS_SWE else {}


def output_json(data):
    """统一JSON输出"""
    print(json.dumps(data, ensure_ascii=False, indent=2, default=str))


def _add_chart_args(p):
    """为需要出生数据的子命令添加公共参数"""
    p.add_argument('--year', type=int, required=True)
    p.add_argument('--month', type=int, required=True)
    p.add_argument('--day', type=int, required=True)
    p.add_argument('--hour', type=int, required=True)
    p.add_argument('--minute', type=int, required=True)
    p.add_argument('--lat', type=float, required=True)
    p.add_argument('--lon', type=float, required=True)
    p.add_argument('--tz', type=float, default=0)


# ============================================================================
# 公共星盘计算（供 chart/shadbala/ashtakavarga 共用，v3.4提取）
# ============================================================================
def compute_chart_data(year, month, day, hour, minute, lat, lon, tz):
    """计算星盘核心数据，返回 (result_dict, asc_idx, jd, ayanamsa)"""
    if not HAS_SWE:
        return None, None, None, None
    swe.set_ephe_path('')
    hour_decimal = hour + minute / 60.0 - tz
    jd = swe.julday(year, month, day, hour_decimal)
    ayanamsa = swe.get_ayanamsa(jd)

    result = {"birth_info": {
        "date": f"{year}-{month:02d}-{day:02d}", "time": f"{hour:02d}:{minute:02d}",
        "tz": f"UTC{'+' if tz >= 0 else ''}{tz}", "lat": lat, "lon": lon,
        "julian_day": round(jd, 6), "ayanamsa": round(ayanamsa, 4)
    }, "ascendant": None, "planets": {}, "houses": {}}

    asc_lon, _ = swe.houses(jd, lat, lon, b'A')
    asc_deg = (asc_lon[0] - ayanamsa) % 360
    asc_idx = int(asc_deg / 30)
    asc_sign = SIGNS[asc_idx]
    result["ascendant"] = {"sign": asc_sign, "sign_cn": SIGNS_CN[asc_sign],
        "degree": round(asc_deg, 4), "degree_in_sign": round(asc_deg - asc_idx * 30, 4),
        "lord": SIGN_LORDS[asc_sign]}

    for i in range(12):
        c = (asc_lon[i] - ayanamsa) % 360
        si = int(c / 30)
        result["houses"][f"house_{i+1}"] = {"cusp_sign": SIGNS[si],
            "cusp_sign_cn": SIGNS_CN[SIGNS[si]], "cusp_degree": round(c, 4),
            "lord": SIGN_LORDS[SIGNS[si]]}

    nak_span = 360.0 / 27
    for pname, pid in PLANETS_SWE.items():
        try:
            pos, _ = swe.calc_ut(jd, pid)
            lon_p = (pos[0] - ayanamsa) % 360; lat_p = pos[1]; spd = pos[3]
            si = int(lon_p / 30); d_in_s = lon_p - si * 30; sign = SIGNS[si]
            retro = spd < 0
            house = ((si - asc_idx) % 12) + 1
            status = "中性"
            if EXALTATION.get(pname) == sign: status = "入庙(Exalted)"
            elif DEBILITATION.get(pname) == sign: status = "落陷(Debilitated)"
            elif SIGN_LORDS.get(sign) == pname: status = "入庙(Own Sign)"
            ni = int(lon_p / nak_span); pada = int((lon_p % nak_span) / (nak_span / 4)) + 1
            nak_n, nak_l, _ = NAKSHATRA_LIST[ni % 27]
            result["planets"][pname] = {
                "sign": sign, "sign_cn": SIGNS_CN[sign], "degree": round(lon_p, 4),
                "degree_in_sign": round(d_in_s, 4), "house": house, "status": status,
                "retrograde": retro, "speed": round(spd, 6),
                "nakshatra": nak_n, "nakshatra_pada": pada, "nakshatra_lord": nak_l}
            if pname == 'Rahu':
                klon = (lon_p + 180) % 360; ksi = int(klon / 30); kd = klon - ksi * 30
                kni = int(klon / nak_span); kp = int((klon % nak_span) / (nak_span / 4)) + 1
                kn, kl, _ = NAKSHATRA_LIST[kni % 27]
                result["planets"]["Ketu"] = {
                    "sign": SIGNS[ksi], "sign_cn": SIGNS_CN[SIGNS[ksi]],
                    "degree": round(klon, 4), "degree_in_sign": round(kd, 4),
                    "house": ((ksi - asc_idx) % 12) + 1, "status": "中性",
                    "retrograde": True, "speed": round(spd, 6),
                    "nakshatra": kn, "nakshatra_pada": kp, "nakshatra_lord": kl}
        except Exception as e:
            result["planets"][pname] = {"error": str(e)}
    return result, asc_idx, jd, ayanamsa


# ============================================================================
# 1. 星盘计算
# ============================================================================
def cmd_chart(args):
    result, asc_idx, jd, ayanamsa = compute_chart_data(args.year, args.month, args.day, args.hour, args.minute, args.lat, args.lon, args.tz)
    if result is None:
        return {"error": "swisseph未安装"}
    # v3.5: --validate 触发 R1-R10 校验
    if getattr(args, 'validate', False):
        try:
            sys.path.insert(0, SCRIPT_DIR)
            from ashtakavarga import calc_ashtakavarga
            asht_result = calc_ashtakavarga(result.get('planets', {}), asc_idx)
            from validate import validate_chart
            validation = validate_chart(result, asht_result)
            result['validation'] = validation
        except Exception as e:
            result['validation'] = {"error": str(e), "valid": False}
    return result


# ============================================================================
# 2. Dasha计算
# ============================================================================
def cmd_dasha(args):
    nak_info = None; progress = 0.5
    if args.moon_lon is not None:
        ns = 360.0 / 27; idx = int(args.moon_lon / ns); progress = (args.moon_lon % ns) / ns
        nak_info = NAKSHATRA_LIST[idx % 27]
    elif args.nakshatra:
        nl = args.nakshatra.lower().replace(" ", "").replace("-", "")
        for n in NAKSHATRA_LIST:
            if nl in n[0].lower().replace(" ", "") or n[0].lower().replace(" ", "").startswith(nl[:5]):
                nak_info = n; break
        if not nak_info: return {"error": f"未找到Nakshatra: {args.nakshatra}"}
        if args.pada: progress = (max(1, min(4, args.pada)) - 1) / 4 + 0.125
    else:
        return {"error": "请提供 --nakshatra 或 --moon-lon"}

    nak_name, start_lord, start_years = nak_info
    birth_dt = datetime.strptime(args.birthdate, "%Y-%m-%d")
    elapsed = progress * start_years; remaining = start_years - elapsed
    dt = birth_dt - timedelta(days=elapsed * 365.25)
    si = DASHA_ORDER.index(start_lord)
    timeline = []
    for i in range(9):
        lord = DASHA_ORDER[(si + i) % 9]; years = DASHA_YEARS[lord]
        end_dt = dt + timedelta(days=years * 365.25)
        timeline.append({"lord": lord, "lord_cn": PLANET_CN[lord], "start": dt.strftime("%Y-%m-%d"), "end": end_dt.strftime("%Y-%m-%d"), "years": years})
        dt = end_dt

    today = datetime.strptime(args.today, "%Y-%m-%d") if args.today else datetime.now()
    current = None
    for d in timeline:
        ds = datetime.strptime(d["start"], "%Y-%m-%d"); de = datetime.strptime(d["end"], "%Y-%m-%d")
        if ds <= today < de:
            total_days = (de - ds).days; li = DASHA_ORDER.index(d["lord"])
            sub = []; sdt = ds
            for j in range(9):
                sl = DASHA_ORDER[(li + j) % 9]; sd = total_days * DASHA_YEARS[sl] / 120
                se = sdt + timedelta(days=sd)
                sub.append({"lord": sl, "lord_cn": PLANET_CN[sl], "start": sdt.strftime("%Y-%m-%d"), "end": se.strftime("%Y-%m-%d"), "is_current": sdt <= today < se})
                sdt = se
            d["antardasha"] = sub; current = d; break

    return {"moon_nakshatra": nak_name, "birth_date": args.birthdate, "reference_date": today.strftime("%Y-%m-%d"), "timeline": timeline, "current_dasha": current}


# ============================================================================
# 3. Yoga识别
# ============================================================================
def cmd_yoga(args):
    planets = {}
    if args.planets:
        for item in args.planets.split(','):
            parts = item.strip().split(':')
            if len(parts) >= 3:
                planets[parts[0].strip()] = {"sign": parts[1].strip(), "house": int(parts[2].strip())}
    asc = args.ascendant or "Aries"
    ai = SIGNS.index(asc) if asc in SIGNS else 0
    kl = list(set([SIGN_LORDS[SIGNS[(ai + h - 1) % 12]] for h in [1, 4, 7, 10]]))
    tl = list(set([SIGN_LORDS[SIGNS[(ai + h - 1) % 12]] for h in [1, 5, 9]]))
    yogas = []

    # Raja Yoga
    for k in kl:
        for t in tl:
            if k != t and k in planets and t in planets and planets[k]["house"] == planets[t]["house"]:
                yogas.append({"name": "Raja Yoga", "name_cn": "王者格局", "combination": f"{k}+{t}同在第{planets[k]['house']}宫", "effects": ["权力地位", "事业成功", "社会影响力"], "strength": "强" if planets[k]["sign"] in [EXALTATION.get(k, ''), SIGN_LORDS.get(planets[k]["sign"], '')] else "中"})

    # Mahapurusha Yoga
    yoga_names = {'Mars': 'Ruchaka', 'Mercury': 'Bhadra', 'Jupiter': 'Hamsa', 'Venus': 'Malavya', 'Saturn': 'Sasa'}
    for p, info in planets.items():
        if info["house"] in [1, 4, 7, 10] and p in yoga_names:
            if EXALTATION.get(p) == info["sign"] or SIGN_LORDS.get(info["sign"]) == p:
                st = "入旺" if EXALTATION.get(p) == info["sign"] else "入庙"
                yogas.append({"name": f"{yoga_names[p]} Yoga", "name_cn": f"{PLANET_CN.get(p, p)}{st}格局", "combination": f"{p}{st}在{info['sign']}(第{info['house']}宫)", "effects": ["卓越才能", "领域领军", "人格魅力"], "strength": "极强" if st == "入旺" else "强"})

    # Gajakesari
    if 'Jupiter' in planets and 'Moon' in planets:
        jh = planets['Jupiter']['house']; mh = planets['Moon']['house']
        if jh in [1, 4, 7, 10] and mh in [1, 4, 7, 10]:
            yogas.append({"name": "Gajakesari Yoga", "name_cn": "象狮格局", "combination": f"木星第{jh}宫+月亮第{mh}宫", "effects": ["智慧学识", "财富名声", "道德品质"], "strength": "中"})

    # Neechabhanga
    for p, info in planets.items():
        if DEBILITATION.get(p) == info["sign"]:
            dl = SIGN_LORDS[info["sign"]]
            if dl in planets and planets[dl]["house"] in [1, 4, 7, 10]:
                yogas.append({"name": "Neechabhanga Raja Yoga", "name_cn": "落陷取消格局", "combination": f"{p}落陷在{info['sign']}，{dl}在角宫化解", "effects": ["克服困难", "逆境崛起", "转化能力"], "strength": "中强"})

    # Dhana Yoga
    wl = set(); wh = [2, 5, 9, 11]
    for h in wh:
        wl.add(SIGN_LORDS[SIGNS[(ai + h - 1) % 12]])
    wc = sum(1 for w in wl if w in planets and planets[w]["house"] in wh)
    if wc >= 2:
        yogas.append({"name": "Dhana Yoga", "name_cn": "财富格局", "combination": f"{wc}个财富宫主星落入财富宫", "effects": ["财富积累", "物质成功", "投资收益"], "strength": "中强" if wc >= 3 else "中"})

    return {"ascendant": asc, "planets_analyzed": len(planets), "kendra_lords": kl, "trikona_lords": tl, "yogas_detected": len(yogas), "yogas": yogas}


# ============================================================================
# 4. 三层验证法事件预测（v3.4增强：优先EventPredictionModel规则引擎）
# ============================================================================
def cmd_predict(args):
    # 验前事模式（v3.5新增）
    if getattr(args, 'past_verify', False) and args.year:
        chart, asc_idx, jd, ayanamsa = compute_chart_data(
            args.year, args.month, args.day, args.hour, args.minute,
            args.lat, args.lon, args.tz)
        if chart is None:
            return {"error": "swisseph未安装"}
        return _past_event_verify(chart, asc_idx, args)

    chart = json.loads(args.chart) if args.chart else {}
    evt = args.event_type or "all"

    # 尝试加载 EventPredictionModel（替代LAM神经网络）
    try:
        sys.path.insert(0, SCRIPT_DIR)
        from event_prediction_model import EventPredictionModel
        asc_sign = chart.get("ascendant", {}).get("sign", "Unknown")
        planets = chart.get("planets", {})
        # 构建模型需要的行星简化数据
        planet_positions = {}
        for pn, pd in planets.items():
            if isinstance(pd, dict) and 'house' in pd:
                planet_positions[pn] = {'sign': pd.get('sign', ''), 'house': pd.get('house', 0)}
        model = EventPredictionModel(chart_data={"ascendant": asc_sign, "planets": planet_positions})
        raw_preds = model.predict_all_events()
        # 将 Prediction dataclass 转为可序列化 dict
        predictions = []
        for p in raw_preds:
            predictions.append({
                "event_type": str(p.event_type.value) if hasattr(p.event_type, 'value') else str(p.event_type),
                "description": p.description,
                "probability": p.probability,
                "risk_level": str(p.risk_level.value) if hasattr(p.risk_level, 'value') else str(p.risk_level),
                "timing": p.timing,
                "key_factors": p.key_factors,
                "recommendations": p.recommendations,
            })
        return {
            "method": "三层验证法（EventPredictionModel规则引擎）",
            "engine": "event_prediction_model.py",
            "event_type": evt,
            "predictions": predictions,
            "note": "基于规则引擎的三层验证法，替代LAM神经网络（准确率从0.17%大幅提升）"
        }
    except Exception as e:
        # 降级到简化版
        result = {"method": "三层验证法（简化版）", "fallback_reason": str(e),
                  "event_type": evt, "predictions": []}
        planets = chart.get("planets", {})
        indicators_map = {
            "marriage": {"houses": [7], "karaka": "Venus", "cn": "婚姻"},
            "career": {"houses": [10, 6], "karaka": "Sun", "cn": "职业"},
            "wealth": {"houses": [2, 11], "karaka": "Jupiter", "cn": "财富"},
            "health": {"houses": [6, 8, 12], "karaka": "Saturn", "cn": "健康"},
        }
        for ek, ei in indicators_map.items():
            if evt != "all" and evt != ek: continue
            found = []
            for hn in ei["houses"]:
                for pn, pd in planets.items():
                    if isinstance(pd, dict) and pd.get("house") == hn:
                        found.append({"planet": pn, "house": hn, "sign": pd.get("sign", ""), "status": pd.get("status", "中性")})
            if found:
                result["predictions"].append({"event": ei["cn"], "key": ek, "static_indicators": found, "note": "需要结合Dasha和Transit进行精确预测"})
        return result


# ============================================================================
# 验前事模式（v3.5新增，避免冷读效应）
# ============================================================================
def _past_event_verify(chart: Dict, asc_idx: int, args) -> Dict:
    """
    验前事：从星盘数据推断 2-4 个高信号历史时段，供用户确认。
    AI 先推断，用户后确认——避免冷读效应。
    """
    planets = chart.get('planets', {})
    asc_sign = chart.get('ascendant', {}).get('sign', 'Unknown')
    birth_year = args.year

    signals = []

    # 1. 土星回归（约29.5年一次）
    saturn_sign = planets.get('Saturn', {}).get('sign', '')
    saturn_house = planets.get('Saturn', {}).get('house', 0)
    # 土星绕黄道一圈约29.5年
    for cycle_age in [29, 58]:
        event_year = birth_year + cycle_age
        signals.append({
            'type': '土星回归',
            'age': cycle_age,
            'year': event_year,
            'description': f'约{event_year}年（{cycle_age}岁），土星回归周期',
            'confidence': '高',
            'indicators': [f'土星在{saturn_sign}（第{saturn_house}宫）'],
        })

    # 2. 木星回归（约12年一次）
    jupiter_sign = planets.get('Jupiter', {}).get('sign', '')
    jupiter_house = planets.get('Jupiter', {}).get('house', 0)
    for cycle_age in [12, 24, 36, 48]:
        event_year = birth_year + cycle_age
        signals.append({
            'type': '木星回归',
            'age': cycle_age,
            'year': event_year,
            'description': f'约{event_year}年（{cycle_age}岁），木星回归周期',
            'confidence': '中高',
            'indicators': [f'木星在{jupiter_sign}（第{jupiter_house}宫）'],
        })

    # 3. Rahu-Ketu 对冲过境（约18.6年半周期）
    rahu_sign = planets.get('Rahu', {}).get('sign', '')
    for half_cycle in [9, 18, 27, 36]:
        event_year = birth_year + half_cycle
        signals.append({
            'type': 'Rahu-Ketu半周期',
            'age': half_cycle,
            'year': event_year,
            'description': f'约{event_year}年（{half_cycle}岁），Rahu-Ketu对冲轴变化',
            'confidence': '中',
            'indicators': [f'本命Rahu在{rahu_sign}'],
        })

    # 4. 关键宫位激活（基于 Dasha 可能性）
    # 7宫主星相关 → 婚姻/合作时间窗
    libra_idx = SIGNS.index('Libra') if 'Libra' in SIGNS else 6
    sign_7 = SIGNS[(asc_idx + 6) % 12]
    lord_7 = SIGN_LORDS.get(sign_7, 'Unknown')
    lord_7_info = planets.get(lord_7, {})
    if lord_7_info:
        signals.append({
            'type': '7宫主星活跃期',
            'age_range': '24-32',
            'year_range': f'{birth_year + 24}-{birth_year + 32}',
            'description': f'{lord_7}（7宫主星，7宫={sign_7}）活跃期，可能涉及婚姻/重要合作',
            'confidence': '中',
            'indicators': [f'{lord_7}在{lord_7_info.get("sign", "")}（第{lord_7_info.get("house", 0)}宫）'],
        })

    # 5. 10宫主星相关 → 事业突破
    sign_10 = SIGNS[(asc_idx + 9) % 12]
    lord_10 = SIGN_LORDS.get(sign_10, 'Unknown')
    lord_10_info = planets.get(lord_10, {})
    if lord_10_info:
        signals.append({
            'type': '10宫主星活跃期',
            'age_range': '28-40',
            'year_range': f'{birth_year + 28}-{birth_year + 40}',
            'description': f'{lord_10}（10宫主星，10宫={sign_10}）活跃期，可能涉及事业突破',
            'confidence': '中',
            'indicators': [f'{lord_10}在{lord_10_info.get("sign", "")}（第{lord_10_info.get("house", 0)}宫）'],
        })

    # 按置信度排序，取前4
    priority = {'高': 3, '中高': 2, '中': 1, '低': 0}
    signals.sort(key=lambda s: priority.get(s.get('confidence', '低'), 0), reverse=True)
    top_signals = signals[:4]

    return {
        'method': '验前事（Past Event Reverse Verification）',
        'version': '3.5',
        'note': 'AI从星盘推断的高信号历史时段，请用户确认——避免冷读效应',
        'birth_year': birth_year,
        'ascendant': asc_sign,
        'inferred_periods': top_signals,
        'disclaimer': '这些是基于星盘结构推断的可能时段，需要用户确认是否实际发生了相关事件。',
    }


# ============================================================================
# 5. 分盘计算
# ============================================================================
def cmd_varga(args):
    if not HAS_SWE: return {"error": "swisseph未安装"}
    swe.set_ephe_path('')
    hd = args.hour + args.minute / 60.0 - args.tz
    jd = swe.julday(args.year, args.month, args.day, hd)

    # Lahiri Ayanamsa（恒星黄道修正，与cmd_chart一致）
    ayanamsa = swe.get_ayanamsa(jd)

    natal = {}
    for pn, pid in PLANETS_SWE.items():
        pos, _ = swe.calc_ut(jd, pid); natal[pn] = (pos[0] - ayanamsa) % 360  # 恒星黄道
    if 'Rahu' in natal: natal['Ketu'] = (natal['Rahu'] + 180) % 360
    asc_lon, _ = swe.houses(jd, args.lat, args.lon, b'A'); asc_deg = (asc_lon[0] - ayanamsa) % 360  # 恒星黄道

    def navamsa(lon):
        si = int(lon / 30); d = lon - si * 30; ni = int(d / (30/9))
        el_starts = {0: 0, 1: 9, 2: 6, 3: 3}; return SIGNS[(el_starts[si % 4] + ni) % 12]

    def dasamsa(lon):
        si = int(lon / 30); d = lon - si * 30; di = int(d / 3)
        return SIGNS[di % 12] if si % 2 == 0 else SIGNS[(6 + di) % 12]

    result = {"birth_info": f"{args.year}-{args.month:02d}-{args.day:02d} {args.hour:02d}:{args.minute:02d}", "divisional_charts": {}}
    if args.d9 or args.all:
        d9 = {"ascendant": navamsa(asc_deg)}
        for p, l in natal.items(): d9[p] = {"sign": navamsa(l), "sign_cn": SIGNS_CN[navamsa(l)]}
        result["divisional_charts"]["D9_Navamsa"] = d9
    if args.d10 or args.all:
        d10 = {"ascendant": dasamsa(asc_deg)}
        for p, l in natal.items(): d10[p] = {"sign": dasamsa(l), "sign_cn": SIGNS_CN[dasamsa(l)]}
        result["divisional_charts"]["D10_Dasamsa"] = d10
    if not result["divisional_charts"]: result["note"] = "请指定 --d9, --d10 或 --all"
    return result


# ============================================================================
# 6. 名人案例查询
# ============================================================================
def cmd_celebrity(args):
    result = {"query": args.name or "all", "results": []}
    if os.path.exists(DB_PATH):
        try:
            conn = sqlite3.connect(DB_PATH); c = conn.cursor()
            if args.name: c.execute("SELECT * FROM cases WHERE name LIKE ?", (f'%{args.name}%',))
            else: c.execute("SELECT * FROM cases LIMIT ?", (args.limit or 20,))
            cols = [d[0] for d in c.description]
            for r in c.fetchall(): result["results"].append(dict(zip(cols, r)))
            conn.close()
        except Exception as e: result["db_error"] = str(e)

    if os.path.exists(PERSON_CSV) and args.name:
        try:
            matches = []
            with open(PERSON_CSV, 'r', encoding='utf-8') as f:
                for row in csv.DictReader(f):
                    if args.name.lower() in row.get('Name', '').lower():
                        matches.append({"name": row.get('Name', ''), "birth_time": row.get('BirthTime', ''), "gender": row.get('Gender', '')})
                        if len(matches) >= 10: break
            result["person_list_matches"] = matches; result["person_list_total"] = 15807
        except Exception as e: result["csv_error"] = str(e)
    return result


# ============================================================================
# 7. 数据库统计
# ============================================================================
def cmd_db_stats(args):
    result = {}
    if os.path.exists(DB_PATH):
        try:
            conn = sqlite3.connect(DB_PATH); c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM cases"); result["total_cases"] = c.fetchone()[0]
            c.execute("SELECT case_type, COUNT(*) FROM cases GROUP BY case_type"); result["by_type"] = dict(c.fetchall())
            c.execute("SELECT difficulty, COUNT(*) FROM cases GROUP BY difficulty"); result["by_difficulty"] = dict(c.fetchall())
            c.execute("SELECT name, accuracy_rate, sample_size, correct_predictions FROM techniques"); result["techniques"] = [{"name": r[0], "accuracy": r[1], "samples": r[2], "correct": r[3]} for r in c.fetchall()]
            conn.close()
        except Exception as e: result["error"] = str(e)
    else:
        result["error"] = f"数据库不存在: {DB_PATH}"
    return result


# ============================================================================
# 8. 过境查询
# ============================================================================
def cmd_transit(args):
    result = {"year": args.year, "month": args.month, "transits": {}}
    if os.path.exists(TRANSIT_JSON):
        try:
            with open(TRANSIT_JSON, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if isinstance(data, list):
                for entry in data:
                    if isinstance(entry, dict) and entry.get("year") == args.year and entry.get("month") == args.month:
                        result["transits"] = entry; break
            if not result["transits"]:
                avail = [(e.get("year"), e.get("month")) for e in data if isinstance(e, dict)]
                result["note"] = f"未找到{args.year}年{args.month}月的过境数据"
                result["available_months"] = [f"{y}-{m:02d}" for y, m in avail]
        except Exception as e:
            result["error"] = str(e)
    else:
        result["error"] = f"过境配置文件不存在: {TRANSIT_JSON}"
    return result


# ============================================================================
# 9. Shadbala 六重力量（v3.4新增）
# ============================================================================
def cmd_shadbala(args):
    chart, asc_idx, jd, ayanamsa = compute_chart_data(
        args.year, args.month, args.day, args.hour, args.minute,
        args.lat, args.lon, args.tz)
    if chart is None:
        return {"error": "swisseph未安装"}
    try:
        sys.path.insert(0, SCRIPT_DIR)
        from shadbala import calc_shadbala
    except ImportError as e:
        return {"error": f"shadbala模块导入失败: {e}"}
    planets = chart.get("planets", {})
    asc_sign = chart.get("ascendant", {}).get("sign", "Aries")
    birth_hour = args.hour + args.minute / 60.0
    sun_lon = planets.get("Sun", {}).get("degree", 0)
    moon_lon = planets.get("Moon", {}).get("degree", 0)
    return calc_shadbala(planets, asc_sign, birth_hour, sun_lon, moon_lon)


# ============================================================================
# 10. Ashtakavarga 八分法（v3.4新增）
# ============================================================================
def cmd_ashtakavarga(args):
    chart, asc_idx, jd, ayanamsa = compute_chart_data(
        args.year, args.month, args.day, args.hour, args.minute,
        args.lat, args.lon, args.tz)
    if chart is None:
        return {"error": "swisseph未安装"}
    try:
        sys.path.insert(0, SCRIPT_DIR)
        from ashtakavarga import calc_ashtakavarga
    except ImportError as e:
        return {"error": f"ashtakavarga模块导入失败: {e}"}
    planets = chart.get("planets", {})
    return calc_ashtakavarga(planets, asc_idx)


# ============================================================================
# 11. Hermes 记忆系统（v3.4新增）
# ============================================================================
def cmd_memory(args):
    try:
        sys.path.insert(0, SCRIPT_DIR)
        from hermes_memory_core import HermesMemoryCore
    except ImportError as e:
        return {"error": f"Hermes记忆模块导入失败: {e}", "hint": "确保hermes_memory_core.py在scripts/目录下"}
    db_file = os.path.join(SCRIPT_DIR, 'hermes_memory.db')
    mem = HermesMemoryCore(db_file)
    result = {"action": args.action}
    if args.action == "store":
        if not args.content:
            return {"error": "store操作需要 --content 参数"}
        tags = args.tags.split(',') if args.tags else []
        importance = args.importance if args.importance else 5
        metadata = {"tags": tags, "importance": importance}
        mem_id = mem.store_memory(args.content, metadata)
        result.update({"stored": True, "memory_id": mem_id, "content": args.content, "tags": tags})
    elif args.action == "search":
        if not args.query:
            return {"error": "search操作需要 --query 参数"}
        results = mem.search(args.query, limit=args.limit or 10)
        result.update({"query": args.query, "found": len(results), "results": results})
    elif args.action == "context":
        session_id = f"jyotish-cli-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        ctx = mem.get_context_for_session(session_id)
        result.update({"session_id": session_id, "context": ctx})
    elif args.action == "stats":
        # Hermes没有get_stats，用搜索空串获取总数
        try:
            all_mem = mem.search("", limit=1000)
            result["total_memories"] = len(all_mem)
        except:
            result["total_memories"] = "unknown"
        result["db_path"] = db_file
    else:
        result["error"] = f"未知action: {args.action}，支持: store/search/context/stats"
    return result


# ============================================================================
# 12. R1-R10 数学验证（v3.5新增）
# ============================================================================
def cmd_validate(args):
    chart, asc_idx, jd, ayanamsa = compute_chart_data(
        args.year, args.month, args.day, args.hour, args.minute,
        args.lat, args.lon, args.tz)
    if chart is None:
        return {"error": "swisseph未安装"}
    try:
        sys.path.insert(0, SCRIPT_DIR)
        from ashtakavarga import calc_ashtakavarga
        asht_result = calc_ashtakavarga(chart.get('planets', {}), asc_idx)
    except ImportError:
        asht_result = None
    try:
        from validate import validate_chart
        return validate_chart(chart, asht_result)
    except ImportError as e:
        return {"error": f"validate模块导入失败: {e}"}


# ============================================================================
# 13. P1-P12 行星审计管线（v3.5新增）
# ============================================================================
def _assess_conjunction_quality(lord, houses, planets):
    """评估仓库耦合的吉凶质量"""
    lord_info = planets.get(lord, {})
    lord_status = lord_info.get('status', '中性')
    # 凶宫组合
    dusthana = {6, 8, 12}
    trikona = {1, 5, 9}
    kendra = {1, 4, 7, 10}
    
    has_dusthana = any(h in dusthana for h in houses)
    has_trikona = any(h in trikona for h in houses)
    has_kendra = any(h in kendra for h in houses)
    
    if has_dusthana and has_trikona:
        return f"凶吉混合 — 挑战与成长并存"
    elif has_dusthana and has_kendra:
        return f"压力型 — 通过努力获取成就"
    elif has_trikona:
        return f"吉庆型 — 自然流畅的支持"
    elif has_dusthana:
        return f"消耗型 — 需要额外努力维持"
    else:
        return f"中性 — 标准互动"

def _conflict_arbitration(report):
    """
    冲突仲裁规则（CNWU16框架）：
    1. P1清理者+P7入旺 = "带毒高价值资产"，禁止说逢凶化吉
    2. P5凶宫+BAV高 = "乱世出英雄"
    3. P1吉+P2受损 = "空有雄心无着力点"
    """
    conflicts = []
    planets = report.get('planets', {})
    audit = report.get('audit', {})
    
    p1 = audit.get('P1_identity', {})
    p7 = audit.get('P7_dignity', {})
    p2 = audit.get('P2_health', {})
    
    asc_lord = p1.get('asc_lord', '')
    
    # 规则1: P1清理者+P7入旺 → 检查上升主是否掌管8/12宫（清理者角色）
    # 清理者定义：掌管8宫或12宫的行星
    SIGN_LORDS_MAP = {'Aries': 'Mars', 'Taurus': 'Venus', 'Gemini': 'Mercury', 'Cancer': 'Moon',
                      'Leo': 'Sun', 'Virgo': 'Mercury', 'Libra': 'Venus', 'Scorpio': 'Mars',
                      'Sagittarius': 'Jupiter', 'Capricorn': 'Saturn', 'Aquarius': 'Saturn', 'Pisces': 'Jupiter'}
    
    asc_sign = p1.get('asc_sign', '')
    asc_idx_local = SIGNS.index(asc_sign) if asc_sign in SIGNS else 0
    
    # 找8宫主和12宫主
    h8_sign = SIGNS[(asc_idx_local + 7) % 12]
    h12_sign = SIGNS[(asc_idx_local + 11) % 12]
    destroyer_lords = {SIGN_LORDS_MAP.get(h8_sign, ''), SIGN_LORDS_MAP.get(h12_sign, '')}
    
    for dl in destroyer_lords:
        if dl and dl in p7:
            dl_status = p7[dl].get('status', '')
            if 'Exalted' in dl_status or 'Own' in dl_status:
                conflicts.append({
                    'rule': 'Destroyer+Exalted',
                    'planets': [dl],
                    'verdict': '带毒高价值资产',
                    'instruction': f"{dl}既是清理者(掌8/12宫)又入旺/入庙，力量极强但方向凶险——禁止说逢凶化吉",
                })
    
    # 规则2: P5凶宫+BAV高 → 检查6/8/12宫的SAV是否 >28
    asht_data = report.get('ashtakavarga', {})
    house_scores = {}
    if asht_data:
        # 从ashtakavarga原始数据获取house_scores
        try:
            sys.path.insert(0, SCRIPT_DIR)
            from ashtakavarga import calc_ashtakavarga
            asht_result = calc_ashtakavarga(planets, asc_idx_local)
            house_scores = asht_result.get('house_scores', {})
        except:
            pass
    
    for h in [6, 8, 12]:
        hs = house_scores.get(f'house_{h}', {})
        sav_score = hs.get('score', 0)
        if sav_score > 28:
            conflicts.append({
                'rule': 'Dusthana+HighBAV',
                'house': h,
                'sav': sav_score,
                'verdict': '乱世出英雄',
                'instruction': f"{h}宫是凶宫但SAV={sav_score}（>28），在困境中反而能出成就",
            })
    
    # 规则3: P1吉+P2受损 → 上升主星状态好但太阳(健康指标)受损
    sun_info = p2.get('sun_status', '')
    lord_info = p7.get(asc_lord, {})
    lord_status = lord_info.get('status', '')
    if ('Exalted' in lord_status or 'Own' in lord_status) and ('Debilitated' in sun_info or 'Enemy' in sun_info):
        conflicts.append({
            'rule': 'GoodP1+DamagedP2',
            'planets': [asc_lord, 'Sun'],
            'verdict': '空有雄心无着力点',
            'instruction': f"上升主{asc_lord}强健但太阳受损，有野心但执行力/健康跟不上",
        })
    
    return conflicts


def cmd_audit(args):
    """P1-P12 行星审计：调用 chart→shadbala→ashtakavarga→yoga，输出统一审计报告"""
    chart, asc_idx, jd, ayanamsa = compute_chart_data(
        args.year, args.month, args.day, args.hour, args.minute,
        args.lat, args.lon, args.tz)
    if chart is None:
        return {"error": "swisseph未安装"}

    planets = chart.get('planets', {})
    asc_sign = chart.get('ascendant', {}).get('sign', 'Unknown')

    report = {
        'version': '3.5',
        'birth_info': chart.get('birth_info', {}),
        'ascendant': chart.get('ascendant', {}),
        'planets': planets,
        'audit': {},
    }

    # P1 Identity（本命身份）: 上升星座 + 上升主星
    asc_lord = chart.get('ascendant', {}).get('lord', 'Unknown')
    lord_info = planets.get(asc_lord, {})
    report['audit']['P1_identity'] = {
        'asc_sign': asc_sign,
        'asc_lord': asc_lord,
        'lord_sign': lord_info.get('sign', 'Unknown'),
        'lord_house': lord_info.get('house', 0),
        'lord_status': lord_info.get('status', '未知'),
    }

    # P2 Health（健康指标）: 6宫 + 8宫 + 12宫主星 + 太阳状态
    health_houses = [6, 8, 12]
    health_lords = set()
    health_info = {}
    for h in health_houses:
        sign_idx = (asc_idx + h - 1) % 12
        sign_name = SIGNS[sign_idx]
        lord = SIGN_LORDS.get(sign_name, 'Unknown')
        health_lords.add(lord)
        health_info[f'house_{h}'] = {'sign': sign_name, 'lord': lord}
    sun_info = planets.get('Sun', {})
    report['audit']['P2_health'] = {
        'houses': health_info,
        'sun_status': sun_info.get('status', '未知'),
        'sun_house': sun_info.get('house', 0),
    }

    # P3 Warehouse Coupling（仓库耦合）: 双宫掌管=货物捆绑
    # CNWU16逻辑：如果一颗行星同时掌管两个宫位，则两个宫位的事务被"捆绑"
    house_lord_map = {}
    for h in range(1, 13):
        sign_idx = (asc_idx + h - 1) % 12
        sname = SIGNS[sign_idx]
        lord = SIGN_LORDS.get(sname, 'Unknown')
        if lord not in house_lord_map:
            house_lord_map[lord] = []
        house_lord_map[lord].append(h)

    warehouse_coupling = {}
    for lord, houses in house_lord_map.items():
        if len(houses) > 1:
            warehouse_coupling[lord] = {
                'houses': houses,
                'meaning': f"{lord}同时掌管{houses[0]}宫和{houses[1]}宫，事务捆绑",
                'conjunction_quality': _assess_conjunction_quality(lord, houses, planets),
            }
    report['audit']['P3_warehouse_coupling'] = warehouse_coupling

    # P8 Age Status（年龄状态）: 青壮=主动, 老婴=辅助, 死=自动执行
    # 基于行星在星座中的度数区间判定生命周期
    age_status_map = {}
    for pname, pd in planets.items():
        deg_in_sign = pd.get('degree_in_sign', 0)
        if pname in ['Rahu', 'Ketu']:
            age_status_map[pname] = {'status': '永远逆行', 'phase': 'Rahu/Ketu无年龄状态'}
            continue
        if deg_in_sign < 10:
            phase = '婴幼(0-10°)'
            quality = '辅助型 — 能量尚未完全展开'
        elif deg_in_sign < 20:
            phase = '青壮(10-20°)'
            quality = '主动型 — 能量最活跃，主导性强'
        else:
            phase = '老年(20-30°)'
            quality = '自动执行型 — 已内化的能力，自动化运作'
        age_status_map[pname] = {
            'degree_in_sign': round(deg_in_sign, 2),
            'phase': phase,
            'quality': quality,
        }
    report['audit']['P8_age_status'] = age_status_map

    # P4 Resource SAV（资源SAV）& P6 Exit SAV（退出SAV）
    # 需要 Ashtakavarga 数据
    asht_data = None
    try:
        sys.path.insert(0, SCRIPT_DIR)
        from ashtakavarga import calc_ashtakavarga
        asht_data = calc_ashtakavarga(planets, asc_idx)
        report['ashtakavarga'] = {
            'sav_total': asht_data.get('sav', {}).get('total', 0),
            'sav_valid': asht_data.get('sav', {}).get('valid', False),
            'strongest': asht_data.get('strongest_signs', []),
            'weakest': asht_data.get('weakest_signs', []),
        }
        house_scores = asht_data.get('house_scores', {})
        # P4: 财富宫(2,11) SAV
        p4_info = {}
        for h in [2, 11]:
            hs = house_scores.get(f'house_{h}', {})
            p4_info[f'house_{h}'] = hs
        report['audit']['P4_resource_sav'] = p4_info
        # P6: 退出宫(12) SAV + 8宫
        p6_info = {}
        for h in [8, 12]:
            hs = house_scores.get(f'house_{h}', {})
            p6_info[f'house_{h}'] = hs
        report['audit']['P6_exit_sav'] = p6_info
        # P5: 路况(1,5,9三宫) SAV
        p5_info = {}
        for h in [1, 5, 9]:
            hs = house_scores.get(f'house_{h}', {})
            p5_info[f'house_{h}'] = hs
        report['audit']['P5_road_condition'] = p5_info
    except Exception as e:
        report['audit']['ashtakavarga_error'] = str(e)

    # P7 Dignity（尊严状态）
    dignity_map = {}
    for pname, pd in planets.items():
        dignity_map[pname] = {
            'sign': pd.get('sign', ''),
            'status': pd.get('status', '中性'),
            'house': pd.get('house', 0),
            'retrograde': pd.get('retrograde', False),
        }
    report['audit']['P7_dignity'] = dignity_map

    # P9 Shadbala（六重力量）
    try:
        sys.path.insert(0, SCRIPT_DIR)
        from shadbala import calc_shadbala
        birth_hour = args.hour + args.minute / 60.0
        sun_lon = planets.get('Sun', {}).get('degree', 0)
        moon_lon = planets.get('Moon', {}).get('degree', 0)
        shadbala = calc_shadbala(planets, asc_sign, birth_hour, sun_lon, moon_lon)
        report['audit']['P9_shadbala'] = {
            'summary': shadbala.get('summary', {}),
            'ishta_bala_ranking': shadbala.get('ishta_bala_ranking', []),
        }
    except Exception as e:
        report['audit']['P9_shadbala_error'] = str(e)

    # P10 Aspects（相位）简化版
    aspect_map = {}
    for pname, pd in planets.items():
        if pname in ['Rahu', 'Ketu']:
            continue
        house = pd.get('house', 0)
        # 标准 7/4 相位（从该行星宫位数起）
        aspects_from_house = {1: [7], 2: [7], 3: [5, 9, 7], 4: [7, 10],
                              5: [7], 6: [7], 7: [7], 8: [7],
                              9: [5, 7], 10: [7], 11: [7], 12: [7]}
        # 特殊相位
        special = {'Mars': [4, 7, 8], 'Jupiter': [5, 7, 9], 'Saturn': [3, 7, 10]}
        if pname in special:
            aspect_houses = special[pname]
        else:
            aspect_houses = [7]  # 标准对宫
        aspect_map[pname] = {
            'from_house': house,
            'aspect_houses': aspect_houses,
        }
    report['audit']['P10_aspects'] = aspect_map

    # P11 Nakshatra
    nak_map = {}
    for pname, pd in planets.items():
        nak_map[pname] = {
            'nakshatra': pd.get('nakshatra', ''),
            'pada': pd.get('nakshatra_pada', 0),
            'lord': pd.get('nakshatra_lord', ''),
        }
    report['audit']['P11_nakshatra'] = nak_map

    # P12 Yogas（格局识别）
    try:
        yoga_planets = {}
        for pname, pd in planets.items():
            if isinstance(pd, dict) and 'sign' in pd and 'house' in pd:
                yoga_planets[pname] = {'sign': pd['sign'], 'house': pd['house']}
        yoga_result = cmd_yoga(type('Args', (), {
            'ascendant': asc_sign,
            'planets': ','.join([f"{k}:{v['sign']}:{v['house']}" for k, v in yoga_planets.items()])
        })())
        report['audit']['P12_yogas'] = {
            'count': yoga_result.get('yogas_detected', 0),
            'yogas': yoga_result.get('yogas', []),
        }
    except Exception as e:
        report['audit']['P12_yogas_error'] = str(e)

    # 验证
    try:
        from validate import validate_chart
        validation = validate_chart(chart, asht_data)
        report['validation'] = validation
    except Exception as e:
        report['validation'] = {"error": str(e)}

    # 冲突仲裁（CNWU16框架3条规则）
    report['conflict_arbitration'] = _conflict_arbitration(report)

    return report


# ============================================================================
# 14. 报告生成（v3.6新增）
# ============================================================================
def cmd_report(args):
    """调用 report_builder.py 生成 HTML 报告"""
    try:
        sys.path.insert(0, SCRIPT_DIR)
        from report_builder import main as report_main
    except ImportError as e:
        return {"error": f"report_builder模块导入失败: {e}"}

    # 构造 sys.argv 并调用 report_builder
    folder = args.folder
    if not os.path.isdir(folder):
        return {"error": f"目录不存在: {folder}"}

    report_argv = [
        'report_builder.py', folder,
        '--name', args.name,
        '--lagna', args.lagna,
        '--gender', args.gender,
        '--status', args.status,
        '--lang', args.lang,
    ]
    if args.output:
        report_argv.extend(['--output', args.output])

    old_argv = sys.argv
    sys.argv = report_argv
    try:
        report_main()
        output_path = args.output or os.path.join(folder, 'report.html')
        return {
            'status': 'ok',
            'output': output_path,
            'name': args.name,
            'lagna': args.lagna,
            'lang': args.lang,
        }
    except SystemExit:
        return {"error": "report_builder执行出错，请检查MD文件格式"}
    except Exception as e:
        return {"error": f"报告生成失败: {e}"}
    finally:
        sys.argv = old_argv


# ============================================================================
# 15. BPHS十六分盘完整计算（v3.7新增）
# ============================================================================
def cmd_varga_full(args):
    chart, asc_idx, jd, ayanamsa = compute_chart_data(
        args.year, args.month, args.day, args.hour, args.minute,
        args.lat, args.lon, args.tz)
    if chart is None:
        return {"error": "swisseph未安装"}
    try:
        sys.path.insert(0, SCRIPT_DIR)
        from varga import calc_all_vargas
    except ImportError as e:
        return {"error": f"varga模块导入失败: {e}"}
    planets = chart.get('planets', {})
    planet_lons = {pn: pd['degree'] for pn, pd in planets.items() if isinstance(pd, dict) and 'degree' in pd}
    asc_deg = chart.get('ascendant', {}).get('degree', 0)
    divisions = [int(d.strip().replace('D','')) for d in args.divisions.split(',')] if args.divisions else None
    return calc_all_vargas(planet_lons, asc_deg, divisions)


# ============================================================================
# 16. 度数精确相位系统（v3.7新增）
# ============================================================================
def cmd_aspects(args):
    chart, asc_idx, jd, ayanamsa = compute_chart_data(
        args.year, args.month, args.day, args.hour, args.minute,
        args.lat, args.lon, args.tz)
    if chart is None:
        return {"error": "swisseph未安装"}
    try:
        sys.path.insert(0, SCRIPT_DIR)
        from aspects import calc_all_aspects
    except ImportError as e:
        return {"error": f"aspects模块导入失败: {e}"}
    planets = chart.get('planets', {})
    planet_lons = {}
    for pn, pd in planets.items():
        if isinstance(pd, dict) and 'degree' in pd:
            planet_lons[pn] = pd['degree']
    asc_deg = chart.get('ascendant', {}).get('degree', 0)
    return calc_all_aspects(planet_lons, asc_deg)


# ============================================================================
# 17. Jaimini系统（v3.7新增）
# ============================================================================
def cmd_jaimini(args):
    chart, asc_idx, jd, ayanamsa = compute_chart_data(
        args.year, args.month, args.day, args.hour, args.minute,
        args.lat, args.lon, args.tz)
    if chart is None:
        return {"error": "swisseph未安装"}
    try:
        sys.path.insert(0, SCRIPT_DIR)
        from jaimini import calc_chara_karaka_7, calc_chara_karaka_8, calc_chara_dasha, calc_karakamsha
        from varga import calc_varga
    except ImportError as e:
        return {"error": f"jaimini模块导入失败: {e}"}
    planets = chart.get('planets', {})
    planet_lons = {}
    for pn, pd in planets.items():
        if isinstance(pd, dict) and 'degree' in pd:
            planet_lons[pn] = pd['degree']
    asc_deg = chart.get('ascendant', {}).get('degree', 0)

    result = {}
    # Chara Karaka
    mode = args.mode or 'all'
    if mode in ('all', 'karaka'):
        result['chara_karaka_7'] = calc_chara_karaka_7(planet_lons)
        result['chara_karaka_8'] = calc_chara_karaka_8(planet_lons)
    if mode in ('all', 'dasha'):
        result['chara_dasha'] = calc_chara_dasha(asc_idx, planet_lons, args.year, args.month)
    if mode in ('all', 'karakamsha'):
        # DK的D9位置
        ck7 = calc_chara_karaka_7(planet_lons)
        dk_name = ck7.get('DK', {}).get('planet', 'Moon')
        dk_lon = planet_lons.get(dk_name, 0)
        dk_d9 = calc_varga(dk_lon, 9)
        result['karakamsha'] = calc_karakamsha(dk_d9.get('sign', 'Aries'), dk_d9.get('degree_in_sign', 0))
    return result


# ============================================================================
# 18. 高级Nakshatra分析（v3.7新增）
# ============================================================================
def cmd_nakshatra_adv(args):
    chart, asc_idx, jd, ayanamsa = compute_chart_data(
        args.year, args.month, args.day, args.hour, args.minute,
        args.lat, args.lon, args.tz)
    if chart is None:
        return {"error": "swisseph未安装"}
    try:
        sys.path.insert(0, SCRIPT_DIR)
        from nakshatra_advanced import find_nakshatra, calc_all_tara_balas, calc_sub_lord, nakshatra_compatibility
    except ImportError as e:
        return {"error": f"nakshatra_advanced模块导入失败: {e}"}
    planets = chart.get('planets', {})
    planet_lons = {}
    for pn, pd in planets.items():
        if isinstance(pd, dict) and 'degree' in pd:
            planet_lons[pn] = pd['degree']

    result = {'planets': {}}
    mode = args.mode or 'all'

    if mode in ('all', 'detail'):
        for pn, lon in planet_lons.items():
            result['planets'][pn] = find_nakshatra(lon)

    if mode in ('all', 'tara'):
        moon_lon = planet_lons.get('Moon', 0)
        moon_nak_idx = int(moon_lon / (360/27)) % 27
        result['tara_bala'] = calc_all_tara_balas(moon_nak_idx, planet_lons)

    if mode in ('all', 'sublord'):
        result['sub_lords'] = {pn: calc_sub_lord(lon) for pn, lon in planet_lons.items()}

    return result


# ============================================================================
# 19. Argala门闩系统（v3.7新增）
# ============================================================================
def cmd_argala(args):
    chart, asc_idx, jd, ayanamsa = compute_chart_data(
        args.year, args.month, args.day, args.hour, args.minute,
        args.lat, args.lon, args.tz)
    if chart is None:
        return {"error": "swisseph未安装"}
    try:
        sys.path.insert(0, SCRIPT_DIR)
        from argala import calc_argala
    except ImportError as e:
        return {"error": f"argala模块导入失败: {e}"}
    planets = chart.get('planets', {})
    # 构建宫位到行星的映射 - argala需要sign_indices
    planet_sign_indices = {}
    for pn, pd in planets.items():
        if isinstance(pd, dict) and 'sign' in pd:
            si = SIGNS.index(pd['sign']) if pd['sign'] in SIGNS else 0
            planet_sign_indices[pn] = si
    return calc_argala(planet_sign_indices, asc_idx)


# ============================================================================
# 20. Tajika/Varshaphala年运盘（v3.7新增）
# ============================================================================
def cmd_tajika(args):
    chart, asc_idx, jd, ayanamsa = compute_chart_data(
        args.year, args.month, args.day, args.hour, args.minute,
        args.lat, args.lon, args.tz)
    if chart is None:
        return {"error": "swisseph未安装"}
    try:
        sys.path.insert(0, SCRIPT_DIR)
        from tajika import calc_muntha, calc_year_lord, calc_mudda_dasha, calc_tri_pataka
    except ImportError as e:
        return {"error": f"tajika模块导入失败: {e}"}
    planets = chart.get('planets', {})
    planet_lons = {}
    for pn, pd in planets.items():
        if isinstance(pd, dict) and 'degree' in pd:
            planet_lons[pn] = pd['degree']
    asc_deg = chart.get('ascendant', {}).get('degree', 0)
    asc_si = int(asc_deg / 30) % 12  # sign index
    age = args.age
    if age is None:
        return {"error": "请提供 --age 参数（当前年龄）"}

    result = {}
    mode = args.mode or 'all'
    if mode in ('all', 'muntha'):
        result['muntha'] = calc_muntha(asc_si, age)
    if mode in ('all', 'yearlord'):
        result['year_lord'] = calc_year_lord(asc_si, age)
    if mode in ('all', 'mudda'):
        # 需要先获取 varsha_lord
        yl = calc_year_lord(asc_si, age)
        varsha_lord = yl.get('year_lord', 'Jupiter')
        result['mudda_dasha'] = calc_mudda_dasha(asc_si, varsha_lord, args.month)
    if mode in ('all', 'tripataka'):
        yl = calc_year_lord(asc_si, age)
        varsha_lord = yl.get('year_lord', 'Jupiter')
        muntha_si = (asc_si + age) % 12
        result['tri_pataka'] = calc_tri_pataka(planet_lons, varsha_lord, muntha_si)
    return result


# ============================================================================
# 21. 合盘分析（v3.7新增）
# ============================================================================
def cmd_synastry(args):
    try:
        sys.path.insert(0, SCRIPT_DIR)
        from synastry import calc_synastry
    except ImportError as e:
        return {"error": f"synastry模块导入失败: {e}"}
    # 构建两人数据
    p1 = {'moon_lon': args.moon1, 'gender': args.gender1 or 'M'}
    p2 = {'moon_lon': args.moon2, 'gender': args.gender2 or 'F'}
    if args.mars1 is not None: p1['mars_lon'] = args.mars1
    if args.mars2 is not None: p2['mars_lon'] = args.mars2
    if args.asc1 is not None: p1['asc_lon'] = args.asc1
    if args.asc2 is not None: p2['asc_lon'] = args.asc2
    return calc_synastry(p1, p2)


# ============================================================================
# CLI入口
# ============================================================================
def main():
    parser = argparse.ArgumentParser(description='印度占星统一引擎 v3.7.0', formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest='command', help='子命令')

    # 1. chart
    p = sub.add_parser('chart', help='计算完整星盘')
    _add_chart_args(p)
    p.add_argument('--validate', action='store_true', help='附加R1-R10数学验证')

    # 2. dasha
    p = sub.add_parser('dasha', help='计算Dasha大运')
    p.add_argument('--nakshatra', default=None); p.add_argument('--pada', type=int, default=None)
    p.add_argument('--moon-lon', type=float, default=None); p.add_argument('--birthdate', required=True)
    p.add_argument('--today', default=None)

    # 3. yoga
    p = sub.add_parser('yoga', help='Yoga格局识别')
    p.add_argument('--ascendant', default=None)
    p.add_argument('--planets', default=None, help="格式: 'Sun:Aries:9,Moon:Aquarius:7,...'")

    # 4. predict
    p = sub.add_parser('predict', help='三层验证法事件预测')
    p.add_argument('--chart', default=None, help='星盘JSON字符串')
    p.add_argument('--event-type', default='all', choices=['all', 'marriage', 'career', 'wealth', 'health'])
    p.add_argument('--past-verify', action='store_true', help='验前事模式：推断2-4个高信号历史时段')
    p.add_argument('--year', type=int, default=None, help='出生年（验前事模式需要）')
    p.add_argument('--month', type=int, default=None, help='出生月')
    p.add_argument('--day', type=int, default=None, help='出生日')
    p.add_argument('--hour', type=int, default=None, help='出生时')
    p.add_argument('--minute', type=int, default=None, help='出生分')
    p.add_argument('--lat', type=float, default=None, help='纬度')
    p.add_argument('--lon', type=float, default=None, help='经度')
    p.add_argument('--tz', type=float, default=0, help='时区')

    # 5. varga
    p = sub.add_parser('varga', help='分盘计算')
    _add_chart_args(p)
    p.add_argument('--d9', action='store_true'); p.add_argument('--d10', action='store_true')
    p.add_argument('--all', action='store_true')

    # 6. celebrity
    p = sub.add_parser('celebrity', help='名人案例查询')
    p.add_argument('--name', default=None); p.add_argument('--limit', type=int, default=20)

    # 7. db-stats
    sub.add_parser('db-stats', help='验证数据库统计')

    # 8. transit
    p = sub.add_parser('transit', help='行星过境查询')
    p.add_argument('--year', type=int, required=True); p.add_argument('--month', type=int, required=True)

    # 9. shadbala (v3.4新增)
    p = sub.add_parser('shadbala', help='Shadbala六重力量计算')
    _add_chart_args(p)

    # 10. ashtakavarga (v3.4新增)
    p = sub.add_parser('ashtakavarga', help='Ashtakavarga八分法计算')
    _add_chart_args(p)

    # 11. memory (v3.4新增)
    p = sub.add_parser('memory', help='Hermes记忆系统')
    p.add_argument('--action', default='stats', choices=['store', 'search', 'context', 'stats'])
    p.add_argument('--content', default=None, help='存储内容（store操作必填）')
    p.add_argument('--query', default=None, help='搜索查询（search操作必填）')
    p.add_argument('--tags', default=None, help='标签，逗号分隔')
    p.add_argument('--importance', type=int, default=5, help='重要性 1-10')
    p.add_argument('--limit', type=int, default=10, help='搜索结果数量')

    # 12. validate (v3.5新增)
    p = sub.add_parser('validate', help='R1-R10数学验证')
    _add_chart_args(p)

    # 13. audit (v3.5新增)
    p = sub.add_parser('audit', help='P1-P12行星审计管线')
    _add_chart_args(p)

    # 14. report (v3.6新增)
    p = sub.add_parser('report', help='MD→HTML报告生成（羊皮纸主题）')
    p.add_argument('folder', help='包含MD文件的目录路径')
    p.add_argument('--name', default='Client', help='客户姓名')
    p.add_argument('--lagna', default='—', help='上升星座')
    p.add_argument('--gender', default='—', help='性别')
    p.add_argument('--status', default='—', help='当前状态')
    p.add_argument('--lang', default='cn', choices=['cn', 'en'], help='语言 (默认cn)')
    p.add_argument('--output', default=None, help='输出HTML路径')

    # 15. varga-full (v3.7新增)
    p = sub.add_parser('varga-full', help='BPHS十六分盘完整计算')
    _add_chart_args(p)
    p.add_argument('--divisions', default=None, help='指定分盘，逗号分隔(如 D2,D9,D60)，空=全部')

    # 16. aspects (v3.7新增)
    p = sub.add_parser('aspects', help='度数精确相位系统')
    _add_chart_args(p)

    # 17. jaimini (v3.7新增)
    p = sub.add_parser('jaimini', help='Jaimini系统（Chara Karaka/Dasha/Karakamsha）')
    _add_chart_args(p)
    p.add_argument('--mode', default='all', choices=['all','karaka','dasha','karakamsha'], help='分析模式')

    # 18. nakshatra-adv (v3.7新增)
    p = sub.add_parser('nakshatra-adv', help='高级Nakshatra分析')
    _add_chart_args(p)
    p.add_argument('--mode', default='all', choices=['all','detail','tara','sublord'], help='分析模式')

    # 19. argala (v3.7新增)
    p = sub.add_parser('argala', help='Argala门闩系统')
    _add_chart_args(p)

    # 20. tajika (v3.7新增)
    p = sub.add_parser('tajika', help='Tajika/Varshaphala年运盘')
    _add_chart_args(p)
    p.add_argument('--age', type=int, required=True, help='当前年龄')
    p.add_argument('--mode', default='all', choices=['all','muntha','yearlord','mudda','tripataka'], help='分析模式')

    # 21. synastry (v3.7新增)
    p = sub.add_parser('synastry', help='合盘分析（Ashta Koota 36分制）')
    p.add_argument('--moon1', type=float, required=True, help='Person1月亮黄经')
    p.add_argument('--moon2', type=float, required=True, help='Person2月亮黄经')
    p.add_argument('--mars1', type=float, default=None, help='Person1火星黄经')
    p.add_argument('--mars2', type=float, default=None, help='Person2火星黄经')
    p.add_argument('--asc1', type=float, default=None, help='Person1上升黄经')
    p.add_argument('--asc2', type=float, default=None, help='Person2上升黄经')
    p.add_argument('--gender1', default='M', help='Person1性别')
    p.add_argument('--gender2', default='F', help='Person2性别')

    args = parser.parse_args()
    if not args.command:
        parser.print_help(); sys.exit(1)

    cmds = {'chart': cmd_chart, 'dasha': cmd_dasha, 'yoga': cmd_yoga, 'predict': cmd_predict,
            'varga': cmd_varga, 'celebrity': cmd_celebrity, 'db-stats': cmd_db_stats, 'transit': cmd_transit,
            'shadbala': cmd_shadbala, 'ashtakavarga': cmd_ashtakavarga, 'memory': cmd_memory,
            'validate': cmd_validate, 'audit': cmd_audit, 'report': cmd_report,
            'varga-full': cmd_varga_full, 'aspects': cmd_aspects, 'jaimini': cmd_jaimini,
            'nakshatra-adv': cmd_nakshatra_adv, 'argala': cmd_argala, 'tajika': cmd_tajika,
            'synastry': cmd_synastry}
    result = cmds[args.command](args)
    output_json(result)


if __name__ == '__main__':
    main()
