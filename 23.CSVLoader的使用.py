from langchain_community.document_loaders import CSVLoader
loader = CSVLoader(
    file_path="./data/stu.csv",
    encoding="utf-8",

)

documents = loader.load()

for document in documents:
    print(document)