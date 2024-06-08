# -*- coding: utf8 -*-
# @File    : build_historicalgraph.py
# @Time    : 2024-06-05 14:44
# @Author  : songhc

import os
import json
from py2neo import Graph, Node


class HistoricalGraph:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.data_path = os.path.join(cur_dir, 'data/celebrity.json')
        # 创建实例
        self.g = Graph("bolt://neo4j:password@localhost:7687", auth=("neo4j", "xxxxxxxxx"))

    '''读取文件，返回包含所有节点/关系的元组'''

    def read_nodes(self):
        # 共9类节点
        figures = []  # 历史人物
        ages = []  # 所处时代
        ethnics = []  # 民族族群
        works = []  # 作品
        stories = []  # 主要事迹
        vocations = []  # 职业
        officials = []  # 官职
        pre_emperors = []  # 前任（皇帝）
        next_emperors = []  # 继任（皇帝）

        figures_infos = []  # 历史人物信息，
        # 里面是字典格式[{'name':...,'story':...,...,...},{}],里面是所有的实体节点

        # 构建节点实体关系，共8类关系
        rels_ages = []  # 人物－所处时代关系
        rels_ethnics = []  # 人物－民族族群关系
        rels_works = []  # 人物－作品关系
        rels_stories = []  # 人物－主要事迹关系
        rels_vocations = []  # 人物－职业
        rels_officials = []  # 人物－官职
        rels_pre_emperors = []  # 人物－前任皇帝
        rels_next_emperors = []  # 人物－继任皇帝

        count = 0
        with open(self.data_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for data_json in data:
            history_dict = {}
            count += 1
            print(count)
            figure = data_json.get('name', '')
            history_dict['name'] = figure # 历史人物名称
            figures.append(figure)  # 历史人物名称的list
            # 创建空值键值对
            history_dict['alia'] = data_json.get('alia', '')
            history_dict['age'] = data_json.get('age', '')
            history_dict['ethnic'] = data_json.get('ethnic', '')
            history_dict['birthplace'] = data_json.get('birthplace', '')
            history_dict['birthdate'] = data_json.get('birthdate', '')
            history_dict['deathdate'] = data_json.get('deathdate', '')
            history_dict['deathplace'] = data_json.get('deathplace', '')
            history_dict['work'] = data_json.get('work', '')
            history_dict['story'] = data_json.get('story', '')
            history_dict['vocation'] = data_json.get('vocation', '')
            history_dict['official'] = data_json.get('official', '')
            history_dict['nickname'] = data_json.get('nickname', '')
            history_dict['reigntime'] = data_json.get('reigntime', '')
            history_dict['pre_emperor'] = data_json.get('pre_emperor', '')
            history_dict['next_emperor'] = data_json.get('next_emperor', '')

            if history_dict['age']:
                ages.append(history_dict['age'])
                rels_ages.append([figure, history_dict['age']])

            if history_dict['ethnic']:
                ethnics.append(history_dict['ethnic'])
                rels_ethnics.append([figure, history_dict['ethnic']])

            if history_dict['work']:
                works.append(history_dict['work'])
                rels_works.append([figure, history_dict['work']])

            if history_dict['story']:
                stories.append(history_dict['story'])
                rels_stories.append([figure, history_dict['story']])

            if history_dict['vocation']:
                vocations.append(history_dict['vocation'])
                rels_vocations.append([figure, history_dict['vocation']])

            if history_dict['official']:
                officials.append(history_dict['official'])
                rels_officials.append([figure, history_dict['official']])

            if history_dict['pre_emperor']:
                pre_emperors.append(history_dict['pre_emperor'])
                rels_pre_emperors.append([figure, history_dict['pre_emperor']])

            if history_dict['next_emperor']:
                next_emperors.append(history_dict['next_emperor'])
                rels_next_emperors.append([figure, history_dict['next_emperor']])

            figures_infos.append(history_dict)
        return set(figures), set(ages), set(ethnics), set(works), set(stories), set(vocations), set(officials), set(
            pre_emperors), set(next_emperors), figures_infos, \
            rels_ages, rels_ethnics, rels_works, rels_stories, rels_vocations, rels_officials, rels_pre_emperors, rels_next_emperors

    '''建立节点，需要操作数据库的'''

    def create_node(self, label, nodes):
        count = 0
        for node_name in nodes: # 新建节点,每个节点有一个name属性
            node = Node(label, name=node_name)
            self.g.create(node) # 新建数据库节点
            count += 1
            print(count, len(nodes))
        return

    '''创建知识图谱历史人物的节点'''

    def create_figures_nodes(self, figures_infos):
        count = 0
        for history_dict in figures_infos: # 创建所有的实体节点,每个节点具有以下属性
            node = Node("History_Figure", name=history_dict['name'], age=history_dict['age'],
                        ethnic=history_dict['ethnic'],
                        birthplace=history_dict['birthplace'], birthdate=history_dict['birthdate'],
                        deathdate=history_dict['deathdate'], deathplace=history_dict['deathplace'],
                        work=history_dict['work'], story=history_dict['story'],
                        vocation=history_dict['vocation'], official=history_dict['official'],
                        nickname=history_dict['nickname'],
                        reigntime=history_dict['reigntime'], pre_emperors=history_dict['pre_emperor'],
                        next_emperors=history_dict['next_emperor'])

            self.g.create(node) # 新建实体节点
            count += 1
            print(count)
        return

    '''创建知识图谱实体节点类型schema'''

    def create_graphnodes(self): # 为每一个疾病都创建了一个节点,每个节点有9个属性
        Figures, Ages, Ethnics, Works, Stories, Vocations, Officials, Pre_emperors, Next_emperors, figures_infos, rels_ages, \
            rels_ethnics, rels_works, rels_stories, rels_vocations, rels_officials, rels_pre_emperors, rels_next_emperors = self.read_nodes()
        self.create_figures_nodes(figures_infos)
        self.create_node('Figure', Figures)
        print(len(Figures))
        self.create_node('Age', Ages)
        print(len(Ages))
        self.create_node('Ethnic', Ethnics)
        print(len(Ethnics))
        self.create_node('Work', Works)
        print(len(Works))
        self.create_node('Story', Stories)
        print(len(Stories))
        self.create_node('Vocation', Vocations)
        print(len(Vocations))
        self.create_node('Official', Officials)
        print(len(Officials))
        self.create_node('Pre_emperor', Pre_emperors)
        print(len(Pre_emperors))
        self.create_node('Next_emperor', Next_emperors)
        print(len(Next_emperors))
        return

    '''创建实体关系边'''

    def create_graphrels(self):
        Figures, Ages, Ethnics, Works, Stories, Vocations, Officials, Pre_emperors, Next_emperors, figures_infos, rels_ages, rels_ethnics, rels_works, rels_stories, rels_vocations, rels_officials, rels_pre_emperors, rels_next_emperors = self.read_nodes()
        self.create_relationship('Figure', 'Age', rels_ages, 'figure_age', '属于')
        self.create_relationship('Figure', 'Ethnic', rels_ethnics, 'figure_ethnic', '属于')
        self.create_relationship('Figure', 'Work', rels_works, 'figure_work', '人物作品or所属作品')
        self.create_relationship('Figure', 'Story', rels_stories, 'figure_story', '人物事迹')
        self.create_relationship('Figure', 'Vocation', rels_vocations, 'figure_vocation', '人物职业')
        self.create_relationship('Figure', 'Official', rels_officials, 'figure_official', '人物官职')
        self.create_relationship('Figure', 'Pre_emperor', rels_pre_emperors, 'pre_emperor', '上一代皇帝')
        self.create_relationship('Figure', 'Next_emperor', rels_next_emperors, 'next_emperor', '下一代皇帝')

    '''创建实体关联边'''

    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name):
        count = 0
        # 去重处理
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))
        all = len(set(set_edges))
        for edge in set(set_edges):
            edge = edge.split('###')
            p = edge[0]
            q = edge[1]
            query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name)
            try:
                self.g.run(query)
                # run()的用法大概是这样的,比如start_node, end_node这两种节点已经提前存进去了，比如label分别是Disease和Food,现在需要在他们间建立关系，括号里面是neo4j的查询语句cql，语法jiegou类似sql语句。关系就是rel_typ，还带了一个属性{name:'rel_name'}。
                # run("MATCH (p:start_node),(q:end_node) WHERE p.name='p' and q.name='q' create (p)-[rel:'rel_type'{name:'rel_name'}]->(q))

                count += 1
                print(rel_type, count, all)
            except Exception as e:
                print(e)
        return

    '''导出数据'''

    def export_data(self):
        Figures, Ages, Ethnics, Works, Stories, Vocations, Officials, Pre_emperors, Next_emperors, figures_infos, rels_ages, rels_ethnics, rels_works, rels_stories, rels_vocations, rels_officials, rels_pre_emperors, rels_next_emperors = self.read_nodes()
        f_figure = open('figure.txt', 'w+', encoding='utf-8')
        f_age = open('age.txt', 'w+', encoding='utf-8')
        f_ethnic = open('ethnic.txt', 'w+', encoding='utf-8')
        f_work = open('work.txt', 'w+', encoding='utf-8')
        f_story = open('story.txt', 'w+', encoding='utf-8')
        f_vocation = open('vocation.txt', 'w+', encoding='utf-8')
        f_official = open('official.txt', 'w+', encoding='utf-8')
        f_pre_emperor = open('pre_emperor.txt', 'w+', encoding='utf-8')
        f_next_emperor = open('next_emperor.txt', 'w+', encoding='utf-8')

        f_figure.write('\n'.join(list(Figures)))
        f_age.write('\n'.join(list(Ages)))
        f_ethnic.write('\n'.join(list(Ethnics)))
        f_work.write('\n'.join(list(Works)))
        f_story.write('\n'.join(list(Stories)))
        f_vocation.write('\n'.join(list(Vocations)))
        f_official.write('\n'.join(list(Officials)))
        f_pre_emperor.write('\n'.join(list(Pre_emperors)))
        f_next_emperor.write('\n'.join(list(Next_emperors)))

        f_figure.close()
        f_age.close()
        f_ethnic.close()
        f_work.close()
        f_story.close()
        f_vocation.close()
        f_official.close()
        f_pre_emperor.close()
        f_next_emperor.close()

        return


if __name__ == '__main__':
    handler = HistoricalGraph()
    handler.create_graphnodes()  # 建立节点
    handler.create_graphrels()  # 建立实体关系边
    handler.export_data() # 生成导出.txt文件
