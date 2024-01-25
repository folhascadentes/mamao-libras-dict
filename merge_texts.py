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

for file in sorted(os.listdir("texts")):
    with open(f"texts/{file}", "r") as f:
        for line in f.read().split("\n"):
            normalized_line = (
                unicodedata.normalize("NFKD", line)
                .encode("ascii", "ignore")
                .decode("ascii")
            ).lower()

            if not detect_header(normalized_line) and len(normalized_line) > 3:
                lines.append(line)

processed_lines = []

for index, line in enumerate(lines):
    if index > 0 and (
        "(" not in line
        or ":" not in line
        or (processed_lines[-1][-1] != ")" and processed_lines[-1][-1] != ".")
    ):
        processed_lines[-1] = processed_lines[-1] + " " + line
    elif not is_first_word_upper(line):
        processed_lines[-1] = processed_lines[-1] + " " + line
    else:
        processed_lines.append(line)

for line in processed_lines:
    print(line)
