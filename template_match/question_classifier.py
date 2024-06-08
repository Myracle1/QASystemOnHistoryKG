#!/usr/bin/env python3
# coding: utf-8
# File: question_classifier.py

import os
import ahocorasick



class QuestionClassifier:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        # 特征词路径
        self.figure_path = os.path.join(cur_dir, 'dict/figure.txt')
        self.age_path = os.path.join(cur_dir, 'dict/age.txt')
        self.ethnic_path = os.path.join(cur_dir, 'dict/ethnic.txt')
        self.work_path = os.path.join(cur_dir, 'dict/work.txt')
        self.story_path = os.path.join(cur_dir, 'dict/story.txt')
        self.vocation_path = os.path.join(cur_dir, 'dict/vocation.txt')
        self.official_path = os.path.join(cur_dir, 'dict/official.txt')
        self.pre_emperor_path = os.path.join(cur_dir, 'dict/pre_emperor.txt')
        self.next_emperor_path = os.path.join(cur_dir, 'dict/next_emperor.txt')
        # 加载特征词
        self.figure_wds = [i.strip() for i in open(self.figure_path, encoding='utf-8') if i.strip()]
        self.age_wds = [i.strip() for i in open(self.age_path, encoding='gbk') if i.strip()]
        self.ethnic_wds = [i.strip() for i in open(self.ethnic_path, encoding='gbk') if i.strip()]
        self.work_wds = [i.strip() for i in open(self.work_path, encoding='gbk') if i.strip()]
        self.story_wds = [i.strip() for i in open(self.story_path, encoding='gbk') if i.strip()]
        self.vocation_wds = [i.strip() for i in open(self.vocation_path, encoding='gbk') if i.strip()]
        self.official_wds = [i.strip() for i in open(self.official_path, encoding='gbk') if i.strip()]
        self.pre_emperor_wds = [i.strip() for i in open(self.pre_emperor_path, encoding='gbk') if i.strip()]
        self.next_emperor_wds = [i.strip() for i in open(self.next_emperor_path, encoding='gbk') if i.strip()]
        self.region_words = set(self.figure_wds + self.age_wds + self.ethnic_wds + self.work_wds + self.story_wds + self.vocation_wds + self.official_wds + self.pre_emperor_wds + self.next_emperor_wds)
        # 构造领域actree
        self.region_tree = self.build_actree(list(self.region_words))
        # 构建词典
        self.wdtype_dict = self.build_wdtype_dict()
        # 问句疑问词
        self.age_qwds = ['时代', '年代', '朝代']
        self.ethnic_qwds = ['民族', '族群']
        self.work_qwds = ['作品', '著作']
        self.story_qwds = ['事迹', '故事']
        self.vocation_qwds = ['职业', '工作']
        self.official_qwds = ['官职', '职位']
        self.pre_emperor_qwds = ['前任', '前皇帝']
        self.next_emperor_qwds = ['继任', '下任', '继皇帝']
        self.attribute_qwds = ['别名', '昵称', '在位时间', '出生地', '出生日期', '死亡地', '死亡日期', '生平', '简介']
        self.figure_qwds = ['历史人物', '有哪些人', '人物']
        self.summary_qwds = ['生平', '简介', '介绍']
        print('model init finished ......')

    '''分类主函数'''
    def classify(self, question):
        data = {}
        history_dict = self.check_history(question)
        if not history_dict:
            return {}
        data['args'] = history_dict
        # 收集问句当中所涉及到的实体类型
        types = []
        for type_ in history_dict.values():
            types += type_
        question_type = 'others'

        question_types = []

        # 时代
        if self.check_words(self.age_qwds, question) and ('age' in types):
            question_type = 'figure_age'
            question_types.append(question_type)

        # 民族
        if self.check_words(self.ethnic_qwds, question) and ('ethnic' in types):
            question_type = 'figure_ethnic'
            question_types.append(question_type)

        # 作品
        if self.check_words(self.work_qwds, question) and ('work' in types):
            question_type = 'figure_work'
            question_types.append(question_type)

        # 事迹
        if self.check_words(self.story_qwds, question) and ('story' in types):
            question_type = 'figure_story'
            question_types.append(question_type)

        # 职业
        if self.check_words(self.vocation_qwds, question) and ('vocation' in types):
            question_type = 'figure_vocation'
            question_types.append(question_type)

        # 官职
        if self.check_words(self.official_qwds, question) and ('official' in types):
            question_type = 'figure_official'
            question_types.append(question_type)

        # 前任皇帝
        if self.check_words(self.pre_emperor_qwds, question) and ('pre_emperor' in types):
            question_type = 'figure_pre_emperor'
            question_types.append(question_type)

        # 继任皇帝
        if self.check_words(self.next_emperor_qwds, question) and ('next_emperor' in types):
            question_type = 'figure_next_emperor'
            question_types.append(question_type)

        # 属性查询
        if self.check_words(self.attribute_qwds, question) and ('figure' in types):
            if '别名' in question or '昵称' in question:
                question_type = 'figure_alias_nickname'
            elif '在位时间' in question:
                question_type = 'figure_reigntime'
            elif '出生地' in question:
                question_type = 'figure_birthplace'
            elif '出生日期' in question:
                question_type = 'figure_birthdate'
            elif '死亡地' in question:
                question_type = 'figure_deathplace'
            elif '死亡日期' in question:
                question_type = 'figure_deathdate'
            question_types.append(question_type)

        # 查询特定时代下的历史人物
        if self.check_words(self.figure_qwds, question) and ('age' in types):
            question_type = 'age_figures'
            question_types.append(question_type)

        # 查询别名或昵称对应的历史人物
        if '别名' in question or '昵称' in question:
            question_type = 'figure_by_alias_nickname'
            question_types.append(question_type)

        # 查询出生地对应的历史人物
        if '出生地' in question:
            question_type = 'figure_by_birthplace'
            question_types.append(question_type)

        # 查询前任皇帝对应的继任皇帝
        if '前任皇帝'in question:
            question_type = 'figure_by_pre_emperor'
            question_types.append(question_type)

        # 查询历史人物的生平或简介
        if self.check_words(self.summary_qwds, question):
            question_type = 'figure_summary'
            question_types.append(question_type)

        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types

        return data

    '''构造词对应的类型'''
    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.figure_wds:
                wd_dict[wd].append('figure')
            if wd in self.age_wds:
                wd_dict[wd].append('age')
            if wd in self.ethnic_wds:
                wd_dict[wd].append('ethnic')
            if wd in self.work_wds:
                wd_dict[wd].append('work')
            if wd in self.story_wds:
                wd_dict[wd].append('story')
            if wd in self.vocation_wds:
                wd_dict[wd].append('vocation')
            if wd in self.official_wds:
                wd_dict[wd].append('official')
            if wd in self.pre_emperor_wds:
                wd_dict[wd].append('pre_emperor')
            if wd in self.next_emperor_wds:
                wd_dict[wd].append('next_emperor')
        return wd_dict

    '''构造actree，加速过滤'''
    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    '''问句过滤'''
    def check_history(self, question):
        region_wds = []
        for i in self.region_tree.iter(question):
            wd = i[1][1]
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i:self.wdtype_dict.get(i) for i in final_wds}

        return final_dict

    '''基于特征词进行分类'''
    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False


if __name__ == '__main__':
    handler = QuestionClassifier()
    while 1:
        question = input('input a question:')
        data = handler.classify(question)
        print(data)
