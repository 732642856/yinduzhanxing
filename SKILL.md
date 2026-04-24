---
name: jyotish-vedic-astrology
version: 3.7.4
description: 印度占星（Jyotish）专业解盘与推运系统。核心能力：PDF星盘输入→严谨解盘→精确推运应期输出。覆盖行星配置、Yoga格局、Nakshatra解读、宫位分析、现代生活场景映射、现代措辞解读、案例对比分析、自动出生时间矫正、常见误判纠错、Dasha+Transit推运、精确预测、PDF星盘读取、Swiss Ephemeris计算引擎、星盘计算、分盘计算、名人案例查询、Shadbala六重力量、Ashtakavarga八分法（BPHS完整表SAV=337）、Hermes记忆系统、事件预测、R1-R10数学验证（含R2b BAV列→SAV列校验）、P1-P12行星审计（含P3仓库耦合+P8年龄状态+冲突仲裁3条规则）、验前事、MD→HTML报告生成（羊皮纸主题）、BPHS十六分盘精确计算（D2-D60）、度数精确相位系统（Drishti）、Jaimini完整系统（Chara Karaka 7/8+Chara Dasha+Karakamsha）、高级Nakshatra分析（Tara Bala+Sub-Lord KP系统）、Argala门闩系统（Virodha反干预）、Tajika年运盘（Muntha+YearLord+Mudda Dasha+Tri-Pataka三旗）、合盘分析（Ashta Koota 36分制+Mangal Dosha+Papasamya+Dasha兼容性）、配偶多层综合分析（DK+7宫主+金星+木星+昼夜区分+Rahu辅助六层交叉确认）、行星度数精确旺衰判定（精确度数+渐变效应+Moolatrikona区间+行星生命阶段+Sandhi交界点）、燃烧阈值、落陷取消Neecha Bhanga、Sect昼夜区分法、Pushkara Navamsha、Vargottama。触发词：印度占星、吠陀占星、Jyotish、解盘、推运、星盘分析、Dasha、Transit、Nakshatra、Yoga、出生时间矫正、吠陀占星、印占、PDF星盘、读取PDF、分析PDF星盘、矫正出生时间、出生时间验证、生时矫正、现代解读、现代措辞、误判纠错、错题本、Varga分盘、全球占星师方法论、三合盘、综合分析、过境分析、Double Transit、Sade Sati、合盘、婚姻匹配、关系分析、Koota、Mangal Dosha、年运盘、Varshaphala、太阳返照、Tajika、星宿速查、综合解盘工作流、应期预测、推运应期、事件时机、什么时候结婚、什么时候升职、什么时候发财、Argala、门闩、行星干预、Dasa收敛、Yogini大运、Chara Dasha、AI解盘、算星盘、排盘、计算星盘、查名人、Shadbala、六重力量、Ashtakavarga、八分法、行星力量、记忆系统、事件预测、验证、校验、审计、验前事、R1-R10、P1-P12、仓库耦合、冲突仲裁、报告生成、HTML报告、精确相位、Drishti、Jaimini、Chara Karaka、Atmakaraka、Darakaraka、Karakamsha、Tara Bala、Sub-Lord、KP系统、Navamsa、D9、D60、Shashtyamsa、十六分盘、门闩分析、Muntha、年主星、三旗系统、合盘评分、Nadi Koota、Gana、Yoni、Papasamya、Dasha兼容、配偶分析、配偶星、配偶征象、婚姻分析、配偶画像、DK配偶星、多层配偶、昼夜区分、旺衰度数、行星燃烧、落陷取消、Neecha Bhanga、Sect昼夜、Pushkara、Vargottama、行星尊严、Moolatrikona、行星生命阶段、Avastha。
---

# 印度占星专业解盘与推运系统

## ⚠️ 核心定位

**三种输入 → 严谨解盘 → 精确推运应期输出**

本Skill支持三种输入方式，AI自动识别并路由：

### 三条入口路径（自动判断，无需用户触发）

| 路径 | 用户输入 | AI行为 |
|------|---------|--------|
| **路径A：精准出生信息** | 出生日期+时间+地点 | 直接调用 `full-reading` 引擎全链路计算（13模块一键出） |
| **路径B：PDF/文字星盘** | 上传PDF星盘 或 详细的文字星盘描述 | 提取文档中的星象数据（落宫、度数、Dasha等），直接基于文档数据推算 |
| **路径C：时间不明确** | "不知道几点出生" / "大概下午" | 启动互动式出生时间矫正（外表体质→事件验证→D9/D10校正）→ 确认后走路径A |

**强制工作流**（→ 完整规范见 `references/ai-reading-workflow-prompt.md` v3.0）：
1. **阶段零**：入口路由（路径A/B/C自动判断）
2. **阶段一**（仅路径B）：PDF/图片输入 → 提取数据 + Quality Gate（→ `references/pdf-chart-reading-guide.md`）
3. **阶段二**：用户意图识别 → 路由到目标宫位（无明确意图→综合解盘Level 2）
4. **阶段三**：静态分析10步（宫位→承诺→Yoga→Argala→逆行→NK→Shadbala→AV→Ketu→分盘）
5. **阶段四**：动态推运7步（Dasha→Dasa Convergence轻量三系统→Transit→Double Transit→Jaimini→KP→Varshaphala）
6. **阶段五**：应期输出（五层验证法→精确时间窗口）
7. **阶段六**：补救措施（可选）
8. **阶段七**：现代措辞包装

---

## 核心能力

### 1. 静态星盘分析
- 行星配置解读（入庙、落陷、合相、相位）→ 详见 `references/planets.md`、`references/signs-and-houses.md`
- Yoga格局识别（Raja Yoga、Dhana Yoga、Neechabhanga Raja Yoga、Viparita Raja Yoga）→ 详见 `references/yoga_list.md`、`references/yoga-list-chinese.md`、`references/neechabhanga-raja-yoga.md`、`references/yoga-strength-scoring-system.md`
- Yoga Phala Timing（五大方法精确预测Yoga结果时机）→ 详见 `references/yoga-phala-timing-guide.md`
- Nakshatra解读（27星宿完整解读）→ 详见 `references/nakshatra_deities.md`、`references/nakshatra-chinese-quick-ref.md`
- 宫位分析（12宫位现代生活场景映射）→ 详见 `references/house-modern-mapping.md`、`references/house-domain-planet-mapping.md`、`references/modern-life-scenarios-complete.md`
- **Argala行星干预分析**（四类型Argala+Virodha反干预+12宫完整速查+10领域模板）→ 详见 `references/argala-complete-guide.md` ⭐ v3.2 新增
- Shadbala评估（六种力量）→ 详见 `references/shadbala-complete-methodology.md`、`references/planetary-strength-quick-ref.md`
- Ashtakavarga评估（八层分盘法）→ 详见 `references/ashtakavarga-complete-system.md`
- **Shodasavarga十六分盘体系**（16种分盘+Vimsopaka Bala权重+Varga Dignity尊严等级+分盘实战工作流）→ 详见 `references/shodasavarga-complete-guide.md` ⭐ v3.3 新增

