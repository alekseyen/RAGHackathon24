from langchain.embeddings import HuggingFaceEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import YandexGPT
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain.storage import InMemoryStore
from langchain_community.vectorstores import Chroma


model_name = "clips/mfaq"      # эти эмбеддинги СОТА для RAG'ов
model_kwargs = {'device': 'cpu'}

embeddings = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
)

vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

# The storage layer for the parent documents
store = InMemoryStore()
id_key = "doc_id"

# The retriever (empty to start)
retriever = MultiVectorRetriever(
    vectorstore=vectorstore,
    docstore=store,
    id_key=id_key,
)

prompt_text = """Вы — ассистент, в задачи которого входит составление кратких описаний.\
 Если вам дали текст, Предоставьте сжатое резюме текста.
 Если вам дали таблицу, Предоставьте названия каждой строки и каждой колонки, без значений ячеек.
 Таблица или фрагмент текста: {element} 
 в кратком описании всегда должна содержаться информация о том, к какой компании относится данный текст или таблица."""
prompt = ChatPromptTemplate.from_template(prompt_text)

# Summary chain
model = YandexGPT(api_key="AQVNy-2Y671NYKrRd0Ig_MMuKSw5L2DTyohvia6R",
                  model_uri="gpt://{0}/yandexgpt/latest".format('b1g8mvm4vfdho6fl7ole'), temperature=0)
summarize_chain = {"element": lambda x: x} | prompt | model | StrOutputParser()

# Prompt template
template = """Кратко Ответь на вопрос, основываясь исключительно на следующем контексте, который может включать текст и таблицы в формате markdown:
{context}
Вопрос: {question}
Также если вопрос из списка ответ:

"""
prompt = ChatPromptTemplate.from_template(template)

# LLM

# RAG pipeline
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

def answer_question(question):
    print('retriever is: ', retriever.invoke(question), '\n\n')
    # if retriever.invoke(question):
    #     print('Перефразируй')
    return chain.invoke(question)
    