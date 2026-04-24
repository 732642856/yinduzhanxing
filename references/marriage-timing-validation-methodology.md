# 婚姻应期技法验证方法论与修正经验

> 版本：v1.2 | 日期：2026-04-25 | 基于10名人案例验证 | **7星/8星双轨并行**

---

## 一、验证框架

### 4技法交叉检验体系

| 技法 | 来源 | 检验内容 |
|------|------|---------|
| **Double Transit (DT)** | KN Rao | 木星+土星同时相位7宫/7主/功能征象星 |
| **DK木星激活** | Jaimini | 木星过境DK所在星座（Parashari相位 + Jaimini星座相位） |
| **UL激活** | Jaimini/Parashara | 木星或土星过境相位Upapada Lagna |
| **Dasha支持** | Parashara | 7主/DK/Venus出现在大运(Mahadasha)或小运(Antardasha)中 |

### 验证结果（10案例）

> ⚠️ 以下为8星系统DK（v3验证结果）。7星系统DK需重新验证。

| 案例 | DK(8星) | DK(7星)* | DT | DK激活 | UL | Dasha | 总分 |
|------|---------|----------|-----|--------|-----|-------|------|
| 奥巴马 | Sun@狮子 | — | ❌ | ✅ Jaimini | ❌ | ❌ | 1/4 |
| 克林顿 | Jupiter@天秤 | — | ✅ 7主DT | ✅ Jaimini | ❌ | ✅ | 3/4 |
| 比尔盖茨 | Jupiter@狮子 | — | ❌ | ✅ Jaimini | ✅ | ✅ | 3/4 |
| 特朗普 | Saturn@巨蟹 | — | ✅ 7宫DT | ✅ Jaimini | ✅ | ✅ | **4/4** |
| 朱莉 | Moon@天秤 | — | ✅ 7宫DT | ✅ Jaimini | ✅ | ✅ | **4/4** |
| 贝克汉姆 | Venus@金牛 | — | ❌ | ✅ Jaimini | ✅ | ❌ | 2/4 |
| 乔丹 | Venus@摩羯 | — | ❌ | ✅ Jaimini | ❌ | ❌ | 1/4 |
| 梅根 | Jupiter@处女 | — | ❌ | ✅ Jaimini | ❌ | ✅ | 2/4 |
| 马斯克 | Jupiter@天蝎 | — | ❌ | ✅ Jaimini | ✅ | ✅ | 3/4 |
| 凯特王妃 | Venus@摩羯 | — | ❌ | ✅ Jaimini | ✅ | ✅ | 3/4 |

*7星DK列待补充（需重新计算）

### 统计

| 技法 | 命中率 | 评价 |
|------|--------|------|
| DK木星Jaimini激活 | **10/10 (100%)** | ⚠️ 可能含虚命中（见修正3） |
| Dasha支持 | 7/10 (70%) | 中高可靠 |
| UL激活 | 6/10 (60%) | 中等可靠 |
| Double Transit | 4/10 (40%) | 被高估，不应做唯一判据 |

---

## 二、关键修正经验

### 修正1：Chara Karaka 7星/8星双轨并行（2026-04-25 定稿）

**原则**：7星和8星两套系统**分开分析，并行使用，不做排他选择**。

**理由**（基于全网专家研究）：
1. **BPHS原文两说并存**：Parasara 记载"太阳到土星7个，或太阳到罗睺8个"，未做排他性裁决
2. **当代专家分歧**：K.N. Rao 支持7星，Sanjay Rath 支持8星，两派均有大量实战验证
3. **两套DK可能捕捉不同维度**：7星DK = 传统配偶征象，8星DK = 业力/灵魂层面的配偶征象
4. **Future Samachar 结论**："没有一种方案能持续给出正确结果" → 双轨互补更稳妥
5. **用户数据源**：JH PDF标注7星结果，部分教材用8星方案 → 两套都需要

**全网专家立场汇总**：

