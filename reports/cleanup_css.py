#!/usr/bin/env python3
"""Remove duplicate .tbl td CSS rules from files that batch_fix.py ran on twice."""
import re

BASE = '/data/data/com.termux/files/home/.hermes/hermes-agent/report-portal/reports'
FILES = ['byd.html', 'maotai.html', 'ningde.html', 'zhaoshang.html', 
         'pingan.html', 'wuliangye.html', 'yili.html']

def clean_duplicates(content):
    """Remove extra copies of the three tbl td rules."""
    # We want to keep ONE block of:
    # .tbl td{...}
    # .tbl td:first-child{white-space:nowrap}
    # .tbl td:nth-child(2){white-space:nowrap}
    # .tbl td:nth-child(3){text-align:left;font-size:11px}
    
    # Find all groups and remove extras
    # Pattern: .tbl td:first-child{...} followed by optional .tbl td:nth-child... 
    # Remove ALL occurrences after the first one
    patterns = [
        r'\.tbl td:first-child\{white-space:nowrap\}',
        r'\.tbl td:nth-child\(2\)\{white-space:nowrap\}',
        r'\.tbl td:nth-child\(3\)\{text-align:left;font-size:11px\}',
    ]
    
    for pat in patterns:
        # Replace all but the first occurrence
        first = True
        def replacer(m):
            nonlocal first
            if first:
                first = False
                return m.group(0)  # keep first
            return ''  # remove extras
        
        content = re.sub(pat, replacer, content)
    
    return content

def main():
    for fname in FILES:
        fpath = f'{BASE}/{fname}'
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        before = content.count('td:first-child{white-space:nowrap}')
        content = clean_duplicates(content)
        after = content.count('td:first-child{white-space:nowrap}')
        
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f'{fname}: {before}→{after} copies')

if __name__ == '__main__':
    main()
