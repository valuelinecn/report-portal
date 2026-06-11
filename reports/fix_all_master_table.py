#!/usr/bin/env python3
"""
Add <br> between master name and 「philosophy」 in ALL rows that don't have it.
Handles all 14 reports (excl seres which is already correct).
"""
import re, os

BASE = '/data/data/com.termux/files/home/.hermes/hermes-agent/report-portal/reports'
FILES = ['byd.html', 'maotai.html', 'ningde.html', 'zhaoshang.html', 
         'pingan.html', 'wuliangye.html', 'yili.html',
         'haitian.html', 'mindray.html', 'lixun.html', 'fuyao.html', 
         'hengrui.html', 'haikang.html', 'zhongjixuchuang.html']

def fix_rows(content):
    """Add <br> between name and 「philosophy」 in rows that lack it."""
    # Pattern: <td>NAME「PHILOSOPHY」</td> (no <br> between name and 「)
    count = 0
    # Match rows where name and 「」 are directly adjacent (no <br> in between)
    pattern = r'(<td>)([^<]+?)「([^」]+)」(\s*</td>)'
    
    def replacer(m):
        nonlocal count
        count += 1
        return m.group(1) + m.group(2) + '<br>「' + m.group(3) + '」' + m.group(4)
    
    new_content = re.sub(pattern, replacer, content)
    return new_content, count

total_fixed = 0
for fname in FILES:
    fpath = os.path.join(BASE, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content, n = fix_rows(content)
    if n > 0:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'✅ {fname}: fixed {n} rows')
        total_fixed += n
    else:
        print(f'⏭️ {fname}: already correct (0 rows to fix)')

print(f'\nTotal: {total_fixed} rows fixed across {len(FILES)} files')