### 2. 动态星盘分析
- Vimshottari Dasha推运系统（五级大运联动）→ 详见 `references/vimshottari_dasha_guide.md`、`references/dasha-transit-method.md`、`references/dasha-calculation-tool.md`、`references/yoga-and-dasha.md`
- **Dasa Convergence多系统交叉验证**（9大Dasha系统独立性分析+Convergence等级量化+概率提升公式+轻量三系统手工推算法）→ 详见 `references/dasa-convergence-methodology.md` ⭐ v3.2 升级
- **替代推运系统**（Ashtottari 108年条件性+Yogini 36年八女神+Kalachakra 144年双模式+Prashna问卜占星）→ 详见 `references/alternative-dasha-systems.md` ⭐ v3.3 新增
- **条件Dasha系统**（BPHS记载8大条件Dasha+适用条件判定+实战策略）→ 详见 `references/condition-dasha-complete.md` ⭐ v3.3 新增
- Jaimini Chara Dasha推运系统（星座大运）→ 详见 `references/jaimini-complete-system.md`
- Transit系统（Double Transit双过境+Ashtakavarga引导评分+四参考点分析）→ 详见 `references/transit-comprehensive-guide.md`、`references/transit-multi-reference-guide.md`
- Varshaphala年运盘系统（Tajika太阳返照+Muntha+年主星+Mudda月度Dasha）→ 详见 `references/varshaphala-annual-chart-guide.md`、`references/tajika-yoga-complete-guide.md`
- Pratyantar微运精确计算 → 详见 `references/pratyantar-calculation-guide.md`
- 三层验证法（Dasha + Transit + Varga）
- 精确时间点预测（年度、月度、每日）
- **预测精度边界与输出规范**（四等级深度标注+置信度评估+禁用绝对断言）→ 详见 `references/prediction-boundary-protocol.md`、`references/prediction-output-protocol.md` ⭐ v3.2 新增

### 2.1 Jaimini系统
- **Chara Karakas**：七大可变象征星（Atmakaraka、Amatyakaraka、Bhratrukaraka、Matrukaraka、Putrakaraka、Gnatikaraka、Darakaraka）
- **Chara Dasha**：星座大运系统（基于太阳和地球，反映实际事件）
- **Karakamsha**：灵魂上升点（Navamsha盘中的AK位置）
- **Jaimini Drishti**：星座相位系统
- **应用场景**：婚姻时机预测、事业突破预测、灵魂课题解读
- → 详见 `references/jaimini-complete-system.md`

### 2.2 KP占星系统
- **249个Sub-Lord系统**：精确事件时机预测
- **四层级Significator分析**：星宿领主优先于宫主星
- **Cuspal Sub-Lord分析**：宫头子领主决定承诺实现
- **问答占星（Horary）**：1-249数字问卜法
- **Ruling Planets**：统治行星系统
- **应用场景**：是/否答案、精确事件时间、求职/婚姻/出国预测
- → 详见 `references/kp-astrology-complete-system.md`、`references/kp-practical-event-timing.md`

### 2.3 Ashtakavarga系统
- **BAV（Bhinna Ashtakavarga）**：7行星+Lagna完整分配表（标准Parashara法+额外Bindhu规则）
- **SAV（Sarva Ashtakavarga）**：337点聚合方法与校验
- **Shodhya Pinda**：终极行星强度评分
- **过境预测应用**：结合BAV和SAV双系统评分
- **SAV关键阈值**：事业/关系/财富各领域的实战评分标准
- **应用场景**：行星强度排名、过境效果预测、宝石推荐依据
- → 详见 `references/ashtakavarga-complete-system.md`

### 3. 关系占星/合盘分析
- **Koota匹配体系**：36分制传统匹配（Nadi 8分+Gana 6分+Yoni 4分等8项评分）
- **D9伴侣分析**：Navamsa深度关系模式解读
- **Mangal Dosha配对**：火星煞的形成、分级与取消条件
- **Jaimini关系分析**：Darakaraka（DK）配偶象征星+DK在12宫位的含义
- **现代关系形态**：同居/商业合作/灵性伴侣/跨文化关系的宫位映射
- **⭐ 配偶多层综合分析**（v3.7.2 新增）：6层交叉确认法——DK（性别中立）+7宫主+金星（天然征象）+木星/月亮（传统）+昼夜区分法+Rahu辅助。禁止"男命金星女命木星"单一判据。标准六步分析流程+置信度评估。
- **应用场景**：婚姻匹配、关系预测、伴侣特质分析、关系时机判断、配偶画像
- → 详见 `references/relationship-astrology-guide.md`、`references/navamsa-d9-interpretation-template.md`、**`references/spouse-multi-layer-methodology.md`** ⭐ v3.7.2 新增

### 4. Varshaphala年运盘系统
- **Tajika体系**：太阳返照年运盘（生日到生日的年度运势）
- **Muntha**：年度推进上升（每年推进一宫的年度主题）
- **年主星（Varshaeshwara）**：年度主宰行星评估
- **Tajika Yoga**：年运盘专属Yoga（Ithasala结合、Easarapha分离、Ishkavala帝王等）
- **Mudda Dasha**：年运盘内的月度Dasha系统
- **应用场景**：年度规划、月度精确预测、太阳年运势分析
- → 详见 `references/varshaphala-annual-chart-guide.md`、`references/tajika-yoga-complete-guide.md`

### 5. 综合解盘工作流
- **三级深度体系**：Level 1 快速概览（5分钟）→ Level 2 专项分析（20分钟）→ Level 3 完整解盘（60分钟+）
- **分析决策树**：根据用户问题自动路由到正确的宫位/分盘/Karaka
- **10领域快速路由表**：事业/婚姻/财富/健康/子女/出国/教育/灵性/占星/投资
- **承诺判定（Promise Assessment）**：10领域逐项检查→承诺等级量化→Promise vs Activation两步分析→ 详见 `references/promise-assessment-templates.md` ⭐ v3.2 新增
- **三系统交叉验证矩阵**：Parashara+Jaimini+KP一致性判断
- **报告质量检查清单**：Level 1/2/3各有专属检查项
- **应用场景**：标准化解盘流程、新人培训、质量把控
- → 详见 `references/comprehensive-reading-workflow.md`、`references/tri-system-analysis-template.md`、`references/varga-system-quick-reference.md`、`references/varga-divisional-charts-quick-reference.md`、`references/prediction-checklist.md`

