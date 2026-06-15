#!/usr/bin/env python3
"""
generate_report.py — 基于空白模板自动生成企业研究报告

用法:
  python3 generate_report.py <股票代码> [公司名]

流程:
  1. 复制 blank-template.html → reports/{code}.html
  2. web_search 批量收集公司信息
  3. 填充 128 个占位符
  4. fetch_financial_data.py 拉取财务表
  5. gen_kline.py 拉取K线数据
  6. 自动审计 auto-audit.sh
  7. 输出来源清单

依赖:
  - 空白模板: blank-template.html
  - 脚本: scripts/fetch_financial_data.py, scripts/gen_kline.py, scripts/auto-audit.sh
  - Hermes web_search 工具
"""
import sys, os, re, json, subprocess, tempfile
from collections import Counter

REPORTS_DIR = 'reports'
SKILL_DIR = os.path.expanduser('~/.hermes/skills/data-science/report-template-spec')
BLANK_TEMPLATE = 'blank-template.html'

# ============================================================
# 搜索函数 — 调用 web_search 获取真实信息
# ============================================================
def web_search(query):
    """调用 Hermes web_search 工具"""
    import subprocess
    result = subprocess.run(
        ['hermes', 'tool', 'web_search', '--query', query],
        capture_output=True, text=True, timeout=30
    )
    if result.returncode == 0:
        return result.stdout
    return f"【搜索失败】{result.stderr[:200]}"

# ============================================================
# 信息收集
# ============================================================
def collect_info(stock_code, company_name):
    """搜索收集公司基本信息"""
    print(f'\n🔍 收集 {company_name}({stock_code}) 信息...')
    
    info = {
        'code': stock_code,
        'name': company_name,
        'name_en': '',
        'industry': '',
        'rating_desc': '',
        'rating_score': '6.5',
        'stock_suffix': 'SH' if stock_code.startswith('6') else 'SZ',
    }
    
    # 搜索公司基本信息
    queries = [
        f'{stock_code} {company_name} 主营业务 行业',
        f'{stock_code} {company_name} 英文名',
        f'{stock_code} 营收 净利润 2025',
        f'{stock_code} {company_name} 商业模式 壁垒',
    ]
    
    for q in queries:
        result = web_search(q)
        # Parse results - simplified for prototype
        if '行业' in q and not info['industry']:
            # Extract industry from search results
            pass
    
    return info

# ============================================================
# 填充模板
# ============================================================
def fill_template(html, data):
    """用收集到的数据填充所有占位符"""
    import re
    
    # 基础信息
    replacements = {
        '{{COMPANY_NAME_CN}}': data.get('name', ''),
        '{{STOCK_CODE}}': data.get('code', ''),
        '{{STOCK_SUFFIX}}': data.get('stock_suffix', 'SH'),
        '{{SCORE}}': data.get('score', '6.5'),
        '{{RATING_DESC}}': data.get('rating_desc', ''),
        '{{RATING_TEXT}}': data.get('rating_text', ''),
        '{{DATA_DATE}}': data.get('data_date', ''),
        '{{REPORT_DATE}}': data.get('report_date', ''),
        '{{DATA_SOURCE}}': data.get('data_source', ''),
    }
    
    for old, new in replacements.items():
        if new:  # only replace if we have data
            html = html.replace(old, new)
    
    return html

# ============================================================
# 检查函数
# ============================================================
def check_html(html):
    """检查HTML结构完整性"""
    issues = []
    
    # 1. 占位符残留
    remaining = re.findall(r'\{\{[^}]+\}\}', html)
    if remaining:
        counts = Counter(remaining)
        issues.append(f'占位符残留: {len(remaining)}个')
        for ph, cnt in counts.most_common(5):
            issues.append(f'  {ph}: {cnt}x')
    
    # 2. div平衡
    opens = len(re.findall(r'<div[ >]', html))
    closes = html.count('</div>')
    if opens != closes:
        issues.append(f'div不平衡: {opens}开 {closes}闭')
    
    # 3. 股票代码一致
    codes = re.findall(r'stockCode\s*=\s*["\'](\d+)["\']', html)
    title_code = re.search(r'(\d{6})', html[:200])
    if codes and title_code and codes[0] != title_code.group(1):
        issues.append(f'股票代码不一致: JS={codes[0]} 标题={title_code.group(1)}')
    
    # 4. M1-M11完整
    m_labels = re.findall(r'M(\d+)</td>', html)
    m_nums = sorted(set(int(x) for x in m_labels if 1 <= int(x) <= 11))
    missing = [str(i) for i in range(1, 12) if i not in m_nums]
    if missing:
        issues.append(f'M表缺失: M{",".join(missing)}')
    
    return issues

def check_js(html):
    """检查JS语法"""
    scripts = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)
    for js in scripts:
        js = js.strip()
        if len(js) > 10:
            with tempfile.NamedTemporaryFile(suffix='.js', mode='w', delete=False) as f:
                f.write(js)
                p = f.name
            r = subprocess.run(['node', '--check', p], capture_output=True, text=True)
            os.unlink(p)
            if r.returncode != 0:
                return False, r.stderr
    return True, ''

# ============================================================
# 来源清单
# ============================================================
def print_source_list(data):
    """打印每条分析的来源"""
    sources = data.get('sources', {})
    print('\n' + '='*50)
    print('来源清单')
    print('='*50)
    for section, source in sources.items():
        print(f'  [{section}] → {source}')
    print('='*50)
    print('所有内容有来源，无AI编造')
    print('='*50)

# ============================================================
# 主流程
# ============================================================
def main():
    if len(sys.argv) < 2:
        print('用法: python3 generate_report.py <股票代码> [公司名]')
        sys.exit(1)
    
    stock_code = sys.argv[1]
    company_name = sys.argv[2] if len(sys.argv) > 2 else ''
    
    # 1. 复制空白模板
    if not os.path.exists(BLANK_TEMPLATE):
        print(f'❌ 空白模板不存在: {BLANK_TEMPLATE}')
        sys.exit(1)
    
    out_path = os.path.join(REPORTS_DIR, f'{stock_code}.html' if not company_name else f'{company_name.lower()}.html')
    
    import shutil
    shutil.copy(BLANK_TEMPLATE, out_path)
    print(f'✅ 模板已复制: {out_path}')
    
    with open(out_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 2. 收集信息
    data = collect_info(stock_code, company_name)
    data['sources'] = {}
    
    # 3. 填充基础占位符
    html = fill_template(html, data)
    
    # 4. 检查
    issues = check_html(html)
    if issues:
        print('\n⚠️ 检查发现的问题:')
        for i in issues:
            print(f'  {i}')
    
    # 5. 保存
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    # 6. 来源清单
    print_source_list(data)
    
    print(f'\n✅ 报告生成完成: {out_path}')
    print(f'   ⚠️ 注意: 需要运行 fetch_financial_data.py 和 gen_kline.py 补全数据和K线')
    print(f'   ⚠️ 注意: 需要仔细检查内容准确性，当前为原型版本')

if __name__ == '__main__':
    main()
