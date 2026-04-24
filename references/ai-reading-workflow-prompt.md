# AI解盘工作流Prompt工程（AI Reading Workflow）

> **适用场景**：AI收到出生信息、PDF星盘或文字星盘后，如何一步步执行完整的解盘+推运分析
> **版本**：v3.0.0 | **更新日期**：2026-04-25
> **优先级**：⭐⭐⭐⭐⭐（AI解盘质量的决定性文件）
> **定位**：本文件是AI解盘的**执行引擎**，将Skill中所有参考资料串联成可执行的工作流
> **v3.0重大变更**：三条入口路径明确分流，引擎全自动计算无需用户逐模块触发

---

## ⚠️ 核心原则

1. **不跳步**：每个阶段必须完成后才能进入下一阶段
2. **不猜测**：数据缺失时标注"缺失"，不编造数据
3. **不锚定**：先输出星盘推导，再等用户反馈，不先知道用户生活再"找依据"
4. **必标注**：每个结论标注来源系统、置信度、精度边界
5. **全自动优先**：引擎有能力自动完成的计算，绝不要求用户手动触发
6. **尊重用户数据**：用户提供的PDF/文字星盘数据即为事实来源，优先使用而非重新计算

---

## 🔴🔴🔴 性别前置检查（必读！每次解盘前必须确认！）

> **⚠️ 这是从多次用户纠正中提炼的硬性规则，违反会导致全盘分析方向错误！**

### 规则1：性别决定征象星体系

**分析配偶/婚姻/感情之前，必须先确认命主性别！**

| 性别 | 日/夜盘 | 丈夫征象星 | 妻子征象星 |
|------|---------|-----------|-----------|
| **女性** | 日盘（白天出生） | **木星 Jupiter**（入Sect，权重最高）+ **火星 Mars**（出Sect，次之） | — |
| **女性** | 夜盘（夜晚出生） | **火星 Mars**（入Sect，权重升高）+ **木星 Jupiter**（出Sect，权重降低） | — |
| **男性** | 日盘 | — | **金星 Venus**（出Sect）+ **月亮 Moon** |
| **男性** | 夜盘 | — | **金星 Venus**（入Sect，权重最高）+ **月亮 Moon** |

### 规则2：DK系统是性别中立的

- DK（Darakaraka）= 度数最低的行星，**不分男女**
- 但DK必须与上述性别征象星交叉验证，不能替代
- **禁止**："女命只看木星" 或 "男命只看金星" 的单一判据

### 规则3：具体纠正记录

以下错误曾反复发生，务必避免：

- ❌ **错误**：分析女性命盘时用"她"描述配偶（配偶应为"他"）
- ❌ **错误**：女性日盘用Venus作为丈夫征象星（应用Jupiter+Mars）
- ❌ **错误**：忽略昼夜区分对征象星权重的影响
- ❌ **错误**：只看DK不看传统征象星，或只看传统征象星不看DK
- ✅ **正确**：多层交叉确认（DK + 7宫主 + 天然征象 + 昼夜区分）

### 规则4：案例分析示例

**一楠（女性，日盘，14:45出生）：**
- Mars同时承担三重身份：DK配偶星 + 女性日盘丈夫征象星 + Leo上升Yogakaraka
- 木星Jupiter是丈夫首要天然征象星（女性日盘入Sect）
- 分析配偶时必须用"他"（男性），不能用"她"

---

## 🔴 阶段零：入口路由（三条路径）

### 用户消息到达后，AI立即判断走哪条路径：

```
用户消息到达
  │
  ├─→ 【路径A】用户提供了精准出生信息（日期+时间+地点）
  │     → 直接调用 full-reading 引擎全链路计算
  │     → 跳到阶段二
  │
  ├─→ 【路径B】用户提供了PDF/图片星盘 或 丰富的文字星盘描述
  │     → 提取文档中的所有星象数据（落宫、度数、Dasha等）
  │     → 直接基于提取的数据进行推算分析
  │     → 跳到阶段二
  │
  └─→ 【路径C】用户出生时间不明确 或 仅知道大概时间
        → 启动互动式出生时间矫正
        → 矫正完成后走路径A
```

---

### 路径A：精准出生信息 → full-reading 全自动计算

**触发条件**：用户提供了明确的出生日期+时间+地点（三者齐全）

**示例输入**：
- "1993年4月17日 14:45 邯郸"
- "我出生于 1990-08-15 早上6:30 北京"
- "April 17, 1993, 2:45 PM, Handan, China (36.6N, 114.5E)"

