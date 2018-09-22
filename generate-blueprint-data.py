#!/usr/bin/env python

import json

def find_item_by_name(core_data, name):
    for item in core_data['blueprints']:
        if item['name'] == name:
            return item

    raise RuntimeError("Failed to find '" + name + "' in core blueprint data")


def resolve_dependencies(core_data, item):
    children = []

    if 'depends' not in item:
        return children

    for d in item['depends']:
        count = 1
        if 'count' in d:
            count = d['count']

        children.append({
            'name': d['name'],
            'count': count,
            'children': resolve_dependencies(core_data, find_item_by_name(core_data, d['name']))
        })

    return children


with open('core-data.json') as f:
    core_data = json.load(f)


bp_list = []
for blueprint in core_data['blueprints']:
    bp_list.append({
        'name': blueprint['name'],
        'children': resolve_dependencies(core_data, blueprint)
    })

base_items = []
for item in bp_list:
    if item['children'] == []:
        base_items.append(item)

bp_list = [{'name': 'Basic Items', 'children': base_items}] + [item for item in bp_list if item['children'] != []]

graph_data = {
    'name': 'Subnautica',
    'children': bp_list
}


with open('graph-data.json', 'w') as f:
    json.dump(graph_data, f)
