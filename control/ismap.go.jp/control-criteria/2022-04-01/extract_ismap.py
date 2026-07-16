import re, json, csv

with open('ismap-parsed-raw.json') as f:
    entries = json.load(f)

def top_domain(id_str):
    return int(id_str.split('.')[0])

def criteria_type(id_str):
    d = top_domain(id_str)
    if d == 3:
        return 'governance'
    if d == 4:
        return 'management'
    return 'controls'

# Track running domain/category context as we walk the ordered list
domain_title = {}
DOMAIN_TITLE_OVERRIDE = {
    "3": "Governance criteria",
    "4": "Management criteria",
    "5": "Information security policies",
    "6": "Organization of information security",
    "7": "Human resource security",
    "8": "Asset management",
    "9": "Access control",
    "10": "Cryptography",
    "11": "Physical and environmental security",
    "12": "Operations security",
    "13": "Communications security",
    "14": "System acquisition, development and maintenance",
    "15": "Supplier relationships",
    "16": "Information security incident management",
    "17": "Information security aspects of business continuity management",
    "18": "Compliance",
}

category_title = {}
category_objective = {}

rows = []
cur_domain_id = None
cur_category_id = None

for e in entries:
    id_str, depth, text = e['id'], e['depth'], e['text']
    core = re.sub(r'\.(PB|P|B)$', '', id_str)
    segs = core.split('.')

    if depth == 1:
        cur_domain_id = id_str
        domain_title[id_str] = text.split(' Control Objective:')[0].split(' Information security governance')[0]
        # for chapter headers the whole text may include a leading narrative; keep first sentence-ish as title
        # simpler: title = text up to first period if long, else whole text for short titles
        if len(text) > 120:
            domain_title[id_str] = text  # keep raw; will trim in review
        continue

    if depth == 2:
        cur_category_id = id_str
        # split "Title Control Objective: ..." pattern
        m = re.match(r'^(.*?)\s*Control Objective:\s*(.*)$', text)
        if m:
            category_title[id_str] = m.group(1).strip()
            category_objective[id_str] = m.group(2).strip()
        else:
            category_title[id_str] = text
            category_objective[id_str] = ''
        continue

    # depth 3 or 4: a control-level (or sub-control) entry -> emit a row
    dom_id = segs[0]
    cat_id = '.'.join(segs[:2]) if len(segs) >= 2 else segs[0]
    is_cloud_specific = bool(re.search(r'\.(PB|P|B)$', id_str))
    iso_ref = None
    m = re.search(r'ISO/IEC (27\d{3}(?::\d{4})?)', text)
    if m:
        iso_ref = m.group(1)

    rows.append({
        'criteria_type': criteria_type(id_str),
        'domain_id': dom_id,
        'domain_title': DOMAIN_TITLE_OVERRIDE.get(dom_id, domain_title.get(dom_id, '')),
        'category_id': cat_id,
        'category_title': category_title.get(cat_id, ''),
        'control_objective': category_objective.get(cat_id, ''),
        'control_id': id_str,
        'is_cloud_specific': is_cloud_specific,
        'iso_reference': iso_ref or '',
        'control_text': text,
    })

print(f"Total control-level rows: {len(rows)}")

with open('ismap-control-criteria-2022-04-01.json', 'w') as f:
    json.dump(rows, f, indent=2, ensure_ascii=False)

fieldnames = ['criteria_type','domain_id','domain_title','category_id','category_title',
              'control_objective','control_id','is_cloud_specific','iso_reference','control_text']
with open('ismap-control-criteria-2022-04-01.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(rows)

from collections import Counter
print(Counter(r['criteria_type'] for r in rows))
print('cloud-specific count:', sum(1 for r in rows if r['is_cloud_specific']))
