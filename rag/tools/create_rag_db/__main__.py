import os
import time
import argparse

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import Docx2txtLoader, DirectoryLoader


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--load_data_patch', help='path for load data', default="{0}/pet_projects/eliza/tools/pdf_to_word_format/docx".format("/".join(os.getcwd().split("/")[:3])))
    parser.add_argument('--db_patch',  help='path for db save', default="embeddings/db_faiss")
    parser.add_argument('--chunk_size',  help='the number of characters in chunk', default=500, type=int)
    parser.add_argument('--chunk_overlap',  help='the number of chunk overlapping characters', default=100, type=int)
    parser.add_argument('--embeddings_model_name',  help='the name of the model that is used for embeddings', default="sergeyzh/rubert-tiny-sts")
    args = parser.parse_args()

    return args


def main(args):
    loader = DirectoryLoader(args.load_data_patch, glob="*.docx", loader_cls=Docx2txtLoader)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap
    )

    texts = text_splitter.split_documents(documents)
    embeddings = HuggingFaceEmbeddings(
        model_name = args.embeddings_model_name,
        model_kwargs={'device': 'cpu'}
    )

    print("start create embeddings")
    now_time = int(time.time())
    db = FAISS.from_documents(texts, embeddings)
    db.save_local(args.db_patch)

    print("processing the creation of the database took {0} time".format(int(time.time()) - now_time))

if __name__ == "__main__":
    main(parse_args())