### 6. 自动出生时间矫正（核心能力）
- **八大矫正方法**：
  1. 运限与星曜过宫法（最常用）
  2. D9 Navamsa上升判定法
  3. D10 Dasamsa上升判定法
  4. 六亲关系验证法
  5. 外表和体质验证法
  6. 身体缺陷胎记伤疤法
  7. 职业判断法
  8. 卜卦法（Horary Astrology）
- → 详见 `references/birth-time-rectification-advanced.md`、`references/birth-time-rectification-cases.md`
- **自动化矫正流程**：
  - 第一阶段：信息收集（基本信息、外表体质、事件列表）
  - 第二阶段：初步筛选（上升星座范围、外表体质验证）
  - 第三阶段：事件验证（Dasha周期验证、Transit验证）
  - 第四阶段：精确校正（D9上升判定、D10上升判定）
  - 第五阶段：验证报告生成（置信度评估）
- **验证标准**：
  - ✅ 高度吻合：80%以上事件吻合 → 出生时间准确
  - ⚠️ 中度吻合：60-80%事件吻合 → 需要微调（±15分钟）
  - ❌ 低度吻合：60%以下事件吻合 → 需要大幅调整（±1-2小时）
- **精确度要求**：
  - 最少10个事件，推荐15-25个事件
  - 事件分布在不同年龄段
  - 时间精度：精确到月份（最佳）、季度（可接受）、年份（需要更多事件）

### 7. 案例对比分析
- 全网相似案例搜索
- 详细对比分析
- 独特性评估
- 命运差异分析
- → 详见 `references/famous-case-library.md`、`references/consultation-case-library.md`、`references/celebrity-cases.md`、`references/verified-celebrity-cases.md`、`references/verified-celebrity-cases-summary.md`、`references/verified-celebrity-cases-part2-elvis.md`、`references/verified-celebrity-cases-part2-trump.md`、`references/verified-celebrity-cases-part3-marilyn-monroe.md`、`references/verified-celebrity-cases-part3-michael-jackson.md`、`references/verified-celebrity-cases-part3-summary.md`、`references/verified-celebrity-cases-part4-leonardo-dicaprio.md`、`references/case-study-collection-2026-04-22.md`、`references/shatabhisha-complete.md`

### 8. 现代生活场景映射
- 12宫现代生活场景（跨国职业、数字游民、远程工作、在线社区）
- 8宫现代生活场景（投资、风险管理、心理学、深度研究）
- 7宫现代生活场景（商业合作、专业合作、成熟稳定的关系）
- → 详见 `references/house-modern-mapping.md`、`references/modern-life-scenarios-complete.md`

### 9. 现代措辞解读能力
- **传统术语 → 现代措辞映射**：
  - 行星现代措辞（太阳→个人品牌、月亮→心理健康、火星→执行力等）
  - 宫位现代措辞（1宫→个人品牌、2宫→资产管理、7宫→商业合作等）
  - Yoga现代措辞（Raja Yoga→成功格局、Dhana Yoga→财富格局等）
  - Nakshatra现代措辞（Shatabhisha→探索未知+转化能力等）
  - Dasha现代措辞（大运→人生阶段、小运→子阶段等）
- → 详见 `references/modern-language-guide.md`
- **现代生活场景优先**：
  - 职业：创业、投资、研究、咨询、艺术创作
  - 关系：商业合作、专业合作、客户关系、婚姻关系
  - 财富：投资转化、资产管理、财富自由、收入增长
  - 生活：远程工作、数字游民、国际事务、在线社区
- **直接坦率风格**：
  - 直接给出核心优势和挑战领域
  - 避免模糊和传统术语
  - 提供具体的职业建议、合作建议、工作方式建议

### 10. PDF星盘读取能力（管线入口）
- 自动读取PDF格式的印度占星星盘报告（Jagannatha Hora / Parashara's Light）
- 提取**全量数据**：出生信息+D1九星位置/度数/Dignity/逆行/燃烧/战争+特殊Lagna（AL/UL/HL/GL）+Jaimini七Karakas+分盘（D2-D60）+Shadbala+Ashtakavarga+Dasha五级周期+Yoga清单
- 数据完整性门：P0数据缺失时禁止进入完整分析
- 交叉校验：D1 Nakshatra↔D9位置、SAV=337、Moon NK↔Dasha起始
- → 详见 `references/pdf-chart-reading-guide.md`（v3.0）、`references/data-bridge-mapping.md`
- **排盘软件与Ayanamsa配置**：8种Ayanamsa体系对比+JH/Maitreya等桌面软件+在线工具矩阵 → 详见 `references/software-comparison-guide.md` ⭐ v3.3 新增

### 11. 补救措施系统
- **宝石疗法**：九大行星对应宝石、佩戴方法、禁忌事项
- **Mantra疗法**：各行星咒语、种子音、修行要求
- **Puja/Homa**：火祭仪式（Navagraha Shanti、Rudrabhishek、Kaal Sarp Dosh等）
- **Yantra**：几何曼陀罗、开光仪式
- **Daan（布施）**：各行星对应捐赠物品、布施日
- **Fasting（断食）**：各行星断食日、断食方式
- **Doshas补救**：Mangal Dosha、Kaal Sarp Dosha、Sade Sati
- **应用场景**：行星受克化解、业力调和、能量平衡
- → 详见 `references/remedies-complete-system.md`、`references/personalized-remedies-system.md`

### 12. 常见误判纠错能力（错题本）
- **全网常见误判记录**：
  - 宫位解读误判（8宫是"死亡宫"、12宫是"监狱宫"、7宫是"婚姻宫"等）
  - 行星状态误判（火星落陷一定是坏事、土星在7宫表示婚姻延迟等）
  - Yoga格局误判（Neechabhanga Raja Yoga一定形成、Raja Yoga一定成功等）
  - Dasha周期误判（大运一定决定人生阶段、Transit可以单独预测等）
  - 出生时间矫正误判（一个事件验证就足够、D9上升不重要等）
  - 现代生活场景误判（传统解读适用于现代生活等）
  - 不同流派误判（Parashara系统和Jaimini系统冲突等）
- → 详见 `references/common-misconceptions.md`
- **高级技法与全球方法论**：→ 详见 `references/advanced-techniques.md`、`references/global-astrologer-practical-methodology.md`、`references/global-astrologer-reflections.md`、`references/qin_ruisheng_system.md`

