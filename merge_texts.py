import os
import unicodedata


def detect_header(text):
    header_keywords = "dicionario lingua sinais brasil libras suas maos".split()
    author_names = (
        "fernando capovilla walkiria raphael janice temoteo antonielle martins".split()
    )

    def count_occurrences(word_list):
        return sum(word in text for word in word_list)

    if count_occurrences(header_keywords) >= 6 or count_occurrences(author_names) >= 6:
        return True

    return False


def is_first_word_upper(sentence):
    first_word = sentence.split()[0]
    return first_word.isupper()


lines = []

# clean header and page numbers
for file in sorted(os.listdir("raw_texts")):
    with open(f"raw_texts/{file}", "r") as f:
        for line in f.read().split("\n"):
            normalized_line = (
                unicodedata.normalize("NFKD", line)
                .encode("ascii", "ignore")
                .decode("ascii")
            ).lower()

            if not detect_header(normalized_line) and len(normalized_line) > 3:
                lines.append(line)


# Merge lines
text = list(" ".join(lines))
line = ""
buffer = ""
hand_found = False
lines_merged = []


# Look for the "mão" pattern and the ) terminator to break line
for c in text:
    line += c
    buffer += c
    buffer = buffer[-4:]

    if buffer == " mão" or buffer == " Mão" or buffer == "(Mão" or buffer == "(mão":
        hand_found = True

    if hand_found and (buffer[-2:] == ".)" or buffer[-2:] == ")."):
        lines_merged.append(line.strip())
        hand_found = False
        line = ""

if line != "":
    lines_merged.append(line)


# Fix etimology content
for index, line in enumerate(lines_merged):
    parts = line.split()

    if "etimologia" not in parts[0].lower().strip():
        print(line, end="")

    if "etimologia" in parts[0].lower().strip():
        index = line.find("(sinal") or line.find("(usado")

        if index != -1:
            etymology_part = line[:index].split(".")
            remaining_part = etymology_part[-1] + " " + line[index:]
            etymology_part = ".".join(etymology_part[:-1]) + "."

            print("", etymology_part)

            if remaining_part.strip() != "":
                print(remaining_part.strip(), end="")

    elif index + 1 < len(lines_merged):
        next_line = lines_merged[index + 1]
        next_line_parts = next_line.split()

        if "etimologia" not in next_line_parts[0].lower().strip():
            print(next_line_parts[0].lower().strip())
