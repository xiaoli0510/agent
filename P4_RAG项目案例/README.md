# 🚀 基于 RAG 的智能电商客服系统

这是本项目最核心的实战落地案例。通过结合 **LangChain**、**ChromaDB** 向量数据库以及 **阿里云通义千问** 大模型，实现了一个具备“私有知识库检索”与“多轮对话记忆”的智能客服系统。

前端使用 Streamlit 构建，并彻底打通了原生的**打字机流式输出（Streaming）**效果。

## 📂 文件结构说明

*   `app_file_upload.py`：**知识库后台管理端**。提供 Web 界面供用户上传 `.txt` 文件，系统会自动进行 MD5 去重、按行切分，并向量化存入 ChromaDB。
*   `app_qa.py`：**用户智能问答端**。提供类似 ChatGPT 的对话界面，支持流式输出与上下文记忆。
*   `knowledge_base.py`：封装了知识库的底层操作（文本切分、向量化入库、MD5 查重）。
*   `vector_stores.py`：封装了 ChromaDB 向量库的初始化与检索器（Retriever）的构建。
*   `rag.py`：核心业务逻辑。利用 LCEL（LangChain Expression Language）组装了 RAG 链（检索 -> 组装 Prompt -> 调用 LLM -> 输出解析）。
*   `file_history_store.py`：自定义的本地文件会话历史存储（将聊天记录持久化为 JSON）。
*   `get_table_data.py`：辅助脚本，用于处理结构化数据。
*   `config_data.py`：全局配置文件（**注意：此文件已被 `.gitignore` 忽略，请根据 `config_data.example.py` 自行创建**）。

## 🌟 核心技术亮点

1.  **高精度切分策略**：针对表格型文本（如尺码推荐），放弃了传统的递归切分，采用 `splitlines()` 按行切分，并加上前缀提示，极大提高了检索精准度。
2.  **流式输出排坑**：去除了 `RunnableWithMessageHistory` 导致的流式阻塞，通过底层 Chain 组装与 `st.write_stream` 结合，实现了丝滑的打字机体验。
3.  **本地持久化**：实现了向量库（Chroma）和聊天记录（FileChatMessageHistory）的本地落盘。

## ⚙️ 如何运行

1. **准备配置文件**
   在运行前，请确保本目录下存在 `config_data.py` 文件，并填入你的 API Key 和模型名称：
   ```python
   # config_data.py 示例
   dashscope_api_key = "sk-你的百炼API密钥"
   chat_model_name = "qwen-max"
   embedding_text_name = "qwen3.7-text-embedding"
   # ... 其他路径配置
2. 启动知识库上传服务
  streamlit run app_file_upload.py
3. 启动智能客服对话
  streamlit run app_qa.py