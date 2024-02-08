with open("merge2.out", "r") as f:
    lines = f.read().split("\n")

    for line in lines:
        parts = line.split()

        for index, part in enumerate(parts):
            upper_count = 0
            for c in part:
                if c.isupper():
                    upper_count += 1

            if upper_count > 0 and upper_count / len(part) > 0.60:
                print(" ".join(parts[index:]))
                break
