---
name: stock-analyst
description: "AI 股票短线分析助手。输入股票代码或名称，自动收集行情、资金流向、技术指标、龙虎榜、新闻舆情、市场环境等数据，结合 AI 推理生成含 ECharts 图表的专业 HTML 短线投资分析报告。支持 A 股、港股、美股。触发词：股票分析、短线分析、股票报告、个股分析、分析股票、stock analysis、分析一下、看看这只股票。"
agent_created: true
---

# Stock Analyst - AI 股票短线分析助手

## 概述

输入股票代码/名称，通过 westock-data CLI 收集行情、资金流向、技术指标、龙虎榜、新闻舆情、市场环境等数据，结合 AI 推理生成含 ECharts 图表的专业 HTML 短线投资分析报告。

- **数据源**: westock-data CLI（WorkBuddy 内置 skill）
- **市场覆盖**: A 股 + 港股 + 美股
- **报告输出**: 12 节 HTML 报告（暗色终端主题 + ECharts 图表）
- **分析链路**: 行业 -> 板块 -> 个股 -> 技术 -> 资金 -> 情绪 -> 风险

## 触发条件

用户输入股票代码或名称并要求分析/生成报告。例如：
- "分析一下贵州茅台"
- "600519 短线分析"
- "看看这只股票 hk00700"
- "分析苹果股票"

## 前置条件

- westock-data skill 已连接（数据源）
- Python 3.13+ 可用：`C:\Users\SRNS\.workbuddy\binaries\python\versions\3.13.12\python.exe`
- 当前项目目录有 outputs/ 子目录（不存在则创建）

## westock-data 调用方式

westock-data 不是系统 PATH 中的命令，需用 Node.js 执行其入口脚本：

```bash
NODE="C:/Users/SRNS/.workbuddy/binaries/node/versions/22.22.2/node.exe"
WD="C:/Program Files/WorkBuddy/resources/app.asar.unpacked/resources/builtin-skills/westock-data/scripts/index.js"
"$NODE" "$WD" <command> [params] --raw
```

下文为简洁起见用 `westock-data <command>` 代替完整调用。实际执行时替换为上述 `$NODE "$WD"` 形式。

## 执行流程

### Step 1: 解析股票代码

1. 若用户给名称而非代码：运行 `westock-data search <名称> --raw` 获取代码
2. 从代码前缀判断市场：
   - `sh`/`sz`/`bj` = A 股（CNY）
   - `hk` = 港股（HKD）
   - `us` = 美股（USD）
3. 确定货币单位

### Step 2: 数据采集

加载 `references/data_source_mapping.md` 获取完整命令映射。所有命令加 `--raw` 获取 JSON。

**通用数据（所有市场）**：

```bash
westock-data quote <code> --raw
westock-data kline <code> --period day --limit 60 --raw
westock-data technical <code> --group ma,macd,kdj,rsi,boll --raw
westock-data technical <code> --group macd,rsi --start <30d_ago> --end <today> --raw
westock-data profile <code> --raw
westock-data news article <code> --limit 20 --raw
```

> **注意**：`news article` 命令在某些渠道可能不可用（返回 `CLI_CMD_UNAVAILABLE`）。此时改用 WebSearch 搜索"<股票名称> <股票代码> 最新消息"获取新闻舆情数据，手动分类为利好/利空/中性。

**A 股专用数据**：

```bash
westock-data fund flow <code> --raw
westock-data fund flow <code> --start <5d_ago> --end <today> --raw
westock-data search <industry> --type sector --raw
westock-data fund flow <sector_code> --raw
westock-data sector info <sector_code> --raw
westock-data sector ranking --raw
westock-data lhb --type institution,hotmoney --raw
westock-data market-overview --type summary --raw
westock-data market-overview --type updown --raw
westock-data changedist --raw
westock-data quote sh000001,sz399001 --raw
westock-data risk <code> --raw
westock-data events tags <code> --raw
westock-data fund margin <code> --raw
```

**港股数据**：

```bash
westock-data fund flow hk<code> --raw
westock-data fund short hk<code> --raw
westock-data quote hkHSI --raw
westock-data rating hk<code> --raw
```

**美股数据**：

```bash
westock-data fund short us<code> --raw
westock-data quote us.IXIC,us.INX --raw
westock-data rating us<code> --raw
```

**关键命令语法注意**（详见 references/data_source_mapping.md）：
- `fund flow`（带空格，不是 fundflow）
- `news article`（两个词，不是 news <code>）
- `events tags`（两个词）
- `fund margin` / `fund short`（带空格）
- `--period day`（不是 daily）
- `lhb` 是全市场查询，需在结果中过滤目标股票

### Step 3: AI 推理分析

基于采集的数据，完成以下章节的 AI 分析：

