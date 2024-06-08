# -*- coding: utf-8 -*-
# @File    : update_nodeAttribute.py
# @Time    : 2024-06-06 16:25
# @Author  : songhc

# 基于当前的知识图谱，对历史人物的属性进行更新，增加一个summary（生平）的属性

import os
import json
from py2neo import Graph, NodeMatcher

class UpdateHistoricalGraph:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.summary_path = os.path.join(cur_dir, 'data/celebrity_summary.json')
        self.g = Graph("bolt://neo4j:password@localhost:7687", auth=("neo4j", "xxxxxxxx"))

    def add_summaries(self):
        matcher = NodeMatcher(self.g)

        with open(self.summary_path, 'r', encoding='utf-8') as file:
            summaries = json.load(file)

        count = 0
        for item in summaries:
            name = item.get('name')
            summary = item.get('summary', '')

            if name and summary:
                node = matcher.match("History_Figure", name=name).first()
                if node:
                    node['summary'] = summary
                    self.g.push(node)
                    count += 1
                    print(f"Updated {count} nodes: {name}")

if __name__ == '__main__':
    handler = UpdateHistoricalGraph()
    handler.add_summaries()
