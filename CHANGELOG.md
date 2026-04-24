# 印度占星 Skill 更新日志

## v3.7.0（2026-04-25）— 7大新模块：BPHS十六分盘+精确相位+Jaimini+高级Nakshatra+Argala+Tajika+合盘

### 新增模块（7个）

- **`scripts/varga.py`**：BPHS Shodasavarga十六分盘完整计算
  - 支持全部16个分盘：D2/D3/D4/D7/D9/D10/D12/D16/D20/D24/D27/D30/D40/D45/D60
  - 每个分盘输出精确度数（非仅星座名）
  - D30 Trimsamsa 特殊不等宽映射
  - D9 含 Jaimini 分析（7宫/Venus/Jupiter/尊严状态）
  - D60 含业力分析（角宫吉凶星分布）

- **`scripts/aspects.py`**：度数精确相位系统（Drishti）
  - 标准7宫对冲 + 火星4/7/8 + 木星5/7/9 + 土星3/7/10
  - Orb分类：tight(≤3°) / moderate(≤6°) / loose(≤10°)
  - 计算每个相位的入相位/出相位状态
  - 合相精度分析

- **`scripts/jaimini.py`**：Jaimini系统完整实现
  - `calc_chara_karaka_7()`：7行星 Chara Karaka（AK→DK）
  - `calc_chara_karaka_8()`：8行星 Chara Karaka（含Rahu逆行度数处理）
  - `calc_chara_dasha()`：星座大运（基于上升奇偶性决定方向）
  - `calc_karakamsha()`：灵魂方向分析（DK的D9位置解读）

- **`scripts/nakshatra_advanced.py`**：高级Nakshatra分析
  - 精确Nakshatra定位（名称/Pada/度数/Gana/元素）
  - `calc_tara_bala()`：9循环Tara关系分析
  - `calc_sub_lord()`：KP系统 Sub-Lord 计算
  - `nakshatra_compatibility()`：Tara+元素+Gana综合兼容性

- **`scripts/argala.py`**：Argala门闩系统
  - 主Argala：2/4/11宫 → 财富/幸福/收益
  - 副Argala：5/8宫 → 权力/转化
  - Virodha（阻断）：12→2, 10→4, 3→11, 9→5, 2→8
  - 净评分计算和吉凶判定

- **`scripts/tajika.py`**：Tajika/Varshaphala年运盘
  - `calc_muntha()`：年度上升进展
  - `calc_year_lord()`：年度守护星 + 辅助星（2/5/9/11宫主）
  - `calc_mudda_dasha()`：12个月比例大运
  - `calc_tri_pataka()`：三旗系统评估

- **`scripts/synastry.py`**：合盘分析系统
  - Ashta Koota 36分制（8维度：Varna/Vashya/Tara/Yoni/Graha Maitri/Gana/Bhakuta/Nadi）
  - Mangal Dosha 检查（火星在1/2/4/7/8/12宫）
  - Papasamya 凶星抵消度评估
  - Dasha时间线兼容性分析
  - 自动生成化解建议

### 引擎升级（jyotish_engine.py）

- 版本 v3.6.0 → **v3.7.0**
- 新增7个CLI子命令：`varga-full` / `aspects` / `jaimini` / `nakshatra-adv` / `argala` / `tajika` / `synastry`
- 总子命令数：14 → **21**
- 所有新模块通过一楠星盘验证（1993-04-17 14:45）

### 验证结果

| 模块 | 子命令 | 一楠星盘验证 | 关键输出 |
|------|--------|-------------|---------|
| varga | varga-full | ✅ | D9 Navamsa 精确度数+尊严 |
| aspects | aspects | ✅ | 6个精确相位（Moon-Saturn合相等）|
| jaimini | jaimini | ✅ | AK=Venus, DK=Mars, Chara Dasha序列 |
| nakshatra | nakshatra-adv | ✅ | 9行星Tara Bala, Sub-Lord |
| argala | argala | ✅ | 9行星门闩分析 |
| tajika | tajika | ✅ | 33岁 Muntha=金牛座, YearLord=Venus |
| synastry | synastry | ✅ | Ashta Koota 26/36 (72.2%) |

