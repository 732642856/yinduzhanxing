# 印度占星 Skill 实用速查指南

> **用途**：本指南是 v3.13.1 新增的实用入口文件。当用户提出问题时，快速定位到正确的分析路径和所需文件。
>
> **使用方式**：CTRL+F 搜索本文件，或直接复制对应场景的执行模板。

---

## 场景一：用户说"帮我看盘"或"分析我的星盘"

**判断类型**：全面综合解盘（Level 2/3）

**执行顺序**：

```
1. 收集出生数据：
   - 阳历出生日期（精确到日）
   - 出生时间（精确到分钟）
   - 出生地点（经纬度或城市名）
   - 时区

2. 调用引擎铸造星盘：
   python3 scripts/jyotish_engine.py full-reading \
     --year YYYY --month MM --day DD \
     --hour HH --minute MM \
     --lat LAT --lon LON --tz TZ

3. 参考文件（按顺序）：
   a) references/vedic-astrology-fundamentals.md（基础知识）
   b) references/yoga-identification-guide.md（Yoga识别）
   c) references/comprehensive-reading-workflow.md（综合解盘工作流）
   d) references/qin_ruisheng_system.md（秦瑞生体系：星曜/宫位/大运/流年）

4. 质量检查（references/deep-analysis-complete-workflow.md）：
   - Shadbala六重力量
   - Ashtakavarga八分法
   - D1+D9双盘验证
   - 三级置信度评分
```

---

## 场景二：用户说"什么时候结婚"或"感情/婚姻应期"

**判断类型**：婚姻专项推运应期（高复杂度）

**执行顺序**：

```
1. 执行四技法交叉验证（必须全部执行）：
   references/marriage-timing-validation-methodology.md
   → Double Transit + DK木星激活 + UL激活 + Dasha支持

2. 补充综合技法：
   references/marriage-timing-comprehensive-techniques.md
   → KN Rao Double Transit + VP Goel功能征象星 + Jaimini DK

3. 配偶多层画像：
   references/spouse-multi-layer-methodology.md
   → DK+7宫主+金星+木星+昼夜区分+Rahu六层确认

4. 婚姻Navamsa深度：
   references/navamsa-marriage-deep-analysis.md
   → D9婚姻五维 + Pushkara + 婚姻8步算法

5. 如果是复合/分阶段：
   references/marriage-timing-comprehensive-techniques.md
   → Ketu期感情特征判断

6. 婚姻计数法（补充）：
   references/bhrigu-pada-dasha-marriage-counting.md
   → 7宫主D1→D9距离计数

7. 引擎调用：
   python3 scripts/jyotish_engine.py dasha \
     --year YYYY --month MM --day DD \
     --hour HH --minute MM --lat LAT --lon LON --tz TZ

   python3 scripts/jyotish_engine.py transit \
     --target-date YYYY-MM-DD \
     --target-planets Jupiter,Venus,Rahu,Ketu \
     --lat LAT --lon LON --tz TZ
```

**注意事项**：
- 7星系统命中率DK 90%/Dasha 70%/UL 40%/DT 20%
- 8星系统命中率DK 100%/UL 60%/DT 40%
- **DK Jaimini激活100%命中率存在虚命中**（11/12星座被相位）→ 作必要条件非充分条件
- 必须转世界时(UT)计算，否则Moon偏移6-8°
- 优先用Double Transit检验7宫/7主/功能DT/UL/DK多个目标组合
- 7星/8星双轨并行，不排他——80%案例两系统给出不同DK

---

## 场景三：用户说"看看事业/财运/学业"（单项分析）

**判断类型**：专项事件分析

**参考路由**：

| 用户意图 | 主参考文件 | 引擎命令 |
|---------|-----------|---------|
| 事业时机 | references/yoga-phala-timing-guide.md | `dasha` + `transit` |
| 财运来源 | references/darakaraka-complete-guide.md（DK财富5模式）| `chart` + `yoga` |
| 学业考试 | references/planetary-dignity-complete-reference.md（D24分析） | `varga -d 24` |
| 健康预后 | references/advanced-techniques.md（8宫+6宫） | `chart` + `shadbala` |
| 职业方向 | references/d10-varga-guide.md（D10事业盘） | `varga -d 10` |

