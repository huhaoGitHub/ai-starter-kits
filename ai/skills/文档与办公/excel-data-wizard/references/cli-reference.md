# CLI Reference

## 命令总览

| 命令 | 功能 | 示例 |
|------|------|------|
| `read` | 读取并预览文件 | `excel_ops.py read data.xlsx --limit 10` |
| `clean` | 数据清洗 | `excel_ops.py clean data.xlsx --dedup --fill-na 0` |
| `merge` | 多文件合并 | `excel_ops.py merge *.xlsx --mode vconcat -o all.xlsx` |
| `filter` | 条件筛选 | `excel_ops.py filter data.xlsx --where "金额>1000"` |
| `pivot` | 数据透视 | `excel_ops.py pivot data.xlsx --group-by 部门 --agg "薪资:mean"` |
| `chart` | 生成图表 | `excel_ops.py chart data.xlsx --type bar --x 部门 --y 薪资` |
| `convert` | 格式转换 | `excel_ops.py convert data.csv --to xlsx` |

## 聚合函数

pivot命令支持以下聚合函数:
- `sum` - 求和
- `mean` - 平均值
- `median` - 中位数
- `min` / `max` - 最小/最大值
- `count` - 计数
- `std` - 标准差
- `var` - 方差
- `first` / `last` - 首个/末个值

## 筛选条件语法

`--where "列名运算符值"` 支持的运算符:
- `>`, `>=`, `<`, `<=` - 数值比较
- `=`, `==` - 等于
- `!=`, `<>` - 不等于

示例:
- `--where "金额>1000"` - 金额大于1000
- `--where "城市=北京"` - 城市等于北京
- `--where "年龄>=18"` - 年龄大于等于18
