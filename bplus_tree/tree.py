from bplus_tree.node import Leaf, Node


class BPlusTree:
    def __init__(self, b_factor=32):
        self.b_factor = b_factor
        self.root = Leaf(None, None, None, b_factor)
        self.size = 0

    def get(self, key):
        return self.root.get(key)

    def __getitem__(self, key):
        return self.get(key)

    def __len__(self):
        return self.size

    def insert(self, key, value):
        self.root.insert(key, value)
        self.size += 1
        if self.root.parent is not None:
            self.root = self.root.parent

    def range_search(self, notation, cmp_key):
        notation = notation.strip()
        if notation not in [">", "<", ">=", "<="]:
            raise Exception("Nonsupport notation: {}. Only '>' '<' '>=' '<=' are supported")
        if notation == '>':
            return self.root.find_right(cmp_key, False)
        if notation == '>=':
            return self.root.find_right(cmp_key, True)
        if notation == '<':
            return self.root.find_left(cmp_key, False)
        if notation == '<=':
            return self.root.find_left(cmp_key, True)

    def show(self):
        layer = 0
        node = self.root
        while node is not None:
            print("Layer: {}".format(layer))
            inner_node = node
            while inner_node is not None:
                print(inner_node.keys, end=' ')
                inner_node = inner_node.next
            print('')
            node = node.children[0]
            layer += 1
            if type(node) != Leaf and type(node) != Node:
                break

    def leftmost_leaf(self):
        leaf = self.root
        while type(leaf) != Leaf:
            leaf = leaf.children[0]
        return leaf

    def items(self):
        leaf = self.leftmost_leaf()
        items = []
        while leaf is not None:
            pairs = list(leaf.items())
            items.extend(pairs)
            leaf = leaf.next
        return items

    def keys(self):
        leaf = self.leftmost_leaf()
        ks = []
        while leaf is not None:
            ks.extend(leaf.keys)
            leaf = leaf.next
        return ks

    def values(self):
        leaf = self.leftmost_leaf()
        vals = []
        while leaf is not None:
            for elem in leaf.children:
                if type(elem) == list:
                    vals.extend(elem)
                else:
                    vals.append(elem)
            leaf = leaf.next
        return vals

    def height(self):
        node = self.root
        height = 0
        while type(node) != Leaf:
            height += 1
            node = node.children[0]
        return height


if __name__ == '__main__':
    t = BPlusTree(32)
    nums = [55,44,65,16,80,74,14,19,95,36,2,90,74,94,27,89,85]
    for x in nums:
        t.insert(x, x)
    print(t.items())