import re

with open('blank-template.html', 'r') as f:
    html = f.read()

# Find all tables and their surrounding context to identify which ones to clean
# List all tables with their preceding h3 text
pos = 0
table_info = []
while True:
    tbl_start = html.find('<table class="tbl">', pos)
    if tbl_start < 0:
        break
    # Find the preceding h3
    before = html[max(0, tbl_start-300):tbl_start]
    h3 = re.findall(r'<h3>([^<]+)</h3>', before)
    label = h3[-1] if h3 else 'unknown'
    
    tbl_end = html.find('</table>', tbl_start) + 8
    tbl = html[tbl_start:tbl_end]
    # Get structure info
    rows = tbl.split('\n')
    first_row_cells = re.findall(r'<t[dh][^>]*>([^<]*)</t[dh]>', rows[0]) if rows else []
    table_info.append((label, tbl_start, tbl_end))
    pos = tbl_end

for label, start, end in table_info:
    print(f'  "{label}" at offset {start}')
PYEOF