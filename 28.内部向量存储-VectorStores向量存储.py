from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import CSVLoader

vector_store = InMemoryVectorStore(
    embedding=DashScopeEmbeddings(),
)

loader = CSVLoader(
    file_path="./data/info.csv",
    encoding="utf-8",
    source_column="source"
)

documents = loader.load()

vector_store.add_documents(
    documents=documents, #存入的documents
    ids=["id"+str(i) for i in range(1, len(documents)+1)] # 存入的文档的id
)

# vector_store.delete(
#     ids=["id1","id2"]
# )

res = vector_store.similarity_search(
    query="Python是世界上最好的编程语言吗",
    k=1,
)
print(res)