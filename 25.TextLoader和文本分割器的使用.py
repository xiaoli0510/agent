from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

"""
递归字符文本分割器:将Document分割成小的Document
"""

loader = TextLoader(
    file_path="./data/尺码推荐.txt",
    encoding="utf-8",
)

doc = loader.load()
print(type(doc),len(doc),doc)

spitter = RecursiveCharacterTextSplitter(
    chunk_size=50, #分段的最大字符数
    chunk_overlap=10,  #分段之间允许重叠字符数
    separators=["\n\n","\n","。","!","?","，"],#文本自然段落分割的依据
    length_function=len, # 统计字符的依据函数
)

split_docs = spitter.split_documents(doc)
print(type(split_docs),len(split_docs))
for split_doc in split_docs:
    print(split_doc)
 # 得到的是分段的list