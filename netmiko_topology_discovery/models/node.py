import json


class node:
    i = 0
    def __init__(self, name: str):
        self.name = name
        self.id = node.i
        node.i += 1

    
