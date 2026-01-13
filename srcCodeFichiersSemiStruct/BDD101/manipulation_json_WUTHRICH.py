import json

f = open('data.json')

data = json.load(f)
f.close

print(data)

print(data["features"])

print(data["features"][0]["geometry"])

for i in data["features"]:
    print(i["geometry"]["coordinates"][0])

data["features"][0]["geometry"]["coordinates"][0] = 72.0
print(data["features"][0]["geometry"]["coordinates"][0])

data["ville"] = "strasbourg"

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)