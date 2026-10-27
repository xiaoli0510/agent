from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings

# 注意：这里的 collection_name 和 persist_directory 要和 config 里的完全一致
db = Chroma(
    collection_name="rag_v5",
    embedding_function=DashScopeEmbeddings(model="qwen3.7-text-embedding"),
    persist_directory="./chroma_db5"
)

# 获取所有数据
data = db.get()

print(f"数据库中一共有 {len(data['documents'])} 条数据")
print("-" * 50)
for i, doc in enumerate(data['documents']):
    print(f"第 {i+1} 条: {doc}")