---

## 场景四：用户上传PDF星盘文件

**执行顺序**：

```
1. 使用 PDF Skill 提取PDF文本（见 use_skill tool）

2. 提取数据验证清单（references/pdf-data-extraction-guide.md）：
   □ D1 12宫主星及落宫
   □ D9 Navamsa 关键星曜
   □ D10 Dashamsha 事业格局
   □ Vimshottari Dasha 时间线
   □ Shadbala 六重力量表
   □ Ashtakavarga SAV值
   □ 特殊Lagna（Chalit/OM/Sahaj）
   □ Karaka列表（除标准7个外+Chara Karaka）

3. 完整性门检查（references/comprehensive-reading-workflow.md §1）：
   → 数据完整 → 进入全链路分析
   → 数据缺失 → 降级分析并注明限制

4. 全链路分析：
   references/deep-analysis-complete-workflow.md
   → 12模块系统化分析
```

---

## 场景五：用户说"我没有出生时间"或"只有年月日"

**判断类型**：生时矫正 / 有限数据分析

**执行顺序**：

```
1. 出生时间矫正：
   references/birth-time-rectification-guide.md
   → 收集10-25个生命事件
   → 8大矫正方法自动验证
   → 输出矫正结果+置信度

   引擎命令：
   python3 scripts/jyotish_engine.py cmd_rectify \
     --events "事件描述1 日期1,事件描述2 日期2,..."

2. 如果无法矫正（有限数据模式）：
   references/vedic-astrology-modern-practice-guide.md
   → 使用星宿+星座+行星分布做有限分析
   → 明确注明置信度限制
```

---

## 场景六：用户提出一个具体问题（不提供出生时间）

**判断类型**：Prashna单事件问事（时卦/卜卦）

**执行顺序**：

```
1. 调用引擎铸造即时星盘：
   python3 scripts/jyotish_engine.py prashna \
     --datetime "YYYY-MM-DD HH:MM" \
     --lat LAT --lon LON --mode chart

2. 参考文件：
   references/single-event-inquiry-protocol.md（标准十步断卦模板）
   references/prashna-complete-guide.md（完整方法论）

3. 问题类型路由（references/single-event-inquiry-protocol.md）：
   | 问题类型 | 征象宫位 | 关键行星 |
   |---------|---------|---------|
   | 婚姻/感情 | 7宫+金星 | Jupiter/Saturn |
   | 事业/职业 | 10宫+太阳 | Saturn/Mars |
   | 财务/投资 | 2宫+11宫 | Jupiter/Venus |
   | 健康/疾病 | 6宫+8宫 | Mars/Saturn |
   | 法律/诉讼 | 6宫+8宫+12宫 | Saturn/Ketu |
   | 失物/寻人 | 8宫+2宫 | Mercury/Rahu |

4. 十步断卦执行（references/single-event-inquiry-protocol.md）：
   Step 1: 输入信息收集
   Step 2: 铸造Prashna星盘
   Step 3: 计算AL/Trisphuta
   Step 4: 征象星力量对比
   Step 5: Tajika Yoga检查
   Step 6: Sphuta组合
   Step 7: 阻碍排查
   Step 8: 时间判断
   Step 9: KP Sub-Lord补充
   Step 10: 综合结论

5. 特殊场景补充：
   - 失物：references/prashna-complete-guide.md（Chor Graha+Kunda）
   - 健康：references/prashna-complete-guide.md（Mrityu Chakra）
```

---

## 场景七：用户说"查一下XXX的星盘"或"验证某个名人的盘"

**执行顺序**：

```
1. 名人数据库查询：
   python3 scripts/jyotish_engine.py celebrity \
     --name "姓名"

   数据库统计：
   python3 scripts/jyotish_engine.py db-stats

2. 参考文件：
   references/famous-case-library.md（24个案例索引）
   references/celebrity-cases.md（案例分析）

3. 验前事标准流程：
   references/deep-analysis-complete-workflow.md
   → 用已知事件验证星盘正确性
   → 再做未知事件预测

4. Shatabhisha专项（如果涉及）：
   references/shatabhisha-complete.md
   → 星宿深度解读
```

