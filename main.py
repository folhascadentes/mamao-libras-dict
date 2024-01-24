import os

from PIL import Image
import fitz
import pytesseract

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


# Main functions


def pdfs_to_imgs(pdfs_dir):
    files = sorted(os.listdir(pdfs_dir))

    for file in files:
        pdf_to_img(f"{pdfs_dir}/{file}")


def imgs_to_txt(image_path):
    pass


def raw_txt_to_formatted_txt(raw_txt):
    pass


def formatted_txt_to_json():
    pass


def main():
    pdfs_to_imgs("book")
    imgs_to_txt("")
    raw_txt_to_formatted_txt("")
    formatted_txt_to_json()


if __name__ == "__main__":
    main()