**执行指令**（一条命令搞定所有计算）：

```bash
python3 scripts/jyotish_engine.py full-reading \
  --year YYYY --month MM --day DD --hour HH --minute MM \
  --lat XX.XX --lon XX.XX --tz X
```

**此命令自动执行13个计算步骤**：
1. chart — 核心星盘（上升、行星位置、宫位）
2. dasha — Vimshottari大运时间线
3. yoga — Yoga格局识别
4. varga_full — BPHS十六分盘（D2-D60）
5. aspects — 度数精确相位系统
6. jaimini — Chara Karaka + Chara Dasha + Karakamsha
7. nakshatra_adv — Tara Bala + Sub-Lord
8. argala — Argala门闩系统
9. tajika — Tajika年运盘
10. shadbala — 六重力量
11. ashtakavarga — 八分法
12. validation — R1-R10数学验证
13. audit — P1-P12行星审计

**输出结构**：
- `chart`：完整星盘数据
- `modules`：12个模块各自的结果
- `summary`：计算耗时、模块数、错误数
- `errors`/`warnings`：异常信息

**数据质量门**：

| 字段 | 检查项 | 判定 |
|------|--------|------|
| `summary.errors` | 是否为空 | 空则继续，非空需评估 |
| `summary.modules_computed` | 是否≥10 | ≥10正常，<10说明多模块失败 |
| `chart.ascendant` | 是否有上升星座 | 无则计算失败，需排查 |

**完成后**：直接跳到阶段二（意图识别）

---

### 路径B：PDF/文字星盘 → 数据提取 + 直接推算

**触发条件**：用户上传了PDF星盘、截图，或提供了详细的文字星盘描述

**示例输入**：
- 上传11页JhoroWatch PDF
- 上传Parashara's Light截图
- 文字描述："我的上升是狮子座，太阳在白羊座9宫，月亮在水瓶座7宫..."

**⚠️ 核心原则：用文档的数据，不重新排盘**

用户提供的PDF/文字星盘中的数据就是**事实来源**。AI不需要从出生时间重新计算星盘，而是直接使用文档中已有的：
- 行星落宫落座
- Dasha时间线
- Shadbala分数
- Ashtakavarga点数
- Yoga列表
- 分盘数据

**执行步骤**：

```
1. 识别来源（JH / Parashara's Light / 其他软件）
2. 逐页/逐段提取所有星象数据
3. 填充标准JSON Schema（见下方模板）
4. 执行数据完整性门（Quality Gate）
5. 如有出生时间+地点，额外调用 full-reading 补充计算
6. 输出提取报告
```

**数据提取模板**：

```markdown
## 📋 星盘数据提取报告

**来源**：[JH / PL / 文字描述] | **完整度**：[XX%]

### 基本信息
- 出生：[YYYY-MM-DD HH:MM] [地点] [性别]
- Ayanamsa：[Lahiri XX°XX'XX"]

### D1概要
- 上升：[星座] [度数]° ([Nakshatra] P[Pada])
- AL：[星座] | UL：[星座] | HL：[星座] | GL：[星座]

### 行星配置表
| 行星 | 星座 | 宫位 | 度数 | NK | Pada | 状态 | 逆行 | 燃烧 | 战争 |
|------|------|------|------|-----|------|------|------|------|------|
| Sun  |      |      |      |     |      |      |      |      |      |
| Moon |      |      |      |     |      |      |      |      |      |
| ...  |      |      |      |     |      |      |      |      |      |

### Jaimini Karakas
- AK=[行星] AmK=[行星] BK=[行星] MK=[行星] PK=[行星] GK=[行星] DK=[行星]

### 关键分盘
- D9上升：[星座] | D10上升：[星座]

### 当前Dasha
- Maha：[行星] ([起]-[止])
- Antar：[行星] ([起]-[止])
- Pratyantar：[行星] ([起]-[止])

### Shadbala摘要
- 最强：[行星] [分数]R | 最弱：[行星] [分数]R

### Ashtakavarga SAV
- 宫位：1  2  3  4  5  6  7  8  9  10 11 12
- 点数：[XX XX XX XX XX XX XX XX XX XX XX XX]

### Yoga清单
- [Yoga1]：[行星]在[X宫]
```

**数据完整性门**：

