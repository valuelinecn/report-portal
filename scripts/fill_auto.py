#!/usr/bin/env python3
"""
fill_auto.py — 自动填充引擎

用法: python3 fill_auto.py <股票代码>

步骤:
  1. 复制模板 → 运行fetch_financial/gen_kline/colorize
  2. 读回fin-table数据 → 提取所有财务指标
  3. 填充 auto 类占位符（17种固定值）
  4. 构造 construct 类内容（年度行/HB条/DIM评分等）
  5. 整表替换 14 个 whole_table_replace 表
  6. 所有 manual 类填入 __TODO__
  7. 输出待填清单 → 运行验证
"""
import sys, os, re, json, subprocess, shutil

SKILL_DIR = os.path.expanduser('~/.hermes/skills/software-development/report-fill-workflow')
PORTAL_DIR = os.path.expanduser('~/.hermes/hermes-agent/report-portal')
BLANK_HTML = '/sdcard/Download-Termux/blank.html'
MANIFEST = os.path.join(SKILL_DIR, 'references', 'manifest.json')

# 股票代码映射
def get_exchange(code):
    if code.startswith(('6', '9')): return 'sh'
    return 'sz'

def get_full_code(code):
    exch = get_exchange(code)
    return f'{exch}{code}'


def run(cmd, timeout=60):
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, shell=True)
    if result.returncode != 0:
        print(f'  ⚠️ 命令返回非零: {result.stderr[:200]}')
    return result.stdout, result.stderr


def extract_fin_table(html_path):
    """从已着色的HTML中提取fin-table数据"""
    with open(html_path, 'r', encoding='utf-8') as f:
        c = f.read()
    
    # 找到fin-table区域
    m = re.search(r'<table class="fin-table[^>]*">.*?</table>', c, re.DOTALL)
    if not m:
        print('  ❌ 未找到fin-table')
        return {}
    
    tbl = m.group()
    data = {}
    
    # 提取每个指标行
    rows = re.findall(r'<tr><td>([^<]+)</td>(.*?)</tr>', tbl, re.DOTALL)
    for label, cells_html in rows:
        label = label.strip()
        cells = re.findall(r'<td[^>]*>([^<]*)</td>', cells_html)
        # 去掉HTML标签
        clean_cells = []
        for c in cells:
            clean = re.sub(r'<[^>]+>', '', c).strip()
            clean_cells.append(clean)
        
        if clean_cells:
            data[label] = clean_cells
    
    return data


def parse_fin_data(fin_data):
    """将fin-table原始数据解析为可用字典"""
    result = {}
    
    for label, vals in fin_data.items():
        try:
            nums = []
            for v in vals[:6]:  # 2025-2020
                v = v.replace('--', '')
                if v:
                    nums.append(float(v))
                else:
                    nums.append(None)
            result[label] = nums
        except:
            pass
    
    # 构建年份维度的数据
    years = [2025, 2024, 2023, 2022, 2021]
    by_year = {}
    
    KEY_MAP = {
        '每股营业收入(元)': 'REVPS', '每股经营现金流(元)': 'CFPS',
        '每股净利润(元)': 'EPS', '每股净资产(元)': 'BPS',
        '总股本(亿股)': 'SHARES', '营业收入(亿元)': 'REV',
        '毛利率(%)': 'GROSS', '净利润(亿元)': 'NP',
        '净利润率(%)': 'NPR', 'ROE(%)': 'ROE',
    }
    
    for cn_key, eng_key in KEY_MAP.items():
        if cn_key in result:
            by_year[eng_key] = {}
            for i, yr in enumerate(years):
                if i < len(result[cn_key]) and result[cn_key][i] is not None:
                    by_year[eng_key][yr] = result[cn_key][i]
    
    # 计算OCF(经营现金流) = CFPS × SHARES
    if 'CFPS' in by_year and 'SHARES' in by_year:
        by_year['OCF'] = {}
        for yr in years:
            cfps = by_year['CFPS'].get(yr)
            sh = by_year['SHARES'].get(yr)
            if cfps is not None and sh is not None:
                by_year['OCF'][yr] = round(cfps * sh, 2)
    
    return by_year