## v3.6.0（2026-04-24）— CNWU16二次借鉴：report_builder + R2b列校验 + P3/P8/冲突仲裁

### 新增文件
- **`scripts/report_builder.py`**：MD→HTML报告生成器（羊皮纸主题）
  - 基于 CNWU16/vedic-astro-skills 的 report_builder.py 改编适配
  - 18项章节注册表，自动扫描多种 MD 命名模式
  - 羊皮纸CSS + 封面 + 目录 + A4打印优化
  - 中英文双语支持
  - 可通过 engine `report` 子命令调用
  - 浏览器打开后 Ctrl+P → Save as PDF

### 验证模块升级
- **`scripts/validate.py`**：新增 R2b BAV列→SAV列校验
  - 每个星座的7行星BAV bindus列向量之和 = 该星座SAV分数
  - 交叉验证行总和(R2)和列总和的一致性

### 审计管线升级（jyotish_engine.py cmd_audit）
- **P3 仓库耦合**（Warehouse Coupling）：
  - 双宫掌管=货物捆绑分析
  - 识别同时掌管两个宫位的行星（如水星同时掌管双子宫和处女宫）
  - 评估捆绑质量：凶吉混合/压力型/吉庆型/消耗型/中性
- **P8 年龄状态**（Age Status）：
  - 基于行星在星座中的度数区间判定生命周期
  - 婴幼(0-10°)=辅助型，青壮(10-20°)=主动型，老年(20-30°)=自动执行型
- **冲突仲裁3条规则**（Conflict Arbitration）：
  - 规则1: P1清理者+P7入旺 = "带毒高价值资产"（禁止说逢凶化吉）
  - 规则2: P5凶宫+BAV高 = "乱世出英雄"
  - 规则3: P1吉+P2受损 = "空有雄心无着力点"

### 子命令升级
- **新增 `report`** 子命令：调用 report_builder.py 生成 HTML 报告
  - 用法: `python3 jyotish_engine.py report <folder> --name "名字" --lagna "上升" --lang cn`
- 总子命令数：11 → 14

## v3.5.0（2026-04-24）— BPHS完整表校准 + R1-R10验证 + P1-P12审计 + 验前事
- **重写 `scripts/ashtakavarga.py`** v1.0 → v2.0：
  - 从简化 BAV_BASE + EXTRA_BINDHU（SAV=94❌）升级为完整 BPHS 8×8 贡献矩阵
  - 每颗行星的 BAV 从所有 8 个来源（7行星+Lagna）获得贡献，非仅自贡献
  - BPHS 校正：月亮 BAV 木星贡献去12宫→49，金星 BAV 水星贡献加12宫→52
  - SAV 总和 = 337 ✅（7行星 BAV 之和），含 Lagna 完整总分 = 386
  - 两组出生数据端到端验证通过（一楠+奥巴马）
- **新增 `scripts/validate.py`**：R1-R10 数学验证模块
  - R1: SAV 总和 = 337
  - R2: 各 BAV 行常数校验（Sun=48, Moon=49, ...）
  - R3: 水星延伸角 ≤ 28°
  - R4: 金星延伸角 ≤ 47°
  - R5: Rahu-Ketu 严格 180° 对冲
  - R6: 逆行合法性（太阳/月亮不逆行，Rahu/Ketu永远逆行）
  - R7: Dasha 大运年限链总和 = 120 年
  - R8: 行星完整性（7行星 + Rahu + Ketu + Lagna）
  - R9: 星座度数范围 [0, 30)
  - R10: 宫位连续性（1-12宫无断点）
