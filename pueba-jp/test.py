import re

QUERIED = re.compile("(?i)Queried\s+(\d+)(\.\d+)?\s+seconds?\s+ago")

print QUERIED.match("queried 0 seconds ago")