from typing import Any

from pydantic import BaseModel
from unstructured.partition.pdf import partition_pdf
import logging
from tqdm.auto import tqdm

import json


def pdf_convert_to_json(raw_pdf_elems):
    json_to_save = {}
    print(raw_pdf_elems)
    for idx in range(len(raw_pdf_elems)):

        elem_dict = raw_pdf_elems[idx].to_dict()
        json_to_save[idx] = {"type": elem_dict["type"], "structure": elem_dict}

        return json_to_save


def pre_process_docs(
    filenamepath,
    output_path,
    image_output_dir_path="rag/raw_pdf/image_output_dir_path",
):

    print("Starting pre_process_docs: ", filenamepath)

    raw_pdf_elements = partition_pdf(
        filename=filenamepath,
        languages=["rus", "eng"],
        # Unstructured first finds embedded image blocks
        extract_images_in_pdf=False,
        # Use layout model (YOLOX) to get bounding boxes (for tables) and find titles
        # Titles are any sub-section of the document
        infer_table_structure=True,
        # Post processing to aggregate text once we have the title
        chunking_strategy="by_title",
        # Chunking params to aggregate text blocks
        # Attempt to create a new chunk 3800 chars
        # Attempt to keep chunks > 2000 chars
        max_characters=4000,
        new_after_n_chars=3800,
        combine_text_under_n_chars=2000,
        image_output_dir_path=image_output_dir_path,
    )

    # Create a dictionary to store counts of each type
    # category_counts = {}

    # for element in raw_pdf_elements:
    #     category = str(type(element))
    #     if category in category_counts:
    #         category_counts[category] += 1
    #     else:
    #         category_counts[category] = 1

    # # Unique_categories will have unique elements
    # unique_categories = set(category_counts.keys())

    # print("unique_categories", unique_categories)

    # class Element(BaseModel):
    #     type: str
    #     text: Any

    # # Categorize by type
    # categorized_elements = []
    # for element in raw_pdf_elements:
    #     if "unstructured.documents.elements.Table" in str(type(element)):
    #         categorized_elements.append(Element(type="table", text=str(element)))
    #     elif "unstructured.documents.elements.CompositeElement" in str(type(element)):
    #         categorized_elements.append(Element(type="text", text=str(element)))

    # # Tables
    # table_elements = [e for e in categorized_elements if e.type == "table"]
    # print(len(table_elements))

    # # Text
    # text_elements = [e for e in categorized_elements if e.type == "text"]
    # print(len(text_elements))

    # save table_elements and text_elements to a file with name filenamepath
    with open(
        os.path.join(output_path, filenamepath.split("/")[-1].split(".")[0] + ".json"),
        "w",
        encoding="utf-8",
    ) as f:
        json_to_save = pdf_convert_to_json(raw_pdf_elements)
        json.dump(json_to_save, f, ensure_ascii=False, indent=4)

    print("-------------- Done pre_process_docs {filenamepath} --------------")


def logging__():
    import logging
    import os

    # Create the logs directory if it doesn't exist
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # Configure logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create a file handler
    file_handler = logging.FileHandler("logs/info.log")
    file_handler.setLevel(logging.INFO)

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.CRITICAL)

    # Create a formatter and attach it to the handlers
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Write an info log
    logger.info("This is an info log message")


if __name__ == "__main__":
    import os

    logging__()

    folder_path = "rag/raw_pdf/отсканированыне документы"

    for file in tqdm(os.listdir(folder_path)):
        if file.endswith(".pdf"):
            pre_process_docs(
                os.path.join(folder_path, file),
                output_path=os.path.join("PreProcess", folder_path.split("/")[-1]),
            )
