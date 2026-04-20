# PDF星盘读取指南

## 支持的PDF格式

本Skill支持读取以下专业占星软件生成的PDF星盘报告：

### 1. Jagannatha Hora（推荐）
- **格式特点**：标准印度占星格式，包含D1-D60分盘
- **页面结构**：
  - 第1页：D1本命盘（Rasi Chart）
  - 第2页：D9 Navamsa盘
  - 第3页：D10 Dasamsa盘
  - 第4-11页：其他分盘（D2、D7、D16、D20、D24、D27、D30、D40、D45、D60）
  - 第12页：Dasha周期表
  - 第13页：行星度数表

### 2. Parashara's Light
- **格式特点**：专业版，包含详细Yoga分析
- **页面结构**：类似Jagannatha Hora，但包含更多分析报告

### 3. 其他印度占星软件
- **格式要求**：必须包含D1本命盘、行星位置、宫位信息、Nakshatra信息

---

## PDF星盘读取流程

### 第一步：识别PDF格式

**AI会自动识别**：
- PDF是否为印度占星星盘报告
- 使用哪种占星软件生成
- 包含哪些分盘和报告

### 第二步：提取关键信息

**AI会自动提取**：

#### 1. 基本信息
- 出生时间（年月日时分）
- 出生地点（城市、经纬度）
- 性别（如果提供）
- 时区

#### 2. D1本命盘数据
- 上升星座（Lagna）及其度数
- 上升Nakshatra及其Pada
- 12宫宫主星（House Lords）
- 12宫宫内星（Planets in Houses）
- 行星位置（星座、度数、Nakshatra）
- 行星状态（入庙、落陷、逆行等）

#### 3. D9 Navamsa盘数据
- D9上升星座
- D9行星位置
- 关键行星在D9的状态

#### 4. D10 Dasamsa盘数据
- D10上升星座
- D10行星位置
- 关键行星在D10的状态

#### 5. Dasha周期信息
- 当前主运（Maha Dasha）
- 当前小运（Antar Dasha）
- 当前微运（Pratyantar Dasha）
- Dasha开始和结束时间

#### 6. 其他分盘数据（如果提供）
- D2 Hora盘（财富盘）
- D7 Saptamsa盘（子女盘）
- D60 Shashtiamsha盘（业力盘）

### 第三步：转换为结构化数据

**AI会自动转换为以下格式**：

```json
{
  "birth_info": {
    "date": "1993-04-17",
    "time": "14:45",
    "location": "邯郸",
    "latitude": 36.6,
    "longitude": 115.5,
    "timezone": "UTC+8"
  },
  "d1_chart": {
    "lagna": {
      "sign": "Leo",
      "degree": 12.63,
      "nakshatra": "Magha",
      "pada": 4
    },
    "houses": [
      {
        "house_number": 1,
        "sign": "Leo",
        "lord": "Sun",
        "planets": ["Sun"],
        "planet_details": {
          "Sun": {
            "degree": 28.33,
            "nakshatra": "Uttara Phalguni",
            "pada": 1,
            "status": "own_sign"
          }
        }
      }
      // ... 其他11宫
    ]
  },
  "d9_chart": {
    "lagna": {
      "sign": "Scorpio"
    },
    "key_planets": {
      "Venus": {
        "sign": "Libra",
        "status": "own_sign"
      }
    }
  },
  "dasha": {
    "current_maha_dasha": "Saturn",
    "current_antar_dasha": "Mercury",
    "start_date": "2023-09-01",
    "end_date": "2026-07-01"
  }
}
```

---

## PDF星盘读取注意事项

### 1. PDF质量要求
- ✅ 清晰可读，无模糊或遮挡
- ✅ 完整的星盘数据（至少包含D1本命盘）
- ✅ 行星度数精确到小数点后两位
- ❌ 不支持手写或扫描质量差的PDF

### 2. 语言支持
- ✅ 英文PDF（推荐）
- ✅ 中文PDF（支持）
- ✅ 梵文术语（支持）

### 3. 页数要求
- ✅ 最少1页（仅D1本命盘）
- ✅ 推荐11页以上（包含D1、D9、D10、Dasha周期等）
- ✅ 支持多页PDF（D1-D60分盘）

### 4. 数据完整性
- ✅ 必须包含：出生时间、地点、上升星座、行星位置
- ✅ 推荐包含：D9 Navamsa盘、Dasha周期
- ⭐ 最佳包含：D1-D60分盘、Shadbala、Ashtakavarga

---

## 常见问题

### Q1：PDF星盘读取失败怎么办？
**A**：可能原因：
1. PDF格式不支持（非印度占星格式）
2. PDF质量差（模糊、遮挡）
3. 缺少关键信息（出生时间、地点）

**解决方法**：
- 使用Jagannatha Hora重新生成PDF
- 确保PDF清晰可读
- 手动提供关键信息

### Q2：读取的行星度数不准确怎么办？
**A**：可能原因：
1. PDF中的度数显示格式不标准
2. AI识别错误

**解决方法**：
- 使用Jagannatha Hora标准格式
- 手动提供行星度数表

### Q3：可以读取扫描的纸质星盘吗？
**A**：不支持。扫描的纸质星盘质量通常较差，建议使用占星软件重新生成PDF。

### Q4：可以读取图片格式的星盘吗？
**A**：支持。如果图片清晰，AI可以读取图片格式的星盘（PNG、JPG等）。

---

## 使用示例

### 示例1：读取Jagannatha Hora生成的PDF

**用户操作**：
1. 使用Jagannatha Hora生成星盘报告（File → Print → Save as PDF）
2. 上传PDF文件
3. 说："请帮我分析这个印度占星星盘"

**AI响应**：
```
我已读取PDF星盘报告，提取到以下信息：

【基本信息】
- 出生时间：1993年4月17日 14:45
- 出生地点：邯郸（经度115.5°E，纬度36.6°N）
- 性别：男

【D1本命盘】
- 上升：狮子座 12°38'（Magha Nakshatra 4 Pada）
- 关键行星配置：
  - 金星：双鱼座 10°33'（入庙）
  - 土星：水瓶座 4°18'（入庙，在7宫）
  - 火星：巨蟹座 1°19'（落陷，在12宫）
  - 木星：处女座 13°49'（落陷）
  - 水星：双鱼座 8°32'（落陷，但Neechabhanga Yoga）

【D9 Navamsa盘】
- 上升：天蝎座
- 金星：天秤座（入庙）

【当前Dasha周期】
- 主运：Saturn（2020-2039）
- 小运：Mercury（2023.09-2026.07）

现在开始详细分析...
```

---

## 技术实现

### PDF读取技术
- 使用PDF解析工具提取文本内容
- 使用正则表达式匹配关键信息
- 使用NLP技术理解上下文

### 数据提取算法
1. **出生信息提取**：匹配"Birth Details"、"Date"、"Time"、"Place"等关键词
2. **行星位置提取**：匹配行星名称（Sun、Moon、Mars等）+ 度数 + 星座
3. **宫位信息提取**：匹配"House 1"、"House 2"等 + 宫内星
4. **Nakshatra提取**：匹配Nakshatra名称 + Pada
5. **Dasha周期提取**：匹配"Maha Dasha"、"Antar Dasha"等 + 时间范围

---

**版本**：1.0.0
**创建日期**：2026-04-20
**最后更新**：2026-04-20
