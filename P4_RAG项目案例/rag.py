from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models import ChatTongyi
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory, RunnableLambda
from file_history_store import get_history

import config_data as config

from vector_stores import VectorStoreService



class RagService(object):
    def __init__(self):
        self.vector_service = VectorStoreService(
            embedding=DashScopeEmbeddings(model=config.embedding_text_name)
        )
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "以我提供的已知参考资料为主，简洁和专业的回答用户问题。参考资料：{context}"),
                ("system", "并且我提供用户的对话历史记录，如下"),
                MessagesPlaceholder("history"),
                ("user", "请回答用户提问：{input}")
            ]
        )
        self.chat_model = ChatTongyi(
            model=config.chat_model_name,
            streaming=True
        )
        self.chain = self.__get_chain()

    def __get_chain(self):
        """获取最终的执行链"""
        retriever = self.vector_service.get_retriever()

        def format_document(docs: list[Document]):
            if not docs:
                return "无参考资料"
            formatted_str = ""
            for doc in docs:
                formatted_str += f"文档片段：{doc.page_content}\n,文档元数据：{doc.metadata}\n\n"
            return formatted_str

        def format_for_retriever(value):
            return value["input"]  # 检索器接受的参数是str

        def format_for_prompt_template(value):  # prompt_template接受的参数是{input,history,context}
            new_value = {}
            new_value["input"] = value["input"]["input"]
            new_value["history"] = value["input"]["history"]
            new_value["context"] = value["context"]
            return new_value

        # 采用的是一步一步尝试看参数来调试bug
        chain = (
                {
                    "input": RunnablePassthrough(),
                    "context": RunnableLambda(format_for_retriever) | retriever | format_document,  # 将list转变str
                } | RunnableLambda(format_for_prompt_template) | self.prompt_template |self.chat_model | StrOutputParser()
        )

        # 带有历史记录的chain，是以普通chain为基础，然后添加历史记录相关参数
        conversation_chain = RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",
            history_messages_key="history",
        )

        return conversation_chain  # 需注意普通链和带有历史记录的chain的invoke的参数不一样


if __name__ == "__main__":
    pass