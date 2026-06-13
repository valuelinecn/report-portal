#!/usr/bin/env python3
"""Generate K-line market cap JSON files for 中国船舶 (600150).
Uses Tencent proxy API with pagination.
"""
import json, os, requests
from datetime import datetime, timedelta
from collections import OrderedDict

STOCK_CODE = 'sh600150'
CODE_CLEAN = '600150'
TENCENT_KLINE = 'https://proxy.finance.qq.com/ifzqgtimg/appstock/app/fqkline/get'
TENCENT_QUOTE = 'https://qt.gtimg.cn/q='

def fetch_all_kline(code, start_date='2003-01-01', end_date='2026-06-14'):
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
            break
        qfqday = d[code].get('qfqday', [])
        if not qfqday:
            break
        first_date = qfqday[0][0]
        if first_date in seen_dates:
            break
        seen_dates.add(first_date)
        all_data = qfqday + all_data
        if first_date <= start_date:
            break
        current_end = first_date
    return all_data

def fetch_total_shares(code):
    resp = requests.get(TENCENT_QUOTE + code, timeout=10)
    text = resp.text
    fields = text.split('~')
    try:
        price = float(fields[3])
        mcap = float(fields[44])  # 总市值(亿)
        return mcap / price * 1e8
    except:
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

    print(f"=== 中国船舶 (600150) K-line Data Generation ===\n")

    print("Fetching daily K-line...")
    all_days = fetch_all_kline(STOCK_CODE)
    valid = [d for d in all_days if len(d) >= 6 and float(d[2]) > 0]
    print(f"  {len(valid)} entries: {valid[0][0]} ~ {valid[-1][0]}")

    print("Fetching total shares...")
    total_shares = fetch_total_shares(STOCK_CODE)
    if total_shares <= 0:
        total_shares = 5000000000  # fallback ~50亿
    total_shares_yi = total_shares / 1e8
    print(f"  Total shares: {total_shares_yi:.2f}亿")

    daily_data = []
    for d in valid:
        date_str = d[0]
        close_price = float(d[2])
        mcap = round(close_price * total_shares_yi, 2)
        daily_data.append({"time": date_str, "value": mcap})

    if daily_data:
        vals = [x['value'] for x in daily_data]
        print(f"  MCap range: {min(vals):.1f}亿 ~ {max(vals):.1f}亿, current: {vals[-1]:.1f}亿")

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
        print(f"  ✅ {filename}: {len(period_data)} pts")

    print(f"\nDone: {kline_dir}/")

if __name__ == '__main__':
    main()
