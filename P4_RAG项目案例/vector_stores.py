from langchain_chroma import Chroma
import config_data as config


class VectorStoreService(object):
    def __init__(self, embedding):
        self.embedding = embedding
        #向量存储实例
        self.vector_store = Chroma(
            collection_name=config.collection_name,
            embedding_function= self.embedding,
            persist_directory= config.persist_directory
        )

    def get_retriever(self):
        #返回向量检索器，方便加入chain
       return self.vector_store.as_retriever(search_kwargs={"k": config.similarity_threshold})

if __name__ == "__main__":
    from langchain_community.embeddings import DashScopeEmbeddings
    retriever = VectorStoreService(DashScopeEmbeddings(model="qwen3.7-text-embedding")).get_retriever()
    res =  retriever.invoke("体重：180-210斤，建议的尺码是多少")
    print(res)