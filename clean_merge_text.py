import unicodedata


def unicode_to_ascii_unicodedata(s):
    normalized = unicodedata.normalize("NFKD", s)
    ascii_str = normalized.encode("ascii", "ignore").decode("ascii")
    return ascii_str


letters = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
]

letter_index = -1

with open("merge.out", "r") as f:
    lines = f.read().split("\n")

    for line in lines:
        parts = line.split()

        if parts[0] == letters[letter_index + 1] + ",":
            letter_index += 1
            print(line)
        else:
            for index, part in enumerate(parts):
                if (
                    unicode_to_ascii_unicodedata(part[0].upper())
                    != letters[letter_index]
                ):
                    continue

                upper_count = 0
                for c in part:
                    if c.isupper():
                        upper_count += 1

                if upper_count > 0 and upper_count / len(part) > 0.60:
                    print(" ".join(parts[index:]))
                    break

# count = 0

# with open("signs.out", "r") as f:
#     lines = f.read().split("\n")
#     processed_lines = []
#     for line in lines:
#         if line.count("sinal usado") > 1:
#             print(line)
#             count += line.count("sinal usado")

# print(count)
