# BPlusTree
A memory B+tree for Python3.

## QuickStart
Copy the folder `bplustree` to your project.

### Create a BPlusTree object
```python
from bplus_tree import BPlusTree
# Create a b+tree with b factor is 3
t = BPlusTree(3)
```

### Insert key value pair
```python
t.insert(1, 'Hello World!')
t.insert(7, 'a')
t.insert(7, 'b')
t.insert(3, 'c')
t.insert(5, '3')
```

### Retrieve value from tree through key
```python
>>> t.get(1)
['Hello World!']
>>> t.get(7)
['a', 'b']
```
or
```python
>>> t[1]
['Hello World!']
>>> t[7]
['a', 'b']
```

### Range search
```
range_search(self, notation, cmp_key)
```
range search compare with `cmp_key` 

`notation` supports '>' '<' '>=' '<='

```python
>>> t.range_search('>', 3)
['3', 'a', 'b']
>>> t.range_search('>=', 3)
['c', '3', 'a', 'b']
```

### Keys, values and item pairs
```python
>>> t.keys()
[1, 3, 5, 7]
>>> t.values()
['Hello World!', 'c', '3', 'a', 'b']
>>> t.items()
[(1, ['Hello World!']), (3, ['c']), (5, ['3']), (7, ['a', 'b'])]
```