| 完整度 | 判定 | 允许的分析 |
|--------|------|-----------|
| ≥90%（P0全齐） | ✅ Pass | Level 2/3完整分析 |
| 70-89%（P0大部分） | ⚠️ Limited | Level 2，标注限制 |
| <70%（P0缺关键项） | ❌ Fail | Level 1快速概览，要求用户补全 |

**补充计算**（条件触发）：

如果PDF中包含了出生日期+时间+地点信息，AI **应当额外调用** `full-reading` 来补充PDF中可能缺失的计算（如精确相位、Argala、Tajika等v3.7新增模块），将引擎计算结果与PDF提取数据合并，以引擎结果为补充、PDF数据为基准。

**完成后**：直接跳到阶段二（意图识别）

---

### 路径C：时间不明确 → 互动式出生时间矫正

**触发条件**：
- 用户说"不知道出生时间" / "大概下午吧" / "不清楚几点"
- 用户只知道日期不知道时间
- 用户提供的出生证明时间与实际有出入

**⚠️ 核心理念：不猜时间，通过互动逐步锁定**

AI不应该凭空假设一个时间，而应该通过结构化互动帮助用户锁定精确时间。

**矫正流程**（→ `birth-time-rectification-advanced.md`）：

#### C1. 初始信息收集（第一轮互动）

**AI必须收集的基础信息**（只问一轮，最多5个问题）：

```
"为了帮你精准确定出生时间，我需要了解一些信息：

1. 你目前知道的出生时间范围是什么？（比如'下午2点到5点'、'上午'、'完全不知道'）
2. 出生地点是哪里？（城市即可）
3. 你的体型偏瘦/中等/偏壮？脸型偏圆/长/方？
4. 容易出现健康问题的部位是？（比如经常头痛/肠胃不好/腰痛等）
5. 有没有明显的胎记或疤痕？在身体什么位置？"
```

#### C2. 外表体质初筛（AI自动分析）

根据用户回答，确定上升星座范围：
- 体型+脸型+健康倾向 → 缩小到2-3个候选上升星座
- 胎记/疤痕位置 → 进一步缩小范围
- 参照 `birth-time-rectification-advanced.md` 中的外表体质对应表

#### C3. 生活事件验证（第二轮互动）

**AI请求用户提供人生重要事件**：

```
"初步判断你的上升可能在[星座A]或[星座B]。
为了进一步确认，请告诉我你人生中的一些重要转折事件，
大概5-10个就行，包括大概的时间和事件类型。比如：
- 搬家、转学、毕业
- 工作/事业的重要变化
- 开始或结束一段感情
- 亲人离世或重病
- 获奖或重大成就
- 生病或手术"
```

**AI对每个事件做Dasha+Transit验证**：
- 用候选时间分别排盘
- 检查事件时间点的Dasha周期是否激活相关宫位
- 检查Transit是否支持该事件
- 计算每个候选时间的吻合率

#### C4. D9/D10精确校正（第三轮互动，可选）

如果需要更精确（精确到±5分钟以内）：

```
"时间范围已经缩小到[XX:XX-XX:XX]。
为了进一步精确，请告诉我：
1. 你的感情模式是怎样的？（主动/被动、深刻/轻松、重视精神连接/重视现实基础）
2. 你的工作风格是怎样的？（管理型/创意型/研究型/服务型）"
```

- 感情模式 → 判定D9上升 → 缩小时间
- 工作风格 → 判定D10上升 → 缩小时间

#### C5. 矫正结果输出

```markdown
## 🔧 出生时间矫正报告

### 信息收集
- 已知时间范围：[描述]
- 外表体质：[描述]
- 事件验证：[N]个事件

### 矫正过程
- 上升候选：[星座A] / [星座B] → 判定：[星座X]
- Dasha吻合率：[XX%]
- Transit吻合率：[XX%]
- D9上升判定：[星座]（基于感情特质）
- D10上升判定：[星座]（基于事业特质）

### 矫正结果
- **矫正后出生时间**：[HH:MM]
- **置信度**：[高/中/低]（[XX%]事件吻合）
- **精度范围**：±[X]分钟

### ⚠️ 声明
出生时间矫正是基于事件反向推导的概率性方法。
矫正后的时间不能100%保证精确，但基于[X]个事件的验证，
吻合率达到[XX%]，可作为有效参考。
```

**矫正完成后**：使用矫正后的时间走路径A，调用 `full-reading` 全链路计算。

---

## 阶段二：用户意图识别与路由

### 2.1 意图路由表

