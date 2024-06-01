import tempfile
import os

import pytesseract
from PyPDF2 import PdfWriter, PdfReader
from pdf2image import convert_from_path

PROCESSED_PDF_DIR = "processed_pdf"
RAW_PDF_DIR = "raw_pdf"


def page_to_image(page, dpi = 300):
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_pdf:
        temp_pdf_path = temp_pdf.name
        writer = PdfWriter()
        writer.add_page(page)
        writer.write(temp_pdf)
    images = convert_from_path(temp_pdf_path, dpi=dpi)
    os.remove(temp_pdf_path)

    return images[0]


def parse_rotate(page_settings):
  for page_setting in page_settings.split("\n"):
    separate_page_settings = page_setting.split(":")
    if separate_page_settings[0] == "Rotate":
      return int(separate_page_settings[1].strip())


def prepare_pdf(pdf_patch):

    PDF_NAME = pdf_patch.split("/")[1].split(".")[0] + "_processed.pdf"
    print("processed {0} pdf".format(PDF_NAME))

    output = PdfWriter()
    input_pdf = PdfReader(open(pdf_patch, "rb"))
    
    for index, page in enumerate(input_pdf.pages):

        try: # оно не работает на страницах где нет текста
            img = page_to_image(page)
            page_settings = pytesseract.image_to_osd(img)
            rotate_num = parse_rotate(page_settings)
            page.rotate(rotate_num)
        except:
          print("page {0} has not text".format(index))

        output.add_page(page)

    file_patch = os.path.join(PROCESSED_PDF_DIR, PDF_NAME.format(index))
    with open(file_patch, "wb") as outputStream:
        output.write(outputStream)


def main():
  pdfs = os.listdir(RAW_PDF_DIR)

  for pdf in pdfs:
   
    if pdf.lower().endswith('.pdf'):
      prepare_pdf(os.path.join(RAW_PDF_DIR, pdf))

if __name__ == "__main__":
    main()