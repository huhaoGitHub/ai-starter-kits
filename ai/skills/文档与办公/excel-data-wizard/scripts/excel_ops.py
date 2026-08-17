#!/usr/bin/env python3
"""Excel Data Wizard - Excel/CSV数据处理全能工具"""

import argparse
import sys
import os
import json
import re
from pathlib import Path

def read_file(filepath, sheet=None, limit=None, encoding=None):
    """读取Excel/CSV文件"""
    import pandas as pd
    ext = Path(filepath).suffix.lower()
    if ext == '.csv':
        df = pd.read_csv(filepath, encoding=encoding or 'utf-8')
    elif ext in ('.xlsx', '.xls'):
        df = pd.read_excel(filepath, sheet_name=sheet or 0)
    else:
        print(f"不支持的文件格式: {ext}", file=sys.stderr)
        sys.exit(1)
    if limit:
        df = df.head(limit)
    print(f"文件: {filepath}")
    print(f"行数: {len(df)}, 列数: {len(df.columns)}")
    print(f"列名: {list(df.columns)}")
    print(f"\n数据类型:\n{df.dtypes}")
    print(f"\n前5行:\n{df.head()}")
    return df

def clean_file(filepath, dedup=False, fill_na=None, strip_whitespace=False, drop_na_rows=False, output=None):
    """数据清洗"""
    import pandas as pd
    df = _read_any(filepath)
    before = len(df)
    if dedup:
        df = df.drop_duplicates()
        print(f"去重: {before} -> {len(df)} 行 (移除 {before - len(df)} 行)")
    if strip_whitespace:
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].str.strip()
    if fill_na is not None:
        df = df.fillna(fill_na)
    if drop_na_rows:
        df = df.dropna()
    _save(df, output or _auto_output(filepath, 'cleaned'))

def merge_files(files, mode='vconcat', key=None, output=None):
    """多文件合并"""
    import pandas as pd
    dfs = [_read_any(f) for f in files]
    if mode == 'vconcat':
        result = pd.concat(dfs, ignore_index=True)
    elif mode == 'hconcat':
        result = pd.concat(dfs, axis=1)
    elif mode == 'lookup' and key:
        result = dfs[0]
        for df in dfs[1:]:
            result = result.merge(df, on=key, how='left')
    else:
        print(f"未知合并模式: {mode}", file=sys.stderr)
        sys.exit(1)
    print(f"合并完成: {len(result)} 行, {len(result.columns)} 列")
    _save(result, output or 'merged.xlsx')

def filter_data(filepath, where=None, output=None):
    """条件筛选"""
    import pandas as pd
    df = _read_any(filepath)
    if where:
        for condition in where:
            match = re.match(r'(\S+?)([><=!]+)(\S+)', condition)
            if not match:
                print(f"无法解析条件: {condition}", file=sys.stderr)
                continue
            col, op, val = match.groups()
            try:
                val = float(val)
            except ValueError:
                val = val.strip('"').strip("'")
            if op == '>':
                df = df[df[col] > val]
            elif op == '>=':
                df = df[df[col] >= val]
            elif op == '<':
                df = df[df[col] < val]
            elif op == '<=':
                df = df[df[col] <= val]
            elif op in ('=', '=='):
                df = df[df[col] == val]
            elif op in ('!=', '<>'):
                df = df[df[col] != val]
    print(f"筛选后: {len(df)} 行")
    _save(df, output or _auto_output(filepath, 'filtered'))

def pivot_data(filepath, group_by=None, agg=None, output=None):
    """数据透视"""
    import pandas as pd
    df = _read_any(filepath)
    if not group_by:
        print("需要 --group-by 参数", file=sys.stderr)
        sys.exit(1)
    agg_dict = {}
    if agg:
        for a in agg:
            col, func = a.split(':')
            agg_dict[col] = func
    result = df.groupby(group_by).agg(agg_dict if agg_dict else 'size').reset_index()
    print(f"透视结果: {len(result)} 行")
    _save(result, output or _auto_output(filepath, 'pivot'))

def chart_data(filepath, chart_type='bar', x=None, y=None, output=None):
    """生成图表"""
    import pandas as pd
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    df = _read_any(filepath)
    if not x or not y:
        print("需要 --x 和 --y 参数", file=sys.stderr)
        sys.exit(1)
    fig, ax = plt.subplots(figsize=(10, 6))
    if chart_type == 'bar':
        ax.bar(df[x], df[y])
    elif chart_type == 'line':
        ax.plot(df[x], df[y], marker='o')
    elif chart_type == 'pie':
        ax.pie(df[y], labels=df[x], autopct='%1.1f%%')
    elif chart_type == 'scatter':
        ax.scatter(df[x], df[y])
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    out_path = output or 'chart.png'
    fig.savefig(out_path, dpi=150)
    print(f"图表已保存: {out_path}")

