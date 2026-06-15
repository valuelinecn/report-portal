import re

with open('blank-template.html', 'r') as f:
    html = f.read()

# Find the 核心财务指标 table
h3_pos = html.find('<h3>核心财务指标</h3>')
tbl_start = html.find('<table class="tbl">', h3_pos)
tbl_end = html.find('</table>', tbl_start) + 8
tbl = html[tbl_start:tbl_end]

# Process the table
lines = tbl.split('\n')
new_lines = []
for line in lines:
    if '<th>' in line:
        new_lines.append(line)
    elif '<td>' in line:
        # Preserve <tr> and </tr> if present
        has_tr_start = '<tr>' in line
        has_tr_end = '</tr>' in line
        
        # Extract td parts
        parts = re.findall(r'<td[^>]*>.*?</td>', line)
        if len(parts) > 1:
            new_parts = []
            for i, part in enumerate(parts):
                if i == 0:
                    new_parts.append(part)
                else:
                    tag_match = re.match(r'(<td[^>]*>)', part)
                    if tag_match:
                        new_parts.append(tag_match.group(1) + '{{TD}}</td>')
                    else:
                        new_parts.append('<td>{{TD}}</td>')
            new_line = ''.join(new_parts)
            if has_tr_start and not new_line.startswith('<tr>'):
                new_line = '<tr>' + new_line
            if has_tr_end and not new_line.endswith('</tr>'):
                new_line = new_line + '</tr>'
            new_lines.append(new_line)
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

new_tbl = '\n'.join(new_lines)
html = html[:tbl_start] + new_tbl + html[tbl_end:]

with open('blank-template.html', 'w') as f:
    f.write(html)

# Verify
verify = html[html.find('<h3>核心财务指标</h3>'):]
verify = verify[:verify.find('</table>')+8]
print(verify)
