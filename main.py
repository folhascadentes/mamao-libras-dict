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
        book_name = file.split(".")[0]
        if not os.path.exists(f"images/{book_name}-000.png"):
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


def main():
    print("Starting...")
    print("Converting PDFs to images...")
    pdfs_to_imgs("book")
    print("Converting images to text...")
    imgs_to_txt("images")


if __name__ == "__main__":
    main()
