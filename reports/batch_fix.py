#!/usr/bin/env python3
"""
批量修改前7个报告的大师理念表布局：
1. CSS: 在.tbl td{...}后追加3条规则
2. HTML: 在大师理念列的名称和「理念」之间加<br>
"""
import os
import re

BASE = '/data/data/com.termux/files/home/.hermes/hermes-agent/report-portal/reports'
FILES = ['byd.html', 'maotai.html', 'ningde.html', 'zhaoshang.html', 
         'pingan.html', 'wuliangye.html', 'yili.html']

CSS_OLD = '.tbl td{padding:6px 5px;text-align:center;border-bottom:1px solid #1e1e3a}'
CSS_NEW = '''.tbl td{padding:6px 5px;text-align:center;border-bottom:1px solid #1e1e3a}
.tbl td:first-child{white-space:nowrap}
.tbl td:nth-child(2){white-space:nowrap}
.tbl td:nth-child(3){text-align:left;font-size:11px}'''

def fix_css(content):
    """Replace the .tbl td line with extended version"""
    if CSS_OLD in content:
        content = content.replace(CSS_OLD, CSS_NEW, 1)
        print("  CSS: replaced .tbl td rule")
    else:
        print("  CSS: pattern NOT FOUND!")
    return content

def fix_html_rows(content):
    """Add <br> between master name and 「philosophy」 in all rows"""
    # Pattern: <td>NAME「PHILOSOPHY」</td> -> <td>NAME<br>「PHILOSOPHY」</td>
    count = 0
    # Match any <td> with content ending in 「...」
    pattern = r'(<td>)([^<]+?)「([^」]+)」(<\/td>)'
    
    def replacer(m):
        nonlocal count
        count += 1
        return m.group(1) + m.group(2) + '<br>「' + m.group(3) + '」' + m.group(4)
    
    new_content = re.sub(pattern, replacer, content)
    print(f"  HTML: replaced {count} rows")
    if count == 0:
        print("  WARNING: No rows were modified!")
    return new_content

def main():
    for fname in FILES:
        fpath = os.path.join(BASE, fname)
        print(f"\n=== {fname} ===")
        
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        content = fix_css(content)
        content = fix_html_rows(content)
        
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  Done: {fpath}")

if __name__ == '__main__':
    main()
