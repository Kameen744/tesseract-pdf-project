# from PIL import Image

# import pytesseract

# pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

# print(pytesseract.image_to_string(Image.open('scan.jpg')))

import fitz  # PyMuPDF
import pytesseract
import os
from PIL import Image
from reportlab.pdfgen import canvas


def extract_text_from_pdf_images(input_pdf_path, output_pdf_path):
    doc = fitz.open(input_pdf_path)  # open a document
    if os.path.isfile(output_pdf_path):
        out_doc = fitz.open(output_pdf_path)
    else:
        out_doc = fitz.open()

    for page_index in range(len(doc)):  # iterate over pdf pages
        page = doc[page_index]  # get the page
        image_list = page.get_images()

        # print the number of images found on the page
        if image_list:
            print(f"Found {len(image_list)} images on page {page_index}")
        else:
            print("No images found on page", page_index)

        # enumerate the image list
        for image_index, img in enumerate(image_list, start=1):

            xref = img[0]  # get the XREF of the image
            pix = fitz.Pixmap(doc, xref)  # create a Pixmap

            if pix.n - pix.alpha > 3:  # CMYK: convert to RGB first
                pix = fitz.Pixmap(fitz.csRGB, pix)

            image_filename = "page_%s-image_%s.png" % (page_index, image_index)

            pix.save(image_filename)
            image_text = pytesseract.image_to_string(
                Image.open(image_filename))
            os.remove(image_filename)

            n = out_doc.insert_page(page_index,
                                    text=image_text,
                                    fontsize=12,
                                    width=595,
                                    height=842,
                                    fontname="Helvetica",  # default font
                                    fontfile=None,  # any font file name
                                    color=(0, 0, 0))  # text color (RGB)
            out_doc.save(output_pdf_path)

        print("Done - ", page_index)
    # out_doc.save()


# def extract_text_from_pdf_images(pdf_path):

#     doc = fitz.open(pdf_path)
#     text = ""

#     for page_number in range(doc.page_count):
#         page = doc[page_number]
#         image_list = page.get_images(full=True)

#         for img_index, img_info in enumerate(image_list):
#             base_image = doc.extract_image(img_index)
#             print(base_image)
#             if base_image:
#                 image_bytes = base_image["image"]

#                 image = Image.open(io.BytesIO(image_bytes))
#                 text += pytesseract.image_to_string(image)
#                 break
#         break
#     doc.close()
#     return text


# def write_text_to_pdf(text, output_pdf_path):
#     pdf = canvas.Canvas(output_pdf_path)
#     pdf.drawString(10, 800, text)  # Adjust the coordinates as needed
#     pdf.save()


if __name__ == "__main__":
    input_pdf_path = "book.pdf"
    output_pdf_path = "book-text.pdf"

    extracted_text = extract_text_from_pdf_images(
        input_pdf_path, output_pdf_path)

    # print(extracted_text)

    # write_text_to_pdf(extracted_text, output_pdf_path)
