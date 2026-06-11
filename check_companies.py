import sys, re

content = sys.stdin.buffer.read().decode('utf-8')

# Find COMPANIES array
idx = content.find('const COMPANIES')
if idx > 0:
    arr_end = content.find('];', idx)
    companies_js = content[idx:arr_end+2]
    
    # Extract all company entries
    entries = re.findall(r"\{[^}]+\}", companies_js)
    print(f"Total companies: {len(entries)}")
    for e in entries:
        name = re.search(r"name:'([^']+)'", e)
        file = re.search(r"file:'([^']+)'", e)
        print(f"  {name.group(1) if name else '?'} -> {file.group(1) if file else '?'}")
    
    # Check if seres is there
    if 'seres' in companies_js:
        print("\n✅ seres found in COMPANIES")
    else:
        print("\n❌ seres NOT in COMPANIES!")
