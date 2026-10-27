import time

import streamlit as st
from knowledge_base import KnowledgeBaseService

"""
streamlit:web页面元素变化时，代码会重头执行一遍。使用st.session_state来解决这个问题
将文件上传和知识库联系起来
"""

st.title("知识库更新服务")

uploader_file = st.file_uploader(
    "请上传文件",
    type=["txt"],
    accept_multiple_files=False
)

if "service" not in st.session_state:
    #避免每次都去创建，使用session_state来解决
    st.session_state["service"] = KnowledgeBaseService()

if uploader_file is not None:
    # 提取文件的信息
    file_name = uploader_file.name
    file_type = uploader_file.type
    file_size = uploader_file.size / 1024

    st.subheader(f"文件名:{file_name}")
    st.write(f"格式: {file_type},大小：{file_size:.2f} KB")

    # 获取里面的文本，格式是utf-8。getvalue()获取到的是原始二进制内容
    text = uploader_file.getvalue().decode("utf-8")

    with st.spinner("载入知识库中..."): #在spinner内的代码执行过程中，会又一个转圈动画
        time.sleep(1)
        r =  st.session_state["service"].upload_by_str(text,file_name)
        st.write(r)


