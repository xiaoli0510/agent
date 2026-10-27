"""
知识库
"""
import hashlib
import os

from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime

import config_data as config


def check_md5(md5_str: str):
    if not os.path.exists(config.md5_path):
        # 打开这个文件后关闭，如果不存在就会自动创建
        open(config.md5_path, 'w', encoding="utf-8").close()
        return False
    else:
        for line in open(config.md5_path, 'r', encoding="utf-8").readlines():
            line = line.strip()
            if line == md5_str:
                return True
        return False


def save_md5(md5_str: str):
    with open(config.md5_path, 'a', encoding="utf-8") as f:
        f.write(md5_str + "\n")


def get_string_md5(input_str: str, encoding='utf-8'):
    str_bytes = input_str.encode(encoding=encoding)  # 将str转变为bytes字节数组
    md5_obj = hashlib.md5()  # 创建md5对象
    md5_obj.update(str_bytes)  # 更新内容
    return md5_obj.hexdigest()  # md5的十六进制字符串


class KnowledgeBaseService(object):
    def __init__(self):
        # 如果文件夹不存在则创建，如果存在则跳过
        os.makedirs(config.persist_directory, exist_ok=True)
        # chroma向量库
        self.chroma = Chroma(
            collection_name=config.collection_name,  # 数据库的表名
            embedding_function=DashScopeEmbeddings(model="qwen3.7-text-embedding"),
            persist_directory=config.persist_directory,  # 数据库本地存储文件夹
        )  # 向量存储的实例 Chroma向量库对象
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,  # 每一个文本段的最大长度
            chunk_overlap=config.chunk_overlap,  # 连续文本段之间的字符重叠数量
            separators=config.separators,
            length_function=len,

        )  # 文本分割器的对象

    def upload_by_str(self, data: str, filename):
        """将传入的字符串，进行向量化，存入向量数据库中"""
        # 将str变为md5
        md5_hex = get_string_md5(data)

        if check_md5(md5_hex):
            return "[跳过]内容已经存在知识库中"

        # if len(data) > config.max_split_char_number:
        #     knowledge_chunks: list[str] = self.spliter.split_text(data)
        # else:
        #     knowledge_chunks: list[str] = [data]
        knowledge_chunks = []
        for line in data.splitlines():
            line = line.strip()
            if line:
                knowledge_chunks.append(f"尺码推荐：{line}")

        metadata = {
            "source": filename,
            # 2026-10-21 10:01:01
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator": "曹操"
        }
        # 内容加载到向量库中
        self.chroma.add_texts(
            knowledge_chunks,
            metadatas=[metadata for _ in knowledge_chunks],  # 文件的元数据都一样，但是需是一个list,需跟knowledge_chunks的长度对应
        )
        save_md5(md5_hex)
        return "[成功]内容已经成功载入向量库中"


