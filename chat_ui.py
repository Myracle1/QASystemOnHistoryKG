# -*- coding: utf-8 -*-
# @File    : chat_ui.py
# @Time    : 2024-06-07 0:59
# @Author  : songhc
import base64

# chatbot_graph_streamlit.py

import streamlit as st
from nn_classifier import QuestionClassifier
from question_parser import QuestionPaser
from answer_search import AnswerSearcher

class ChatBotGraph:
    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()
        self.searcher = AnswerSearcher()

    def chat_main(self, sent):
        answer = '您好呀，我叫猪猪，是历史人物百科助理，希望能帮到你。如果没有回答上来的问题，可联系https://github.com/Myracle1。祝您身体健康，工作顺利！'
        res_classify = self.classifier.classify(sent)
        res_sql = self.parser.parser_main(res_classify)
        final_answers = self.searcher.search_main(res_sql)
        if not final_answers:
            return answer
        else:
            return '\n'.join(final_answers)

# 初始化聊天机器人
chatbot = ChatBotGraph()

# Streamlit 界面设计
def main_bg(main_bg):
    main_bg_ext = "png"
    st.markdown(
        f"""
         <style>
         .stApp {{
             background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
             background-size: cover
         }}
         </style>
         """,
        unsafe_allow_html=True
    )


main_bg('./assets/background.png')
st.title("历史人物百科问答系统")
st.write("您好呀，我叫小度，是历史人物百科助理，希望能帮到你。如果没有回答上来的问题，可联系https://github.com/Myracle1。祝您身体健康，工作顺利！")

# 获取用户输入
user_input = st.text_input("请输入您的问题：", "")

if st.button("确认"):
    if user_input:
        # 处理用户输入并返回答案
        answer = chatbot.chat_main(user_input)
        st.write("小度:", answer)
    else:
        st.write("请输入一个问题。")