| 章节 | 分析要点 |
|------|---------|
| 第 6 节 主力行为 | 综合资金净流入方向 + 超大单占比 + 量价关系 + 换手率，判断吸筹/出逃/洗盘/拉升 |
| 第 8 节 舆情分析 | 将新闻逐条分类为利好/利空/中性，统计占比，生成摘要 |
| 第 10 节 策略 | 综合趋势/资金/技术/情绪各给 1-5 星，总分 0-100，给出支撑/压力位和 3 场景 |
| 第 11 节 风险 | 检查估值/资金/技术/市场/事件风险 |
| 第 12 节 总结 | 综合所有章节，给出偏多/偏空/中性判断 |

AI 分析指南详见 `references/report_schema.md`。

### Step 4: 组装 JSON 数据文件

按 `references/report_schema.md` 定义的结构组装 JSON 数据，包含：
- `meta`: 报告元数据（股票代码、名称、市场、日期等）
- `section1` ~ `section12`: 12 节分析数据
- `charts`: 图表数据（K线、成交量、资金流、MACD、RSI、MA）

保存到 `outputs/stock_data_<code>_<date>.json`。

**市场差异化处理**：
- A 股：全部 12 节均可采集
- 港股：第 2 节(板块资金流)、第 7 节(龙虎榜)、第 9 节(市场总览)的 `available` 设为 false
- 美股：第 2 节、第 7 节 `available` 设为 false；第 3 节用卖空数据替代

### Step 5: 生成 HTML 报告

```bash
"C:\Users\SRNS\.workbuddy\binaries\python\versions\3.13.12\python.exe" \
  "<skill_dir>/scripts/generate_report.py" \
  --data "outputs/stock_data_<code>_<date>.json" \
  --output "outputs/stock_report_<code>_<date>.html" \
  --template "<skill_dir>/assets/report_template.html"
```

其中 `<skill_dir>` = `C:\Users\SRNS\.workbuddy\skills\stock-analyst`。

### Step 6: 呈现报告

使用 `present_files` 工具呈现生成的 HTML 报告文件。

## 数据源映射速查

| 章节 | westock-data 命令 | A 股 | 港股 | 美股 |
|------|------------------|------|------|------|
| 1. 基础信息 | `quote` + `profile` | 全字段 | 全字段 | 全字段 |
| 2. 板块资金流 | `search --type sector` + `fund flow <sector>` + `sector ranking` | 完整 | 不适用 | 不适用 |
| 3. 个股资金流 | `fund flow <code>` | 完整 | 部分 | 用 `fund short` 替代 |
| 4. 技术面 | `technical --group ma,macd,kdj,rsi,boll` | 完整 | 完整 | 完整 |
| 5. 量价关系 | `kline --period day --limit 20` + `quote` | 完整 | 完整 | 完整 |
| 6. 主力行为 | AI 推理 | AI | AI | AI |
| 7. 龙虎榜 | `lhb --type institution,hotmoney` | 仅 A 股 | 不适用 | 不适用 |
| 8. 新闻舆情 | `news article <code> --limit 20` | 完整 | 完整 | 完整 |
| 9. 市场环境 | `market-overview` + `changedist` | 完整 | `quote hkHSI` | `quote us.IXIC,us.INX` |
| 10. 策略 | AI 综合评分 | AI | AI | AI |
| 11. 风险 | `risk` + `events tags` + `fund margin` | 完整 | AI 推理 | AI 推理 |
| 12. 总结 | AI 综合 | AI | AI | AI |

完整映射详见 `references/data_source_mapping.md`。

## 脚本说明

- `scripts/generate_report.py`：JSON -> HTML 生成器
  - 参数：`--data <json> --output <html> --template <html_template>`
  - 逻辑：读取 JSON + 模板，替换 `__DATA_JSON__` 占位符，输出 HTML
  - 依赖：仅 Python 标准库
  - 容错：缺失章节时输出警告但不中断

## 参考文档

- `references/data_source_mapping.md`：12 节 -> westock-data 命令完整映射 + 市场差异 + 易错点
- `references/report_schema.md`：JSON 数据结构定义 + AI 分析指南 + 图表数据格式

## 报告结构（12 节）

1. **股票基础信息概览** - 名称/代码/行业/概念/市值/价格/涨跌/换手/PE/PB
2. **所属行业/板块资金流分析** - 板块主力净流入/超大单/大单/涨跌家数/排名
3. **个股资金流向分析** - 主力/超大单/大单/中单/小单 + 5 日趋势 + 图表
4. **技术面短线趋势分析** - MA/MACD/KDJ/RSI/BOLL + 买卖信号 + MACD/RSI 图表
5. **量价关系分析** - 成交量/量比/放量缩量判断 + K 线/成交量图表
6. **主力资金行为分析** - AI 推理：吸筹/出逃/洗盘/拉升
7. **龙虎榜/机构行为分析** - 买卖席位/机构净买入/游资参与（仅 A 股）
8. **新闻舆情分析** - 利好/利空分类 + AI 情绪摘要
9. **市场环境分析** - 大盘指数/涨停跌停/北向资金/市场情绪
10. **短线交易策略建议** - 综合评分/四维星级/支撑压力位/3 场景
11. **风险提示** - 估值/资金/技术/市场/事件风险
12. **AI 最终总结** - 综合判断/优势/风险/短线观点/关注点
