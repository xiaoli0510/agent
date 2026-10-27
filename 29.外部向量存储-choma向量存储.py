from langchain_community.document_loaders import CSVLoader
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_chroma import Chroma

vector_store = Chroma(
    collection_name="test",
    embedding_function=DashScopeEmbeddings(),
    persist_directory="./chroma_db1" #指定数据存放的文件夹
)

loader = CSVLoader(
    file_path="./data/info.csv",
    encoding="utf-8",
    source_column="source"
)

documents = loader.load()

# 向量存储的 add delete search
vector_store.add_documents(
    documents=documents,
    ids=["id"+ str(i) for i in range(1, len(documents)+1)]
)
# vector_store.delete(
#     ids=["id1"]
# )

res = vector_store.similarity_search(
    query="Python是世界上最好的编程语言吗",
    k=1,  #得到多少条数据
    filter={"source":"传智教育"} #过滤的条件
)

print(res)