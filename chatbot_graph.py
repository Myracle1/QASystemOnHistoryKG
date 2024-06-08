# -*- coding: utf8 -*-
# @File    : chatbot_graph.py
# @Time    : 2024-06-05 14:44
# @Author  : songhc

from nn_classifier import *
from question_parser import *
from answer_search import *

'''问答类'''
class ChatBotGraph:
    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()
        self.searcher = AnswerSearcher()

    def chat_main(self, sent):
        answer = '您好呀，我叫小度，是历史人物百科助理，希望能帮到你。如果没有回答上来的问题，可联系https://github.com/Myracle1。祝您身体健康，工作顺利！'
        res_classify = self.classifier.classify(sent)
        res_sql = self.parser.parser_main(res_classify)
        final_answers = self.searcher.search_main(res_sql)
        if not final_answers:
            return answer
        else:
            return '\n'.join(final_answers)

if __name__ == '__main__':
    handler = ChatBotGraph()
    while 1:
        question = input('用户:')
        answer = handler.chat_main(question)
        print('小度:', answer)
