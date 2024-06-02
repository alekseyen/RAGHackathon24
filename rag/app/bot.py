import os
import argparse
import streamlit as st

from langchain import PromptTemplate
from langchain.chains import RetrievalQA
from prompts import CUSTOM_PROMPT_TEMPLATE
from settings import API_TOKEN, CATALOG_NUMBER, CUSTOM_MODEL_YRL
from langchain_community.llms import YandexGPT
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from QABot import answer_question


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--db_faiss_path",
        help="path for load db",
        default="{0}/pet_projects/eliza/tools/create_rag_db/embeddings/db_faiss_1".format(
            "/".join(os.getcwd().split("/")[:3])
        ),
    )
    parser.add_argument(
        "--embeddings_model_name",
        help="the name of the model that is used for embeddings",
        default="sergeyzh/rubert-tiny-sts",
    )
    args = parser.parse_args()

    return args


# def load_llm_model(model_url):
#     # example gpt://{индификатор каталога}/yandexgpt-lite/latest
#     llm = YandexGPT(
#         model_uri=model_url.format(CATALOG_NUMBER=CATALOG_NUMBER),
#         api_key=API_TOKEN,
#         temperature=0,
#         max_tokens=4000,
#     )
#     return llm


# def load_db(args):
#     embeddings = HuggingFaceEmbeddings(
#         model_name=args.embeddings_model_name,
#         model_kwargs={"device": "cpu"},
#     )

#     db = FAISS.load_local(
#         args.db_faiss_path, embeddings, allow_dangerous_deserialization=True
#     )

#     return db


# def load_bot(prompt, db, llm, search_kwargs):
#     question_answer_system = RetrievalQA.from_chain_type(
#         llm=llm,
#         chain_type="stuff",
#         retriever=db.as_retriever(search_kwargs=search_kwargs),
#         return_source_documents=True,
#         chain_type_kwargs={"prompt": prompt},
#     )

#     return question_answer_system


def show_history():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


# db = load_db(parse_args())
st.title("🎈 RAG pipline")

st.text(
    "🤖 Chat IS NOT supported yet \n"
    "Please don't expect conversation context support and don't ask clarifying questions"
)

# model_url = CUSTOM_MODEL_YRL

# llm = load_llm_model(model_url)

if "messages" not in st.session_state:
    st.session_state.messages = []


if question := st.chat_input():
    show_history()

    with st.chat_message("user"):
        st.markdown(question)
        st.session_state.messages.append({"role": "user", "content": question})

    answer = answer_question(
        question
    )  # "Some Answer "  # answer_bot({"query": question})

    print("answer is ", answer)
    with st.chat_message("assistant"):
        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
