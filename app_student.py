import time
import streamlit as st
from agent.react_agent import ReactAgent

# 页面配置
st.set_page_config(page_title="学生解题助手", page_icon="📝")

# 标题
st.title("👨‍🎓 学生解题助手")
st.text("遇到不会的问题？请在下方发送搜题内容，我会为你解答并自动记录到错题本哦！")
st.divider()

if "agent" not in st.session_state:
    st.session_state["agent"] = ReactAgent()

if "message" not in st.session_state:
    st.session_state["message"] = []

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

# 用户输入提示词
prompt = st.chat_input("请输入你想搜索的题目或提问...")

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role": "user", "content": prompt})

    response_messages = []
    with st.spinner("AI老师正在为你解答..."):
        # 强制使用搜题场景的提示，这样更靠谱地命中 student_rag_search
        enforced_prompt = f"请使用学生搜题记录rag工具为你寻找答案：{prompt}"
        res_stream = st.session_state["agent"].execute_stream(enforced_prompt)

        def capture(generator, cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                for char in chunk:
                    time.sleep(0.01)
                    yield char

        st.chat_message("assistant").write_stream(capture(res_stream, response_messages))
        st.session_state["message"].append({"role": "assistant", "content": response_messages[-1]})
        st.rerun()
