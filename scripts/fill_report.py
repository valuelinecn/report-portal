#!/usr/bin/env python3
"""
fill_report.py — 统一报告填充脚本

依赖: fill_auto.py 已执行完毕 (reports/{code}.html 已生成)
用法: python3 fill_report.py <股票代码>
"""
import json, os, re, sys

PORTAL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL_DIR = os.path.expanduser('~/.hermes/skills/software-development/report-fill-workflow')
MANIFEST = os.path.join(SKILL_DIR, 'references', 'manifest.json')

def load_manifest():
    with open(MANIFEST) as f:
        return json.load(f)

def get_fin_data(code):
    """从报告HTML中提取fin-table数据"""
    html_path = os.path.join(PORTAL_DIR, 'reports', f'{code}.html')
    if not os.path.exists(html_path):
        print(f'❌ 报告不存在: {html_path}')
        print('   先运行: python3 scripts/fill_auto.py {code}')
        sys.exit(1)
    with open(html_path) as f:
        c = f.read()
    
    # 解析fin-table
    import csv, io
    fin = {}
    # 用正则提取关键财务指标
    patterns = {
        'PE': r'PE\(TTM\)[^<]*<[^>]*>([^<]+)',
        'PB': r'PB[^<]*<[^>]*>([^<]+)',
        'REV_2025': r'营业收入.*?2025[^<]*<[^>]*>(\d+\.?\d*)',
        'NP_2025': r'净利润.*?2025[^<]*<[^>]*>(\d+\.?\d*)',
        'ROE': r'ROE[^%]*?(\d+\.?\d*)%',
    }
    return c


def fill_all(code):
    """填充报告"""
    html_path = os.path.join(PORTAL_DIR, 'reports', f'{code}.html')
    with open(html_path, encoding='utf-8') as f:
        c = f.read()
    
    manifest = load_manifest()
    guidance = manifest.get('guidance', {})
    
    filled = 0
    skipped = 0
    
    # Phase 1: 自动填充 (auto类，不需要分析的)
    # 日期/来源等
    auto_fills = {
        'REPORT_DATE': '2026.06.17',
        'DATA_DATE': '2026-06-17',
        'DATA_SOURCE': '2025年报 + fin-table API',
    }
    for k, v in auto_fills.items():
        ph = '{{' + k + '}}'
        if ph in c:
            c = c.replace(ph, v, 1)
            filled += 1
    
    # Phase 2: 清理模板示例行
    for pat in ['目标公司', '同行A', '同行B']:
        idx = c.find(f'<div class="hb"><span class="hl">{pat}</span>')
        if idx >= 0:
            end = c.find('</div>', c.find('</div></div>', idx) + 6) + 6
            c = c[:idx] + c[end:]
    
    # Phase 3: 清理旧注释和残留样式
    c = c.replace('<!-- PE比较条使用dim-row样式，参考下方格式 -->', '')
    c = c.replace('<!-- PE比较条使用hl/ht/hf样式（匹配M2壁垒），参考下方格式） -->', '')
    
    # Phase 4: 清理dim-sc残留（从之前的修复脚本中遗留）
    c = re.sub(r'<div class="dim-sc[^>]*>[^<]*</div>', '', c)
    c = re.sub(r'(<div class="hb">.*?</div></div></div>)</div>', r'\1', c)
    
    # Phase 5: 列出待填项
    remaining = set(re.findall(r'\{\{[A-Z_0-9]+\}\}', c))
    # 排除TD
    remaining = {p for p in remaining if p != '{{TD}}'}
    
    print(f'\n{"="*50}')
    print(f'  fill_report.py — {code}')
    print(f'  已自动填充: {filled} 项')
    print(f'  模板清理: 完成')
    print(f'  剩余待填: {len(remaining)} 项')
    print(f'{"="*50}\n')
    
    if remaining:
        print('仍需手动的项（列出前20项，含引导语）:')
        for i, ph in enumerate(sorted(remaining)):
            if i >= 20:
                print(f'  ... 还有{len(remaining)-20}项')
                break
            name = ph.strip('{}')
            g = guidance.get(name, '')
            g_short = g[:60] + '...' if len(g) > 60 else g
            print(f'  {ph:30s} → {g_short}')
    
    # Phase 6: 写入
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(c)
    
    # Phase 7: TODO统计
    todo = c.count('__TODO__')
    if todo > 0:
        print(f'\n⚠️ 还有 {todo} 个TODO标记（在12张表中），需整表替换')
        print(f'   运行: grep -c "__TODO__" reports/{code}.html')
    
    return remaining, todo


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'用法: python3 {sys.argv[0]} <股票代码>')
        print(f'示例: python3 {sys.argv[0]} 600183')
        sys.exit(1)
    
    code = sys.argv[1]
    remaining, todo = fill_all(code)
    
    print(f'\n下一步:')
    print(f'  1. fill_manual.py reports/{code}.html --list  查看待填')
    print(f'  2. 逐项填写 (--set)')
    print(f'  3. grep -c "__TODO__" reports/{code}.html  确认TODO=0')
    print(f'  4. verify_report.py reports/{code}.html  验证通过')
