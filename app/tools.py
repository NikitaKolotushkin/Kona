#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import codecs
import json
import heapq
from pyisemail import is_email


def graph_maker(graph, start, end):
    queue = [(0, start, [])]
    visited = set()
    shortest_paths = {start: (0, [])}
    while queue:
        (cost, node, path) = heapq.heappop(queue)
        if node not in visited:
            visited.add(node)
            path = path + [node]
            if node == end:
                return cost, path
            for next_node in graph[node]:
                if next_node not in visited:
                    heapq.heappush(queue, (cost + 1, next_node, path))
                    if next_node not in shortest_paths or cost + 1 < shortest_paths[next_node][0]:
                        shortest_paths[next_node] = (cost + 1, path + [next_node])

    return shortest_paths[end]


def validate_email(email) -> bool:
    """ Проверяет валидность электронной почте по заданному регулярным выражением шаблону
    
    :rtype: bool
    :return: True если email прошел валидацию, иначе - False
    """
    pattern = '(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
    bool_result_with_dns = is_email(email, check_dns=True)

    return bool(re.match(pattern, email)) and bool_result_with_dns

def open_relations():
    with codecs.open('relations.json', 'r', 'utf_8_sig') as f:
        dict_obj = json.load(f)
    return dict_obj


def dump_relations(dict_obj):
    with codecs.open('relations.json', 'w', 'utf_8_sig') as file:
        json.dump(dict_obj, file)
