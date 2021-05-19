import json

with open("userdata\data.json", "r", encoding = "utf8") as f:
    data = json.load(f)

user = "abc"

if (user not in data):
    data[user] = ""

with open("userdata\data.json", "w", encoding = "utf8") as f:
    json.dump(data, f, indent = 4)