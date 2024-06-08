#!/usr/bin/env python3
# coding: utf-8
# File: question_parser.py

class QuestionPaser:
    '''构建实体节点'''
    def build_entitydict(self, args):
        entity_dict = {}

        for arg, types in args.items():
           # for type in types:
            if types not in entity_dict:
                entity_dict[types] = [arg]
            else:
                entity_dict[types].append(arg)
        # print(entity_dict)
        return entity_dict

    '''解析主函数'''
    def parser_main(self, res_classify):
        args = res_classify['args']
        entity_dict = self.build_entitydict(args)
        question_types = res_classify['question_types']
        sqls = []
        for question_type in question_types:
            sql_ = {}
            sql_['question_type'] = question_type
            sql = []
            if question_type == 'figure_age':
                sql = self.sql_transfer(question_type, entity_dict.get('figure'))

            elif question_type == 'figure_ethnic':
                sql = self.sql_transfer(question_type, entity_dict.get('figure'))

            elif question_type == 'figure_work':
                sql = self.sql_transfer(question_type, entity_dict.get('figure'))

            elif question_type == 'figure_story':
                sql = self.sql_transfer(question_type, entity_dict.get('figure'))

            elif question_type == 'figure_vocation':
                sql = self.sql_transfer(question_type, entity_dict.get('figure'))

            elif question_type == 'figure_official':
                sql = self.sql_transfer(question_type, entity_dict.get('figure'))

            elif question_type == 'figure_pre_emperor':
                sql = self.sql_transfer(question_type, entity_dict.get('figure'))

            elif question_type == 'figure_next_emperor':
                sql = self.sql_transfer(question_type, entity_dict.get('figure'))

            elif question_type == 'figure_alias_nickname':
                sql = self.sql_transfer(question_type, entity_dict.get('figure'))

            elif question_type == 'figure_reigntime':
                sql = self.sql_transfer(question_type, entity_dict.get('figure'))

            elif question_type == 'figure_birthplace':
                sql = self.sql_transfer(question_type, entity_dict.get('figure'))

            elif question_type == 'figure_birthdate':
                sql = self.sql_transfer(question_type, entity_dict.get('figure'))

            elif question_type == 'figure_deathplace':
                sql = self.sql_transfer(question_type, entity_dict.get('figure'))

            elif question_type == 'figure_deathdate':
                sql = self.sql_transfer(question_type, entity_dict.get('figure'))

            elif question_type == 'age_figures':
                sql = self.sql_transfer(question_type, entity_dict.get('age'))

            elif question_type == 'figure_by_alias':
                sql = self.sql_transfer(question_type, entity_dict.get('figure'))

            elif question_type == 'figure_by_nickname':
                sql = self.sql_transfer(question_type, entity_dict.get('figure'))

            elif question_type == 'figure_by_birthplace':
                sql = self.sql_transfer(question_type, entity_dict.get('figure'))

            elif question_type == 'figure_by_pre_emperor':
                sql = self.sql_transfer(question_type, entity_dict.get('figure'))

            elif question_type == 'figure_summary':
                sql = self.sql_transfer(question_type, entity_dict.get('figure'))

            if sql:
                sql_['sql'] = sql
                sqls.append(sql_)

        return sqls

    '''针对不同的问题，分开进行处理'''
    def sql_transfer(self, question_type, entities):
        if not entities:
            return []

        # 查询语句
        sql = []
        # 查询历史人物的时代
        if question_type == 'figure_age':
            sql = ["MATCH (m:History_Figure) where m.name = '{0}' return m.name, m.age".format(i) for i in entities]

        # 查询历史人物的民族
        elif question_type == 'figure_ethnic':
            sql = ["MATCH (m:History_Figure) where m.name = '{0}' return m.name, m.ethnic".format(i) for i in entities]

        # 查询历史人物的作品
        elif question_type == 'figure_work':
            sql = ["MATCH (m:History_Figure) where m.name = '{0}' return m.name, m.work".format(i) for i in entities]

        # 查询历史人物的事迹
        elif question_type == 'figure_story':
            sql = ["MATCH (m:History_Figure) where m.name = '{0}' return m.name, m.story".format(i) for i in entities]

        # 查询历史人物的职业
        elif question_type == 'figure_vocation':
            sql = ["MATCH (m:History_Figure) where m.name = '{0}' return m.name, m.vocation".format(i) for i in entities]

        # 查询历史人物的官职
        elif question_type == 'figure_official':
            sql = ["MATCH (m:History_Figure) where m.name = '{0}' return m.name, m.official".format(i) for i in entities]

        # 查询历史人物的前任皇帝
        elif question_type == 'figure_pre_emperor':
            sql = ["MATCH (m:History_Figure) where m.name = '{0}' return m.name, m.pre_emperor".format(i) for i in entities]

        # 查询历史人物的继任皇帝
        elif question_type == 'figure_next_emperor':
            sql = ["MATCH (m:History_Figure) where m.name = '{0}' return m.name, m.next_emperor".format(i) for i in entities]

        # 查询历史人物的别名或昵称
        elif question_type == 'figure_alias_nickname':
            sql = ["MATCH (m:History_Figure) where m.name = '{0}' return m.name, m.alia, m.nickname".format(i) for i in entities]

        # 查询历史人物的在位时间
        elif question_type == 'figure_reigntime':
            sql = ["MATCH (m:History_Figure) where m.name = '{0}' return m.name, m.reigntime".format(i) for i in entities]

        # 查询历史人物的出生地
        elif question_type == 'figure_birthplace':
            sql = ["MATCH (m:History_Figure) where m.name = '{0}' return m.name, m.birthplace".format(i) for i in entities]

        # 查询历史人物的出生日期
        elif question_type == 'figure_birthdate':
            sql = ["MATCH (m:History_Figure) where m.name = '{0}' return m.name, m.birthdate".format(i) for i in entities]

        # 查询历史人物的死亡地
        elif question_type == 'figure_deathplace':
            sql = ["MATCH (m:History_Figure) where m.name = '{0}' return m.name, m.deathplace".format(i) for i in entities]

        # 查询历史人物的死亡日期
        elif question_type == 'figure_deathdate':
            sql = ["MATCH (m:History_Figure) where m.name = '{0}' return m.name, m.deathdate".format(i) for i in entities]

        # 查询特定时代下的历史人物
        elif question_type == 'age_figures':
            sql = ["MATCH (m:History_Figure)-[:figure_age]->(n:Age) where n.name = '{0}' return m.name".format(i) for i in entities]

        # 查询别名对应的历史人物
        elif question_type == 'figure_by_alias':
            sql = ["MATCH (m:History_Figure) where m.alia = '{0}' return m.name".format(i) for i in entities]

        # 查询昵称对应的历史人物
        elif question_type == 'figure_by_nickname':
            sql = ["MATCH (m:History_Figure) where m.nickname = '{0}' return m.name".format(i) for i in entities]

        # 查询出生地对应的历史人物
        elif question_type == 'figure_by_birthplace':
            sql = ["MATCH (m:History_Figure) where m.birthplace = '{0}' return m.name".format(i) for i in entities]

        # 查询前任皇帝对应的继任皇帝
        elif question_type == 'figure_by_pre_emperor':
            sql = ["MATCH (m:History_Figure) where m.pre_emperor = '{0}' return m.name, m.next_emperor".format(i) for i in entities]

        # 查询历史人物的生平
        elif question_type == 'figure_summary':
            sql = ["MATCH (m:History_Figure) where m.name = '{0}' return m.name, m.summary".format(i) for i in entities]

        return sql

if __name__ == '__main__':
    handler = QuestionPaser()
