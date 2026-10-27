import time
from rag import RagService
import config_data as config

import streamlit as st

st.title("智能客服")
st.divider()

if "message" not in st.session_state:
    st.session_state["message"] = [{
        "role": "assistant", "content": "你好，有什么可以帮助你的？"
    }]

if "rag" not in st.session_state:
    st.session_state["rag"] = RagService()

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])
# 页面最下方提供用户输入栏
prompt = st.chat_input()

if prompt:
    # 页面输出用户的提问
    st.session_state["message"].append({
        "role": "user", "content": prompt
    })
    st.chat_message("user").write(prompt)


    ai_res_list=[]
    with st.spinner("ai思考中...."):
        #invoke是一次性显示全部 stream是流式输出
        res_stream = st.session_state["rag"].chain.stream({"input": prompt}, config.session_config)
        #流数据消耗掉了就没有了，这里使用capture来处理
        # 这个写法比较好玩，没有消耗迭代器，原样返回，还根据自己的需求来获取到了数据
        def capture(generator, cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                yield chunk #按原来的返回，即返回的还是一个迭代器

        st.chat_message("assistant").write_stream(capture(res_stream, ai_res_list))
        st.session_state["message"].append({
            "role": "assistant", "content": "".join(ai_res_list) #将list转变为str
        })