### 13. 计算引擎集成（Swiss Ephemeris + 数据库）⭐ v3.4.0

**统一引擎入口**：`scripts/jyotish_engine.py` v3.7.1（基于 Swiss Ephemeris 天文计算库）

**调用方式**：AI 通过 `execute_command` 调用以下子命令（所有输出为 JSON）：

```bash
# 使用系统 Python 3.11
PYTHON=/Library/Frameworks/Python.framework/Versions/3.11/bin/python3
SCRIPT=~/.workbuddy/skills/jyotish-vedic-astrology/scripts/jyotish_engine.py
$PYTHON $SCRIPT <子命令> [参数]
```

**13大子命令** → **22大子命令**（v3.7.1 升级）：

| 子命令 | 功能 | 典型用法 |
|--------|------|----------|
| **`full-reading`** | **⭐ v3.7.1 全自动综合解盘（一条命令串起13个模块）** | `full-reading --year 1993 --month 4 --day 17 --hour 14 --minute 45 --lat 36.6 --lon 114.5 --tz 8` |
| `chart` | 完整星盘计算（含Ayanamsa修正）+ `--validate` 附加R1-R10验证 | `chart --validate --year 1993 --month 4 --day 17 --hour 14 --minute 45 --lat 36.6 --lon 114.5 --tz 8` |
| `dasha` | Vimshottari大运时间线+小运展开 | `dasha --moon-lon 326.5 --birthdate 1993-04-17 --today 2026-04-24` |
| `yoga` | Yoga格局识别（5种Yoga） | `yoga --ascendant Leo --planets 'Sun:Aries:9,Moon:Aquarius:7,...'` |
| `predict` | 三层验证法事件预测（EventPredictionModel规则引擎）+ `--past-verify` 验前事模式 | `predict --chart '<JSON>' --event-type marriage` |
| `varga` | 分盘计算（D9 Navamsa/D10 Dasamsa） | `varga --year 1993 --month 4 --day 17 --hour 14 --minute 45 --lat 36.6 --lon 114.5 --tz 8 --d9 --d10` |
| `celebrity` | 名人案例查询（SQLite + 15,807条CSV） | `celebrity --name Einstein` |
| `db-stats` | 验证数据库统计（15,840条+10种技法） | `db-stats` |
| `transit` | 行星过境查询（2026-2028） | `transit --year 2026 --month 7` |
| `shadbala` | 六重力量计算（Sthana/Dig/Kala/Chesta/Naisargika/Drik Bala） | `shadbala --year 1993 --month 4 --day 17 --hour 14 --minute 45 --lat 36.6 --lon 114.5 --tz 8` |
| `ashtakavarga` | 八分法计算（BPHS完整8×8矩阵，SAV=337） | `ashtakavarga --year 1993 --month 4 --day 17 --hour 14 --minute 45 --lat 36.6 --lon 114.5 --tz 8` |
| `memory` | Hermes记忆系统（store/search/context/stats） | `memory --action store --content "..." --tags "chart" --importance 8` |
| `validate` | R1-R10数学验证（SAV/BAV/延伸角/Rahu-Ketu/逆行/Dasha/完整性/度数/宫位） | `validate --year 1993 --month 4 --day 17 --hour 14 --minute 45 --lat 36.6 --lon 114.5 --tz 8` |
| `audit` | P1-P12行星审计管线（Identity/Health/Resource/SAV/Dignity/Shadbala/Aspects/Nakshatra/Yogas） | `audit --year 1993 --month 4 --day 17 --hour 14 --minute 45 --lat 36.6 --lon 114.5 --tz 8` |
| `varga-full` | v3.7 BPHS十六分盘精确计算（D2-D60全部16分盘，精确度数输出） | `varga-full --year 1993 --month 4 --day 17 --hour 14 --minute 45 --lat 36.6 --lon 114.5 --tz 8 --divisions D9,D60` |
| `aspects` | v3.7 度数精确相位系统（tight/moderate/loose + 入相位/出相位） | `aspects --year 1993 --month 4 --day 17 --hour 14 --minute 45 --lat 36.6 --lon 114.5 --tz 8` |
| `jaimini` | v3.7 Jaimini完整系统（Chara Karaka 7/8 + Chara Dasha + Karakamsha） | `jaimini --year 1993 --month 4 --day 17 --hour 14 --minute 45 --lat 36.6 --lon 114.5 --tz 8 --mode all` |
| `nakshatra-adv` | v3.7 高级Nakshatra（Tara Bala + Sub-Lord KP + 兼容性） | `nakshatra-adv --year 1993 --month 4 --day 17 --hour 14 --minute 45 --lat 36.6 --lon 114.5 --tz 8 --mode all` |
| `argala` | v3.7 Argala门闩系统（主/副Argala + Virodha反干预 + 净评分） | `argala --year 1993 --month 4 --day 17 --hour 14 --minute 45 --lat 36.6 --lon 114.5 --tz 8` |
| `tajika` | v3.7 Tajika年运盘（Muntha + YearLord + Mudda Dasha + Tri-Pataka） | `tajika --year 1993 --month 4 --day 17 --hour 14 --minute 45 --lat 36.6 --lon 114.5 --tz 8 --age 33` |
| `synastry` | v3.7 合盘分析（Ashta Koota 36分 + Mangal Dosha + Papasamya） | `synastry --moon1 310.89 --moon2 45.5 --mars1 90.43 --mars2 120.3` |
| `report` | MD→HTML报告生成（羊皮纸主题） | `report ./report_folder --name 一楠 --lagna Leo` |

**外部数据源**（引擎自动读取）：
- 验证数据库：`~/WorkBuddy/Claw/vedic_astrology_validation.db`（15,840条案例，10种技法准确率）
- 名人CSV：`~/WorkBuddy/Claw/vedastro_data/PersonList-15k.csv`（15,807条AA级数据）
- 过境配置：`~/WorkBuddy/Claw/月运过境配置-2026-2028.json`（36个月行星位置）

**典型工作流**（v3.7.1 升级）：

### 🟢 路径A：精准出生信息（推荐，一条命令搞定）
```bash
# 一键全链路计算（13模块自动串行）
$PYTHON $SCRIPT full-reading --year YYYY --month MM --day DD --hour HH --minute MM --lat XX.XX --lon XX.XX --tz X
# 输出：chart + dasha + yoga + varga_full + aspects + jaimini + nakshatra_adv + argala + tajika + shadbala + ashtakavarga + validation + audit
# 完成后直接进入阶段二（意图识别）
```

