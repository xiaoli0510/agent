md5_path="./md5.txt"

#Chroma
collection_name="rag_v1"

persist_directory="./chroma_db"

chunk_size=20
chunk_overlap=1

separators=["\r\n", "\n\n", "\n", ".", "!", "?","，","。","！","？"," ",""]

max_split_char_number= 50

similarity_threshold = 3 #检索返回的阈值的个数

embedding_text_name="qwen3.7-text-embedding"

chat_model_name="qwen-max"

session_config = {'configurable': {'session_id': 'use_04'}}