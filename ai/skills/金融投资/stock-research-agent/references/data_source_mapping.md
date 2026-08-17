# 数据源映射：报告章节 -> westock-data 命令

## westock-data 命令语法速查

所有命令前缀为 `westock-data`，全局参数 `--raw` 输出 JSON 格式。

| 命令 | 精确语法 | 关键参数 | 备注 |
|------|---------|---------|------|
| 行情 | `quote <code>` | `--date YYYY-MM-DD`; `--raw` | 位置参数，支持批量逗号分隔 |
| 搜索 | `search <name>` | `--type etf\|sector\|index\|bond\|futures\|forex` | 位置参数。`--type sector` 搜板块 |
| K线 | `kline <code> --period day --limit 60` | `--period day\|week\|month\|season\|year`; `--limit N`; `--start/--end`; `--fq qfq\|hfq\|bfq` | period 是 `day` 不是 `daily` |
| 技术指标 | `technical <code> --group ma,macd,kdj,rsi,boll` | `--group`(逗号分隔): ma/macd/kdj/rsi/boll/bias/wr/dmi/all; `--start/--end`(历史区间) | 支持历史技术数据 |
| 个股资金流 | `fund flow <code>` | `--start YYYY-MM-DD`; `--end YYYY-MM-DD` | **带空格** `fund flow`。5日趋势用区间查询 |
| 板块资金流 | `fund flow <sector_code>` | 同个股 | 板块代码 pt 开头 |
| 板块排名 | `sector ranking` | 无额外参数 | 子命令形式。返回行业涨幅Top10+概念Top10+资金流入Top5+北向热门 |
| 板块信息 | `sector info <code>` | 支持批量逗号分隔 | 子命令形式 |
| 龙虎榜 | `lhb --type institution,hotmoney` | `--type`(逗号分隔); `--date YYYY-MM-DD` | **全市场**查询，仅A股。需在结果中过滤目标股票 |
| 市场总览 | `market-overview --type all` | `--type summary\|trade\|interval\|technical\|updown\|margin\|valuation\|rotation\|all`; `--date` | 不带 --type 默认 summary |
| 涨跌分布 | `changedist` | `--raw` | 沪深A股全市场截面，含11档涨跌幅区间 |
| 新闻 | `news article <code> --limit 20` | `--limit N` | **两个词** `news article` |
| 风险事件 | `risk <code>` | `--types pledge,unlock`(逗号分隔过滤); 支持批量 | 仅A股(sh/sz/bj)。8种风险类型 |
| 事件标签 | `events tags <code>` | `--types 23,24`(按事件ID过滤); 支持批量 | **两个词** `events tags`。42类事件 |
| 融资融券 | `fund margin <code>` | 无额外参数 | **两个词** `fund margin`。仅沪深 |
| 卖空数据 | `fund short <code>` | `--start`; `--end` | **两个词** `fund short`。港股和美股 |
| 机构评级 | `rating <code>` | 无额外参数 | 港股/美股。A股用 `score <code>` |
| 公司简况 | `profile <code>` | 支持批量逗号分隔 | 位置参数 |
| 连接标的 | `connect --exchange sh` | `--exchange sh\|sz` | 沪深港通标的池 |
| 评分(A股) | `score <code>` | 无额外参数 | A股综合评分 |

## 报告章节 -> 命令映射表

### 第 1 节：股票基础信息概览

| 数据项 | 命令 | A 股 | 港股 | 美股 |
|--------|------|------|------|------|
| 名称/代码/行业/概念 | `profile <code> --raw` | 全字段 | 全字段 | 全字段 |
| 实时行情(价格/涨跌/量额/换手/PE/PB) | `quote <code> --raw` | 全字段 | 全字段(HKD) | 全字段(USD,含盘前盘后) |
| 搜索(若用户给名称) | `search <name>` | 可用 | 可用 | 可用 |

### 第 2 节：所属行业/板块资金流分析

| 数据项 | 命令 | A 股 | 港股 | 美股 |
|--------|------|------|------|------|
| 板块代码 | `search <industry> --type sector` | 可用 | 不适用 | 不适用 |
| 板块资金流 | `fund flow <sector_code> --raw` | 主力/超大单/大单净流入 | 不适用 | 不适用 |
| 板块排名 | `sector ranking --raw` | 涨幅Top10+资金流入Top5 | 不适用 | 不适用 |
| 板块信息 | `sector info <sector_code> --raw` | 基础信息+区间交易 | 不适用 | 不适用 |

### 第 3 节：个股资金流向分析

| 数据项 | 命令 | A 股 | 港股 | 美股 |
|--------|------|------|------|------|
| 今日资金流 | `fund flow <code> --raw` | 主力/超大单/大单/中单/小单 | MainNetFlow/RetailNetFlow | 不适用 |
| 5日趋势 | `fund flow <code> --start <5d_ago> --end <today> --raw` | 区间每日数据 | 区间数据 | 不适用 |
| 卖空数据(美股替代) | `fund short <code> --raw` | 不适用 | 不适用 | 卖空比率/股数/回补天数 |

### 第 4 节：技术面短线趋势分析

| 数据项 | 命令 | A 股 | 港股 | 美股 |
|--------|------|------|------|------|
| 技术指标(截面) | `technical <code> --group ma,macd,kdj,rsi,boll --raw` | 完整 | 完整 | 完整 |
| 技术指标(历史) | `technical <code> --group macd,rsi --start <30d_ago> --end <today> --raw` | MACD+RSI历史 | 同 | 同 |