### 📄 路径B：PDF/文字星盘（用文档数据直接推算）
1. 提取PDF/文字中的所有星象数据（行星落宫、度数、Dasha、Shadbala等）
2. 数据完整性门 → Pass/Limited/Fail
3. 如有出生时间+地点，额外调用 `full-reading` 补充计算v3.7新增模块
4. 进入阶段二（意图识别）

### 🔧 路径C：时间不明确（互动式矫正）
1. 收集外表体质+生活事件（3-5轮互动）
2. 多候选时间对比验证（Dasha吻合率+Transit吻合率）
3. D9/D10精确校正
4. 矫正完成后走路径A
8. `jaimini --mode all` 计算Chara Karaka + Dasha + Karakamsha ⭐ v3.7
9. `nakshatra-adv --mode all` 计算Tara Bala + Sub-Lord ⭐ v3.7
10. `argala` 计算门闩干预分析 ⭐ v3.7
11. `transit` 查询当月过境 → 配合 dasha 做推运分析
12. `tajika --age 33` 计算年运盘（Muntha+Tri-Pataka） ⭐ v3.7
13. `predict` 事件预测（EventPredictionModel规则引擎） ⭐ v3.4
14. `celebrity` 查找相似案例做对比验证
15. 合盘场景：`synastry --moon1 ... --moon2 ...` 计算Ashta Koota 36分制 ⭐ v3.7
16. `memory --action store` 保存分析结论供后续引用 ⭐ v3.4

## 使用方法

调用此Skill后，AI将自动加载所有印度占星知识，可以：

1. **读取PDF星盘报告**：自动提取PDF中的星盘信息（出生时间、行星位置、宫位、Nakshatra、Dasha周期）
2. **自动矫正出生时间**：通过八大矫正方法自动验证和矫正出生时间（核心能力）
3. **进行静态星盘分析**：解读行星配置、Yoga格局、Nakshatra、宫位（使用现代措辞，避免常见误判）
4. **进行动态推运预测**：使用Dasha+Transit进行精确预测（使用现代措辞，避免常见误判）
5. **进行案例对比分析**：搜索全网相似案例并进行对比
6. **提供精确的预测报告**：生成专业的解盘报告（使用现代措辞，符合现代生活，避免常见误判）
7. **纠错常见误判**：自动识别和纠错全网常见误判（错题本）

## 核心方法论

### 三层验证法
1. **本命征象**：静态星盘中的征象
2. **大运激活**：Dasha系统激活相关宫位
3. **过境触发**：Transit系统触发具体事件（⚠️ 必须多参考点检查）

### ⚠️ 过境分析强制规范（v1.9.0新增）

**任何过境分析必须同时从至少两个参考点评估**：
1. **Lagna（上升）**：实际事件层面
2. **Chandra Lagna（月亮）**：心理+职业层面（⚠️ 强制，与Lagna等权）
3. **Arudha Lagna（AL）**：公众形象层面（Level 3强制）
4. **Navamsa Lagna**：灵魂层面（辅助确认）

**禁止行为**：
- ❌ 只从Lagna一个参考点做过境判断
- ❌ 忽略Chandra Lagna给出的矛盾信号
- ❌ 职业预测时不检查Chandra Lagna的6宫/10宫

**详细规范**：见 `references/transit-multi-reference-guide.md`

### ⚠️ Ketu双重属性解读规范（v2.0.0新增）

**Ketu同时具有两种属性，分析时必须同时考虑**：
1. **属性A：放手/解脱/脱离**（Moksha Karaka）——结束、分离、超脱
2. **属性B：突然转变/非预期开启/突破**——职业突变、技术突破、灵性觉醒

**禁止行为**：
- ❌ 将Ketu简化为只有"放手/清零"的单面解读
- ❌ 忽略Ketu的"突然突破"属性

**判断主导属性**：根据宫位（3/9/11偏B）、星座（射手/天蝎偏B）、相位（吉星偏B）综合判断。

**详细规范**：见 `references/ketu-dual-nature-guide.md`

### ⚠️ Shadbala评估规范（v2.0.0新增）

**Shadbala六种力量必须全部评估**：
1. **Sthana Bala**（位置力量）：入庙/落陷/友星/敌星
2. **Dig Bala**（方向力量）：角宫位置
3. **Kala Bala**（时间力量）：昼夜/月相/太阳南北行
4. **Chesta Bala**（运动力量）：逆行/直行速度
5. **Naisargika Bala**（天然力量）：固定先天等级
6. **Drik Bala**（相位力量）：吉凶相位加减

**快速估算**：入庙角宫木星看=最强；落陷暗宫土星压=最弱。

**详细方法**：见 `references/shadbala-complete-methodology.md`

### ⚠️ Yoga Phala Timing规范（v2.1.0新增）

**识别Yoga≠预测何时发生**。五大方法必须综合使用：
1. **Dasha触发法**：Yoga中的行星Dasha期间才给出结果（最核心）
2. **Transit触发法**：Dasha决定"是否发生"，Transit决定"何时发生"
3. **分盘验证法**：D1中有Yoga需对应分盘确认（D10事业/D9关系/D2财富）
4. **Ashtakavarga评分法**：BAV/SAV决定结果质量和规模
5. **Tajika年运盘确认法**：Ithasala+无Manahoo=最终确认

**标准流程**：识别Yoga→Dasha窗口→Transit精确窗口→分盘确认→AV评分→综合输出

**详细规范**：见 `references/yoga-phala-timing-guide.md`

### ⚠️ 逆行/燃烧/行星战争规范（v2.1.0新增）

**静态星盘解读的最后一环，必须检查**：
1. **逆行**：本命逆行行星=该领域有"前世未完成课题"。木星逆行=好事（深化智慧），火星逆行=小心（能量内爆）
2. **燃烧**：行星与太阳度数差小于阈值=独立力被太阳吞噬。月亮燃烧最严重，水星燃烧最常见。入庙可缓解
3. **行星战争**：两星同星座且度数差<1°=激烈交锋。度数大者胜。败者征象受阻
4. **三重叠加**：逆行+燃烧+战争败者=最极端情况

**详细规范**：见 `references/retrograde-combustion-war-guide.md`

