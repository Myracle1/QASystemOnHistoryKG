#!/usr/bin/env python3
# coding: utf-8
# File: answer_search.py

from py2neo import Graph

class AnswerSearcher:
    def __init__(self):
        self.g = Graph("bolt://neo4j:password@localhost:7687", auth=("neo4j", "xxxxxxxx"))
        self.num_limit = 20

    '''执行cypher查询，并返回相应结果'''
    def search_main(self, sqls):
        final_answers = []
        for sql_ in sqls:
            question_type = sql_['question_type']
            queries = sql_['sql']
            answers = []
            for query in queries:
                ress = self.g.run(query).data()
                answers += ress
            final_answer = self.answer_prettify(question_type, answers)
            if final_answer:
                final_answers.append(final_answer)
        return final_answers

    '''根据对应的question_type，调用相应的回复模板'''
    def answer_prettify(self, question_type, answers):
        final_answer = []
        if not answers:
            return ''
        if question_type == 'figure_age':
            desc = [i['m.age'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}所属的时代是：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'figure_ethnic':
            desc = [i['m.ethnic'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}所属的民族是：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'figure_work':
            desc = [i['m.work'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的作品包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'figure_story':
            desc = [i['m.story'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的事迹包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'figure_vocation':
            desc = [i['m.vocation'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的职业是：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'figure_official':
            desc = [i['m.official'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的官职是：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'figure_pre_emperor':
            desc = [i['m.pre_emperor'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的前任皇帝是：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'figure_next_emperor':
            desc = [i['m.next_emperor'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的继任皇帝是：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'figure_alias_nickname':
            alias = [i['m.alia'] for i in answers]
            nickname = [i['m.nickname'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的别名是：{1}，昵称是：{2}'.format(subject, '；'.join(list(set(alias))[:self.num_limit]), '；'.join(list(set(nickname))[:self.num_limit]))

        elif question_type == 'figure_reigntime':
            desc = [i['m.reigntime'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的在位时间是：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'figure_birthplace':
            desc = [i['m.birthplace'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的出生地是：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'figure_birthdate':
            desc = [i['m.birthdate'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的出生日期是：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'figure_deathplace':
            desc = [i['m.deathplace'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的死亡地是：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'figure_deathdate':
            desc = [i['m.deathdate'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的死亡日期是：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'age_figures':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['m.age']
            final_answer = '{0}时期的人物有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'figure_by_alias_nickname':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['m.alia'] if answers[0]['m.alia'] else answers[0]['m.nickname']
            final_answer = '别名或昵称为{0}的人物是：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'figure_by_birthplace':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['m.birthplace']
            final_answer = '出生地为{0}的人物是：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'figure_by_pre_emperor':
            desc = [i['m.name'] for i in answers]
            pre_emperor = answers[0]['m.pre_emperor']
            next_emperor = answers[0]['m.next_emperor']
            final_answer = '前任皇帝是{0}的人物是：{1}，其继任皇帝是：{2}'.format(pre_emperor, '；'.join(list(set(desc))[:self.num_limit]), next_emperor)

        elif question_type == 'figure_summary':
            desc = [i['m.summary'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的生平是：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        return final_answer


if __name__ == '__main__':
    searcher = AnswerSearcher()
