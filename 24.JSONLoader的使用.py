from langchain_community.document_loaders  import JSONLoader

# loader = JSONLoader(
#     file_path="./data/stu1.json", #文件路径
#     jq_schema=".", #jq解析语法
#     text_content=False, #抽取到的是否是string
# )

# loader = JSONLoader(
#     file_path="./data/stu.json",
#     jq_schema=".[1].name"
# )

loader = JSONLoader(
    file_path="./data/stu2.json",
    jq_schema=".name",
   json_lines=True # 是否是JsonLines文件，可以是json对象或者list或者每一行都是json的数据(末尾没有,)


)

result = loader.load()
print(result)