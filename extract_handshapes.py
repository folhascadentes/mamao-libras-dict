import re


words = set()

with open("filtered.out", "r") as f:
    descriptions = f.read().split("\n")

    for description in descriptions:
        pattern = r"mãos? [^,.]*[,.]"

        match = re.findall(pattern, description, re.IGNORECASE)
        if len(match):
            print(match)
            for m in match:
                for word in m.split(" "):
                    if word:
                        words.add(re.sub(r"[^a-zA-Z0-9]", "", word).upper())
        else:
            print(description.split(":")[0], "####", "Not specified")

print("#################")
for word in sorted(words):
    if len(word) < 2:
        print(word)
