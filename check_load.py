import sys, re

content = sys.stdin.buffer.read().decode('utf-8')

# Find the function that loads reports
idx = content.find('function loadReport')
if idx < 0:
    idx = content.find('function openReport')
if idx < 0:
    idx = content.find('.html')
    
# Find all scripts
scripts = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
for i, s in enumerate(scripts):
    # Check for report-loading code
    if 'fetch' in s or 'load' in s.lower() or 'report' in s.lower():
        print(f"=== Script #{i} (relevant) ===")
        # Print lines that mention report, load, fetch, iframe
        lines = s.split('\n')
        for line in lines:
            if any(kw in line.lower() for kw in ['fetch', 'report', 'load', 'iframe', 'open']):
                if len(line.strip()) > 5:
                    print(f"  {line.strip()[:150]}")
        print()
