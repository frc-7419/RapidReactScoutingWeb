# convert entries in main to json

output = "entries.json"

from main import entries
import json

done = []

for entry in entries:
    t = dict(entry._asdict())
    for a in range(len(t['entries'])):
        t['entries'][a] = dict(t['entries'][a]._asdict())
    done.append(t)

with open(output, 'w') as f:
    f.write(json.dumps(done, indent=4))