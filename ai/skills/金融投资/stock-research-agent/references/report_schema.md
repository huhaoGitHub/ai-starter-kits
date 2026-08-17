# JSON 数据结构 Schema + AI 分析指南

## 顶层结构

```json
{
  "meta": { ... },
  "section1_basic": { ... },
  "section2_sector_flow": { ... },
  "section3_stock_flow": { ... },
  "section4_technical": { ... },
  "section5_volume_price": { ... },
  "section6_ai_inference": { ... },
  "section7_dragon_tiger": { ... },
  "section8_news_sentiment": { ... },
  "section9_market_env": { ... },
  "section10_strategy": { ... },
  "section11_risks": [ ... ],
  "section12_ai_summary": { ... },
  "charts": { ... }
}
```

## meta - 报告元数据

```json
{
  "stock_code": "sh600519",
  "stock_name": "贵州茅台",
  "market": "A",
  "market_label": "A股",
  "report_date": "2026-08-07",
  "currency": "CNY",
  "currency_symbol": "¥"
}
```

- `market`: "A" | "HK" | "US"
- `currency`: "CNY" | "HKD" | "USD"

## section1_basic - 股票基础信息

```json
{
  "name": "贵州茅台",
  "code": "sh600519",
  "industry": "白酒",
  "concepts": ["消费升级", "机构重仓"],
  "price": 1689.50,
  "change_pct": 2.35,
  "prev_close": 1650.80,
  "open": 1655.00,
  "high": 1698.00,
  "low": 1652.00,
  "volume": 2500000,
  "amount": 4200000000,
  "turnover_rate": 0.20,
  "volume_ratio": 1.85,
  "pe_ttm": 28.5,
  "pe_fwd": 25.3,
  "pb": 9.8,
  "total_market_cap": 2120000000000,
  "circulating_market_cap": 2120000000000,
  "total_shares": 1256000000,
  "high_52week": 1800.00,
  "low_52week": 1500.00,
  "dividend_yield_ttm": 1.2
}
```

**字段说明**:
- `volume`: 成交量(手)
- `amount`: 成交额(元)
- `turnover_rate`: 换手率(%)
- `volume_ratio`: 量比
- `pe_ttm`: 市盈率TTM
- `pe_fwd`: 预期市盈率
- `pb`: 市净率
- `total_market_cap`: 总市值(元)
- `circulating_market_cap`: 流通市值(元)

**市场差异**:
- A 股: 所有字段可用
- 港股: 货币=HKD，可能有 `lot` 字段(每手股数)
- 美股: 货币=USD，可能有 `pre_market_price`/`post_market_price`

## section2_sector_flow - 行业/板块资金流

```json
{
  "available": true,
  "sector_name": "白酒",
  "sector_code": "pt01801081",
  "main_net_flow": 500000000,
  "jumbo_net_flow": 300000000,
  "block_net_flow": 200000000,
  "advancing_count": 15,
  "declining_count": 3,
  "week_cumulative": 1200000000,
  "ranking": 5,
  "total_sectors": 30,
  "sector_change_pct": 1.85
}
```

- `available`: false 时(港股/美股)，模板显示"不适用"
- `main_net_flow`: 主力净流入(元)
- `jumbo_net_flow`: 超大单净流入(元)
- `block_net_flow`: 大单净流入(元)

## section3_stock_flow - 个股资金流向

```json
{
  "available": true,
  "today": {
    "main_net": 150000000,
    "jumbo_net": 80000000,
    "block_net": 70000000,
    "mid_net": -30000000,
    "small_net": -120000000,
    "main_inflow": 200000000,
    "main_outflow": 50000000
  },
  "trend_5d": [
    {"date": "2026-08-01", "main_net": 80000000},
    {"date": "2026-08-04", "main_net": -20000000},
    {"date": "2026-08-05", "main_net": 100000000},
    {"date": "2026-08-06", "main_net": 50000000},
    {"date": "2026-08-07", "main_net": 150000000}
  ],
  "trend_rating": "连续净流入",
  "main_inflow_rank": 15,
  "main_inflow_circ_rate": 0.07,
  "main_inflow_industry_rank": 2
}
```

