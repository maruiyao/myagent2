import streamlit as st
import pandas as pd
from utils.student_db import get_most_searched_questions

st.set_page_config(page_title="教师错题数据看板", page_icon="📊", layout="wide")

st.title("📊 教师错题数据看板")
st.text("查看学生搜题量最多的题目，掌握学生薄弱环节。")
st.divider()

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🔥 搜题热度排行榜")
    data = get_most_searched_questions(limit=20)
    
    if data:
        # Convert to pandas dataframe
        df = pd.DataFrame(data, columns=["题目 (Question)", "搜索次数 (Search Count)"])
        # df.index += 1 # Base index from 1
        
        st.dataframe(df, use_container_width=True)
        
        st.bar_chart(df.set_index("题目 (Question)"))
    else:
        st.info("目前还没有学生搜题记录。")

with col2:
    st.subheader("说明")
    st.info("这个看板自动汇总了使用【学生解题助手】的全体学生的搜题记录。数据通过多智能体协作(Agent)自动获取并录入错题数据库。")
    if st.button("刷新数据"):
        st.rerun()
