import re

with open('blank-template.html', 'r') as f:
    html = f.read()

# Find the financial table and clear all data cells
# The fin-table has: first column = metric name, subsequent columns = yearly data

def clean_fin_table(match):
    table = match.group(0)
    lines = table.split('\n')
    new_lines = []
    for line in lines:
        # Keep header row (contains <th>)
        if '<th>' in line:
            new_lines.append(line)
            continue
        # For data rows, keep first <td> (metric name), clear rest
        if '<tr>' in line or '</tr>' in line:
            new_lines.append(line)
            continue
        if '<td>' in line:
            # Split by td boundaries
            parts = re.findall(r'<td[^>]*>.*?</td>', line)
            if parts:
                new_parts = []
                for i, part in enumerate(parts):
                    if i == 0:
                        # Keep first td (metric name)
                        new_parts.append(part)
                    else:
                        # Replace content with empty
                        new_parts.append(re.sub(r'>.*?</td>', '></td>', part))
                new_line = line
                for old, new in zip(parts, new_parts):
                    new_line = new_line.replace(old, new, 1)
                new_lines.append(new_line)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
    return '\n'.join(new_lines)

# Apply to fin-table
html = re.sub(
    r'<table class="fin-table">.*?</table>',
    clean_fin_table,
    html,
    flags=re.DOTALL
)

# Now do the same for ALL <table class="tbl"> tables
# These include: M1 annual, M1 revenue, M3 management, M5 cost, M5 bargaining,
# M7 industry, M7 competitors, M8 catalyst, M10 risk, M10 sensitivity,
# M10 checklist, M10 liquidation, M10 M-table

def clean_tbl_table(match):
    table = match.group(0)
    lines = table.split('\n')
    new_lines = []
    for line in lines:
        # Keep header rows (contain <th>)
        if '<th>' in line:
            new_lines.append(line)
            continue
        # For data rows, keep first <td>, clear rest
        if '<td>' in line:
            parts = re.findall(r'<td[^>]*>.*?</td>', line)
            if len(parts) > 1:
                new_parts = []
                for i, part in enumerate(parts):
                    if i == 0:
                        new_parts.append(part)  # Keep first td
                    else:
                        new_parts.append(re.sub(r'>.*?</td>', '></td>', part))  # Clear others
                new_line = line
                for old, new in zip(parts, new_parts):
                    new_line = new_line.replace(old, new, 1)
                new_lines.append(new_line)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
    return '\n'.join(new_lines)

html = re.sub(
    r'<table class="tbl">.*?</table>',
    clean_tbl_table,
    html,
    flags=re.DOTALL
)

# Verify
import re
# Check fin-table
fin = re.search(r'<table class="fin-table">.*?</table>', html, re.DOTALL)
if fin:
    lines = fin.group().split('\n')
    for line in lines[:15]:
        cells = re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', line)
        if cells:
            print(' | '.join(c[:10] for c in cells))

print('\n=== tbl tables ===')
tbls = re.findall(r'<table class="tbl">.*?</table>', html, re.DOTALL)
for i, tbl in enumerate(tbls[:3]):
    lines = tbl.split('\n')
    for line in lines[:3]:
        cells = re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', line)
        if cells:
            print(f'Table {i}: {" | ".join(c[:10] for c in cells[:5])}')

with open('blank-template.html', 'w') as f:
    f.write(html)
print('\nDone')
