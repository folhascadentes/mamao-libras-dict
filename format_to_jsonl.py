import json
import re


def parse_input(input_text):
    # Split the input text into parts separated by '```json' and '```'
    parts = re.split(r"```json|```", input_text)

    # Filter out empty strings
    parts = [part.strip() for part in parts if part.strip()]

    # Initialize the result structure
    results = []

    # Process each part
    for i in range(0, len(parts), 2):
        description = parts[i]
        json_content = parts[i + 1]

        result = {"messages": []}
        result["messages"].append(
            {
                "role": "system",
                "content": "Given a description of a Libras sign, extract the parameters and format in JSON.",
            }
        )
        result["messages"].append(
            {"role": "user", "content": description.split(" : ")[-1]}
        )
        result["messages"].append({"role": "assistant", "content": json_content})

        results.append(result)

    return results


# Sample input
input_text = open("notes2.md", "r", encoding="utf-8").read()

output = parse_input(input_text)

for o in output:
    print(json.dumps(o, ensure_ascii=False))
