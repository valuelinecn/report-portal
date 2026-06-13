#!/usr/bin/env python3
"""Generate K-line market cap JSON files for 三一重工 (600031).
Uses Tencent proxy API with pagination to get full history.
"""
import json, os, requests
from datetime import datetime, timedelta
from collections import OrderedDict

STOCK_CODE = 'sh600031'
CODE_CLEAN = '600031'
TENCENT_KLINE = 'https://proxy.finance.qq.com/ifzqgtimg/appstock/app/fqkline/get'
TENCENT_QUOTE = 'https://qt.gtimg.cn/q='

def fetch_all_kline(code, start_date='2003-01-01', end_date='2026-06-14'):
    """Fetch ALL daily K-line by paginating with max_rows=2000 (Tencent API limit)."""
    all_data = []
    current_end = end_date
    seen_dates = set()
    
    while True:
        params = f'{code},day,{start_date},{current_end},2000,qfq'
        url = f'{TENCENT_KLINE}?param={params}'
        resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=20)
        data = resp.json()
        d = data.get('data')
        if not isinstance(d, dict) or code not in d:
            print(f"  No data for {start_date} ~ {current_end}")
            break
        
        sd = d[code]
        qfqday = sd.get('qfqday', [])
        if not qfqday:
            print(f"  No qfqday for {start_date} ~ {current_end}")
            break
        
        # Dedup: check if we've already seen these dates
        first_date = qfqday[0][0]
        if first_date in seen_dates:
            print(f"  Dedup break at {first_date}")
            break
        seen_dates.add(first_date)
        
        print(f"  {len(qfqday)} entries: {qfqday[0][0]} ~ {qfqday[-1][0]}")
        all_data = qfqday + all_data  # prepend (we're fetching backwards)
        
        if first_date <= start_date:
            break
        current_end = first_date
    
    return all_data

def fetch_total_shares(code):
    """Fetch total shares from Tencent quote API."""
    resp = requests.get(TENCENT_QUOTE + code, timeout=10)
    text = resp.text
    fields = text.split('~')
    for f in fields:
        if '总股本' in f:
            idx = fields.index(f)
            if idx > 0:
                try:
                    return float(fields[idx-1])
                except:
                    pass
    return 0

def aggregate_by_period(data, period='week'):
    grouped = OrderedDict()
    for item in data:
        d = item['time']
        if period == 'week':
            dt = datetime.strptime(d, '%Y-%m-%d')
            key = (dt - timedelta(days=dt.weekday())).strftime('%Y-%m-%d')
        elif period == 'month':
            key = d[:7]
        elif period == 'year':
            key = d[:4]
        else:
            key = d
        grouped[key] = item
    result = list(grouped.values())
    result.sort(key=lambda x: x['time'])
    return result

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_dir = os.path.dirname(script_dir)
    kline_dir = os.path.join(repo_dir, 'kline')
    os.makedirs(kline_dir, exist_ok=True)

    print(f"=== 三一重工 (600031) K-line Data Generation ===\n")

    # Step 1: Fetch all daily K-line
    print("Step 1: Fetching ALL daily K-line via paginated Tencent proxy...")
    all_days = fetch_all_kline(STOCK_CODE)
    if not all_days:
        print("ERROR: No data!")
        return
    
    valid = [d for d in all_days if len(d) >= 6 and float(d[2]) > 0]
    print(f"\n  Total valid entries: {len(valid)}")
    print(f"  Date range: {valid[0][0]} ~ {valid[-1][0]}")
    
    # Step 2: Fetch total shares
    print("\nStep 2: Fetching total shares...")
    total_shares = fetch_total_shares(STOCK_CODE)
    print(f"  Total shares: {total_shares:.2f}")
    if total_shares <= 0:
        total_shares = 8490000000
        print(f"  Using default: {total_shares:.2f}")
    total_shares_yi = total_shares / 1e8
    print(f"  = {total_shares_yi:.2f}亿股")

    # Step 3: Calculate market cap
    print("\nStep 3: Calculating market cap...")
    daily_data = []
    for d in valid:
        date_str = d[0]
        close_price = float(d[2])
        mcap = round(close_price * total_shares_yi, 2)
        daily_data.append({"time": date_str, "value": mcap})

    if daily_data:
        vals = [x['value'] for x in daily_data]
        print(f"  Min: {min(vals):.1f}亿")
        print(f"  Max: {max(vals):.1f}亿")
        print(f"  Current: {daily_data[-1]['value']:.1f}亿 ({daily_data[-1]['time']})")

    # Step 4: Generate period files
    print("\nStep 4: Generating period files...")
    periods = {
        'day': daily_data,
        'week': aggregate_by_period(daily_data, 'week'),
        'month': aggregate_by_period(daily_data, 'month'),
        'year': aggregate_by_period(daily_data, 'year'),
    }
    for period_name, period_data in periods.items():
        filename = f"{CODE_CLEAN}_{period_name}.json"
        filepath = os.path.join(kline_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(period_data, f, ensure_ascii=False)
        print(f"  ✅ {filename}: {len(period_data)} data points")

    print(f"\n✅ All files saved to: {kline_dir}/")

if __name__ == '__main__':
    main()
