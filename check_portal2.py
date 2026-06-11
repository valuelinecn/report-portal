import sys, re

content = sys.stdin.buffer.read().decode('utf-8')

# Look for the full HTML to understand the structure
# Find where the report listing or navigation is
for marker in ['报告列表', '企业列表', 'report-list', 'report-grid', 'card', 'reports"', "reports'"]:
    idx = content.find(marker)
    if idx >= 0:
        print(f"Found '{marker}' at position {idx}")
        print(content[max(0,idx-100):idx+500])
        print("---")

# Check if there's inline JS that builds report list
scripts = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
for i, s in enumerate(scripts):
    if 'report' in s.lower() or 'reports' in s.lower():
        print(f"\nScript #{i} contains 'report':")
        print(s[:600])
        print("---")