- `trend_rating`: "连续净流入" | "连续净流出" | "流入流出交替" 等
- `main_inflow_circ_rate`: 主力净流入占流通市值比例
- 美股时 `available: false`，用卖空数据替代

## section4_technical - 技术面

```json
{
  "available": true,
  "ma": {"MA5": 1680.0, "MA10": 1670.0, "MA20": 1650.0, "MA60": 1600.0},
  "macd": {"DIF": 5.2, "DEA": 4.1, "MACD": 1.1},
  "kdj": {"K": 75.3, "D": 68.5, "J": 88.9},
  "rsi": {"RSI6": 72.5, "RSI12": 65.3, "RSI24": 58.0},
  "boll": {"UP": 1720.0, "MID": 1680.0, "LOW": 1640.0},
  "signals": [
    {"indicator": "MACD", "signal": "金叉", "direction": "看多"},
    {"indicator": "KDJ", "signal": "J值偏高", "direction": "注意回调"},
    {"indicator": "RSI", "signal": "偏强", "direction": "中性偏多"},
    {"indicator": "MA", "signal": "多头排列", "direction": "看多"}
  ]
}
```

**信号判断规则**:
- MACD: DIF > DEA = 金叉(看多)；DIF < DEA = 死叉(看空)
- KDJ: J > 90 = 超买(注意回调)；J < 10 = 超卖(关注反弹)
- RSI: RSI6 > 80 = 超买；RSI6 < 20 = 超卖；50 附近 = 中性
- MA: 价格 > MA5 > MA10 > MA20 = 多头排列(看多)；反之空头排列

## section5_volume_price - 量价关系

```json
{
  "available": true,
  "today_volume": 2500000,
  "yesterday_volume": 1350000,
  "volume_ratio": 1.85,
  "volume_change_pct": 85.2,
  "avg_20d_volume": 1200000,
  "judgment": "显著放量",
  "anomaly": "今日成交量较20日均值放大85%，量价配合良好",
  "price_change_pct": 2.35
}
```

**判断规则**:
- 量比 > 2.0: 显著放量
- 量比 1.5-2.0: 温和放量
- 量比 0.8-1.5: 正常
- 量比 < 0.8: 缩量
- 上涨 + 放量 = 健康(资金参与度提升)
- 上涨 + 缩量 = 谨防诱多
- 下跌 + 放量 = 资金出逃
- 下跌 + 缩量 = 抛压减轻

## section6_ai_inference - 主力资金行为分析 (AI)

```json
{
  "behavior": "主力净流入",
  "behavior_label": "主力资金呈净流入态势",
  "reasoning": "今日主力净流入1.5亿元，超大单净流入0.8亿元，连续5日中4日净流入。成交量放大约85%，换手率0.2%处于正常水平。量价齐升，主力资金行为偏积极，短期有继续走强可能。",
  "confidence": "medium",
  "key_signals": [
    "主力连续净流入",
    "超大单占比高",
    "量价齐升",
    "换手率正常"
  ]
}
```

**AI 分析要点**:
- 综合资金净流入方向 + 超大单占比 + 量价关系 + 换手率
- 判断行为类型: 吸筹 / 出逃 / 震荡洗盘 / 拉升 / 观望
- `confidence`: "high" | "medium" | "low"

## section7_dragon_tiger - 龙虎榜/机构行为

```json
{
  "available": true,
  "on_list": false,
  "note": "今日未上龙虎榜",
  "buy_seats": [],
  "sell_seats": [],
  "institutional_net": null,
  "hot_money_seats": []
}
```

