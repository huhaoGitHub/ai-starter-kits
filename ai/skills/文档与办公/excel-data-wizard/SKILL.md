---
name: excel-data-wizard
description: "Excel数据处理神器。读取、分析、合并、拆分、格式化Excel/CSV文件，支持批量操作、数据透视、公式计算、图表生成、多表合并、条件筛选、去重、格式转换。当用户需要处理Excel/CSV数据、做数据分析、合并多个表格、筛选特定数据、生成数据报表时触发。"
---

# Excel Data Wizard

Excel/CSV数据处理全能工具，覆盖办公场景中最常见的Excel操作需求。

## 核心能力

1. **读取与解析** - 读取 .xlsx/.xls/.csv 文件，自动检测编码和分隔符
2. **数据清洗** - 去重、空值处理、格式标准化、异常值检测
3. **数据筛选** - 条件过滤、正则匹配、多列联合筛选
4. **数据合并** - 多文件纵向合并(vconcat)、多表横向拼接(hconcat)、VLOOKUP式关联
5. **数据透视** - 分组聚合、交叉表、多维统计
6. **公式计算** - 新增列计算、条件求和/计数、排名、占比
7. **格式输出** - 导出为 xlsx(带格式)/csv/json/Markdown表格
8. **图表生成** - 柱状图、折线图、饼图、散点图，输出为图片

## 快速开始

### 读取文件

```python
python3 scripts/excel_ops.py read input.xlsx --sheet Sheet1 --limit 20
```

### 数据清洗

```python
python3 scripts/excel_ops.py clean input.xlsx --dedup --fill-na 0 --strip-whitespace -o cleaned.xlsx
```

### 多文件合并

```python
python3 scripts/excel_ops.py merge file1.xlsx file2.xlsx file3.xlsx --mode vconcat -o merged.xlsx
```

### 条件筛选

```python
python3 scripts/excel_ops.py filter input.xlsx --where "金额>1000" --where "城市=北京" -o filtered.xlsx
```

### 数据透视

```python
python3 scripts/excel_ops.py pivot input.xlsx --group-by 部门 --agg "薪资:mean" --agg "人数:count" -o pivot.xlsx
```

### 生成图表

```python
python3 scripts/excel_ops.py chart input.xlsx --type bar --x 部门 --y 薪资 -o chart.png
```

## 依赖安装

```bash
pip install openpyxl pandas matplotlib
```

## 命令参考

完整命令行参数说明见 [references/cli-reference.md](references/cli-reference.md)

## 常见场景

| 场景 | 命令示例 |
|------|----------|
| 去重导出 | `excel_ops.py clean data.xlsx --dedup -o deduped.xlsx` |
| 多月报表合并 | `excel_ops.py merge jan.xlsx feb.xlsx mar.xlsx -o q1.xlsx` |
| 筛选大额订单 | `excel_ops.py filter orders.xlsx --where "金额>5000" -o big.xlsx` |
| 部门统计 | `excel_ops.py pivot staff.xlsx --group-by 部门 --agg "薪资:mean" -o stat.xlsx` |
| CSV转Excel | `excel_ops.py convert data.csv --to xlsx -o data.xlsx` |