| 用户意图 | 目标宫位 | 核心参考文件 | 承诺模板 |
|----------|---------|-------------|---------|
| 婚姻/恋爱/关系 | 7宫 | `relationship-astrology-guide.md` | §1 |
| 事业/职业/工作 | 10宫 | `house-modern-mapping.md` | §2 |
| 财富/收入/投资 | 2宫+11宫 | `house-domain-planet-mapping.md` | §3 |
| 子女/创作 | 5宫 | `modern-life-scenarios-complete.md` | §4 |
| 健康/体质 | 1宫+6宫+8宫 | — | §5 |
| 教育/学业 | 4宫+9宫 | — | §6 |
| 出国/迁移 | 9宫+12宫 | — | §7 |
| 灵性/修行 | 9宫+12宫 | — | §8 |
| 合盘/关系匹配 | 7宫 | `synastry` + `relationship-astrology-guide.md` | §1 |
| 综合解盘（全盘） | 全部 | `comprehensive-reading-workflow.md` | 全部 |

**（承诺模板→ `promise-assessment-templates.md`）**

### 2.2 用户未明确意图时的默认流程

如果用户没有说具体问什么（比如只给了出生信息或上传了PDF）：
1. 执行**综合解盘工作流Level 2**（`comprehensive-reading-workflow.md`）
2. 先输出10宫位快速扫描
3. 识别最强和最弱的领域
4. 重点展开当前Dasha激活的领域
5. 主动提示用户可以深入询问任何领域

---

## 阶段三：静态星盘分析（→ 多个参考文件）

### 3.1 执行顺序（严格按此顺序）

```
Step 3.1  宫位-行星基础分析
          → references/planets.md
          → references/signs-and-houses.md

Step 3.2  承诺评估（Promise Assessment）
          → references/promise-assessment-templates.md
          → 输出：承诺等级（完整/部分/缺失）

Step 3.3  Yoga格局识别
          → references/yoga_list.md
          → references/yoga-list-chinese.md
          → references/yoga-strength-scoring-system.md

Step 3.4  Argala检查（目标宫的2/4/5/8/11宫）
          → references/argala-complete-guide.md
          → 输出：目标宫是否被"开门"或"锁门"

Step 3.5  逆行/燃烧/行星战争检查
          → references/retrograde-combustion-war-guide.md
          → 每颗行星检查三重叠加

Step 3.6  Nakshatra深度解读
          → references/nakshatra_deities.md
          → references/nakshatra-chinese-quick-ref.md

Step 3.7  Shadbala评估
          → references/shadbala-complete-methodology.md
          → 输出：行星力量排名

Step 3.8  Ashtakavarga评估
          → references/ashtakavarga-complete-system.md
          → 输出：SAV 12宫排名 + 关键阈值判断

Step 3.9  Ketu双属性检查
          → references/ketu-dual-nature-guide.md
          → 如果命盘有Ketu，必须同时评估"放手"和"突破"

Step 3.10 分盘确认
          → references/varga-system-quick-reference.md
          → D9（关系）+ D10（事业）+ 对应领域分盘
```

### 3.2 静态分析输出模板

```markdown
## 🔍 静态星盘分析

### 承诺评估（Promise）
| 领域 | 宫位 | 宫主星 | Karaka | 分盘确认 | 承诺等级 |
|------|------|--------|--------|---------|---------|
| [领域] | [强/中/弱] | [状态] | [状态] | [✅/❌] | [完整/部分/缺失] |

### Yoga格局
| Yoga | 构成 | 强度 | 领域影响 |
|------|------|------|---------|
| [名称] | [行星]在[X宫] | [强/中/弱] | [促进/阻碍] |

### Argala分析（目标宫=[X宫]）
| 干预宫 | 行星 | 效应 | Virodha | 最终 |
|--------|------|------|---------|------|
| 2宫 | [行星] | [吉/凶]Argala | 12宫[空/行星] | [开门/锁门/对冲] |
| 4宫 | ... | ... | 10宫 ... | ... |
| 11宫 | ... | ... | 3宫 ... | ... |

### 行星异常状态
| 行星 | 逆行 | 燃烧 | 战争 | 影响 |
|------|------|------|------|------|
| [行星] | ✅/❌ | ✅/❌ | ✅/❌ | [描述] |

### Shadbala排名
1. [行星] — [分数]R（最强）
...
9. [行星] — [分数]R（最弱）

### SAV关键宫位
| 宫位 | SAV | 阈值判断 |
|------|-----|---------|
| [目标宫] | [分数] | [强>30 / 中25-30 / 弱<25] |

### 静态分析结论
- **先天承诺**：[强/中/弱] — [描述]
- **关键优势**：[列出]
- **关键障碍**：[列出]
```