**若上榜**:
```json
{
  "available": true,
  "on_list": true,
  "note": "今日上龙虎榜",
  "buy_seats": [
    {"name": "机构专用", "amount": 250000000, "type": "institution"},
    {"name": "东方财富证券拉萨团结路", "amount": 80000000, "type": "hotmoney"}
  ],
  "sell_seats": [
    {"name": "机构专用", "amount": 100000000, "type": "institution"}
  ],
  "institutional_net": 150000000,
  "hot_money_seats": ["东方财富证券拉萨团结路"]
}
```

- `available`: false 时(港股/美股)显示"不适用"
- `on_list`: 是否上榜
- `institutional_net`: 机构净买入额(元)

## section8_news_sentiment - 新闻舆情

```json
{
  "available": true,
  "news_list": [
    {"title": "茅台三季报业绩超预期", "source": "证券时报", "time": "2026-08-06 15:30", "sentiment": "positive", "summary": "公司三季度营收同比增长15%..."},
    {"title": "白酒行业面临消费降级压力", "source": "经济观察报", "time": "2026-08-05 10:00", "sentiment": "negative", "summary": "高端白酒消费需求..."}
  ],
  "positive_count": 5,
  "negative_count": 1,
  "neutral_count": 4,
  "ai_summary": "近期新闻以正面为主，主要利好因素包括三季报业绩超预期、白酒板块资金持续流入。利空因素主要为行业消费降级担忧。整体情绪偏正面。"
}
```

**AI 分析要点**:
- 将每条新闻分类为 positive / negative / neutral
- 统计占比
- 生成摘要，突出主要利好/利空因素
- 给出整体情绪判断: 偏正面 / 偏负面 / 中性

## section9_market_env - 市场环境

```json
{
  "available": true,
  "index_data": {
    "sh000001": {"name": "上证指数", "price": 3200.0, "change_pct": 0.85},
    "sz399001": {"name": "深证成指", "price": 10500.0, "change_pct": 1.20}
  },
  "limit_up_count": 45,
  "limit_down_count": 5,
  "advancing_count": 2800,
  "declining_count": 1500,
  "total_turnover": 85000000000,
  "north_bound_net": 5000000000,
  "market_sentiment": "偏强",
  "risk_appetite": "较高"
}
```

**市场情绪判断规则**:
- 涨停 > 50 且 跌停 < 10: 强势
- 涨停 20-50 且 上涨 > 下跌: 偏强
- 涨跌各半: 震荡
- 跌停 > 20 且 下跌 > 上涨: 偏弱
- 跌停 > 50: 弱势

**港股/美股**: `available: false`，仅展示对应市场指数行情

## section10_strategy - 短线策略

```json
{
  "overall_score": 75,
  "trend_stars": 4,
  "capital_stars": 4,
  "technical_stars": 3,
  "sentiment_stars": 4,
  "support_levels": [1650.0, 1620.0, 1600.0],
  "resistance_levels": [1700.0, 1720.0, 1800.0],
  "scenarios": {
    "strong": {
      "condition": "放量突破1700",
      "target": "1750-1800",
      "stop_loss": 1650,
      "probability": "30%"
    },
    "normal": {
      "condition": "1650-1700震荡",
      "target": "1680-1720",
      "stop_loss": 1620,
      "probability": "50%"
    },
    "weak": {
      "condition": "跌破1650",
      "target": "1600-1620",
      "stop_loss": 1580,
      "probability": "20%"
    }
  }
}
```

**评分规则**:
- `overall_score`: 0-100，综合趋势/资金/技术/情绪
- `trend_stars`: 1-5，基于 MA 排列 + MACD 方向
- `capital_stars`: 1-5，基于主力净流入 + 5日趋势
- `technical_stars`: 1-5，基于 KDJ + RSI + BOLL
- `sentiment_stars`: 1-5，基于新闻情绪 + 市场环境

**支撑/压力位**:
- 支撑: 近期低点、MA20、MA60、整数关口
- 压力: 近期高点、前高、整数关口、BOLL 上轨