### 预测清单
- [ ] 静态星盘分析（行星配置、Yoga格局、Nakshatra、宫位）
- [ ] Argala检查（⚠️ 目标宫的2/4/5/8/11宫干预+Virodha对冲）⭐ v3.2 新增
- [ ] 逆行/燃烧/行星战争检查（⚠️ 每颗行星必须检查三重叠加条件）
- [ ] Shadbala评估（⚠️ 六种力量完整评估：Sthana+Dig+Kala+Chesta+Naisargika+Drik）
- [ ] Ashtakavarga评估（⚠️ BAV完整分配+SAV聚合校验337点）
- [ ] Ketu双重属性检查（⚠️ 每次涉及Ketu时必须同时评估"放手"和"突破"）
- [ ] Dasha推运（当前大运、小运、Pratyantar微运精确到月/周）
- [ ] Dasa Convergence轻量三系统法（⚠️ Vimsottari+Yogini+Chara交叉验证，见dasa-convergence-methodology.md §七）⭐ v3.2 新增
- [ ] Jaimini系统分析（AK/AmK/BK/MK/PK/GK/DK + Chara Dasha）
- [ ] KP系统分析（Significator层级 + Cuspal Sub-Lord）
- [ ] Transit分析（⚠️ 多参考点强制：Lagna + Chandra Lagna + AL + Navamsa Lagna）
- [ ] Tajika Yoga审计（⚠️ 年运盘10种Yoga完整检查：Ithasala/Easarapha/Nakta/Yamaya/Manahoo/Kamboola等）
- [ ] Yoga Phala Timing（⚠️ 识别Yoga后必须预测何时发生：Dasha窗口→Transit窗口→分盘确认→AV评分）
- [ ] 分盘验证（D1/D2/D3/D4/D7/D9/D10/D12/D24/D27/D30/D40/D45/D60）
- [ ] 补救措施评估（如需要）
- [ ] 综合报告生成（Jaimini+KP+Parashara三系统协同解读）
- [ ] 预测边界检查（⚠️ 标注预测深度Level+置信度，禁止绝对断言→ `references/prediction-boundary-protocol.md`、`references/prediction-output-protocol.md`）⭐ v3.2 新增

## 能力水平

当前能力水平：**顶级专业占星师水平（6.0/5）**

### 核心优势（按能力域分组）

**静态解读**：
- ✅ 行星配置+Nakshatra+Yoga格局识别+逆行/燃烧/行星战争深度检查
- ✅ **Argala行星干预分析**（四类型Argala+Virodha反干预+12宫完整速查+10领域模板+PAC-DARES整合）⭐ v3.2 新增
- ✅ Shadbala六力量化评估+Ashtakavarga完整BAV/SAV体系
- ✅ 九层分盘体系（D1-D60完整解析）+Ketu双属性+Yoga Phala Timing

**动态推运**：
- ✅ Vimshottari五级Dasha+Jaimini Chara Dasha+KP Sub-Lord三系统协同
- ✅ **替代推运系统**（Ashtottari+Yogini+Kalachakra+Prashna问卜+条件Dasha 8大系统）⭐ v3.3 新增
- ✅ **Dasa Convergence轻量三系统法**（Vimsottari+Yogini+Chara手工推算交叉验证，无需外部工具即可达到Level 2收敛）⭐ v3.2 新增
- ✅ 四参考点过境分析（Lagna+Chandra+AL+Navamsa）+Double Transit+Pratyantar月/周精度
- ✅ Varshaphala年运盘（Tajika+Muntha+年主星+10种Yoga审计）

**专项分析**：
- ✅ 关系占星（Koota 36分+D9伴侣+Mangal Dosha+DK分析）
- ✅ 自动出生时间矫正（八大方法+自动化流程+验证报告）
- ✅ 补救措施（宝石+Mantra+Puja+Yantra+Daan+个性化方案）

**元能力**：
- ✅ 现代措辞解读+现代生活场景映射+常见误判纠错（错题本）
- ✅ PDF星盘读取+案例对比分析+全球占星师方法论整合
- ✅ 综合解盘工作流（三级深度+10领域路由+质量检查清单）
- ✅ **AI解盘工作流Prompt工程**（7阶段完整执行引擎：PDF提取→意图路由→静态10步→动态7步→应期→补救→现代措辞包装）⭐ v3.2 新增
- ✅ **古典文献体系+专业发展路径**（BPHS翻译版本对比+当代诠释者+6大认证体系+文献引用置信度评级）⭐ v3.3 新增

## 更新记录

详见 `CHANGELOG.md`。当前版本：v3.7.0。

## 参考资料

本Skill包含以下参考资料（存储在references/目录），共75个文件：

### AI解盘工作流（1个）⭐ v3.2 新增
0. **ai-reading-workflow-prompt.md**：AI解盘工作流Prompt工程（7阶段完整执行引擎：PDF提取→意图路由→静态分析10步→动态推运7步→应期输出→补救→现代措辞包装）⭐⭐⭐⭐⭐

### 核心方法论（9个）
1. **common-misconceptions.md**：印度占星常见误判与冲突问题集（错题本）⭐⭐⭐⭐⭐
2. **modern-language-guide.md**：现代生活措辞指南（传统术语→现代措辞映射）⭐⭐⭐⭐⭐
3. **birth-time-rectification-advanced.md**：出生时间矫正高级方法论（八大矫正方法+自动化矫正流程）⭐⭐⭐⭐⭐
4. **birth-time-rectification-cases.md**：出生时间矫正案例集（实践验证案例）⭐⭐⭐⭐
5. **pdf-chart-reading-guide.md**：PDF星盘读取指南 v3.0（全量数据提取+完整性门+交叉校验+管线桥接）⭐⭐⭐⭐⭐
6. **prediction-checklist.md**：预测清单
7. **data-bridge-mapping.md**：数据桥接映射（PDF提取字段→方法论需求全量对照+外部依赖处理）⭐⭐⭐⭐⭐ v3.0 新增
8. **prediction-boundary-protocol.md**：预测精度边界规范（能/不能预测的维度+四等级预测深度+禁用绝对断言+修正语言模板）⭐⭐⭐⭐⭐ v3.2 新增
9. **prediction-output-protocol.md**：预测输出规范（四等级深度标注+置信度评估+措辞标准+禁用措辞清单）⭐⭐⭐⭐⭐ v3.2 新增

### 基础知识体系（7个）
10. **planets.md**：行星详解（九大行星完整属性、关系、征象）⭐⭐⭐⭐⭐
11. **signs-and-houses.md**：星座与宫位基础知识（12星座+12宫位完整参考）⭐⭐⭐⭐
12. **nakshatra_deities.md**：27星宿神祇详解（每宿主神+神话+现代映射）⭐⭐⭐⭐⭐
13. **nakshatra-chinese-quick-ref.md**：27 Nakshatra中文速查表（完整参数+现代映射+职业倾向）⭐⭐⭐⭐⭐
14. **vimshottari_dasha_guide.md**：Vimshottari大运系统指南（120年周期+行星年限+计算方法）⭐⭐⭐⭐
15. **dasha-transit-method.md**：Dasha+Transit方法论
16. **software-comparison-guide.md**：排盘软件与天文计算完全指南（8种Ayanamsa体系对比+桌面/在线/移动软件矩阵+三种图表格式+排盘精度要求）⭐⭐⭐⭐ v3.3 新增