| 占星师 | 立场 | 关键理由 |
|--------|------|---------|
| K.N. Rao | 7星 | Rahu不能当AK；父亲用BK+太阳判断；强调Sthira Karaka配合 |
| Sanjay Rath | 8星 | 有情众生应用8星 |
| P.V.R. Narasimha Rao (JH作者) | 混合7/8 | JH默认7星，提供8星切换 |
| Debraj Roy (3000+咨询) | 7星 | "实战中取得良好结果" |
| sarvatobhadra.com | 8星 | 个人命盘推荐8星 |
| Future Samachar (Harsha Indrasena) | 都不完美 | "没有方案能持续准确"，提出Matru+Pitru合并方案 |
| Barbara Pijan Lama | 7星 | 明确跟随Rao |
| 用户教学材料 | 8星 | 明确使用8星方案，不含Ketu |

**双轨代码实现**：

```python
# === 7星系统（K.N. Rao / JH默认）===
planets_7 = {n: l for n, l in planets.items() if n != 'Rahu'}
pdeg_7 = {n: l % 30 for n, l in planets_7.items()}
sorted_7 = sorted(pdeg_7.items(), key=lambda x: x[1], reverse=True)
dk_7 = sorted_7[6][0]  # 第7个 = DK（度数最低）

# === 8星系统（Sanjay Rath / 含Rahu）===
pdeg_8 = {n: l % 30 for n, l in planets.items()}
rahu_lon = get_planet_lon(jd, 10)
rahu_corrected = 30.0 - (rahu_lon % 30)  # 逆行校正
pdeg_8['Rahu'] = rahu_corrected
sorted_8 = sorted(pdeg_8.items(), key=lambda x: x[1], reverse=True)
dk_8 = sorted_8[6][0]  # 第7高 = DK（第8颗被排除）

# === 输出对比 ===
print(f"DK(7星): {dk_7}@{signs[int(planets_7[dk_7]/30)]}")
print(f"DK(8星): {dk_8}@{signs[int(planets[dk_8]/30)]}")
```

**一楠的对比**：
| 项目 | 7星系统（JH PDF） | 8星系统 |
|------|-----------------|---------|
| DK | Mars@Cancer 19°51' | Sun@Aries 3°02' |
| AK | Sun@Aries | Jupiter@Aries |
| 配偶征象 | 火星特质（行动/保护/军事） | 太阳特质（领导/权威/自信） |

### 修正2：出生时间必须转UT（世界时）

**问题**：v2验证直接用当地时间输入swisseph，导致行星位置偏差5-15°。

**正确做法**：
```python
# 名人出生时间多为当地时间 → 必须转UT
ut_hour = local_hour - timezone_offset
jd = swe.julday(year, month, day, ut_hour, gregflag=1)
```

**时区参考**（常用）：
| 地区 | 时区偏移 |
|------|---------|
| 美东夏令(EDT) | -4 |
| 美东标准(EST) | -5 |
| 美中(CST) | -6 |
| 美西夏令(PDT) | -7 |
| 美西标准(PST) | -8 |
| 夏威夷 | -10 |
| 英国夏令(BST) | +1 |
| 英国标准(GMT) | 0 |
| 南非(SAST) | +2 |
| 中国(CST) | +8 |

**影响**：1小时偏差≈15°地球自转→Moon可能偏移6-8°→影响Nakshatra判定→影响Dasha起始点。

### 修正3：Jaimini星座相位的覆盖面极广

**问题**：DK木星Jaimini激活100%命中，但这个"100%"可能包含大量虚命中。

**原因分析**：Jaimini星座相位定义中，除了同星座外几乎都互相相位：
```
移动组(白羊/巨蟹/天秤/摩羯)：互相相位 + 相位固定组
固定组(金牛/狮子/天蝎/水瓶)：互相相位 + 相位变动组
变动组(双子/处女/射手/双鱼)：互相相位 + 相位移动组
```
12个星座中，木星只"不相位"自己所在的星座（同星座无相位），即11/12的星座都被相位。

**这意味着**：只要DK不在白羊（木星大约每12年经过白羊1年），DK Jaimini激活就会成立。一年中约92%的时间这个条件都满足。

**修正建议**：
1. DK Jaimini激活应作为**必要条件**而非充分条件
2. 必须结合其他技法（DT/UL/Dasha）做交叉验证
3. 更精确的检验应加入**Parashari度数相位**（5-9-7-3-1距）而非仅Jaimini星座相位
4. 考虑加入**DK度数精确激活**（木星过境DK的精确度数±5°以内）

### 修正4：Double Transit不应作为唯一判据

**数据**：仅4/10案例在结婚日满足完整7宫Double Transit。

