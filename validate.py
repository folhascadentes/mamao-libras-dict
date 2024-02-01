from openai import OpenAI
import concurrent.futures

# Assuming OpenAI is correctly initialized
client = OpenAI()

system = """Given a description of a Libras sign, extract the parameters and format in JSON."""

# Load texts from a file
with open("parameters5.out", "r") as file:
    texts = file.read().split("\n")


def make_api_call(text):
    response = client.chat.completions.create(
        model="ft:gpt-3.5-turbo-1106:personal::8nZTEWft",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": text},
        ],
        temperature=0.0,
        top_p=1,
    )
    return text, response.choices[0].message.content


# Use ThreadPoolExecutor to parallelize the API calls
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    # Map texts to the executor
    future_to_text = {executor.submit(make_api_call, text): text for text in texts}
    for future in concurrent.futures.as_completed(future_to_text):
        text, response_content = future.result()
        print(text)
        print()
        print("```json")
        print(response_content)
        print("```")
        print()