## section11_risks - 风险提示

```json
[
  {"type": "估值风险", "level": "medium", "description": "PE(TTM) 28.5倍，高于行业均值"},
  {"type": "资金风险", "level": "low", "description": "近期主力资金呈净流入"},
  {"type": "技术风险", "level": "medium", "description": "RSI6=72.5，接近超买区域"},
  {"type": "市场风险", "level": "low", "description": "大盘情绪偏强"},
  {"type": "事件风险", "level": "low", "description": "近期无质押/解禁/ST等风险事件"}
]
```

**风险检查清单**:
- 估值风险: PE/PB 高于行业均值？
- 资金风险: 主力资金是否持续流出？
- 技术风险: RSI 超买？KDJ 高位？
- 市场风险: 大盘是否弱势？
- 事件风险(A股): 质押/解禁/ST/退市预警？
- `level`: "high" | "medium" | "low"

## section12_ai_summary - AI 最终总结

```json
{
  "overall_judgment": "短线偏多",
  "judgment_detail": "综合技术面多头排列、资金面连续净流入、量价齐升等因素，短线偏多看待。但需注意RSI偏高带来的短期回调压力。",
  "advantages": [
    "MACD金叉，技术面偏多",
    "主力资金连续净流入",
    "量价配合良好"
  ],
  "risks": [
    "RSI偏高，短期有回调压力",
    "估值偏高"
  ],
  "short_term_view": "偏多，建议关注1700压力位突破情况",
  "watch_points": [
    "1700压力位能否有效突破",
    "主力资金流入是否持续",
    "大盘环境是否配合"
  ]
}
```

**AI 总结要点**:
- `overall_judgment`: "短线偏多" | "短线偏空" | "短线中性" | "短线观望"
- 综合所有章节给出判断
- 列出 2-4 个优势和风险
- 给出明确短线观点和关注点

## charts - 图表数据

```json
{
  "kline_data": [
    {"date": "2026-05-08", "open": 1600, "close": 1620, "high": 1630, "low": 1590, "volume": 1200000}
  ],
  "volume_data": [
    {"date": "2026-05-08", "volume": 1200000, "is_up": true}
  ],
  "capital_flow_data": [
    {"category": "主力", "net_flow": 150000000},
    {"category": "超大单", "net_flow": 80000000},
    {"category": "大单", "net_flow": 70000000},
    {"category": "中单", "net_flow": -30000000},
    {"category": "小单", "net_flow": -120000000}
  ],
  "macd_data": {
    "dates": ["2026-07-01", "2026-07-02"],
    "dif": [3.5, 3.8],
    "dea": [2.8, 3.0],
    "macd": [0.7, 0.8]
  },
  "rsi_data": {
    "dates": ["2026-07-01", "2026-07-02"],
    "rsi6": [65.0, 68.0],
    "rsi12": [60.0, 62.0]
  },
  "ma_data": {
    "dates": ["2026-07-01", "2026-07-02"],
    "ma5": [1670.0, 1675.0],
    "ma10": [1660.0, 1662.0],
    "ma20": [1640.0, 1642.0],
    "ma60": [1600.0, 1601.0]
  }
}
```

**数据来源**:
- `kline_data` / `volume_data`: `kline <code> --period day --limit 60`
- `capital_flow_data`: `fund flow <code>`
- `macd_data` / `rsi_data`: `technical <code> --group macd,rsi --start <30d_ago> --end <today>`
- `ma_data`: `technical <code> --group ma --start <60d_ago> --end <today>` 或从 K 线数据计算

**注意事项**:
- 所有金额单位为元(A股)/港元(港股)/美元(美股)
- `kline_data` 至少需要 20 条记录才能绘制有意义图表
- `macd_data` / `rsi_data` 至少需要 15 条记录
- 美股无 `capital_flow_data`，模板跳过该图表
