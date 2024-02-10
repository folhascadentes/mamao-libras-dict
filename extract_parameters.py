from openai import OpenAI
import concurrent.futures
import os  # Import the os module

client = OpenAI()

system = """Given a description of a Libras sign, extract the parameters and format in JSON."""

with open("signs_splited.out", "r") as file:
    texts = file.read().split("\n")


def make_api_call(text, index):
    filename = f"tmp/response_{index}.txt"
    if not os.path.exists(filename):
        response = client.chat.completions.create(
            model="ft:gpt-3.5-turbo-1106:personal::8pdI51i3",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": text},
            ],
            temperature=0.0,
            top_p=1,
        )
        with open(filename, "w") as file:
            file.write(
                text
                + "\n\n"
                + "```json\n"
                + response.choices[0].message.content
                + "\n```"
            )
    else:
        print(f"{filename} already exists. Skipping API call.")
    return filename


with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    future_to_text = {
        executor.submit(make_api_call, text, index): text
        for index, text in enumerate(texts)
    }
    for future in concurrent.futures.as_completed(future_to_text):
        filename = future.result()
        if os.path.exists(filename):
            print(f"Output written to {filename}")
