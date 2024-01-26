import json
import os

files = sorted(os.listdir("json"))
signs = {}
count = 0

for file in files:
    try:
        with open("json/" + file, "r", encoding="utf-8") as f:
            data = json.load(f)
            for sign in data:
                try:
                    signs[sign["id"].upper()] = {
                        "region": sign["region"].split(", "),
                        "parameters": sign["parameters"],
                        "example": sign["example"],
                        "grammatial": sign["grammatical"],
                        "translation": sign["translation"],
                    }
                except:
                    print(sign["id"])
    except:
        print(file)
        count += 1

print(count)

# save the signs to a json file
with open("signs.json", "w", encoding="utf-8") as f:
    json.dump(signs, f, indent=4, ensure_ascii=False)