### Yoga格局体系（5个）
17. **yoga_list.md**：Yoga格局完整列表（300+Yoga分类索引）⭐⭐⭐⭐⭐
18. **yoga-list-chinese.md**：瑜伽格局中文完整列表（现代措辞版）⭐⭐⭐
19. **yoga-and-dasha.md**：Yoga与Dasha结合分析（Yoga激活时机）⭐⭐⭐⭐
20. **yoga-strength-scoring-system.md**：Yoga力量评分系统（量化评估体系）⭐⭐⭐⭐
21. **neechabhanga-raja-yoga.md**：落陷化解详解（Neechabhanga完整条件链）

### 宫位与生活场景映射（3个）
22. **house-modern-mapping.md**：宫位现代场景映射（12宫现代生活）
23. **house-domain-planet-mapping.md**：宫位-领域-行星映射表（避免指标混淆）⭐⭐⭐⭐⭐
24. **modern-life-scenarios-complete.md**：现代生活场景完整版（跨国职业/数字游民/远程工作）⭐⭐⭐⭐

### 占星系统（5个）
25. **jaimini-complete-system.md**：Jaimini占星完整体系（Chara Karakas、Chara Dasha、Karakamsha）⭐⭐⭐⭐⭐
26. **kp-astrology-complete-system.md**：KP占星完整体系（249个Sub-Lord、Significator、问答占星）⭐⭐⭐⭐⭐
27. **kp-practical-event-timing.md**：KP实战案例与Sub-Lord事件时机判断指南 ⭐⭐⭐⭐⭐
28. **remedies-complete-system.md**：补救措施完整体系（宝石、Mantra、Puja、Yantra、Daan）⭐⭐⭐⭐⭐
29. **personalized-remedies-system.md**：个性化补救系统（根据星盘定制方案）⭐⭐⭐⭐

### 分盘与力量评估（7个）
30. **ashtakavarga-complete-system.md**：Ashtakavarga完整体系（BAV完整分配表+SAV聚合+337点校验+自检清单）⭐⭐⭐⭐⭐ v2.0
31. **shadbala-complete-methodology.md**：Shadbala完整计算方法论（六种力量+公式+案例+速查卡）⭐⭐⭐⭐⭐ v2.0
32. **planetary-strength-quick-ref.md**：行星力量速查表（Shadbala+Ashtakavarga双系统）⭐⭐⭐⭐⭐
33. **varga-system-quick-reference.md**：综合九层分盘体系对照手册（D1-D60完整解析）⭐⭐⭐⭐⭐
34. **varga-divisional-charts-quick-reference.md**：分盘快速参考（D1-D60速查卡片）⭐⭐⭐⭐
35. **navamsa-d9-interpretation-template.md**：D9 Navamsa解读模板（伴侣/灵魂层面分析）⭐⭐⭐⭐
36. **shodasavarga-complete-guide.md**：Shodasavarga十六分盘完全指南（16种分盘+Vimsopaka Bala四套权重+Varga Dignity尊严等级+分盘实战工作流）⭐⭐⭐⭐⭐ v3.3 新增

### 过境与推运（9个）
37. **transit-comprehensive-guide.md**：过境综合实战指南（Double Transit+Ashtakavarga过境评分+多参考点分析）⭐⭐⭐⭐⭐ v1.1
38. **transit-multi-reference-guide.md**：多参考点过境分析强制规范（四参考点+案例对照+防回归）⭐⭐⭐⭐⭐ v1.9
39. **pratyantar-calculation-guide.md**：Pratyantar精确计算指南（四级Dasha+Transit叠加+Sookshma/Prana）⭐⭐⭐⭐⭐ v2.0
40. **varshaphala-annual-chart-guide.md**：Varshaphala年运盘指南（Tajika+Muntha+年主星+Mudda Dasha）⭐⭐⭐⭐⭐
41. **dasha-calculation-tool.md**：Dasha计算工具（精确到日的大运计算）⭐⭐⭐⭐
42. **dasa-convergence-methodology.md**：Dasa Convergence多系统大运交叉验证（9大Dasha独立性分析+五步法+Convergence等级量化+JH PDF数据源对照+轻量三系统手工推算法+Yogini推算表）⭐⭐⭐⭐⭐ v3.2 升级
43. **navatara-kantaka-shani-guide.md**：Navatara九星链分析+Kantaka Shani刺土星（双技法合并文件）⭐⭐⭐⭐ v3.1 新增
44. **alternative-dasha-systems.md**：替代推运系统完全指南（Ashtottari 108年+Yogini 36年八女神+Kalachakra 144年双模式+Prashna问卜占星+五步整合法）⭐⭐⭐⭐⭐ v3.3 新增
45. **condition-dasha-complete.md**：条件Dasha系统完全指南（8大条件Dasha适用条件+周期+条件判定流程图+与非条件Dasha对照+软件支持）⭐⭐⭐⭐ v3.3 新增

### 关系占星（3个）
46. **relationship-astrology-guide.md**：关系占星/合盘分析指南（Koota 36分制+D9伴侣+Mangal Dosha+DK分析）⭐⭐⭐⭐⭐
47. **spouse-multi-layer-methodology.md**：配偶多层综合分析方法论（6层交叉确认：DK+7宫主+金星+木星/月亮+昼夜区分+Rahu辅助，标准六步流程，置信度评估，非传统关系适配）⭐⭐⭐⭐⭐ v3.7.2 新增
48. **planetary-dignity-complete-reference.md**：行星尊严与度数完整参考手册（精确旺衰度数+Moolatrikona+行星生命阶段+燃烧阈值+Neecha Bhanga落陷取消+Sect昼夜区分+丈夫征象星木星vs火星+Pushkara Navamsha+Vargottama+DK分析协议+D9婚姻8步算法）⭐⭐⭐⭐⭐ v3.7.3 新增
49. **marriage-timing-comprehensive-techniques.md**：婚姻应期技法综合手册（KN Rao Double Transit精确规则+VP Goel功能征象星+Jaimini DK木星过境激活法+Upapada Lagna完整体系+Ketu期感情特征+木星入庙Cancer 2026影响）⭐⭐⭐⭐⭐ v3.7.3 新增