**替代方案**：DT应检验多个目标：
- 7宫本身（sev_si）
- 7宫主所在星座（sev_lord_si）
- 功能9主/10主所在星座（VP Goel扩展）
- DK所在星座
- UL所在星座

DT命中任一目标组合即算通过。克林顿案例：7宫DT不成立，但7主DT和功能DT同时成立。

---

## 三、验证脚本设计规范

### 标准验证流程

```python
# 1. 出生数据 → UT转换
ut_hour = local_hour - tz_offset
jd = swe.julday(y, m, d, ut_hour, 1)

# 2. 双轨 Chara Karaka（7星+8星并行）
# 7星（K.N. Rao / JH默认）
planets_7 = {n: l for n, l in planets.items() if n != 'Rahu'}
pdeg_7 = {n: l % 30 for n, l in planets_7.items()}
sorted_7 = sorted(pdeg_7.items(), key=lambda x: x[1], reverse=True)
dk_7 = sorted_7[6][0]

# 8星（Sanjay Rath / 含Rahu逆行校正）
pdeg_8 = {n: l % 30 for n, l in planets.items()}
rahu_corrected = 30.0 - (get_planet_lon(jd, 10) % 30)
pdeg_8['Rahu'] = rahu_corrected
sorted_8 = sorted(pdeg_8.items(), key=lambda x: x[1], reverse=True)
dk_8 = sorted_8[6][0]

# 3. 过境检验
jup_lon = calc_ut(marriage_jd, JUPITER, FLG_SIDEREAL)
sat_lon = calc_ut(marriage_jd, SATURN, FLG_SIDEREAL)

# 4. Parashari相位（度数精确）
def jup_asp(jup_si, target_si):
    return (jup_si - target_si) % 12 in {4, 6, 8}  # 5-9-7相位

def sat_asp(sat_si, target_si):
    return (sat_si - target_si) % 12 in {2, 6, 9}  # 3-7-10相位

# 5. Jaimini星座相位（宽松）
def jaimini_aspect(s1, s2):
    movable = {0,3,6,9}; fixed = {1,4,7,10}; dual = {2,5,8,11}
    if s1 == s2: return False
    if s1 in movable and s2 in fixed: return True
    if s1 in fixed and s2 in dual: return True
    if s1 in dual and s2 in movable: return True
    if s2 in movable and s1 in fixed: return True
    if s2 in fixed and s1 in dual: return True
    if s2 in dual and s1 in movable: return True
    if s1 in movable and s2 in movable: return True
    if s1 in fixed and s2 in fixed: return True
    if s1 in dual and s2 in dual: return True
    return False
```

### UL计算标准流程

```python
def calc_ul(asc_si, planets):
    twelfth = (asc_si + 11) % 12
    lord = sign_lords[twelfth]
    lord_si = sidx(planets[lord])
    
    # 例外1: 宫主星在12宫本身 → 跳到第10宫
    if lord_si == twelfth:
        return (twelfth + 9) % 12
    
    # 例外2: 宫主星在12宫的第7宫 → 跳到第4宫
    if lord_si == (twelfth + 6) % 12:
        return (twelfth + 3) % 12
    
    # 标准: 从12宫数到宫主星位置的距离，再从宫主星数同样的距离
    dist = (lord_si - twelfth) % 12
    if dist == 0: dist = 12
    return (lord_si + dist) % 12
```

---

## 四、待办事项与后续验证方向

### 高优先级
- [ ] **7星系统名人验证**：同一批10个名人用7星DK跑验证，与8星结果直接对比
- [ ] **随机对照实验**：对每个案例取结婚日±1年的随机日期，检验4技法命中率基线
- [ ] **DK精确度数激活**：木星过境DK精确度数±5°以内的命中率
- [ ] **Navamsha落点检验**：木星/土星过境DK的D9星座

### 中优先级
- [ ] 扩展到20+案例验证
- [ ] 加入条件Dasha检验（如D9 Navamsha Dasha）
- [ ] 女性案例单独统计（昼夜区分法影响）

### 方法论优化
- [ ] DK Jaimini激活改为"加权命中"：Parashari相位=2分，Jaimini相位=1分
- [ ] DT检验增加DK/UL作为目标
- [ ] Dasha检验扩展到Pratyantar级别

---

*本文件为婚姻应期验证的持续迭代文档，每次验证后更新。*