- **升级 `scripts/jyotish_engine.py`** v3.4.0 → v3.5.0：
  - 11 → 13 个子命令（新增 validate/audit）
  - `chart --validate`：星盘计算附加 R1-R10 验证
  - `validate` 子命令：独立运行 R1-R10 校验
  - `audit` 子命令：P1-P12 行星审计管线（Identity/Health/Resource SAV/Road Condition/Exit SAV/Dignity/Shadbala/Aspects/Nakshatra/Yogas）
  - `predict --past-verify`：验前事模式（推断2-4个高信号历史时段，避免冷读效应）
- **来源**：CNWU16/vedic-astro-skills 仓库分析 + ZODIAQ BPHS 完整表

## v3.4.0（2026-04-24）— 高级计算引擎 + Hermes集成 + EventPredictionModel
- **新增 `scripts/shadbala.py`**：Shadbala六重力量计算模块
  - 完整实现Parashara系统六种Bala：Sthana（位置）、Dig（方向）、Kala（时间）、Chesta（运动）、Naisargika（天然）、Drik（相位）
  - 输出每颗行星的六维得分、总Virupas/Rupas、Ishta Bala百分比、强度等级（极强/强/充足/略弱/弱/极弱）
  - 行星力量排名
  - 端到端验证：一楠星盘 Sun 6.73 Rupas（强）、Moon 5.45 Rupas（略弱）
- **新增 `scripts/ashtakavarga.py`**：Ashtakavarga八分法计算模块
  - BAV（Bhinna Ashtakavarga）8源独立贡献表
  - SAV（Sarva Ashtakavarga）聚合评分 + 吉凶评估（极吉/吉利/中等/挑战）
  - Shodhya Pinda简化计算
  - ⚠️ 已知限制：SAV总分未达标准337（BAV_BASE表为简化版，需后续校准为完整Parashara表）
- **新增 `scripts/hermes_memory_core.py` + `scripts/hermes_bridge.py`**：Hermes Agent中间件
  - 零外部依赖（纯Python stdlib: sqlite3, json, os, re, datetime, hashlib）
  - FTS5全文搜索 + 6张SQLite表
  - 记忆存储/检索/上下文构建
- **新增 `scripts/event_prediction_model.py`**：事件预测规则引擎
  - 替代LAM深度学习模型（原0.17%准确率）
  - 三层验证法：静态星盘征象 + Dasha激活 + Transit触发
  - 覆盖婚姻/职业/财富/健康/教育/子女/旅行/灵性8大领域
  - Prediction dataclass：概率评分 + 风险等级 + 时机 + 关键因素 + 建议
- **升级 `scripts/jyotish_engine.py`** v3.3.1 → v3.4.0：
  - 8 → 11个子命令（新增 shadbala/ashtakavarga/memory）
  - 提取 `compute_chart_data()` 公共函数（chart/shadbala/ashtakavarga共用）
  - `predict` 子命令增强：优先使用 EventPredictionModel，降级到简化版
  - `memory` 子命令：store/search/context/stats 四种操作
  - `_add_chart_args()` 公共参数函数消除CLI定义重复
  - 行星数据增加 `speed` 字段（Shadbala Chesta Bala需要）
- **SKILL.md v3.4.0**：版本号+触发词（Shadbala/六重力量/Ashtakavarga/八分法/事件预测/记忆系统）+11子命令表+工作流增加步骤4-5/8/10

## v3.3.1（2026-04-24）— 计算引擎集成
- **新增 `scripts/jyotish_engine.py`**：印度占星统一计算引擎入口
  - 基于 Swiss Ephemeris 天文计算库（Lahiri Ayanamsa 恒星黄道标准）
  - 8大子命令：chart（星盘计算）、dasha（大运时间线）、yoga（格局识别）、predict（三层验证法）、varga（分盘D9/D10）、celebrity（名人案例查询）、db-stats（数据库统计）、transit（过境查询）
  - 自动连接外部数据源：验证数据库（15,840条）、名人CSV（15,807条）、过境配置（2026-2028）
  - 完成端到端验证：一楠星盘上升狮子座（11.66° vs PDF 12.63°）、D9上升巨蟹座（与PDF一致）
