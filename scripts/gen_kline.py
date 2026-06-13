#!/usr/bin/env python3
"""Generate K-line market cap JSON files for any stock via Tencent proxy API."""
import json, os, sys, requests
from datetime import datetime, timedelta
from collections import OrderedDict

TENCENT_KLINE = 'https://proxy.finance.qq.com/ifzqgtimg/appstock/app/fqkline/get'
TENCENT_QUOTE = 'https://qt.gtimg.cn/q='

def fetch_all_kline(code, start_date='2003-01-01', end_date='2026-06-14'):
    all_data, seen = [], set()
    current_end = end_date
    while True:
        params = f'{code},day,{start_date},{current_end},2000,qfq'
        resp = requests.get(f'{TENCENT_KLINE}?param={params}', timeout=20)
        d = resp.json().get('data')
        if not isinstance(d, dict) or code not in d:
            break
        qfqday = d[code].get('qfqday', [])
        if not qfqday:
            break
        fd = qfqday[0][0]
        if fd in seen:
            break
        seen.add(fd)
        all_data = qfqday + all_data
        if fd <= start_date:
            break
        current_end = fd
    return all_data

def aggregate(daily, period):
    g = OrderedDict()
    for item in daily:
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
        g[key] = item
    return sorted(g.values(), key=lambda x: x['time'])

def main():
    if len(sys.argv) < 2:
        print('Usage: gen_kline.py SZ/SH_CODE')
        sys.exit(1)
    
    stock = sys.argv[1].strip().lower()
    if not stock.startswith(('sh', 'sz')):
        stock = 'sz' + stock if stock.startswith(('0', '3')) else 'sh' + stock
    
    # Get clean code for filename
    code_clean = stock.replace('sh', '').replace('sz', '')
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_dir = os.path.dirname(script_dir)
    kline_dir = os.path.join(repo_dir, 'kline')
    os.makedirs(kline_dir, exist_ok=True)
    
    print(f'=== {stock} K-line ===')
    
    days = fetch_all_kline(stock)
    valid = [d for d in days if len(d) >= 6 and float(d[2]) > 0]
    if not valid:
        print('No data!')
        sys.exit(1)
    print(f'  {len(valid)} entries: {valid[0][0]} ~ {valid[-1][0]}')
    
    # Fetch shares
    resp = requests.get(f'{TENCENT_QUOTE}{stock}', timeout=10)
    fields = resp.text.split('~')
    price = float(fields[3]) if len(fields) > 3 and fields[3] else 0
    mcap = float(fields[44]) if len(fields) > 44 and fields[44] else 0
    shares_yi = mcap / price if price > 0 else 0
    if shares_yi <= 10:  # unlikely for A-shares, use fallback
        shares_yi = float(input(f'  Total shares not found, enter (亿): '))
    print(f'  Shares: {shares_yi:.2f}亿')
    
    daily = [{"time": d[0], "value": round(float(d[2]) * shares_yi, 2)} for d in valid]
    vals = [x['value'] for x in daily]
    print(f'  MCap: {min(vals):.1f}~{max(vals):.1f}, cur={vals[-1]:.1f}')
    
    for pname in ['day', 'week', 'month', 'year']:
        fname = f'{code_clean}_{pname}.json'
        fpath = os.path.join(kline_dir, fname)
        data = daily if pname == 'day' else aggregate(daily, pname)
        with open(fpath, 'w') as f:
            json.dump(data, f, ensure_ascii=False)
        print(f'  ✅ {fname}: {len(data)} pts')
    print(f'\nDone: {kline_dir}/')

if __name__ == '__main__':
    main()
