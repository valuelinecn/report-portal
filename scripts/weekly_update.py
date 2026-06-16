#!/usr/bin/env python3
"""
Weekly K-line update: auto-detect stocks from portal COMPANIES array,
fetch market cap data for ALL of them, and push to GitHub Pages.

Runs every Friday at 17:00 via Hermes cron job.
"""
import json, os, re, subprocess, sys
from datetime import datetime

REPO_DIR = '/data/data/com.termux/files/home/.hermes/hermes-agent/report-portal'
INDEX_HTML = os.path.join(REPO_DIR, 'index.html')
FETCH_SCRIPT = os.path.join(REPO_DIR, 'scripts', 'fetch_kline.py')

# Named-ID → stock_code mapping (for IDs that aren't numeric stock codes)
NAMED_MAP = {
    'ningde': 'sz300750',
}

def run(cmd, cwd=None):
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd or REPO_DIR, timeout=120)
    if result.returncode != 0:
        print(f"ERROR: {' '.join(cmd)}")
        err = result.stderr.strip()[:200]
        if err:
            print(f"  {err}")
        return False
    out = result.stdout.strip()
    if out:
        print(out)
    return True

def parse_companies_from_index():
    """Extract {id:, name:} pairs from COMPANIES array in index.html."""
    with open(INDEX_HTML, 'r', encoding='utf-8') as f:
        html = f.read()
    # Find COMPANIES array between 'const COMPANIES = [' and ']'
    m = re.search(r'const COMPANIES\s*=\s*\[(.*?)\];', html, re.DOTALL)
    if not m:
        print("ERROR: Cannot find COMPANIES array in index.html")
        sys.exit(1)
    array_content = m.group(1)
    # Extract all {id:'xxx',...name:'yyy'...} entries
    pattern = r"\{\s*id\s*:\s*'([^']+)'[^}]*?name\s*:\s*'([^']+)'[^}]*\}"
    entries = re.findall(pattern, array_content)
    print(f"从门户发现 {len(entries)} 家企业")
    for eid, name in entries:
        print(f"  {eid} → {name}")
    return entries

def id_to_stock_code(eid):
    """Convert portal ID to EastMoney stock code."""
    # Named IDs
    if eid in NAMED_MAP:
        return NAMED_MAP[eid]
    # HK stocks: id like 'hk2015' → EastMoney 'hk02015' (fill to 5 digits)
    if eid.lower().startswith('hk'):
        code_digits = eid[2:]  # strip 'hk' prefix
        code_digits = code_digits.zfill(5)  # EastMoney 5-digit HK format
        return f'hk{code_digits}'
    # Numeric IDs: auto-detect exchange prefix
    if eid.isdigit():
        first = eid[0]
        if first in ('0', '2', '3'):
            return f'sz{eid}'
        elif first in ('6'):
            return f'sh{eid}'
        else:
            print(f"  ⚠ 跳过未知格式股票代码: {eid}")
            return None
    print(f"  ⚠ 跳过未知ID: {eid}")
    return None

def main():
    print("=" * 50)
    print(f"K线数据自动更新 — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)

    # Step 1: Parse COMPANIES
    entries = parse_companies_from_index()
    stocks = []
    for eid, name in entries:
        code = id_to_stock_code(eid)
        if code:
            stocks.append((eid, name, code))

    print(f"\n需更新的股票数: {len(stocks)}")

    # Step 2: Fetch all stocks
    success = 0
    fail = 0
    for eid, name, code in stocks:
        print(f"\n[{code} {name}]")
        result = subprocess.run(
            [sys.executable, FETCH_SCRIPT, code],
            capture_output=True, text=True, timeout=120
        )
        for line in result.stdout.strip().split('\n'):
            line_s = line.strip()
            if line_s:
                print(f"  {line_s}")
        if result.returncode != 0:
            err = result.stderr.strip()[:100]
            print(f"  ❌ 失败: {err}")
            fail += 1
        else:
            success += 1

    print(f"\n{'=' * 50}")
    print(f"✅ 成功: {success} | ❌ 失败: {fail}")

    # Step 3: Check if kline/ changed
    print("\n检查数据是否有更新...")
    status = subprocess.run(
        ['git', 'status', '--porcelain', 'kline/'],
        capture_output=True, text=True, cwd=REPO_DIR, timeout=10
    )
    if not status.stdout.strip():
        print("数据无变化，跳过提交。")
        return

    # Step 4: Commit and push
    print("提交并推送到 GitHub Pages...")
    ts = datetime.now().strftime('%Y-%m-%d')
    if not run(['git', 'add', 'kline/']):
        return
    if not run(['git', 'commit', '-m', f'chore: update kline data {ts}']):
        return
    if not run(['git', 'push']):
        return

    print(f"\n✅ 全部更新完成 ({success}/{len(stocks)} 成功)")

if __name__ == '__main__':
    main()