- **SKILL.md v3.3.1**：新增 §13 计算引擎集成说明 + 触发词增加（算星盘/排盘/计算星盘/查名人）
- **已知限制**：LAM深度学习模型（75.84MB）和 Hermes Agent 中间件未集成（超出 CLI 脚本能力范围）

## v3.2.0（2026-04-24）— Argala+AI工作流+Dasa Convergence实操化
- **新增 `argala-complete-guide.md`**：Argala行星干预体系完整指南
  - 四类型Argala（主Argala 2/4/11宫 + 次Argala 5/8宫 + Virodha反干预 + 特殊规则）
  - 12宫位完整Argala矩阵（主Argala + Virodha对照）
  - 10核心领域Argala分析模板（婚姻/事业/财富/子女/健康等）
  - Argala链追踪高级技法
  - PAC-DARES整合位置
- **新增 `ai-reading-workflow-prompt.md`**：AI解盘工作流Prompt工程
  - 7阶段完整执行引擎（PDF提取→意图路由→静态分析10步→动态推运7步→应期输出→补救→现代措辞包装）
  - 每个阶段的严格输出模板
  - 质量门Pass/Limited/Fail规则
  - 完整工作流一页纸速查
- **升级 `dasa-convergence-methodology.md` v2.0**：
  - 新增§〇 JH PDF数据源对照表（9大Dasha系统的PDF可提取性一目了然）
  - 新增§七 轻量Convergence三系统法（Vimsottari+Yogini+Chara，无需外部工具）
  - Yogini Dasha完整手工推算表（8位女神+年数+Nakshatra分组+定位公式）
  - Chara Dasha简化推算法（方向判断+Rashi Drishti速查）
  - 轻量Convergence实战模板（标准表格格式）
  - 一楠案例Yogini推算实战验证（Ulka周期=Venus统治=女命恋爱星确认）
- **SKILL.md v3.2.0**：新增2个参考文件注册（66文件总数）+Argala能力描述+AI工作流描述+预测清单增加Argala检查项和Dasa Convergence轻量法+触发词增加Argala/Yogini/Chara Dasha/AI解盘

## v3.1.0（2026-04-24）— 多Dasa收敛+技法补齐+案例库整合
- **新增 `dasa-convergence-methodology.md`**：Dasa Convergence多系统大运交叉验证方法论
  - 9大Dasha系统独立性对照表（Vimsottari/Yogini/Kalachakra/Sudasa/Chara/Narayana/Nadi/Ashtottari/Shodashottari）
  - Convergence五步法：目标领域→提取Dasha→逐系统检查→寻找重叠→Transit确认
  - Convergence等级量化：Level 0-3 概率提升公式
  - 一楠实战案例（Vimsottari+Yogini+Sudasa三系统收敛2027.3）
- **新增 `navatara-kantaka-shani-guide.md`**：双技法合并文件
  - Navatara九星链分析：27宿三组分组法+行星分布解读+一楠实战
  - Kantaka Shani刺土星：四敏感位置（1/4/8/10宫）+严重程度分级+缓解因素+一楠2025-2032 Kantaka预测
- **整合 `famous-case-library.md` v2.0**：
  - 从"1个案例"升级为"24个案例统一入口"
  - 分级索引：A级（AA级验证12个）、B级（1个，梦露⚠️）、C级（比对级11个）
  - 6大核心验证结论（100%支持率）
- **技法覆盖率提升**：58%→83%→补齐后约88%（M19 Navatara+M22 Kantaka Shani已覆盖）
- **SKILL.md v3.1.0**：新增2个参考文件注册（63文件总数）+Dasa Convergence能力描述+版本号更新

