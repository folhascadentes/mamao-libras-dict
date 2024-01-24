import os

from botocore.exceptions import ClientError
from openai import OpenAI
import boto3
import concurrent.futures
import fitz
import json
import time

# Utils


def pdf_to_img(pdf_path):
    doc = fitz.open(pdf_path)
    filename = pdf_path.split("/")[-1].split(".")[0]

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        image_list = page.get_images(full=True)

        if image_list:
            image_index = image_list[0][0]
            base_image = doc.extract_image(image_index)
            page_num_index = str(page_num).zfill(3)
            output_filename = f"images/{filename}-{page_num_index}.png"

            with open(output_filename, "wb") as image_file:
                image_file.write(base_image["image"])

    doc.close()


def initialize_textract_client():
    return boto3.client(
        "textract",
        region_name="us-east-1",
    )


def analyze_document(client, document_path):
    with open(document_path, "rb") as document:
        image_bytes = document.read()

    response = client.analyze_document(
        Document={"Bytes": image_bytes},
        FeatureTypes=["LAYOUT"],
    )

    text = ""

    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            text += item["Text"] + "\n"

    return text


# Main functions


def pdfs_to_imgs(pdfs_dir):
    files = sorted(os.listdir(pdfs_dir))

    for file in files:
        file_path = f"{pdfs_dir}/{file}"
        if not os.path.exists(file_path):
            pdf_to_img(file_path)


def imgs_to_txt(images_dir):
    images = sorted(os.listdir(images_dir))
    client = initialize_textract_client()

    def process_image(image):
        filename = f"{image.split('.')[0]}.txt"
        file_path = f"raw_texts/{filename}"

        if os.path.exists(file_path):
            return

        max_retries = 5  # Maximum number of retries
        retry_delay = 1  # Initial retry delay in seconds

        for _ in range(max_retries):
            try:
                text = analyze_document(client, f"{images_dir}/{image}")
                with open(file_path, "w") as f:
                    f.write(text)
                break  # Break the loop if successful
            except ClientError as e:
                if (
                    e.response["Error"]["Code"]
                    == "ProvisionedThroughputExceededException"
                ):
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    raise  # Reraise if a different exception occurred

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(process_image, images)


def raw_txt_to_formatted_txt(raw_txt_dir):
    client = OpenAI()
    system = """I have extracted text from various documents using OCR. The text is currently in a series of lines without proper paragraph formatting. Please format these lines into well-structured paragraphs."""

    files = sorted(os.listdir(raw_txt_dir))

    def process_file(file):
        file_path = f"texts/{file}"

        if os.path.exists(file_path):
            return

        with open(f"{raw_txt_dir}/{file}", "r") as f:
            text = f.read()

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": system,
                    },
                    {
                        "role": "user",
                        "content": text,
                    },
                ],
                temperature=0.0,
                top_p=1,
            )

            with open(file_path, "w") as f_out:
                f_out.write(response.choices[0].message.content)

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(process_file, files)


def formatted_txt_to_json(txt_dir):
    client = OpenAI()
    system = """
Process the provided text excerpts to create a structured JSON object. Each entry in the JSON should represent a sign from Brazilian Sign Language (Libras), as described in the text. For each entry, the key should be the name of the sign, and the value should be a detailed description of the sign, including its meaning and physical gesture. Exclude any text that is not directly related to the description of the signs. Ensure that the JSON output is well-formatted and adheres to standard JSON syntax rules.

Input Example:

Text containing various descriptions of signs from the 'Dicionário da Língua de Sinais do Brasil: A Libras em suas mãos', excluding non-relevant details like author names and book titles.

Expected Output:

A structured JSON object where each key-value pair represents a sign and its description, as per the input provided. For instance:

{
    "SignName1": "Description of SignName1...",
    "SignName2": "Description of SignName2...",
    // ... other sign descriptions ...
}

Please ensure the output is accurate and well-formatted according to the given example and standard JSON syntax.
"""

    files = sorted(os.listdir(txt_dir))

    def process_file(file):
        output_filename = f"{file.split('.')[0]}.json"
        file_path = f"json/{output_filename}"

        if os.path.exists(file_path):
            return

        with open(f"{txt_dir}/{file}", "r") as f:
            text = f.read()

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": system,
                    },
                    {
                        "role": "user",
                        "content": text,
                    },
                ],
                temperature=0.0,
                top_p=1,
            )

            with open(file_path, "w") as f_out:
                f_out.write(response.choices[0].message.content)

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(process_file, files)


def merge_json_files(dir_path):
    merged_data = {}

    for file in sorted(os.listdir(dir_path)):
        if file.endswith(".json"):
            file_path = os.path.join(dir_path, file)

            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                merged_data.update(data)

    return merged_data


def main():
    print("Starting...")
    print("Converting PDFs to images...")
    pdfs_to_imgs("book")
    print("Converting images to text...")
    imgs_to_txt("images")
    print("Converting raw text to formatted text...")
    raw_txt_to_formatted_txt("raw_texts")
    print("Converting formatted text to JSON...")
    formatted_txt_to_json("texts")
    print("Merging JSON files...")

    merged_data = merge_json_files("json")

    print("Saving merged JSON file...")
    with open("json/merged.json", "w", encoding="utf-8") as f:
        json.dump(merged_data, f, ensure_ascii=False)


if __name__ == "__main__":
    main()
