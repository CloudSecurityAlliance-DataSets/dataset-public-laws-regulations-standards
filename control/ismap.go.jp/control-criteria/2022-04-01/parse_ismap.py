import re, json

with open('ismap-control-criteria-2022-04-01-raw.txt') as f:
    lines = f.readlines()

# Restrict to Chapter 3 (Governance) through end of Chapter 5 (Controls), before Reference 2 notes
start = None
end = None
for i, l in enumerate(lines):
    if l.strip() == 'Chapter 3          Governance criteria' and start is None and i > 100:
        start = i
    if l.strip().startswith('(Appendix 1) Points to be noted in the selection of detailed controls') and i > 100:
        end = i
        break

body = lines[start:end]

# ID pattern: digits separated by dots, optional trailing .P / .B / .PB, at start of (stripped) line,
# followed by whitespace and more content on same line (title/desc start).
id_re = re.compile(r'^(\d+(?:\.\d+){0,5}(?:\.(?:PB|P|B))?)\s+(.*)$')
chapter_re = re.compile(r'^(\d+)\s+([a-zA-Z].*)$')  # e.g. "5   Information security policies"

entries = []
current = None

def depth(id_str):
    # count numeric segments, ignoring trailing PB/P/B letter suffix
    core = re.sub(r'\.(PB|P|B)$', '', id_str)
    return core.count('.') + 1

for raw in body:
    line = raw.rstrip('\n')
    stripped = line.strip()
    if not stripped:
        continue
    if re.match(r'^\d+$', stripped):
        continue  # page number
    m = id_re.match(stripped)
    if m and (m.group(1)[0].isdigit()):
        id_str, rest = m.group(1), m.group(2)
        # heuristic: avoid false positives where id_str is actually a plain page-ish number with no dots and rest starts lowercase mid-sentence
        current = {'id': id_str, 'depth': depth(id_str), 'text': rest.strip()}
        entries.append(current)
    else:
        if current is not None:
            current['text'] += ' ' + stripped

# Clean whitespace
for e in entries:
    e['text'] = re.sub(r'\s+', ' ', e['text']).strip()

print(f"Total entries: {len(entries)}")
with open('ismap-parsed-raw.json', 'w') as f:
    json.dump(entries, f, indent=2, ensure_ascii=False)

# Print a sample distribution by depth
from collections import Counter
print(Counter(e['depth'] for e in entries))
