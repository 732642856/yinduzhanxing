# AI解盘工作流Prompt工程（AI Reading Workflow）

> **适用场景**：AI收到PDF星盘后，如何一步步执行完整的解盘+推运分析
> **版本**：v1.0.0 | **创建日期**：2026-04-24
> **优先级**：⭐⭐⭐⭐⭐（AI解盘质量的决定性文件）
> **定位**：本文件是AI在收到PDF后的**执行引擎**，将Skill中所有参考资料串联成可执行的工作流

---

## ⚠️ 核心原则

1. **不跳步**：每个阶段必须完成后才能进入下一阶段
2. **不猜测**：数据缺失时标注"缺失"，不编造数据
3. **不锚定**：先输出星盘推导，再等用户反馈，不先知道用户生活再"找依据"
4. **必标注**：每个结论标注来源系统、置信度、精度边界

---

## 阶段一：PDF数据提取（→ `pdf-chart-reading-guide.md`）

### 1.1 执行指令

收到PDF/图片后，AI必须：

```
1. 识别PDF来源软件（JH / Parashara's Light / 其他）
2. 按内容类型逐页提取（不依赖页码顺序）
3. 填充完整JSON Schema（见pdf-chart-reading-guide.md 第三节）
4. 执行数据完整性门（Quality Gate，见第四节）
5. 执行交叉校验（见第五节）
6. 输出提取报告（见第六节）
```

### 1.2 输出模板（阶段一必输出）

```markdown
## 📋 PDF数据提取报告

**来源**：[JH / PL / 其他] | **页数**：[N]页
**完整度**：[XX%] | **分析级别**：[Level 1/2/3]

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
- [Yoga2]：...

### 数据完整性
- ✅ P0全部齐全（N/11）或 ❌ 缺失：[列出]
- ⚠️ P1缺失：[列出]
```

### 1.3 质量门判定规则

| 完整度 | 判定 | 允许的分析 |
|--------|------|-----------|
| ≥90%（P0全齐） | ✅ Pass | Level 2/3完整分析 |
| 70-89%（P0大部分） | ⚠️ Limited | Level 2，标注限制 |
| <70%（P0缺关键项） | ❌ Fail | Level 1快速概览，要求用户补全 |

**如果Quality Gate未通过**：停止在阶段一，告知用户缺失哪些数据、为什么影响分析。

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
| 综合解盘（全盘） | 全部 | `comprehensive-reading-workflow.md` | 全部 |

**（承诺模板→ `promise-assessment-templates.md`）**

### 2.2 用户未明确意图时的默认流程

如果用户只上传了PDF没有说具体问什么：
1. 执行**综合解盘工作流Level 2**（`comprehensive-reading-workflow.md`）
2. 先输出10宫位快速扫描
3. 识别最强和最弱的领域
4. 重点展开当前Dasha激活的领域

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
          → references/argala-complete-guide.md ⭐ 新增
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
          → references/dasa-convergence-methodology.md §七 ⭐ 升级
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
收到PDF
  │
  ├─→ 阶段一：数据提取（pdf-chart-reading-guide.md）
  │     └─→ Quality Gate → Pass/Limited/Fail
  │
  ├─→ 阶段二：意图路由
  │     └─→ 用户问什么 → 目标宫位 → 对应承诺模板
  │
  ├─→ 阶段三：静态分析（10步）
  │     ├─→ 宫位-行星基础
  │     ├─→ 承诺评估（promise-assessment-templates.md）
  │     ├─→ Yoga识别
  │     ├─→ Argala检查（argala-complete-guide.md）⭐
  │     ├─→ 逆行/燃烧/战争
  │     ├─→ Nakshatra深度
  │     ├─→ Shadbala
  │     ├─→ Ashtakavarga
  │     ├─→ Ketu双属性
  │     └─→ 分盘确认
  │
  ├─→ 阶段四：动态推运（7步）
  │     ├─→ Dasha激活
  │     ├─→ Dasa Convergence轻量三系统法 ⭐
  │     ├─→ Transit四参考点
  │     ├─→ Double Transit
  │     ├─→ Jaimini确认
  │     ├─→ KP确认
  │     └─→ Varshaphala确认
  │
  ├─→ 阶段五：应期输出
  │     └─→ 严格遵循prediction-output-protocol.md
  │         禁用措辞 + 强制标注 + 精度声明
  │
  ├─→ 阶段六：补救措施（可选）
  │
  └─→ 阶段七：现代措辞包装
        └─→ modern-language-guide.md + misconceptions check
```

---

**版本**：1.0.0
**创建日期**：2026-04-24
**配套文件**：`pdf-chart-reading-guide.md`（数据提取）、`timing-prediction-template.md`（应期模板）、`prediction-output-protocol.md`（输出规范）、`comprehensive-reading-workflow.md`（综合流程）、`promise-assessment-templates.md`（承诺模板）、`argala-complete-guide.md`（Argala检查）、`dasa-convergence-methodology.md`（Dasa Convergence）