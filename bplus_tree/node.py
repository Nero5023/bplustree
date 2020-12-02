import bisect
import math


def flatten(l):
    return [y for x in l for y in x]


class Leaf:
    def __init__(self, previous_leaf, next_leaf, parent, b_factor):
        self.previous = previous_leaf
        self.next = next_leaf
        self.parent = parent
        self.b_factor = b_factor
        self.a_factor = math.ceil(b_factor/2)
        self.keys = []
        self.children = []

    @property
    def is_root(self):
        return self.parent is None

    def insert(self, key, value):
        index = bisect.bisect_left(self.keys, key)
        if index < len(self.keys) and self.keys[index] == key:
            self.children[index].append(value)
        else:
            self.keys.insert(index, key)
            self.children.insert(index, [value])
            if len(self.keys) > self.b_factor:
                split_index = math.ceil(self.b_factor/2)
                self.split(split_index)

    def get(self, key):
        index = bisect.bisect_left(self.keys, key)
        if index < len(self.keys) and self.keys[index] == key:
            return self.children[index]
        else:
            return None

    def split(self, index):
        new_leaf_node = Leaf(self, self.next, self.parent, self.b_factor)
        new_leaf_node.keys = self.keys[index:]
        new_leaf_node.children = self.children[index:]
        self.keys = self.keys[:index]
        self.children = self.children[:index]
        if self.next is not None:
            self.next.previous = new_leaf_node
        self.next = new_leaf_node
        if self.is_root:
            self.parent = Node(None, None, [new_leaf_node.keys[0]], [self, self.next], b_factor=self.b_factor, parent=None)
            self.next.parent = self.parent
        else:
            self.parent.add_child(self.next.keys[0], self.next)

    def find_left(self, key, include_key=True):
        items = []
        index = bisect.bisect_right(self.keys, key) - 1
        if index == -1:
            items = []
        else:
            if include_key:
                items = self.children[:index+1]
            else:
                if key == self.keys[index]:
                    index -= 1
                items = self.children[:index+1]
        return self.left_items() + flatten(items)

    def find_right(self, key, include_key=True):
        items = []
        index = bisect.bisect_left(self.keys, key)
        if index == len(self.keys):
            items = []
        else:
            if include_key:
                items = self.children[index:]
            else:
                if key == self.keys[index]:
                    index += 1
                items = self.children[index:]
        return flatten(items) + self.right_items()

    def left_items(self):
        items = []
        node = self
        while node.previous is not None:
            node = node.previous
        while node != self:
            for elem in node.children:
                if type(elem) == list:
                    items.extend(elem)
                else:
                    items.append(elem)
            node = node.next
        return items

    def right_items(self):
        items = []
        node = self.next
        while node is not None:
            for elem in node.children:
                if type(elem) == list:
                    items.extend(elem)
                else:
                    items.append(elem)
            node = node.next
        return items

    def items(self):
        return zip(self.keys, self.children)

class Node:
    def __init__(self, previous_node, next_node, keys, children, b_factor, parent=None):
        self.previous = previous_node
        self.next = next_node
        self.keys = keys
        self.children = children
        self.b_factor = b_factor
        self.a_factor = math.ceil(b_factor / 2)
        self.parent = parent

    @property
    def degree(self):
        return len(self.children)

    @property
    def is_root(self):
        return self.parent is None

    def insert(self, key, value):
        index = bisect.bisect_right(self.keys, key)
        node = self.children[index]
        node.insert(key, value)

    def get(self, key):
        index = bisect.bisect_right(self.keys, key)
        return self.children[index].get(key)

    def find_left(self, key, include_key=True):
        index = bisect.bisect_right(self.keys, key)
        return self.children[index].find_left(key, include_key)

    def find_right(self, key, include_key=True):
        index = bisect.bisect_right(self.keys, key)
        return self.children[index].find_right(key, include_key)

    def add_child(self, key, child):
        index = bisect.bisect_right(self.keys, key)
        self.keys.insert(index, key)
        self.children.insert(index+1, child)
        if self.degree > self.b_factor:
            split_index = math.floor(self.b_factor / 2)
            self.split(split_index)

    def split(self, index):
        split_key = self.keys[index]
        new_node = Node(self, self.next, self.keys[index+1:], self.children[index+1:], self.b_factor, self.parent)
        for node in self.children[index+1:]:
            node.parent = new_node
        self.keys = self.keys[:index]
        self.children = self.children[:index+1]

        if self.next is not None:
            self.next.previous = new_node
        self.next = new_node
        if self.is_root:
            self.parent = Node(None, None, [split_key], [self, self.next], b_factor=self.b_factor, parent=None)
            self.next.parent = self.parent
        else:
            self.parent.add_child(split_key, self.next)