### 综合分析框架（5个）
50. **comprehensive-reading-workflow.md**：综合解盘工作流（三级深度+10领域路由+质量检查清单）⭐⭐⭐⭐⭐
51. **tri-system-analysis-template.md**：Jaimini+KP+Parashara三系统协同分析模板 ⭐⭐⭐⭐⭐
52. **yoga-phala-timing-guide.md**：Yoga Phala Timing精确预测（五大方法+标准化流程+一楠案例实战）⭐⭐⭐⭐⭐ v2.1
53. **tajika-yoga-complete-guide.md**：Tajika Yoga完整审计指南（10种Yoga+Orb速查+审计流程+一楠案例）⭐⭐⭐⭐⭐ v2.0
54. **promise-assessment-templates.md**：承诺判定模板（10领域Promise检查+承诺等级量化+Promise vs Activation两步分析法）⭐⭐⭐⭐⭐ v3.2 新增

### 静态解读最后一环（3个）
55. **retrograde-combustion-war-guide.md**：逆行/燃烧/行星战争深度指南（5星逆行12宫+6星燃烧含义+5对战争+三重叠加）⭐⭐⭐⭐⭐ v2.1
56. **ketu-dual-nature-guide.md**：Ketu双重属性解读框架（放手+突破+12宫位双解读+判断矩阵）⭐⭐⭐⭐⭐ v2.0
57. **argala-complete-guide.md**：Argala行星干预体系完整指南（四类型Argala+Virodha反干预+12宫速查+10领域模板+PAC-DARES整合）⭐⭐⭐⭐⭐ v3.2 新增

### 案例库（13个）
58. **famous-case-library.md**：名人案例库统一入口（24个案例索引+验证等级分类+6大核心验证结论）⭐⭐⭐⭐⭐ v2.0 整合版
59. **consultation-case-library.md**：普通人咨询案例库（42个案例）⭐⭐⭐⭐⭐
60. **celebrity-cases.md**：名人案例分析
61. **case-study-collection-2026-04-22.md**：案例研究合集（2026-04-22整理）
62. **shatabhisha-complete.md**：Shatabhisha星宿完整解读（一楠案例深度剖析）
63. **verified-celebrity-cases.md**：名人验证案例集（核心验证）
64. **verified-celebrity-cases-summary.md**：名人验证案例总结
65. **verified-celebrity-cases-part2-elvis.md**：验证案例：猫王（Elvis Presley）
66. **verified-celebrity-cases-part2-trump.md**：验证案例：特朗普（Donald Trump）
67. **verified-celebrity-cases-part3-marilyn-monroe.md**：验证案例：玛丽莲·梦露
68. **verified-celebrity-cases-part3-michael-jackson.md**：验证案例：迈克尔·杰克逊
69. **verified-celebrity-cases-part3-summary.md**：验证案例Part3总结
70. **verified-celebrity-cases-part4-leonardo-dicaprio.md**：验证案例：莱昂纳多·迪卡普里奥

### 高级技法与全球方法论（4个）
71. **advanced-techniques.md**：高级技法合集（综合进阶技法）
72. **global-astrologer-practical-methodology.md**：全球占星师实战方法论（顶级占星师经验汇总）⭐⭐⭐⭐⭐
73. **global-astrologer-reflections.md**：全球占星师反思笔记（方法论迭代记录）
74. **qin_ruisheng_system.md**：秦瑞生占星体系（华人占星师方法论）

### 古典文献与专业发展（2个）⭐ v3.3 新增
75. **classical-texts-translation-guide.md**：古典梵语文献与翻译版本指南（核心文献层级+BPHS翻译版本对比+当代8位诠释者+数字资源路径+文献引用置信度评级）⭐⭐⭐⭐ v3.3 新增
76. **professional-development-guide.md**：专业占星师发展路径与学习资源指南（6大认证体系+分级书单+多媒体资源+咨询实践三阶段+伦理守则+东西方整合）⭐⭐⭐⭐ v3.3 新增

## 模板文件

本Skill包含以下模板文件（存储在assets/目录）：

1. **birth_time_rectification_template.md**：出生时间矫正信息收集模板（用户填写）⭐⭐⭐⭐⭐
2. **chart_analysis_template.md**：星盘分析模板
3. **event_timing_template.md**：事件时机模板
4. **timing-prediction-template.md**：推运应期分析模板（五层验证法+事件专属公式+月/周级精度）⭐⭐⭐⭐⭐ v2.0 升级

## 使用示例

- **读取PDF星盘**：上传Jagannatha Hora/Parashara's Light生成的PDF→提取全量数据（D1+D9+D10+特殊Lagna+Karakas+Shadbala+AV+Dasha+Yoga）→完整性门检查→进入分析
- **精确推运应期**：PDF数据+分析日期→五层验证（本命+Dasha五级+Transit四参考点+Jaimini+KP+Varshaphala）→输出主窗口（月级）+次窗口（周级）+确认/延迟/取消信号
- **出生时间矫正**：提供10-25个生命事件→八大方法自动验证→输出矫正结果+置信度
- **专项事件预测**：描述问题→路由到正确宫位/Karaka/Sub-Lord→事件专属应期公式→精确时间窗口

## 注意事项

1. **出生时间精度**：越精确预测越准（±2分钟内最佳），可通过矫正提高
2. **出生时间矫正**：需提供10-25个生命事件，分布不同年龄段，精确到月份最佳
3. **PDF星盘**：支持Jagannatha Hora、Parashara's Light等专业软件
4. **三层验证法**：所有预测必须Dasha+Transit+Varga交叉验证
5. **现代场景优先**：所有解读使用现代措辞和现代生活场景映射
6. **解盘深度**：默认Level 2（专项分析），复杂问题自动升级Level 3

---

**版本**：3.7.3
**创建日期**：2026-04-20
**最后更新**：2026-04-25（v3.7.3 新增行星尊严与度数完整参考手册——精确旺衰度数+Moolatrikona区间+行星生命阶段+燃烧阈值+Neecha Bhanga落陷取消规则+Sect昼夜区分完整规则+丈夫征象星木星vs火星论证+Pushkara Navamsha精确度数+Vargottama婚姻意义+DK完整8步分析协议+D9婚姻8步旗标算法；v3.7.2 新增配偶多层综合分析方法论+6层交叉确认法+昼夜区分法+标准六步流程；v3.7.1 新增 full-reading 全自动综合解盘子命令 + 三条入口路径路由 + 工作流v3.0；v3.7.0 新增7大计算模块：BPHS十六分盘精确计算+度数精确相位+Jaimini完整系统+高级Nakshatra分析+Argala门闩+Tajika年运盘+合盘分析，引擎子命令21→22）
