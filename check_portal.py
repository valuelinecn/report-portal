import sys, re

content = sys.stdin.buffer.read().decode('utf-8')

# Find all report links
links = re.findall(r'href=[\'"]([^\'"]*reports[^\'"]*)[\'"]', content)
print('Report links found:')
for l in links:
    print(f'  {l}')

# Check if reports are loaded from a JS file
scripts = re.findall(r'src=[\'"]([^\'"]*\.js)[\'"]', content)
print(f'\nJS files:')
for s in scripts:
    print(f'  {s}')

# Check reports tab/dropdown
idx = content.find('研究报告')
if idx < 0:
    idx = content.find('reports')
if idx > 0:
    section = content[idx:idx+3000]
    # Find report names
    report_names = re.findall(r'([\u4e00-\u9fff]{2,6}(?:集团|股份)?(?:[A-Z])?)', section)
    print(f'\nReport names in section around 研究报告:')
    print(section[:500])
