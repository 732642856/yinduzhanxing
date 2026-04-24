#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shadbala 计算模块（六重力量）
基于 Parashara 系统，量化行星力量

六种力量：
1. Sthana Bala（位置力量）
2. Dig Bala（方向力量）
3. Kala Bala（时间力量）
4. Chesta Bala（运动力量）
5. Naisargika Bala（天然力量）
6. Drik Bala（相位力量）
"""

import math
from typing import Dict, Tuple

# ============================================================================
# 常量
# ============================================================================
SIGNS = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
         'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

SIGN_LORDS = {
    'Aries': 'Mars', 'Taurus': 'Venus', 'Gemini': 'Mercury', 'Cancer': 'Moon',
    'Leo': 'Sun', 'Virgo': 'Mercury', 'Libra': 'Venus', 'Scorpio': 'Mars',
    'Sagittarius': 'Jupiter', 'Capricorn': 'Saturn', 'Aquarius': 'Saturn', 'Pisces': 'Jupiter'
}

# 入庙度数（sign_idx * 30 + degree）
EXALTATION_DEG = {
    'Sun': 10.0, 'Moon': 33.0, 'Mars': 298.0, 'Mercury': 165.0,
    'Jupiter': 95.0, 'Venus': 357.0, 'Saturn': 200.0
}

# 落陷度数（入庙 + 180°）
DEBILITATION_DEG = {p: (d + 180) % 360 for p, d in EXALTATION_DEG.items()}

# 行星友好/敌对关系
FRIENDSHIP = {
    'Sun': {'friend': ['Moon', 'Mars', 'Jupiter'], 'enemy': ['Saturn', 'Venus'], 'neutral': ['Mercury']},
    'Moon': {'friend': ['Sun', 'Mercury'], 'enemy': [], 'neutral': ['Mars', 'Jupiter', 'Venus', 'Saturn']},
    'Mars': {'friend': ['Sun', 'Moon', 'Jupiter'], 'enemy': ['Mercury'], 'neutral': ['Venus', 'Saturn']},
    'Mercury': {'friend': ['Sun', 'Venus'], 'enemy': ['Moon'], 'neutral': ['Mars', 'Jupiter', 'Saturn']},
    'Jupiter': {'friend': ['Sun', 'Moon', 'Mars'], 'enemy': ['Mercury', 'Venus'], 'neutral': ['Saturn']},
    'Venus': {'friend': ['Mercury', 'Saturn'], 'enemy': ['Sun', 'Moon'], 'neutral': ['Mars', 'Jupiter']},
    'Saturn': {'friend': ['Mercury', 'Venus'], 'enemy': ['Sun', 'Moon', 'Mars'], 'neutral': ['Jupiter']},
}

# Dig Bala 最强宫位
DIG_BALA_HOUSE = {
    'Sun': 10, 'Mars': 10,  # Midheaven
    'Moon': 4, 'Venus': 4,  # Nadir
    'Jupiter': 1, 'Mercury': 1,  # Ascendant
    'Saturn': 7,  # Descendant
}

# Naisargika Bala（天然力量，单位 Virupas）
NAISARGIKA_BALA = {
    'Sun': 60.0, 'Moon': 60.0, 'Venus': 52.5,
    'Jupiter': 45.0, 'Mercury': 37.5, 'Mars': 30.0, 'Saturn': 22.5
}

# Shadbala 最低要求（Rupas）
MIN_REQUIRED = {
    'Sun': 5.0, 'Moon': 6.0, 'Mars': 5.0,
    'Mercury': 7.0, 'Jupiter': 6.5, 'Venus': 5.5, 'Saturn': 5.0
}

# 昼强/夜强行星
DIURNAL_STRONG = ['Sun', 'Jupiter', 'Venus']
NOCTURNAL_STRONG = ['Moon', 'Mars', 'Saturn']

# 吉星/凶星
BENEFICS = ['Jupiter', 'Venus', 'Mercury']
MALEFICS = ['Saturn', 'Mars', 'Sun']

# 行星相位规则（所有行星都有7宫相位，特殊相位如下）
SPECIAL_ASPECTS = {
    'Mars': [4, 8],     # 火星额外看4宫和8宫
    'Jupiter': [5, 9],  # 木星额外看5宫和9宫
    'Saturn': [3, 10],  # 土星额外看3宫和10宫
}

# Virupas → Rupas 转换（60 Virupas = 1 Rupa）
VIRUPAS_PER_RUPA = 60.0


def calc_shadbala(planets: Dict, asc_sign: str, birth_hour: float,
                  sun_lon: float, moon_lon: float) -> Dict:
    """
    计算完整 Shadbala

    Args:
        planets: 行星数据 dict，每颗行星需要 {sign, degree, house, retrograde, speed}
        asc_sign: 上升星座名称
        birth_hour: 出生时间（当地时间，24小时制）
        sun_lon: 太阳恒星黄道经度
        moon_lon: 月亮恒星黄道经度

    Returns:
        完整的 Shadbala 计算结果
    """
    results = {}
    is_night = birth_hour < 6.0 or birth_hour >= 18.0
    sun_northern = sun_lon >= 270 or sun_lon < 90  # Uttarayana 概略判断

    for pname in ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']:
        if pname not in planets:
            continue
        p = planets[pname]
        lon = p.get('degree', 0)
        sign = p.get('sign', 'Aries')
        house = p.get('house', 1)
        retro = p.get('retrograde', False)
        speed = p.get('speed', 1.0)

        # 1. Sthana Bala（位置力量）
        sthana = calc_sthana_bala(pname, lon, sign, house)

        # 2. Dig Bala（方向力量）
        dig = calc_dig_bala(pname, house)

        # 3. Kala Bala（时间力量）
        kala = calc_kala_bala(pname, is_night, sun_northern, sun_lon, moon_lon)

        # 4. Chesta Bala（运动力量）
        chesta = calc_chesta_bala(pname, retro, speed, sun_lon, moon_lon)

        # 5. Naisargika Bala（天然力量）
        naisargika = NAISARGIKA_BALA.get(pname, 30.0)

        # 6. Drik Bala（相位力量）
        drik = calc_drik_bala(pname, sign, house, planets)

        # 总分（Virupas → Rupas）
        total_virupas = sthana['total'] + dig + kala['total'] + chesta + naisargika + drik
        total_rupas = total_virupas / VIRUPAS_PER_RUPA

        min_req = MIN_REQUIRED.get(pname, 5.0)
        ishta_bala = (total_rupas / min_req * 100) if min_req > 0 else 0

        if ishta_bala >= 150:
            strength_level = "极强"
        elif ishta_bala >= 125:
            strength_level = "强"
        elif ishta_bala >= 100:
            strength_level = "充足"
        elif ishta_bala >= 75:
            strength_level = "略弱"
        elif ishta_bala >= 50:
            strength_level = "弱"
        else:
            strength_level = "极弱"

        results[pname] = {
            'sthana_bala': sthana,
            'dig_bala': round(dig, 2),
            'kala_bala': kala,
            'chesta_bala': round(chesta, 2),
            'naisargika_bala': round(naisargika, 2),
            'drik_bala': round(drik, 2),
            'total_virupas': round(total_virupas, 2),
            'total_rupas': round(total_rupas, 4),
            'min_required': min_req,
            'ishta_bala_pct': round(ishta_bala, 1),
            'strength_level': strength_level,
        }

    # 排名
    ranked = sorted(results.items(), key=lambda x: x[1]['total_rupas'], reverse=True)
    for i, (name, _) in enumerate(ranked):
        results[name]['rank'] = i + 1

    return {
        'method': 'Shadbala六重力量（Parashara系统）',
        'is_night_birth': is_night,
        'sun_uttarayana': sun_northern,
        'planets': results,
        'ranking': [name for name, _ in ranked],
        'strongest': ranked[0][0] if ranked else None,
        'weakest': ranked[-1][0] if ranked else None,
    }


def calc_sthana_bala(pname: str, lon: float, sign: str, house: int) -> Dict:
    """Sthana Bala（位置力量）"""
    # A. Ucha Bala（入庙力量）
    debilit_deg = DEBILITATION_DEG.get(pname, 0)
    offset = (lon - debilit_deg + 360) % 360
    if offset > 180:
        offset = 360 - offset
    ucha_bala = offset / 180 * 60  # 0-60 Virupas

    # B. 简化 Saptavargaja Bala（基于D1位置）
    lord = SIGN_LORDS.get(sign, '')
    if lord == pname:  # 本宫
        sapta_score = 45
    elif pname in FRIENDSHIP.get(lord, {}).get('friend', []):
        sapta_score = 35
    elif pname in FRIENDSHIP.get(lord, {}).get('neutral', []):
        sapta_score = 25
    elif pname in FRIENDSHIP.get(lord, {}).get('enemy', []):
        sapta_score = 15
    else:
        sapta_score = 25
    # 落陷检查
    debilit_sign = SIGNS[int(DEBILITATION_DEG.get(pname, 0) / 30) % 12]
    exalt_sign = SIGNS[int(EXALTATION_DEG.get(pname, 0) / 30) % 12]
    if sign == exalt_sign:
        sapta_score = 50
    elif sign == debilit_sign:
        sapta_score = 5

    # C. Ojayugma Bala（奇偶宫力量）
    if pname in ['Mercury', 'Venus']:
        ojayugma = 15 if house % 2 == 0 else 0
    else:
        ojayugma = 15 if house % 2 == 1 else 0

    # D. Kendra Bala（角宫力量）
    kendra_scores = {1: 60, 4: 40, 7: 20, 10: 30}
    kendra_bala = kendra_scores.get(house, 0)

    # E. Drekkana Bala（三分盘力量）
    deg_in_sign = lon % 30
    if pname in ['Sun', 'Mars', 'Jupiter']:
        drekkana_bala = 15 if deg_in_sign < 10 else 0
    elif pname in ['Moon', 'Venus']:
        drekkana_bala = 15 if 10 <= deg_in_sign < 20 else 0
    else:  # Saturn, Mercury
        drekkana_bala = 15 if deg_in_sign >= 20 else 0

    total = ucha_bala + sapta_score + ojayugma + kendra_bala + drekkana_bala

    return {
        'ucha_bala': round(ucha_bala, 2),
        'sapta_score': round(sapta_score, 2),
        'ojayugma_bala': ojayugma,
        'kendra_bala': kendra_bala,
        'drekkana_bala': drekkana_bala,
        'total': round(total, 2),
    }


def calc_dig_bala(pname: str, house: int) -> float:
    """Dig Bala（方向力量），max 60 Virupas"""
    best_house = DIG_BALA_HOUSE.get(pname, 1)
    # 线性插值：最强宫位=60，对宫=0
    diff = abs(house - best_house)
    if diff > 6:
        diff = 12 - diff
    return max(0, (6 - diff) * 10)


def calc_kala_bala(pname: str, is_night: bool, sun_northern: bool,
                    sun_lon: float, moon_lon: float) -> Dict:
    """Kala Bala（时间力量）"""
    components = {}

    # A. Nathonnata Bala（昼夜力量）
    if pname == 'Mercury':
        nathonnata = 60
    elif is_night and pname in NOCTURNAL_STRONG:
        nathonnata = 60
    elif not is_night and pname in DIURNAL_STRONG:
        nathonnata = 60
    else:
        nathonnata = 0
    components['nathonnata'] = nathonnata

    # B. Paksha Bala（月相力量，简化）
    moon_sun_diff = (moon_lon - sun_lon + 360) % 360
    if pname in ['Jupiter', 'Venus', 'Moon']:
        # 望月（180°）最强
        paksha = moon_sun_diff / 180 * 30
    else:
        # 朔月（0°）最强
        paksha = (180 - moon_sun_diff) / 180 * 30 if moon_sun_diff <= 180 else (moon_sun_diff - 180) / 180 * 30
    components['paksha'] = round(paksha, 2)

    # C. Tribhaga Bala（三段力量）
    if pname == 'Jupiter':
        tribhaga = 45
    elif pname == 'Venus':
        tribhaga = 45
    elif pname == 'Saturn':
        tribhaga = 45
    else:
        tribhaga = 0
    components['tribhaga'] = tribhaga

    # D. Ayana Bala（太阳南北行）
    if pname == 'Mercury':
        ayana = 30
    elif sun_northern and pname in ['Sun', 'Mars', 'Moon']:
        ayana = 30
    elif not sun_northern and pname in ['Jupiter', 'Venus', 'Saturn']:
        ayana = 30
    else:
        ayana = 15
    components['ayana'] = ayana

    total = sum(components.values())
    return {k: v for k, v in components.items()} | {'total': round(total, 2)}


def calc_chesta_bala(pname: str, retro: bool, speed: float,
                     sun_lon: float, moon_lon: float) -> float:
    """Chesta Bala（运动力量），max 60 Virupas"""
    if pname == 'Sun':
        return 60.0  # 太阳始终满分

    if pname == 'Moon':
        # 月亮根据月相：望月=60，朔月=0
        moon_sun_diff = (moon_lon - sun_lon + 360) % 360
        return moon_sun_diff / 180 * 60

    # 其他行星
    if retro:
        return 60.0

    # 速度判断（简化：用speed的绝对值）
    abs_speed = abs(speed)
    if abs_speed > 1.0:  # 快速直行
        return 50.0
    elif abs_speed > 0.5:
        return 35.0
    elif abs_speed > 0.1:
        return 20.0
    else:
        return 10.0  # 接近驻留


def calc_drik_bala(pname: str, sign: str, house: int,
                   all_planets: Dict) -> float:
    """Drik Bala（相位力量），可正可负"""
    drik = 0.0
    p_sign_idx = SIGNS.index(sign) if sign in SIGNS else 0

    for other_name, other_data in all_planets.items():
        if other_name == pname or other_name == 'Rahu' or other_name == 'Ketu':
            continue

        other_sign = other_data.get('sign', '')
        if other_sign not in SIGNS:
            continue
        other_sign_idx = SIGNS.index(other_sign)

        # 计算从other到pname的宫位差
        house_diff = (p_sign_idx - other_sign_idx) % 12 + 1

        # 检查是否形成相位
        has_aspect = False
        if house_diff == 7 or house_diff == 1:  # 7宫相位或合相
            has_aspect = True
        if other_name in SPECIAL_ASPECTS:
            if house_diff in SPECIAL_ASPECTS[other_name]:
                has_aspect = True

        if has_aspect:
            # 判断吉凶
            aspect_value = 15.0
            if house_diff == 1:  # 合相加倍
                aspect_value = 30.0

            if other_name in BENEFICS:
                drik += aspect_value
            elif other_name in MALEFICS:
                drik -= aspect_value
            else:
                drik += aspect_value * 0.5  # 中性行星

    # 限制范围
    return max(-60.0, min(60.0, drik))
