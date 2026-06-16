#!/usr/bin/env python3
"""
fill_manual.py — 交互式手工填写工具

用法:
  python3 fill_manual.py <report.html> --list         列出所有待填项
  python3 fill_manual.py <report.html> --set <NAME> <VALUE>  填入一项
  python3 fill_manual.py <report.html> --status       显示进度
  python3 fill_manual.py <report.html> --fill-all <answers.json>  批量填写
"""
import json, sys, os, re

SKILL_DIR = os.path.expanduser('~/.hermes/skills/software-development/report-fill-workflow')
MANIFEST = os.path.join(SKILL_DIR, 'references', 'manifest.json')

def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def save(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def get_remaining(html, manifest):
    """返回所有待填占位符列表"""
    guidance = manifest.get('guidance', {})
    placeholders = manifest.get('placeholders', {})
    
    # 判断待填优先级: 先auto/construct，再manual
    remaining = []
    for ph in sorted(set(re.findall(r'\{\{[A-Z_0-9]+\}\}', html))):
        name = ph.strip('{}')
        if name == 'TD':
            continue
        info = placeholders.get(name, {})
        ptype = info.get('type', '未知')
        g = guidance.get(name, '')
        
        remaining.append({
            'name': name,
            'placeholder': ph,
            'type': ptype,
            'guidance': g,
            'source': info.get('source', ''),
            'check': info.get('verify_check', ''),
        })
    
    return remaining


def show_list(html_path):
    html = load(html_path)
    with open(MANIFEST) as f:
        manifest = json.load(f)
    
    remaining = get_remaining(html, manifest)
    
    if not remaining:
        print('✅ 所有占位符已填充，无需手动填写')
        return
    
    # 按主题分组
    groups = {
        'BQ': [], '基础信息': [], '综合评价': [], 'LOGIC': [],
        'M1业务': [], 'M2壁垒': [], 'M3管理层': [],
        'M4KPI': [], 'M7KPI': [], '竞争': [],
        '价值理念': [], '三情景': [], '风险': [],
        '亮点': [], '清算': [], 'PE对比': [], '六维': [], '其他': []
    }
    
    GROUP_RULES = [
        ('BQ_ANALYSIS', 'BQ'),
        ('COMPANY_', '基础信息'), ('SCORE', '基础信息'), ('RATING', '基础信息'),
        ('REPORT_DATE', '基础信息'), ('DATA_', '基础信息'), ('INDUSTRY', '基础信息'),
        ('CARD', '综合评价'), ('LABEL_2', '综合评价'), ('LABEL_3', '综合评价'),
        ('LOGIC_', 'LOGIC'),
        ('M1_', 'M1业务'), ('M1_ANALYSIS', 'M1业务'),
        ('MOAT_', 'M2壁垒'), ('CERT_', 'M2壁垒'), ('CUSTOMER_', 'M2壁垒'),
        ('COST_', 'M2壁垒'), ('RESOURCE_', 'M2壁垒'), ('TECH_', 'M2壁垒'),
        ('BARRIER', 'M2壁垒'), ('BRAND_', 'M2壁垒'), ('PRICE_WAR', 'M2壁垒'),
        ('DISRUPTION', 'M2壁垒'), ('DIFF_', 'M2壁垒'), ('FINANCIAL_', 'M2壁垒'),
        ('DEBT_', 'M2壁垒'), ('MARGIN', 'M2壁垒'), ('NET_MARGIN', 'M2壁垒'),
        ('MGMT_', 'M3管理层'),
        ('M4_KPI', 'M4KPI'),
        ('KPI_CARD', 'M7KPI'),
        ('COMPETITOR', '竞争'), ('CORE_BUSINESS', '竞争'),
        ('M1_ANALYSIS', '价值理念'), ('M2_ANALYSIS', '价值理念'),
        ('M3_ANALYSIS', '价值理念'), ('M4_ANALYSIS', '价值理念'),
        ('M5_ANALYSIS', '价值理念'), ('M6_ANALYSIS', '价值理念'),
        ('M7_ANALYSIS', '价值理念'), ('M8_ANALYSIS', '价值理念'),
        ('M9_ANALYSIS', '价值理念'), ('M10_ANALYSIS', '价值理念'),
        ('M11_SAFETY', '价值理念'),
        ('OPTIMISTIC', '三情景'), ('BASE_', '三情景'), ('PESS_', '三情景'),
        ('HIGHLIGHT', '亮点'),
        ('RISK_', '风险'), ('CORE_RISK', '风险'),
        ('LIQ_', '清算'),
        ('PE_COMPARISON', 'PE对比'), ('PE_ANALYSIS', 'PE对比'),
        ('DIM_', '六维'),
    ]
    
    for item in remaining:
        assigned = False
        for keyword, group in GROUP_RULES:
            if keyword in item['name']:
                groups[group].append(item)
                assigned = True
                break
        if not assigned:
            groups['其他'].append(item)
    
    print(f'\n{"="*60}')
    print(f'  待填清单 — 共 {len(remaining)} 项')
    print(f'{"="*60}')
    
    for group_name, items in groups.items():
        if not items:
            continue
        print(f'\n--- {group_name} ({len(items)}项) ---')
        for item in items:
            g = item['guidance']
            if g:
                guidance_short = g[:80] + ('...' if len(g) > 80 else '')
                print(f'  {item["name"]:25s} {guidance_short}')
            else:
                print(f'  {item["name"]:25s} ⚠️ 无引导语')


def set_value(html_path, name, value):
    html = load(html_path)
    ph = '{{' + name + '}}'
    
    if ph not in html:
        print(f'⚠️ 占位符 {ph} 不存在或已被替换')
        return False
    
    html = html.replace(ph, value, 1)
    save(html_path, html)
    print(f'✅ {ph} → {value[:60]}{"..." if len(value) > 60 else ""}')
    return True


def show_status(html_path):
    html = load(html_path)
    with open(MANIFEST) as f:
        manifest = json.load(f)
    
    remaining = get_remaining(html, manifest)
    total = len(remaining)
    
    # 计算已填数量
    all_phs = set(re.findall(r'\{\{[A-Z_0-9]+\}\}', load(html_path)))
    # 从manifest中获取所有非TD占位符
    manifest_phs = set(manifest['placeholders'].keys()) - {'TD'}
    filled = len(manifest_phs - all_phs)
    total_phs = len(manifest_phs)
    
    pct = filled / total_phs * 100 if total_phs > 0 else 0
    
    print(f'\n{"="*50}')
    print(f'  填写进度')
    print(f'{"="*50}')
    print(f'  总占位符: {total_phs}')
    print(f'  已填写:   {filled} ({pct:.0f}%)')
    print(f'  待填写:   {total}')
    if total > 0:
        # 按类型统计
        by_type = {}
        for item in remaining:
            t = item['type']
            by_type[t] = by_type.get(t, 0) + 1
        print(f'\n  按类型:')
        for t, c in sorted(by_type.items(), key=lambda x: -x[1]):
            print(f'    {t}: {c}')
    
    return total


def batch_fill(html_path, answers_path):
    with open(answers_path, 'r', encoding='utf-8') as f:
        answers = json.load(f)
    
    html = load(html_path)
    filled = 0
    errors = []
    
    for name, value in answers.items():
        ph = '{{' + name + '}}'
        if ph in html:
            html = html.replace(ph, value, 1)
            filled += 1
        else:
            errors.append(name)
    
    save(html_path, html)
    print(f'✅ 批量填写完成: {filled} 项成功')
    if errors:
        print(f'⚠️ 未找到: {errors}')


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    
    html_path = sys.argv[1]
    if not os.path.exists(html_path):
        print(f'文件不存在: {html_path}')
        sys.exit(1)
    
    cmd = sys.argv[2]
    
    if cmd == '--list':
        show_list(html_path)
    
    elif cmd == '--set':
        if len(sys.argv) < 4:
            print('用法: fill_manual.py <html> --set <NAME> "<VALUE>"')
            sys.exit(1)
        name = sys.argv[3]
        value = sys.argv[4] if len(sys.argv) > 4 else ''
        set_value(html_path, name, value)
    
    elif cmd == '--status':
        show_status(html_path)
    
    elif cmd == '--fill-all':
        if len(sys.argv) < 4:
            print('用法: fill_manual.py <html> --fill-all <answers.json>')
            sys.exit(1)
        batch_fill(html_path, sys.argv[3])
    
    else:
        print(f'未知命令: {cmd}')
        print(__doc__)
        sys.exit(1)


if __name__ == '__main__':
    main()