---

## 阶段四：动态推运分析（→ 多个参考文件）

### 4.1 执行顺序

```
Step 4.1  Dasha激活评估
          → references/vimshottari_dasha_guide.md
          → 当前Maha/Antar/Pratyantar与目标领域的关系

Step 4.2  Dasa Convergence（轻量三系统法）
          → references/dasa-convergence-methodology.md §七
          → Vimsottari + Yogini + Chara 三系统交叉验证
          → 输出：Convergence等级（Level 0-3）

Step 4.3  Transit触发评估（四参考点强制）
          → references/transit-comprehensive-guide.md
          → references/transit-multi-reference-guide.md
          → 必须从Lagna + Chandra Lagna两个参考点分析
          → Level 3加上AL参考点

Step 4.4  Double Transit确认
          → 土星+木星是否同时激活目标宫位

Step 4.5  Jaimini确认
          → references/jaimini-complete-system.md
          → Karaka状态 + Chara Dasha（如有）

Step 4.6  KP确认
          → references/kp-astrology-complete-system.md
          → Cuspal Sub-Lord分析

Step 4.7  Varshaphala年运盘确认（如需要）
          → references/varshaphala-annual-chart-guide.md
          → references/tajika-yoga-complete-guide.md
```

### 4.2 动态分析输出模板

```markdown
## ⏳ 动态推运分析

### Dasha激活
| 层级 | 行星 | 日期范围 | 与目标关系 | 评估 |
|------|------|---------|-----------|------|
| Maha | [行星] | [日期] | [描述] | [有利/中性/不利] |
| Antar | [行星] | [日期] | [描述] | [有利/中性/不利] |
| Pratyantar | [行星] | [日期] | [描述] | [有利/中性/不利] |

### Dasa Convergence（轻量三系统法）
| 系统 | 当前周期 | 激活？ | 证据 |
|------|---------|--------|------|
| Vimsottari | [Maha]-[Antar] | ✅/❌ | [说明] |
| Yogini | [Yogini名] | ✅/❌ | [说明] |
| Chara | [星座] | ✅/❌ | [说明] |
| **Convergence** | | **Level [X]** | **概率+[XX%]** |

### Transit分析
#### 从Lagna看
| 行星 | 过境[目标宫]时间 | 效应 | SAV |
|------|-----------------|------|-----|
| 土星 | [日期] | [压力/考验] | [分数] |
| 木星 | [日期] | [机遇/祝福] | [分数] |

#### 从Chandra Lagna看 ⚠️强制
| 行星 | 过境[目标宫]时间 | 心理/职业效应 |
|------|-----------------|-------------|
| 土星 | [日期] | [描述] |
| 木星 | [日期] | [描述] |

#### Double Transit
- 土星+木星同时激活目标宫：[是/否]（[时间窗口]）

### 三系统交叉验证
| 系统 | 判断 | 方向 | 置信度 |
|------|------|------|--------|
| Parashara | [描述] | [正面/负面] | [高/中] |
| Jaimini | [描述] | [正面/负面] | [高/中] |
| KP | [描述] | [正面/负面] | [高/中] |
| **一致性** | | [三系统/两系统/矛盾] | |
```

---

## 阶段五：应期输出（→ `timing-prediction-template.md` + `prediction-output-protocol.md`）

### 5.1 输出规范（严格遵守）

每条预测必须包含：

| 必含项 | 说明 |
|--------|------|
| **分析等级** | Level 1/2/3/4 |
| **置信度** | 高/中/低 + 置信区间 |
| **时间窗口** | 主窗口（月级）+ 次窗口（周级） |
| **承诺评估** | 本命盘有无此承诺 |
| **激活评估** | Dasha-Transit是否对齐 |
| **精度边界声明** | ⚠️ 声明预测的边界 |

### 5.2 禁用措辞（→ `prediction-output-protocol.md` 第四节）

**严格禁止**：
- ❌ "完美吻合" / "100%命中" / "一定会"
- ❌ "事业大爆发" / "贵人会联系你"
- ❌ 指定具体行业/项目/人物

**必须使用**：
- ✅ "X月前后，第Y宫处于高度活跃期"
- ✅ "此窗口的行星能量倾向于[增长/收缩/重组]"
- ✅ "高/中/低概率倾向，±X周/月"