## v3.0.0（2026-04-24）— 管线重写：PDF→解盘→应期全链路
- **核心定位重定义**：Skill使命明确为"PDF输入→严谨解盘→精确推运应期输出"
- **重写 `pdf-chart-reading-guide.md` v3.0**（从v1.0升级）：
  - 补全9个P0数据断层：AL/UL/HL/GL特殊Lagna、Jaimini七Karakas、Shadbala六力量、Ashtakavarga BAV/SAV、Yoga清单、逆行/燃烧/战争标记、行星Drishti相位
  - 精确11页JH PDF页面映射
  - 数据完整性门（Quality Gate）：P0数据缺失时禁止完整分析
  - 交叉校验规则：D1 NK↔D9、SAV=337、Moon NK↔Dasha起始
  - 完整JSON Schema覆盖全量数据
  - 管线桥接：提取字段→分析方法→参考文件完整映射
- **升级 `timing-prediction-template.md` v2.0**（从v1.0升级）：
  - 五层验证法：本命征象→Dasha激活（五级Maha→Prana）→Transit触发（四参考点+Double Transit）→Jaimini+KP交叉确认→Varshaphala年运盘确认
  - 应期精度：主窗口（月级）+次窗口（周级）+关键触发日
  - 确认/延迟/取消信号系统
  - 五大事件专属应期公式（婚姻/事业/财富/子女/健康）
- **新增 `data-bridge-mapping.md`**：PDF提取字段→方法论需求全量对照表+外部数据依赖处理
- **SKILL.md v3.0.0**：加入PDF-first强制工作流+核心定位说明+新文件注册

## v2.1.2（2026-04-23）— 瘦身+质量修复
- 删除空占位符 `api_reference.md`、`example_asset.txt`
- 修复4个死链引用
- SKILL.md瘦身130+行：更新记录移至CHANGELOG.md

## v2.1.1（2026-04-23）— 资料审计修复
- 删除空占位符 `api_reference.md`、`example_asset.txt`
- 修复4个死链引用：planetary-configurations→planets.md、yoga-patterns→yoga_list.md、nakshatra-guide→nakshatra_deities.md、birth-time-rectification(基础)→birth-time-rectification-cases.md
- 补注册26个遗漏文件，修复4处编号重复
- 按逻辑重组为11个分类，60个文件全部添加引用路径
- 扩充 `kp-astrology-complete-system.md` v2.0：从4.5KB扩充至完整体系
- SKILL.md瘦身：更新记录移至本文件，精简核心优势列表

## v2.1.0（2026-04-23）— Yoga Timing + 静态解读最后一环
- 新增 `yoga-phala-timing-guide.md`：五大方法预测Yoga结果时机
- 新增 `retrograde-combustion-war-guide.md`：逆行/燃烧/行星战争深度指南
- 预测清单升级：加入逆行/燃烧/战争检查+Yoga Phala Timing步骤

## v2.0.0（2026-04-23）— 五大核心技法完整化
- 新增 `ketu-dual-nature-guide.md`：Ketu双重属性框架
- 新增 `shadbala-complete-methodology.md`：六种力量完整计算
- 新增 `tajika-yoga-complete-guide.md`：10种Tajika Yoga完整审计
- 新增 `pratyantar-calculation-guide.md`：Pratyantar精确计算
- 升级 `ashtakavarga-complete-system.md` v2.0

## v1.9.0（2026-04-23）— 多参考点过境分析强制规范
- 新增 `transit-multi-reference-guide.md`
- 修正：Chandra Lagna提升为强制基准
- 根因：实际分析中遗漏Chandra Lagna视角导致预测偏差

## v1.8.0 及更早（2026-04-20 ~ 2026-04-23）
- 新增过境综合实战、关系占星、Varshaphala年运盘、综合解盘工作流、27 Nakshatra中文速查
- 新增Jaimini完整体系、KP占星体系、补救措施体系、Ashtakavarga体系
- 新增常见误判纠错、现代措辞解读、PDF星盘读取、自动出生时间矫正
- 新增名人案例库、九层分盘体系、三系统协同分析、行星力量速查
