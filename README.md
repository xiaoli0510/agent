# 🤖 AI Agent 探索之旅 (Python + LangChain)

本项目是我从零开始探索大语言模型（LLM）与 Agent 开发的学习历程记录。作为一名前端开发者，我希望通过一步步的代码实践，打通从前端交互到后端 AI 编排的“全栈”能力。

这里记录了我从基础模型调用、记忆管理、文档加载切分，一直到构建完整 RAG 智能客服的完整轨迹。

## 🛠️ 技术栈
*   **语言**: Python 3.11+
*   **核心框架**: LangChain (v1.x)
*   **大模型**: 阿里云通义千问 (Qwen-Max/Flash)
*   **向量与存储**: DashScope Embeddings, ChromaDB
*   **Web UI**: Streamlit
*   **工程化**: Git / SSH

## 📂 目录结构与学习轨迹

项目按照学习顺序分为几个核心阶段：

### 📍 阶段一：基础组件与输出解析 (文件 16-20)
*   `16.查看Runnables的源码.py`：深入探究 LCEL 管道符 `|` 底层原理（`__or__` 运算符重载）。
*   `18.StrOutPutParser.py`：学习如何将模型返回的 `AIMessage` 转化为纯字符串。
*   `19.JsonOutputParser的使用.py`：结构化输出，让模型直接返回 JSON 格式。
*   `20.Lambda函数的使用.py`：利用 `RunnableLambda` 将普通 Python 函数接入 LangChain 链中。

### 📍 阶段二：记忆管理 (文件 21-22)
*   `21.Memory临时会话记录.py`：探究 LLM 的无状态本质，以及如何实现基础的多轮对话。
*   `22.Memory长期会话记录.py` / `22.1...`：将聊天记录持久化到本地文件，解决程序重启后记忆丢失的问题。

### 📍 阶段三：文档加载与向量检索 (文件 23-30)
*   `23-27`：多源数据加载（CSV, JSON, Text, PDF）与文本切分策略（TextSplitter）。
*   `28-29`：向量存储的探索，从内部存储过渡到使用 ChromaDB 外部向量数据库。
*   `30.向量检索构建提示词.py`：实现 RAG 的核心前置条件，通过检索结果动态构建 Prompt。

### 📍 阶段四：完整实战 (文件 31 & `P4_RAG项目案例` 目录)
*   `31.RunnablePassthrough的使用.py`：学习如何在链中透传原始数据。
*   `P4_RAG项目案例/`：**完整的基于 Streamlit 的智能客服项目**（详见目录内代码）。
    *   实现了本地知识库（TXT）的自动读取、切分与向量化。
    *   利用 MD5 校验避免重复数据入库。
    *   前端实现了流畅的**打字机流式输出 (Streaming)** 交互体验。

## 💡 学习难点与排坑记录（核心收获）

作为一个习惯了前后端分离开发的人，在摸索 Agent 时遇到了不少坑，这里记录了部分解决方案：

1.  **关于 LCEL 管道符 `|`**：理解了它并不是 TS 中的类型联合，而是 Python 的 `__or__` 魔术方法的链式调用。
2.  **关于流式输出 (Streaming)**：在实战中遇到了 `RunnableWithMessageHistory` 拦截数据流导致“假流”的问题。最终通过拆分底层 Chain、利用 `st.write_stream` 结合手动管理 History 的方式，彻底打通了原生的流式体验。
3.  **关于文本切分策略 (Chunking)**：对于结构化的表格数据，简单的 `RecursiveCharacterTextSplitter` 并不完美。通过分析发现，直接按行 `splitlines()` 切分，反而能保证每一行尺码规则的语义完整性，大幅提升了检索命中率。

## 🚀 如何运行实战项目

1. 安装依赖：
   ```bash
   pip install -r requirements.txt
2. 配置环境变量：
   * config_data.py：全局配置文件（注意：此文件已被 .gitignore 忽略，请根据 config_data.example.py 自行创建）
   * 本项目通过系统环境变量读取 API 密钥。请在您的系统中配置：
        * 变量名：`DASHSCOPE_API_KEY`
        * 变量值：您的阿里云百炼 API Key (sk-xxx...)
        * (或者您也可以在代码根目录创建一个 `.env` 文件，写入 `DASHSCOPE_API_KEY=sk-xxx`，并在代码中引入 `python-dotenv`)*

## 持续学习中，代码不仅是敲出来的，更是排坑排出来的。