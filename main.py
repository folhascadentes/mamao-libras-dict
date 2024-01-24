import os

from PIL import Image
import boto3
import fitz
from openai import OpenAI

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
        filepath = f"{pdfs_dir}/{file}"
        if not os.path.exists(filepath):
            pdf_to_img(filepath)


def imgs_to_txt(images_dir):
    images = sorted(os.listdir(images_dir))
    client = initialize_textract_client()

    for image in images:
        filename = f"{image.split('.')[0]}.txt"
        filepath = f"raw_texts/{filename}"

        if os.path.exists(filepath):
            continue

        text = analyze_document(client, f"{images_dir}/{image}")

        with open(f"raw_texts/{filename}", "w") as f:
            f.write(text)


def raw_txt_to_formatted_txt(raw_txt_dir):
    client = OpenAI()
    system = """I have extracted text from various documents using OCR. The text is currently in a series of lines without proper paragraph formatting. Please format these lines into well-structured paragraphs."""

    files = sorted(os.listdir(raw_txt_dir))

    for file in files:
        filepath = f"texts/{file}"

        if os.path.exists(filepath):
            continue

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

            with open(filepath, "w") as f:
                f.write(response.choices[0].message.content)


def formatted_txt_to_json(txt):
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
    files = sorted(os.listdir(txt))

    for file in files[0:5]:
        with open(f"{txt}/{file}", "r") as f:
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

            output_filename = f"{file.split('.')[0]}.json"

            with open(f"json/{output_filename}", "w") as f:
                f.write(response.choices[0].message.content)


def main():
    pdfs_to_imgs("book")
    imgs_to_txt("images")
    raw_txt_to_formatted_txt("raw_texts")
    formatted_txt_to_json("texts")


if __name__ == "__main__":
    main()
