from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader(
    file_path="./data/1.pdf",
    mode="page",  #模式有page | single，按页还是整个
    password="123456" #如果pdf有加密的需才需要
)

documents = loader.lazy_load()
i= 0
for document in documents:
    i+=1
    print(document)
    print("="*20,i)