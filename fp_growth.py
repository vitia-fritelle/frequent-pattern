from collections import Counter
from typing import Iterable

class Tree_Node:
    def __init__(self, name_value: str, number_occur: int, parent_node):
        self.name: str = name_value
        self.count: int = number_occur
        self.node_link: Tree_Node | None = None
        self.parent: Tree_Node = parent_node
        self.children: dict[str, Tree_Node] = dict()
    
    def increment(self, num_occur: int):
        self.count += num_occur
    
    def display_tree(self, ind: int = 1):
        print( ' '*ind, self.name, ' ', self.count)
        for child in self.children.values():
            child.display_tree(ind+1)

    def update_node_link(self, target_node): 
        ''' 
        Get the node in the last level that has the same name and points 
        to it
        '''
        if self.node_link:
            self.node_link.update_node_link(target_node)
        else:
            self.node_link = target_node 

    def update_tree(self, items: list[str], h_table, count: int):
        '''Update tree with ordered items'''
        if items:
            item = items[0]
            if item in list(self.children.keys()):
                self.children[item].increment(count)
            else:
                self.children[item] = Tree_Node(item, count, self)
                h_table.update_header(item, self.children)
            self.children[item].update_tree(items[1:], h_table, count)

class Header_Table:
    def __init__(self, words_list: list[str], min_support: int = 1):
        self.header = {
            key: {'count': value, 'first_item': None} #first_item is a Tree_Node
            for key, value in Counter(words_list).items()
            if value >= min_support
        }
        self.freq_itemset = set(self.header.keys())
    def update_header(self, item: str, children: dict[str, Tree_Node]):
        node = children[item]
        if self.header[item]['first_item'] == None:
            self.header[item]['first_item'] = node
        else:
            self.header[item].update_node_link(node) # type: ignore

def get_list_items(acc: list[str], values: list[Iterable[str]]):
    if values:
        acc += list(values[0])
        return get_list_items(acc, values[1:])
    else:
        return acc

def create_tree(data: dict[Iterable[str], int], min_support: int = 1):
    words_list = get_list_items(list(), list(data.keys()))
    h_table = Header_Table(words_list, min_support)
    if not h_table.freq_itemset:
        print("No items meet min support.")
        return None, None
    ret_tree = Tree_Node('Null Set', 1, None)
    for trans_set, count in data.items():
        local_D = {
            item: h_table.header[item]['count']
            for item in trans_set
            if item in h_table.freq_itemset
        }
        if local_D:
            ordered_items = [
                v[0] for v in sorted(
                    local_D.items(),
                    key = lambda p: p[1],
                    reverse = True
                )
            ]
            ret_tree.update_tree(ordered_items, h_table, count)
    return ret_tree, h_table