---

## 场景八：Double Transit 查询（特定行星过境）

**执行顺序**：

```
1. 多参考点过境分析（必须执行）：
   references/transit-multi-reference-guide.md
   → 4个参考点（上升/月亮/太阳/Dasha Lord）
   → 防回归干扰

2. 引擎调用：
   python3 scripts/jyotish_engine.py transit \
     --target-date YYYY-MM-DD \
     --target-planets "Planet1,Planet2" \
     --reference-points "Lagna,Moon,Sun,DashaLord" \
     --lat LAT --lon LON --tz TZ

3. Sade Sati专项（如涉及土星）：
   references/qin_ruisheng_system.md（§6.3 Sade Sati判断）
   references/navatara-kantaka-shani-guide.md

4. 年度运势（Varshaphala）：
   references/varshaphala-annual-chart-guide.md
```

---

## 场景九：全面深度分析（高精度要求）

**执行顺序**：

```
references/deep-analysis-complete-workflow.md（12模块系统化分析）

Level 1 → Level 2 → Level 3 递进：
  Level 1：基础格局（5分钟）
  Level 2：专项分析（20分钟）
  Level 3：深度多系统（60分钟+）

12模块顺序：
  M1: D1本命盘基础
  M2: 特殊Lagna（Chalit/OM/Sahaj）
  M3: Jaimini Karaka系统
  M4: Shadbala六重力量
  M5: Avastha行星状态
  M6: Bhava Bala宫位力量
  M7: Vimsopaka分盘综合
  M8: 19分盘系统
  M9: Ashtakavarga八分法
  M10: 多Dasha收敛（6系统）
  M11: Navamsa婚姻深度
  M12: 综合结论+置信度
```

---

## 场景十：精准解盘质量控制（最后一步必做）

**所有分析完成后执行**：

```
references/precision-reading-methodology.md

PACDARES 框架：
  P: Planets（行星）
  A: Aspects（相位）
  C: Constellations in Signs（星座中的星群）
  D: Dignity（尊严状态）
  A: Analytical Houses（分析宫位）
  R: Rashis（月亮星座）
  E: Essential Strength（本质力量）
  S: Situational Strength（情境力量）

九层复合方法 + L3矛盾检查 + 三级置信度

references/deep-analysis-complete-workflow.md（质量检查清单）：
  □ 验前事通过？
  □ PACDARES通过？
  □ 多系统收敛？
  □ 三级置信度≥2？
  □ 矛盾检查通过？
  □ 置信度≥3才给出确定结论
```

---

## 引擎子命令速查表

| 场景 | 命令 |
|-----|------|
| 星盘计算 | `python3 scripts/jyotish_engine.py chart ...` |
| 全链路解盘 | `python3 scripts/jyotish_engine.py full-reading ...` |
| 大运时间线 | `python3 scripts/jyotish_engine.py dasha ...` |
| Yoga识别 | `python3 scripts/jyotish_engine.py yoga ...` |
| 分盘计算 | `python3 scripts/jyotish_engine.py varga -d 9` |
| 过境查询 | `python3 scripts/jyotish_engine.py transit ...` |
| 六重力量 | `python3 scripts/jyotish_engine.py shadbala ...` |
| 八分法 | `python3 scripts/jyotish_engine.py ashtakavarga ...` |
| Prashna时卦 | `python3 scripts/jyotish_engine.py prashna --datetime ...` |
| 名人查询 | `python3 scripts/jyotish_engine.py celebrity --name ...` |
| 数学验证 | `python3 scripts/jyotish_engine.py validate ...` |
| 行星审计 | `python3 scripts/jyotish_engine.py audit ...` |
| HTML报告 | `python3 scripts/jyotish_engine.py report ...` |

---

*本文件为 v3.13.1 新增，配合 SKILL.md 主文档使用。*
*最后更新：2026-04-26*