### 5.3 应期输出模板

```markdown
## 📅 应期预测

### 事件预测总表
| 项目 | 说明 |
|------|------|
| **事件类型** | [领域] |
| **发生可能性** | [高90%+/中70-89%/低50-69%] |
| **置信度** | [来源：五层验证一致性] |

### 应期时间窗口
| 精度 | 时间窗口 | 判定依据 | 置信度 |
|------|---------|---------|--------|
| **主窗口** | [YYYY-MM 至 YYYY-MM] | Dasha+慢速Transit | 高 |
| **次窗口** | [YYYY-MM 至 YYYY-MM] | Pratyantar+Double Transit | 中 |
| **精确窗口** | [YYYY-MM-DD 至 YYYY-MM-DD] | Sookshma+快速Transit | 中-低 |

### 确认/延迟/取消信号
| 类型 | 信号 | 含义 |
|------|------|------|
| 确认 | [描述] | 事件在该窗口内发生的概率提升 |
| 延迟 | [描述] | 事件可能推迟 |
| 取消 | [描述] | 事件可能不发生 |

### 精度边界声明
⚠️ 本分析基于Jyotish推运系统，描述的是[能量场/时机窗口/宫位活跃度]。
具体事件的形态、个人的角色、具体项目方向——超出星盘精度。
占星给出的是概率和时机，不是保证交付。
```

---

## 阶段六：补救措施（如用户需要）

```
→ references/remedies-complete-system.md
→ references/personalized-remedies-system.md
```

仅在以下情况主动提供：
1. 用户明确要求
2. 分析中发现严重受克且用户询问如何缓解
3. Sade Sati / Kantaka Shani / Mangal Dosha等长期压力期

---

## 阶段七：现代措辞包装

**所有输出最终必须经过现代措辞包装**：
- → `references/modern-language-guide.md`
- → `references/modern-life-scenarios-complete.md`
- → `references/common-misconceptions.md`

**包装规则**：
1. 传统术语→现代措辞映射（太阳→个人品牌、月亮→心理健康）
2. 避免"好命/坏命"等绝对化表述
3. 提供"倾向性描述"而非"命运判定"
4. 直接坦率：给核心优势和挑战，不说废话

---

## 快速参考：完整工作流一页纸

```
用户消息到达
  │
  ├─ 路径判断
  │   ├─→ 【路径A】精准出生信息 → full-reading 全自动计算
  │   ├─→ 【路径B】PDF/文字星盘 → 提取数据 + 直接推算
  │   └─→ 【路径C】时间不明确 → 互动矫正 → 走路径A
  │
  ├─→ 阶段二：意图路由
  │     └─→ 用户问什么 → 目标宫位 → 对应承诺模板
  │         （无明确意图 → 综合解盘Level 2）
  │
  ├─→ 阶段三：静态分析（10步）
  │     ├─→ 宫位-行星基础
  │     ├─→ 承诺评估
  │     ├─→ Yoga识别
  │     ├─→ Argala检查
  │     ├─→ 逆行/燃烧/战争
  │     ├─→ Nakshatra深度
  │     ├─→ Shadbala
  │     ├─→ Ashtakavarga
  │     ├─→ Ketu双属性
  │     └─→ 分盘确认
  │
  ├─→ 阶段四：动态推运（7步）
  │     ├─→ Dasha激活
  │     ├─→ Dasa Convergence三系统法
  │     ├─→ Transit四参考点
  │     ├─→ Double Transit
  │     ├─→ Jaimini确认
  │     ├─→ KP确认
  │     └─→ Varshaphala确认
  │
  ├─→ 阶段五：应期输出
  │     └─→ 严格遵循prediction-output-protocol.md
  │
  ├─→ 阶段六：补救措施（可选）
  │
  └─→ 阶段七：现代措辞包装
```

---

**版本**：3.0.0
**更新日期**：2026-04-25
**配套文件**：`pdf-chart-reading-guide.md`（PDF提取）、`birth-time-rectification-advanced.md`（出生时间矫正）、`timing-prediction-template.md`（应期模板）、`prediction-output-protocol.md`（输出规范）、`comprehensive-reading-workflow.md`（综合流程）、`promise-assessment-templates.md`（承诺模板）、`argala-complete-guide.md`（Argala检查）、`dasa-convergence-methodology.md`（Dasa Convergence）