### 第 5 节：量价关系分析

| 数据项 | 命令 | A 股 | 港股 | 美股 |
|--------|------|------|------|------|
| K线(20日) | `kline <code> --period day --limit 20 --raw` | OHLCV | OHLCV | OHLCV |
| 今日量比 | `quote <code> --raw`(volumeRatio字段) | 可用 | 可用 | 可用 |

### 第 6 节：主力资金行为分析 (AI 推理)

无命令调用，AI 基于第 2+3+5 节数据推理。

### 第 7 节：龙虎榜/机构行为分析

| 数据项 | 命令 | A 股 | 港股 | 美股 |
|--------|------|------|------|------|
| 龙虎榜 | `lhb --type institution,hotmoney --raw` | 全市场查询后过滤目标股票 | 不适用 | 不适用 |

**龙虎榜查询流程**：
1. 运行 `lhb --type institution,hotmoney --raw` 获取全市场龙虎榜
2. 在返回结果中搜索目标股票代码
3. 若上榜：提取买卖席位信息(营业部/机构/金额)
4. 若未上榜：标注"今日未上龙虎榜"

### 第 8 节：新闻舆情分析

| 数据项 | 命令 | A 股 | 港股 | 美股 |
|--------|------|------|------|------|
| 公司新闻 | `news article <code> --limit 20 --raw` | 完整 | 完整 | 完整 |

### 第 9 节：市场环境分析

| 数据项 | 命令 | A 股 | 港股 | 美股 |
|--------|------|------|------|------|
| 大盘画像 | `market-overview --type summary --raw` | 14维度(含北向/两融/估值) | 不适用 | 不适用 |
| 涨跌停/红绿盘 | `market-overview --type updown --raw` | 涨停/跌停/上涨/下跌家数 | 不适用 | 不适用 |
| 涨跌分布 | `changedist --raw` | 11档涨跌幅区间分布 | 不适用 | 不适用 |
| 大盘指数(替代) | `quote <index_code> --raw` | sh000001,sz399001 | hkHSI | us.IXIC,us.INX |

### 第 10 节：短线交易策略建议 (AI 综合评分)

无命令调用，AI 综合所有章节数据评分。

### 第 11 节：风险提示

| 数据项 | 命令 | A 股 | 港股 | 美股 |
|--------|------|------|------|------|
| 风险事件 | `risk <code> --raw` | 8类(质押/解禁/ST等) | 不适用 | 不适用 |
| 事件标签 | `events tags <code> --raw` | 42类事件标签 | 不适用 | 不适用 |
| 融资融券 | `fund margin <code> --raw` | 融资余额/融券余量 | 不适用 | 不适用 |
| AI 推理(替代) | 基于估值/涨跌幅/资金流推理 | -- | AI 分析 | AI 分析 |

### 第 12 节：AI 最终总结

无命令调用，AI 综合所有章节生成总结。

### 图表数据

| 图表 | 命令 | 数据字段 |
|------|------|---------|
| K线图 | `kline <code> --period day --limit 60 --raw` | date/open/close/high/low/volume |
| 成交量图 | 同上(复用 K 线数据) | date/volume/is_up |
| 资金流柱状图 | `fund flow <code> --raw` | category/net_flow |
| MACD 图 | `technical <code> --group macd --start <30d_ago> --end <today> --raw` | dates/dif/dea/macd |
| RSI 图 | `technical <code> --group rsi --start <30d_ago> --end <today> --raw` | dates/rsi6/rsi12 |
| MA 叠加 | 从 K 线数据计算或 `technical <code> --group ma --start <60d_ago> --end <today> --raw` | dates/ma5/ma10/ma20/ma60 |

## 市场差异化字段速查

| 字段 | A 股 | 港股 | 美股 |
|------|------|------|------|
| 货币 | CNY（元） | HKD（港元） | USD（美元） |
| 涨跌停价 | `price_ceiling`/`price_floor` | 无 | 无 |
| 内外盘 | `inner_volume`/`outer_volume` | 无 | 无 |
| 盘前盘后 | 无 | 无 | `pre_market_price`/`post_market_price` |
| 每手股数 | 100股固定 | `lot` 字段 | 无 |
| 机构评级 | `score <code>` | `rating <code>` | `rating <code>` |
| 资金流向 | `fund flow` | `fund flow`(部分字段) | `fund short`(替代) |
| 龙虎榜 | `lhb` | 不适用 | 不适用 |
| 融资融券 | `fund margin` | 不适用 | 不适用 |
| 风险事件 | `risk` + `events tags` | 不适用 | 不适用 |
| 市场总览 | `market-overview` | 不适用 | 不适用 |

## 10 个关键易错点

1. **`fund flow` 带空格**（两个词），不是 `fundflow`
2. **`news article` 带空格**，不是 `news <code>`
3. **`events tags` 带空格**，不是 `events <code>`
4. **`fund margin` / `fund short`** 带空格
5. **`sector ranking` / `sector info`** 是子命令形式，不是 `--ranking` / `--info` flag
6. **`--period day`** 不是 `daily`
7. **`--raw` 是全局参数**，所有命令都支持
8. **代码/关键词是位置参数**，不是 `--code` / `--keyword`
9. **北向资金无独立命令**，分散在 `connect`、`fund flow`、`sector ranking`、`market-overview --type summary` 中
10. **龙虎榜是全市场查询**，不是按个股查
