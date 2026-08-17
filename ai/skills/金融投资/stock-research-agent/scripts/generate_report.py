#!/usr/bin/env python3
"""
Stock Analyst - Report Generator
Reads JSON data + HTML template, outputs final HTML report.

Usage:
    python generate_report.py --data <data.json> --output <report.html> --template <template.html>
"""

import argparse
import json
import sys
from pathlib import Path


REQUIRED_KEYS = [
    "meta",
    "section1_basic",
    "section10_strategy",
    "section12_ai_summary",
    "charts",
]

ALL_SECTIONS = [
    "meta",
    "section1_basic",
    "section2_sector_flow",
    "section3_stock_flow",
    "section4_technical",
    "section5_volume_price",
    "section6_ai_inference",
    "section7_dragon_tiger",
    "section8_news_sentiment",
    "section9_market_env",
    "section10_strategy",
    "section11_risks",
    "section12_ai_summary",
    "charts",
]


def load_json(data_path: str) -> dict:
    """Load JSON data file."""
    path = Path(data_path)
    if not path.exists():
        print(f"ERROR: Data file not found: {data_path}", file=sys.stderr)
        sys.exit(1)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in data file: {e}", file=sys.stderr)
        sys.exit(1)


def load_template(template_path: str) -> str:
    """Load HTML template file."""
    path = Path(template_path)
    if not path.exists():
        print(f"ERROR: Template file not found: {template_path}", file=sys.stderr)
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def validate_data(data: dict) -> list:
    """Validate JSON data structure, return list of warnings."""
    warnings = []
    for key in REQUIRED_KEYS:
        if key not in data:
            warnings.append(f"Missing required key: {key}")
    for key in ALL_SECTIONS:
        if key not in data:
            warnings.append(f"Missing optional section: {key}")
    if "meta" in data:
        meta = data["meta"]
        if "stock_code" not in meta:
            warnings.append("meta.stock_code is missing")
        if "stock_name" not in meta:
            warnings.append("meta.stock_name is missing")
    if "charts" in data:
        charts = data["charts"]
        if "kline_data" not in charts or not charts["kline_data"]:
            warnings.append("charts.kline_data is empty or missing (K-line chart will not render)")
        if "macd_data" not in charts or not charts.get("macd_data", {}).get("dates"):
            warnings.append("charts.macd_data is empty or missing (MACD chart will not render)")
        if "rsi_data" not in charts or not charts.get("rsi_data", {}).get("dates"):
            warnings.append("charts.rsi_data is empty or missing (RSI chart will not render)")
    return warnings


def inject_data(template: str, data: dict) -> str:
    """Inject JSON data into template by replacing placeholders."""
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    # Escape </script> to prevent XSS / template breakage
    json_str = json_str.replace("</script>", "<\\/script>")
    # Replace data placeholder
    result = template.replace("__DATA_JSON__", json_str)
    # Replace title placeholders
    meta = data.get("meta", {})
    stock_name = meta.get("stock_name", "Unknown")
    stock_code = meta.get("stock_code", "N/A")
    result = result.replace("__STOCK_NAME__", stock_name)
    result = result.replace("__STOCK_CODE__", stock_code)
    return result


def main():
    parser = argparse.ArgumentParser(
        description="Stock Analyst - HTML Report Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--data", required=True, help="Path to JSON data file"
    )
    parser.add_argument(
        "--output", required=True, help="Path to output HTML file"
    )
    parser.add_argument(
        "--template", required=True, help="Path to HTML template file"
    )
    args = parser.parse_args()

    # Load and validate data
    print(f"Loading data: {args.data}")
    data = load_json(args.data)

    warnings = validate_data(data)
    if warnings:
        print("Validation warnings:", file=sys.stderr)
        for w in warnings:
            print(f"  WARNING: {w}", file=sys.stderr)

    # Load template
    print(f"Loading template: {args.template}")
    template = load_template(args.template)

    # Inject data
    print("Injecting data into template...")
    html = inject_data(template, data)

    # Write output
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    print(f"Report generated: {args.output}")

    # Summary
    meta = data.get("meta", {})
    print(f"  Stock: {meta.get('stock_name', 'N/A')} ({meta.get('stock_code', 'N/A')})")
    print(f"  Market: {meta.get('market_label', 'N/A')}")
    print(f"  Date: {meta.get('report_date', 'N/A')}")
    sections_found = sum(1 for k in ALL_SECTIONS if k in data)
    print(f"  Sections: {sections_found}/{len(ALL_SECTIONS)}")


if __name__ == "__main__":
    main()