def get_price(code):
    """获取当前股价，返回float"""
    full = get_full_code(code)
    out, _ = run(f"curl -s 'https://hq.sinajs.cn/list={full}' -H 'Referer: https://finance.sina.com.cn' 2>/dev/null | cut -d',' -f4")
    try:
        return float(out.strip())
    except:
        return None


def trend_icon(yr, np_data, rev, years):
    """根据净利和营收趋势判断图标"""
    if yr == years[0]:
        return '—'
    prev_np = np_data.get(years[years.index(yr)-1], 0)
    curr_np = np_data.get(yr, 0)
    if curr_np and prev_np:
        if curr_np > prev_np * 1.2:
            return '↗️'
        elif curr_np > prev_np:
            return '↗️'
        elif curr_np < prev_np * 0.8:
            return '↘️'
        elif curr_np < prev_np:
            return '↘️'
    return '➡️'


def main():
    if len(sys.argv) < 2:
        print('用法: python3 fill_auto.py <股票代码>')
        print('示例: python3 fill_auto.py 000009')
        sys.exit(1)
    
    code = sys.argv[1]
    exch = get_exchange(code)
    full_code = f'{exch}{code}'
    
    # 加载manifest
    with open(MANIFEST) as f:
        manifest = json.load(f)
    
    html_path = os.path.join(PORTAL_DIR, 'reports', f'{code}.html')
    
    print(f'{"="*50}')
    print(f'  fill_auto.py — 自动填充引擎')
    print(f'  股票: {code}')
    print(f'{"="*50}')
    
    # ===== Step 1: 准备 =====
    print('\n--- Step 1: 准备 ---')
    
    # 1.1 复制模板
    shutil.copy2(BLANK_HTML, html_path)
    print('  ✅ 模板已复制')
    
    # 清理模板示例行（PE对比条示例：目标公司/同行A/同行B）
    with open(html_path, 'r', encoding='utf-8') as __f:
        __c = __f.read()
    for __pat in ['目标公司', '同行A', '同行B']:
        __idx = __c.find(f'<div class="hb"><span class="hl">{__pat}</span>')
        if __idx >= 0:
            __end = __c.find('</div>', __c.find('</div></div>', __idx) + 6) + 6
            __c = __c[:__idx] + __c[__end:]
    with open(html_path, 'w', encoding='utf-8') as __f:
        __f.write(__c)
    print('  ✅ 模板示例行已清理（目标公司/同行A/同行B）')
    
    # 1.2 fetch财务数据
    fetch_script = os.path.expanduser('~/.hermes/skills/data-science/report-template-spec/scripts/fetch_financial_data.py')
    if os.path.exists(fetch_script):
        out, _ = run(f'cd {PORTAL_DIR} && python3 {fetch_script} reports/{code}.html {code}', 120)
        print(f'  ✅ fin-table已填充')
    
    # 1.3 colorize
    color_script = os.path.expanduser('~/.hermes/skills/data-science/report-template-spec/scripts/colorize_financial_table.py')
    if os.path.exists(color_script):
        out, _ = run(f'cd {PORTAL_DIR} && python3 {color_script} reports/{code}.html', 60)
        print(f'  ✅ 财务着色完成')
    
    # 1.4 获取股价
    price = get_price(code)
    if price:
        print(f'  ✅ 股价: {price}元')
    else:
        price = 0.0
        print(f'  ⚠️ 股价获取失败，设为0')
    
    # 1.5 K线
    gen_kline = os.path.join(PORTAL_DIR, 'scripts', 'gen_kline.py')
    if os.path.exists(gen_kline):
        out, _ = run(f'cd {PORTAL_DIR} && python3 {gen_kline} {full_code}', 120)
        print(f'  ✅ K线已生成')
    
    # ===== Step 2: 读取财务数据 =====
    print('\n--- Step 2: 读取fin-table数据 ---')
    fin_raw = extract_fin_table(html_path)
    fin = parse_fin_data(fin_raw)
    
    shares = fin.get('SHARES', {}).get(2025, 0)
    rev = fin.get('REV', {})
    np_data = fin.get('NP', {})
    gross_data = fin.get('GROSS', {})
    npr_data = fin.get('NPR', {})
    roe_data = fin.get('ROE', {})
    eps_data = fin.get('EPS', {})
    bps_data = fin.get('BPS', {})
    ocf_data = fin.get('OCF', {})
    cfps_data = fin.get('CFPS', {})
    revps_data = fin.get('REVPS', {})
    
    print(f'  总股本: {shares}亿')
    print(f'  营收2025: {rev.get(2025, "?")}亿')
    print(f'  净利2025: {np_data.get(2025, "?")}亿')
    print(f'  ROE 2025: {roe_data.get(2025, "?")}%')
    
    # ===== Step 3: 读报告HTML =====
    with open(html_path, 'r', encoding='utf-8') as f:
        c = f.read()
    
    mcap = round(price * shares, 1) if price and shares else 0
    
    # ===== Step 4: 填充 auto 类占位符 =====
    print('\n--- Step 3: 填充auto占位符 ---')
    
    AUTO_VALS = {
        '{{STOCK_CODE}}': f'{code}.{"SZ" if exch == "sz" else "SH"}',
        '{{STOCK_SUFFIX}}': f'.{"SZ" if exch == "sz" else "SH"}',
        '{{CODE}}': code,
        '{{PRICE}}': str(price) if price else '0.0',
        '{{BASE_PRICE}}': str(price) if price else '0.0',
        '{{SHARES}}': str(shares) if shares else '0',
        '{{MCAP}}': str(mcap) if mcap else '0',
        '{{ROE_VAL}}': f'{roe_data.get(2025, 0):.2f}%' if roe_data.get(2025) else '0%',
    }
    
    auto_filled = 0
    for k, v in AUTO_VALS.items():
        if k in c:
            c = c.replace(k, v)
            auto_filled += 1
    
    print(f'  auto类: 填充{auto_filled}个')
    
    # ===== Step 5: 构造 construct 类内容 =====
    print('\n--- Step 4: 构造construct内容 ---')
    
    # 5.1 M1年度财务摘要行（含YoY自动计算）
    years_order = [2021, 2022, 2023, 2024, 2025]
    annual_rows = ''
    for i, yr in enumerate(years_order):
        cls = ' class="gold"' if yr == 2025 else ''
        rv = rev.get(yr, '—')
        np_v = np_data.get(yr, '—')
        gr = gross_data.get(yr, '—')
        nr = npr_data.get(yr, '—')
        if isinstance(rv, float): rv = f'{rv:.2f}'
        if isinstance(np_v, float): np_v = f'{np_v:.2f}'
        if isinstance(gr, float): gr = f'{gr:.2f}'
        if isinstance(nr, float): nr = f'{nr:.2f}'
        # YoY计算
        if i == 0:
            yoy = '—'
            yoy_cls = ''
        else:
            prev_rev = rev.get(years_order[i-1], None)
            curr_rev = rev.get(yr, None)
            if prev_rev and curr_rev and isinstance(prev_rev, (int,float)) and isinstance(curr_rev, (int,float)):
                yoy_val = (curr_rev - prev_rev) / prev_rev * 100
                yoy = f'{yoy_val:+.1f}%'
                yoy_cls = ' class="gold"' if yoy_val > 0 else ' class="red"'
            else:
                yoy = '—'
                yoy_cls = ''
        annual_rows += f'<tr><td>{yr}</td><td{cls}>{rv}</td><td{yoy_cls}>{yoy}</td><td{cls}>{np_v}</td><td{cls}>{nr}%</td><td{cls}>{gr}%</td></tr>\n'
    
    c = c.replace('{{M1_ANNUAL_ROWS}}', annual_rows)
    print('  ✅ M1年度摘要行已构造')
    
    # 5.2 M1分业务水平条（保留{{}}供手动填写）
    # 这些保持原样，fill_manual.py会识别
    print('  ✅ construct占位符保持{{}}格式，供fill_manual.py使用')
    
    # ===== Step 6: 整表替换14个whole_table_replace表 =====
    print('\n--- Step 5: 整表替换 ---')
    
    # 6.1 核心财务指标
    m4_rows = ''
    for yr in years_order:
        cls = ' class="gold"' if yr == 2025 else ''
        rv = rev.get(yr, '—'); np_v = np_data.get(yr, '—')
        gr = gross_data.get(yr, '—'); nr = npr_data.get(yr, '—')
        roe_v = roe_data.get(yr, '—')
        if isinstance(rv, float): rv = f'{rv:.2f}'
        if isinstance(np_v, float): np_v = f'{np_v:.2f}'
        if isinstance(gr, float): gr = f'{gr:.2f}'
        if isinstance(nr, float): nr = f'{nr:.2f}'
        if isinstance(roe_v, float): roe_v = f'{roe_v:.2f}'
        m4_rows += f'<tr><td>{yr}</td><td{cls}>{rv}</td><td{cls}>{np_v}</td><td>{gr}%</td><td{cls}>{nr}%</td><td{cls}>{roe_v}%</td><td>{trend_icon(yr, np_data, rev, years_order)}</td></tr>\n'
    
    m4_html = f'<h3>核心财务指标</h3><div style="overflow-x:auto"><table class="tbl"><tr><th>年份</th><th>营收(亿)</th><th>净利(亿)</th><th>毛利率</th><th>净利率</th><th>ROE</th><th>趋势</th></tr>{m4_rows}</table></div>'
    
    idx = c.find('<h3>核心财务指标</h3>')
    if idx >= 0:
        end = c.find('<h3', idx+10)
        if end < 0: end = c.find('<h2', idx+10)
        c = c[:idx] + m4_html + c[end:]
        print('  ✅ 核心财务指标表已替换')
    
    # 6.2 现金流&资产负债
    ocf_25 = ocf_data.get(2025, '—')
    ocf_24 = ocf_data.get(2024, '—')
    ocf_23 = ocf_data.get(2023, '—')
    if isinstance(ocf_25, float): ocf_25 = f'{ocf_25:.2f}'
    if isinstance(ocf_24, float): ocf_24 = f'{ocf_24:.2f}'
    if isinstance(ocf_23, float): ocf_23 = f'{ocf_23:.2f}'
    cf_html = f'<h3>现金流 &amp; 资产负债</h3><div style="overflow-x:auto"><table class="tbl"><tr><th>指标</th><th>2023</th><th>2024</th><th class="gold">2025</th><th>趋势</th></tr><tr><td>经营现金流(亿)</td><td>{ocf_23}</td><td>{ocf_24}</td><td class="gold">{ocf_25}</td><td class="green">➡️</td></tr></table></div>'
    idx_cf = c.find('<h3>现金流')
    if idx_cf >= 0:
        end_cf = c.find('<h3', idx_cf+10)
        if end_cf < 0: end_cf = c.find('<h2', idx_cf+10)
        c = c[:idx_cf] + cf_html + c[end_cf:]
        print('  ✅ 现金流&资产负债已替换')
    
    # 6.3 估值指标
    eps_ttm = eps_data.get(2025, None)
    bps_v = bps_data.get(2025, None)
    revps_v = revps_data.get(2025, None)
    pe_str = f'{round(price/eps_ttm,1)}x' if price and eps_ttm and eps_ttm > 0 else '亏损'
    pb_str = f'{round(price/bps_v,2)}x' if price and bps_v and bps_v > 0 else '—'
    ps_str = f'{round(price/revps_v,2)}x' if price and revps_v and revps_v > 0 else '—'
    val_html = f'<h3>估值指标</h3><table class="tbl"><tr><th>指标</th><th>当前值</th><th>历史区间</th><th>评估</th></tr><tr><td>PE(TTM)</td><td class="gold">{pe_str}</td><td>—</td><td>—</td></tr><tr><td>PB</td><td>{pb_str}</td><td>—</td><td>—</td></tr><tr><td>PS(TTM)</td><td>{ps_str}</td><td>—</td><td>—</td></tr></table>'
    idx_val = c.find('<h3>估值指标</h3>')
    if idx_val >= 0:
        end_val = c.find('<h3', idx_val+10)
        if end_val < 0: end_val = c.find('<h2', idx_val+10)
        c = c[:idx_val] + val_html + c[end_val:]
        print('  ✅ 估值指标表已替换')
    
    # 6.4 敏感性分析（固定5个标准情景）
    sens_html = '<h3>敏感性分析</h3><table class="tbl"><tr><th>压力情景</th><th>净利影响</th><th>股价压力</th></tr><tr><td>营收下降10%</td><td>—</td><td class="orange">—</td></tr><tr><td>毛利率下降3pct</td><td>—</td><td class="orange">—</td></tr><tr><td>费用率上升</td><td>—</td><td class="orange">—</td></tr><tr><td>行业下行周期</td><td>—</td><td class="red">—</td></tr><tr><td>竞争加剧</td><td>—</td><td class="orange">—</td></tr></table>'
    idx_sens = c.find('<h3>敏感性分析</h3>')
    if idx_sens >= 0:
        end_sens = c.find('<h3', idx_sens+10)
        if end_sens < 0: end_sens = c.find('<h2', idx_sens+10)
        c = c[:idx_sens] + sens_html + c[end_sens:]
        print('  ✅ 敏感性分析表已替换')
    
    # 6.5 避雷清单（固定检查项）
    avoid_html = '<h3>避雷清单</h3><table class="tbl"><tr><th>检查项</th><th>结果</th></tr><tr><td>是否存在商誉减值风险</td><td>—</td></tr><tr><td>大股东是否持续减持</td><td>—</td></tr><tr><td>财务造假信号</td><td>—</td></tr><tr><td>现金流是否持续为负</td><td>—</td></tr><tr><td>是否有未决诉讼</td><td>—</td></tr></table>'
    idx_avoid = c.find('<h3>避雷清单</h3>')
    if idx_avoid >= 0:
        end_avoid = c.find('</table>', idx_avoid) + 8
        c = c[:idx_avoid] + avoid_html + c[end_avoid:]
        print('  ✅ 避雷清单表已替换')
    
    # 6.6 其他整表替换表 — 填入{{TD}}为TODO
    # 简单处理：所有{{TD}}替换为__TODO__
    td_count_before = c.count('{{TD}}')
    c = c.replace('{{TD}}', '__TODO__')
    print(f'  ✅ {{TD}}已替换为__TODO__ ({td_count_before}个)')
    
    # ===== Step 7: 所有manual类占位符保持不变（留{{}}供fill_manual.py识别） =====
    print('\n--- Step 7: 分类占位符 ---')
    
    # 检查剩余所有{{PLACEHOLDER}}
    remaining = set(re.findall(r'\{\{[A-Z_0-9]+\}\}', c))
    manual_count = len(remaining)
    
    print(f'  剩余占位符: {manual_count}个（待手动填写）')
    for ph in sorted(remaining):
        print(f'    {ph}')
    
    # ===== Step 8: 保存 =====
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f'\n  ✅ 已保存: {html_path}')
    
    # ===== Step 9: 输出待填清单 =====
    print(f'\n{"="*50}')
    print(f'  📋 待填清单 ({manual_count}项)')
    print(f'{"="*50}')
    
    # 按主题分组
    groups = {
        '基础信息': ['COMPANY_NAME_CN', 'COMPANY_SHORT', 'COMPANY_NAME_EN', 'REPORT_DATE', 'INDUSTRY', 'DATA_DATE', 'DATA_SOURCE', 'SCORE', 'RATING_DESC', 'RATING_TEXT'],
        '综合评价卡片': ['CARD1_VAL', 'CARD1_LABEL', 'CARD1_COLOR', 'CARD2_VAL', 'CARD2_LABEL', 'CARD2_COLOR', 'CARD3_VAL', 'CARD3_LABEL', 'CARD3_COLOR', 'CARD4_VAL', 'CARD4_LABEL', 'CARD4_COLOR', 'LABEL_2', 'LABEL_2_TITLE', 'LABEL_3', 'LABEL_3_TITLE'],
        'LOGIC卡': ['LOGIC_1_VAL', 'LOGIC_1', 'LOGIC_2', 'LOGIC_2_DETAIL', 'LOGIC_3', 'LOGIC_3_DETAIL', 'LOGIC_4', 'LOGIC_4_DETAIL'],
        'BQ × 13': ['BQ_ANALYSIS × 13'],
    }
    
    for group, items in groups.items():
        found = [p for p in items if '{{'+p.strip('{}')+'}}' in c]
        if found or group == 'BQ × 13':
            print(f'\n  [{group}]')
            for item in found:
                print(f'    □ {item}')
            if group == 'BQ × 13':
                print(f'    □ BQ_ANALYSIS × {c.count("{{BQ_ANALYSIS}}")}篇')
    
    # 分类列出其他manual占位符
    manual_groups = {
        'M1商业模式/分业务': [p for p in remaining if 'M1_' in p or 'HB_' in p],
        'M2壁垒': [p for p in remaining if 'MOAT_' in p or 'BARRIER' in p or 'CERT' in p or 'COST_' in p or 'CUSTOMER' in p or 'DISRUPTION' in p or 'MARGIN' in p or 'BRAND' in p or 'PRICE_WAR' in p or 'RESOURCE' in p or 'TECH_' in p],
        'M3管理层': [p for p in remaining if 'MGMT_' in p],
        'M4财务KPI': [p for p in remaining if 'KPI_' in p or 'M4_KPI' in p],
        'M6价值理念': [p for p in remaining if '_ANALYSIS}}' in p or 'SAFETY_MARGIN' in p],
        'M7竞争': [p for p in remaining if 'COMPETITOR' in p or 'CORE_BUSINESS' in p],
        'M10风险/三情景/清算': [p for p in remaining if 'RISK_' in p or 'OPTIMISTIC' in p or 'PESS_' in p or 'BASE_SCENARIO' in p or 'LIQ_' in p or 'FCF_' in p or 'FINANCIAL_' in p],
        '亮点': [p for p in remaining if 'HIGHLIGHT' in p],
        '其他': [p for p in remaining if not any(k in p for k in ['BQ', 'M1_', 'M4_', 'MOAT_', 'MGMT_', 'KPI_', 'COMPETITOR', 'RISK_', 'OPTIMISTIC', 'PESS_', 'BASE_', 'LIQ_', 'HIGHLIGHT', 'FCF_', 'FINANCIAL_', 'CARD', 'LABEL', 'LOGIC', 'COMPANY_', 'REPORT_DATE', 'INDUSTRY', 'DATA_', 'SCORE', 'RATING', '_ANALYSIS', 'SAFETY_MARGIN'])],
    }
    
    for group, items in manual_groups.items():
        remaining_in_group = [p for p in items if '{{'+p.strip('{}')+'}}' in c]
        if remaining_in_group:
            print(f'\n  [{group}]')
            for item in remaining_in_group:
                print(f'    □ {item}')
    
    print(f'\n{"="*50}')
    print(f'  ⚠️ 以上 {manual_count} 项需手动填写')
    print(f'  填完后运行 verify_report.py 验证')
    print(f'{"="*50}')


if __name__ == '__main__':
    main()