def convert_file(filepath, to='xlsx', output=None):
    """格式转换"""
    import pandas as pd
    df = _read_any(filepath)
    out = output or Path(filepath).stem + f'.{to}'
    if to == 'csv':
        df.to_csv(out, index=False, encoding='utf-8-sig')
    elif to == 'xlsx':
        df.to_excel(out, index=False)
    elif to == 'json':
        df.to_json(out, orient='records', force_ascii=False, indent=2)
    print(f"已转换: {out}")

# --- Helpers ---

def _read_any(filepath):
    import pandas as pd
    ext = Path(filepath).suffix.lower()
    if ext == '.csv':
        return pd.read_csv(filepath, encoding='utf-8')
    elif ext == '.json':
        return pd.read_json(filepath)
    return pd.read_excel(filepath)

def _save(df, output):
    ext = Path(output).suffix.lower()
    if ext == '.csv':
        df.to_csv(output, index=False, encoding='utf-8-sig')
    elif ext == '.json':
        df.to_json(output, orient='records', force_ascii=False, indent=2)
    else:
        df.to_excel(output, index=False)
    print(f"已保存: {output}")

def _auto_output(filepath, suffix):
    p = Path(filepath)
    return str(p.parent / f"{p.stem}_{suffix}.xlsx")

def main():
    parser = argparse.ArgumentParser(description='Excel Data Wizard')
    sub = parser.add_subparsers(dest='command')

    # read
    p = sub.add_parser('read', help='读取文件')
    p.add_argument('file', help='文件路径')
    p.add_argument('--sheet', help='Sheet名')
    p.add_argument('--limit', type=int, help='显示行数')
    p.add_argument('--encoding', help='CSV编码')

    # clean
    p = sub.add_parser('clean', help='数据清洗')
    p.add_argument('file', help='文件路径')
    p.add_argument('--dedup', action='store_true', help='去重')
    p.add_argument('--fill-na', help='填充空值')
    p.add_argument('--strip-whitespace', action='store_true', help='去除空白')
    p.add_argument('--drop-na-rows', action='store_true', help='删除空行')
    p.add_argument('-o', '--output', help='输出路径')

    # merge
    p = sub.add_parser('merge', help='多文件合并')
    p.add_argument('files', nargs='+', help='文件列表')
    p.add_argument('--mode', choices=['vconcat', 'hconcat', 'lookup'], default='vconcat')
    p.add_argument('--key', help='关联键列(lookup模式)')
    p.add_argument('-o', '--output', help='输出路径')

    # filter
    p = sub.add_parser('filter', help='条件筛选')
    p.add_argument('file', help='文件路径')
    p.add_argument('--where', action='append', help='筛选条件(如 "金额>1000")')
    p.add_argument('-o', '--output', help='输出路径')

    # pivot
    p = sub.add_parser('pivot', help='数据透视')
    p.add_argument('file', help='文件路径')
    p.add_argument('--group-by', help='分组列')
    p.add_argument('--agg', action='append', help='聚合(如 "薪资:mean")')
    p.add_argument('-o', '--output', help='输出路径')

    # chart
    p = sub.add_parser('chart', help='生成图表')
    p.add_argument('file', help='文件路径')
    p.add_argument('--type', choices=['bar', 'line', 'pie', 'scatter'], default='bar')
    p.add_argument('--x', help='X轴列')
    p.add_argument('--y', help='Y轴列')
    p.add_argument('-o', '--output', help='输出路径')

    # convert
    p = sub.add_parser('convert', help='格式转换')
    p.add_argument('file', help='文件路径')
    p.add_argument('--to', choices=['xlsx', 'csv', 'json'], default='xlsx')
    p.add_argument('-o', '--output', help='输出路径')

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return
    cmds = {
        'read': lambda: read_file(args.file, args.sheet, args.limit, args.encoding),
        'clean': lambda: clean_file(args.file, args.dedup, args.fill_na, args.strip_whitespace, args.drop_na_rows, args.output),
        'merge': lambda: merge_files(args.files, args.mode, args.key, args.output),
        'filter': lambda: filter_data(args.file, args.where, args.output),
        'pivot': lambda: pivot_data(args.file, args.group_by, args.agg, args.output),
        'chart': lambda: chart_data(args.file, args.type, args.x, args.y, args.output),
        'convert': lambda: convert_file(args.file, args.to, args.output),
    }
    cmds[args.command]()

if __name__ == '__main__':
    main()
