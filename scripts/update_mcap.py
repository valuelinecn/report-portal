#!/usr/bin/env python3
"""每日/每周更新所有股票市值数据 → JSON → git push"""

import json, os, requests, sys, time
from datetime import datetime, timedelta

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KLINE_DIR = os.path.join(BASE, "kline")
os.makedirs(KLINE_DIR, exist_ok=True)

# 股票列表: name -> (code, exchange)
STOCKS = {
    "wuliangye":      ("000858", "sz"),
    "maotai":         ("600519", "sh"),
    "haitian":        ("603288", "sh"),
    "mindray":        ("300760", "sz"),
    "ningde":         ("300750", "sz"),
    "pingan":         ("601318", "sh"),
    "byd":            ("002594", "sz"),
    "fuyao":          ("600660", "sh"),
    "hengrui":        ("600276", "sh"),
    "lixun":          ("002475", "sz"),
    "yili":           ("600887", "sh"),
    "zhaoshang":      ("600036", "sh"),
    "zhongjixuchuang":("300308", "sz"),
    "haikang":        ("002415", "sz"),
    "seres":          ("601127", "sh"),
}

def sina_kline(code, exchange, datalen=8000):
    """从新浪获取日K数据，返回 [{day, open, high, low, close, volume}, ...]"""
    symbol = f"{exchange}{code}"
    url = "https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData"
    params = {"symbol": symbol, "scale": "240", "ma": "no", "datalen": str(datalen)}
    resp = requests.get(url, params=params, timeout=30)
    data = resp.json()
    if not isinstance(data, list):
        print(f"  [WARN] 返回异常: {data}")
        return []
    return data

def tencent_total_shares(code, exchange):
    """从腾讯获取总股本（万股）"""
    symbol = f"{exchange}{code}"
    url = f"https://qt.gtimg.cn/q={symbol}"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers, timeout=15)
    line = resp.text.strip()
    parts = line.split('"')[1].split('~')
    # 腾讯API: 总市值的字段索引因股票而异, 我们找数值接近价格的字段
    # 更可靠: 用 [72] 字段 = 总股本(股)
    if len(parts) > 73:
        total_shares_raw = parts[72]  # 总股本, 单位: 股
        if total_shares_raw and total_shares_raw.replace('.','').isdigit():
            return float(total_shares_raw) / 1e8  # 转成亿股
    # 备选: 从流通市值/价格反算
    return None

def update_stock(name, code, exchange):
    """更新单个股票的市值数据"""
    name_cn = name  # 会用新浪数据里的名称覆盖

    # 1. 拉K线
    print(f"  [K线] 正在获取 {code}...")
    kline = sina_kline(code, exchange)
    if not kline:
        print(f"  [SKIP] {code} 无数据")
        return False

    name_cn = kline[0].get('name', kline[0].get('day', name))
    # 有时新浪返回的day是日期，name字段不一定有
    # 用股票代碼取名字從騰訊
    print(f"  K线共 {len(kline)} 条, {kline[0]['day']} ~ {kline[-1]['day']}")

    # 2. 拿总股本
    shares = tencent_total_shares(code, exchange)
    if shares is None or shares <= 0:
        print(f"  [WARN] 无法获取总股本，使用已知值")
        # 备选: 用已有的JSON或者估算
        # 从股价和大致市值估算
        last_close = float(kline[-1]['close'])
        # 查之前保存的数据
        json_path = os.path.join(KLINE_DIR, f"{code}.json")
        if os.path.exists(json_path):
            with open(json_path) as f:
                old = json.load(f)
                shares = old.get("total_shares", 0)
                print(f"  使用旧值总股本: {shares:.2f}亿")
        if not shares:
            print(f"  [FAIL] {code} 无法获取总股本")
            return False

    print(f"  总股本: {shares:.2f}亿股")

    # 3. 构建每日市值数据
    daily = []
    for bar in kline:
        close = float(bar['close'])
        mcap = round(close * shares, 2)  # 市值(亿)
        daily.append({
            "t": bar['day'],
            "c": close,
            "m": mcap
        })

    # 4. 计算周/月/年 (取最后一个交易日的值)
    weekly, monthly, yearly = {}, {}, {}
    for d in daily:
        dt = datetime.strptime(d['t'], "%Y-%m-%d")
        wk = dt.strftime("%Y-W%V")
        mo = dt.strftime("%Y-%m")
        yr = dt.strftime("%Y")
        weekly[wk] = d
        monthly[mo] = d
        yearly[yr] = d

    # 5. 写入JSON
    out = {
        "code": code,
        "name": name_cn,
        "total_shares": shares,
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "count": len(daily),
        "data": {
            "daily": daily,
            "weekly": sorted(weekly.values(), key=lambda x: x['t']),
            "monthly": sorted(monthly.values(), key=lambda x: x['t']),
            "yearly": sorted(yearly.values(), key=lambda x: x['t']),
        }
    }

    filepath = os.path.join(KLINE_DIR, f"{code}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print(f"  [OK] 写入 {filepath} ({len(daily)} 条)")
    return True

def main():
    print(f"=== 市值数据更新 {datetime.now().strftime('%Y-%m-%d %H:%M')} ===")
    success, fail = 0, 0
    for name, (code, exchange) in STOCKS.items():
        print(f"\n>>> {name} ({exchange}{code})")
        try:
            if update_stock(name, code, exchange):
                success += 1
            else:
                fail += 1
        except Exception as e:
            print(f"  [ERROR] {e}")
            fail += 1
        time.sleep(1)  # 礼貌间隔

    print(f"\n=== 完成: {success} 成功, {fail} 失败 ===")

    # Git push
    if success > 0:
        os.chdir(BASE)
        os.system("git add kline/")
        os.system(f'git commit -m "chore: update mcap data {datetime.now().strftime("%Y-%m-%d")}" --allow-empty')
        ret = os.system("git push origin main 2>&1")
        if ret == 0:
            print("[GIT] Push 成功")
        else:
            print("[GIT] Push 失败，稍后重试")

if __name__ == "__main__":
    main()
