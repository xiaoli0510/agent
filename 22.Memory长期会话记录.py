from typing import Sequence

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import message_to_dict,messages_from_dict,BaseMessage
import os, json

"""
BaseChatMessageHistory只定义了下面方法，但是需要自己去实现
因为存储方式有：
存内存
存文件
存Redis
存数据库
ps：临时会话记录+长期会话记录都是废弃，官方推荐使用agent的checkpointer检查点来实现会话记录
"""

class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id, storage_path):
        self.session_id = session_id
        self.storage_path = storage_path
        self.file_path = os.path.join(self.storage_path, f"self.session_id.json")

        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        all_messages = list(self.messages)
        all_messages.extend(messages) #新的msg和旧的融合

        new_messages = [message_to_dict(message) for message in all_messages] #将message转变为dic

        # 将数据写入文件
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(new_messages, f, ensure_ascii=False, indent=4)

    @property #将messages方法变成成员属性使用
    def messages(self) -> list[BaseMessage]:
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                messages_data = json.load(f)
                return messages_from_dict(messages_data) # 将dict转变为message

        except FileNotFoundError:
            return []

    def clear(self) -> None:
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump([],f)