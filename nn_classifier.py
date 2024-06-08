# -*- coding: utf-8 -*-
# @File    : nn_classifier.py
# @Time    : 2024-06-06 19:23
# @Author  : songhc

import os
import re
import torch
import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification
import spacy
import ahocorasick

class MedicalQuestionFilter:
    def __init__(self, custom_names_path='data/celebrity.txt'):
        # 加载预训练的SpaCy模型
        self.nlp = spacy.load('zh_core_web_sm')
        # 加载自定义词典
        with open(custom_names_path, 'r', encoding='utf-8') as file:
            self.custom_names = file.read().splitlines()

    def ner(self, sentence):
        doc = self.nlp(sentence)
        entities = [ent.text for ent in doc.ents if ent.label_ == 'figure']
        return entities

    def check_history(self, question):
        # 使用SpaCy模型识别实体
        region_wds = self.ner(question)
        # 使用自定义词典识别未识别的人名
        for name in self.custom_names:
            if name in question and name not in region_wds:
                region_wds.append(name)
        # 使用正则表达式识别未识别的人名
        regex = re.compile("|".join(self.custom_names))
        matches = regex.findall(question)
        for match in matches:
            if match not in region_wds:
                region_wds.append(match)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i: 'figure' for i in final_wds}  # Assuming all entities are of type 'PERSON'
        # print(final_dict)
        return final_dict

class QuestionClassifier:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.filter = MedicalQuestionFilter()
        # 初始化节点类型
        self.node_types = ['Figure', 'Age', 'Ethnic', 'Work', 'Story', 'Vocation', 'Official', 'Pre_emperor', 'Next_emperor']

    # 定义预测类别的函数
    def classify(self, question):
        data = {}
        history_dict = self.filter.check_history(question)
        data['args'] = history_dict
        # 收集问句当中所涉及到的实体类型
        types = []
        for type_ in history_dict.values():
            if isinstance(type_, list):
                types += type_
            else:
                types.append(type_)
        question_type = 'others'

        question_types = []

        file_path = 'Question_class.csv'  # 请将路径替换为您的文件路径
        datas = pd.read_csv(file_path, encoding='gbk')

        # 确定标签数量
        num_labels = len(datas['label'].unique())
        # 加载tokenizer和模型
        tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
        model = BertForSequenceClassification.from_pretrained('bert-base-chinese',
                                                              num_labels=num_labels)  # 确保num_labels定义正确

        # 加载保存的模型权重
        model_path = 'models/bert_model_weights.pth'  # 请将路径替换为保存模型权重的路径
        try:
            model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
        except Exception as e:
            print(f"Error loading model weights: {e}")
        # 预处理输入句子
        inputs = tokenizer(question, return_tensors='pt', padding=True, truncation=True, max_length=128)

        # 进行预测
        with torch.no_grad():
            outputs = model(**inputs)

        # 获取预测结果
        logits = outputs.logits
        predicted_class_id = torch.argmax(logits, dim=1).item()
        # print(predicted_class_id)

        question_type_map = {
            0: 'figure_birthplace',
            1: 'figure_birthdate',
            2: 'figure_deathdate',
            3: ' ',
            4: 'figure_age',
            5: 'figure_ethnic',
            6: 'figure_work',
            7: 'figure_official',
            8: 'figure_story',
            9: 'figure_alias',
            10: 'figure_nickname',
            11: 'figure_deathplace',
            12: 'figure_reigntime',
            13: 'figure_pre_emperor',
            14: 'figure_next_emperor',
            15: 'figure_summary'
        }

        question_type = question_type_map.get(predicted_class_id, 'others')
        question_types.append(question_type)

        data['question_types'] = question_types
        # print(data)
        return data

    '''构造词对应的类型'''
    def build_wdtype_dict(self):
        wd_dict = dict()
        node_dicts = {
            'figure': self.Figures,
            'age': self.Ages,
            'ethnic': self.Ethnics,
            'work': self.Works,
            'story': self.Stories,
            'vocation': self.Vocations,
            'official': self.Officials,
            'pre_emperor': self.Pre_emperors,
            'next_emperor': self.Next_emperors
        }

        for node_type, nodes in node_dicts.items():
            for node in nodes:
                wd_dict[node] = [node_type]

        return wd_dict

    '''构造actree，加速过滤'''
    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

if __name__ == '__main__':
    handler = QuestionClassifier()
    while True:
        question = input('input a question:')
        data = handler.classify(question)
        # print(data)
