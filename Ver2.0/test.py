import json
from time import time

start = time()

with open(f"data\en_us\set1.json", "r", encoding = "utf8") as f:
    data = json.load(f)

for card in data:
    print(card["name"])

end = time()
print(end - start)
