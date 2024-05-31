from __init__ import add_not_found_module

add_not_found_module()  # must be first

import os
import json
import base64
import argparse
import shutil
import time

from docx import Document
from docx.shared import Pt
from PyPDF2 import PdfWriter, PdfReader

from lib.yandex_ocr_api.client import OCRClient
from settings import (
    MAX_PAGES,
    PDF_DIR,
    PDF_NAME,
    DOCX_DIR,
    DOCX_NAME,
    REPLACE_OFF_FORMAT,
    REPLACE_ON_FORMAT,
    SLEEP_TIME,
)

TOKEN = os.getenv("API_YANDEX_CLOUD_TOKEN")


class OCRpdf(OCRClient):

    def __init__(self, pdf_patch, language_codes, TOKEN, **kwargs):
        super().__init__(TOKEN, **kwargs)
        self.pdf_patch = os.path.join(
            "/".join(os.getcwd().split("/")[:-2]), pdf_patch
        )  # pdf_patch like raw_pdf/pdf_document_0.pdf
        self.tacks_ids = []
        self.language_codes = language_codes

    def save_pdf(self, output, number):
        with open(os.path.join(PDF_DIR, PDF_NAME.format(number)), "wb") as outputStream:
            output.write(outputStream)

    def prepare_pdf(self):
        print("Created pdfs directory", os.path.abspath(PDF_DIR))
        os.makedirs(PDF_DIR, exist_ok=True)
        output = PdfWriter()
        number_separate_pdf = 0

        inputpdf = PdfReader(open(self.pdf_patch, "rb"))
        for index, page in enumerate(inputpdf.pages):
            output.add_page(page)
            if index % MAX_PAGES == 0 and index:
                self.save_pdf(output, number_separate_pdf)
                number_separate_pdf += 1
                output = PdfWriter()
        self.save_pdf(output, number_separate_pdf)

    def encode_pdf_file(self, pdf_file):
        pdf_file_content = pdf_file.read()
        return base64.b64encode(pdf_file_content)

    def create_ocr_pdf_tasks(self):
        pdf_file_names = os.listdir(PDF_DIR)

        pdf_file_names.sort(
            key=lambda x: int(x.split("_")[-1].split(".")[0])
        )  # sort by pdf id

        for pdf_file_name in pdf_file_names:

            pdf_patchs = os.path.join(PDF_DIR, pdf_file_name)

            pdf_file = open(pdf_patchs, "rb")
            pdf_base64 = self.encode_pdf_file(pdf_file)

            json_body = {
                "mimeType": "application/pdf",
                "languageCodes": self.language_codes,
                "model": "page",
                "content": pdf_base64.decode("utf-8"),
            }

            response_json = self.post_process_request(
                json_body=json_body, handle="pdf_async"
            )
            time.sleep(SLEEP_TIME)
            self.tacks_ids.append(response_json["id"])
            print("Pdf OCR task created {0}".format(response_json["createdAt"]))

    def get_ocr_pdf_tasks_result(self):

        doc = Document()
        style = doc.styles["Normal"]
        style.font.name = "Times New Romans"
        style.font.size = Pt(12)

        idx = 0
        while idx < len(self.tacks_ids):
            try:
                text_response = self.get_process_request(
                    handle="get_pdf_async", id=self.tacks_ids[idx]
                )
            except:
                text_response = None
                print(self.tacks_ids[idx])
                idx += 1

            if not text_response:
                continue

            idx += 1
            json_result = json.loads(
                "[" + text_response.replace(REPLACE_OFF_FORMAT, REPLACE_ON_FORMAT) + "]"
            )
            json_result.sort(key=lambda x: int(x["result"]["page"]))

            for page in json_result:
                page_text = page["result"]["textAnnotation"]["fullText"]
                doc.add_paragraph(page_text)
            print("{0} OCR task completed successfully".format(idx))

        os.makedirs(DOCX_DIR, exist_ok=True)
        document_count = len(os.listdir(DOCX_DIR))
        doc.save(os.path.join(DOCX_DIR, DOCX_NAME.format(document_count)))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf_path", help="path for OCP task pdf")
    parser.add_argument(
        "--language_code",
        help='list input with "," delimited',
        type=lambda s: [item for item in s.split(",")],
        default=["ru", "en"],
    )
    args = parser.parse_args()

    return args


def main(args):

    ocr_pdf = OCRpdf(
        pdf_patch=args.pdf_path, language_codes=args.language_code, TOKEN=TOKEN
    )

    ocr_pdf.prepare_pdf()
    ocr_pdf.create_ocr_pdf_tasks()
    ocr_pdf.get_ocr_pdf_tasks_result()
    shutil.rmtree(PDF_DIR)


if __name__ == "__main__":
    main(parse_args())
