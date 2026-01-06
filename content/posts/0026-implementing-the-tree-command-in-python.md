---
title: "用Python实现tree命令"
date: 2021-09-22
draft: false
tags:
  - "Python"
  - "工具"
  - "编程语言"
---

**要点**：在对树结构进行递归时，如果某个节点需要来自父节点的信息，甚至需要来自所有祖先节点的信息时，可以在递归函数中增加参数，将需要的信息传递下去。

初始版本的代码如下：

```python
C_BLANK = ' '
C_V_LINE = '|'
C_H_LINE = '-'
C_MID = '├'
C_LAST = '└'


class TreePrinter:
    def __init__(self, value_field='value', children_field='children', value_getter=None, children_getter=None):
        self.value_field = value_field
        self.children_field = children_field
        self.value_getter = value_getter
        self.children_getter = children_getter

    def print(self, root):
        self._print_tree(root, True, [])

    def _print_tree(self, node, current_is_last, parents_states):
        value = self.value_getter(node) if self.value_getter else getattr(node, self.value_field)
        children = self.children_getter(node) if self.children_getter else getattr(node, self.children_field)

        if parents_states:
            for state in parents_states[1:]:
                print(f'{C_BLANK}{C_BLANK}' if state else f'{C_V_LINE}{C_BLANK}', end='')
            print(f'{C_LAST}{C_H_LINE}' if current_is_last else f'{C_MID}{C_H_LINE}', end='')

        print(value)

        len_children = len(children)
        next_parents_states = [*parents_states, current_is_last]

        for i in range(0, len_children):
            self._print_tree(children[i], i == len_children - 1, next_parents_states)
```

测试用例1：

```python
root = Node('object',
            Node('animal',
                 Node('cat'),
                 Node('dog'),
                 Node('bird'),),
            Node('plant',
                 Node('flower')))

printer = TreePrinter()
printer.print(root)
```

测试用例2：

```python
root = ['object',
            ['animal',
                 ['cat'],
                 ['dog'],
                 ['bird']],
            ['plant',
                 ['flower']]]

printer = TreePrinter(
    value_getter=lambda n: n[0],
    children_getter=lambda n: n[1:])
printer.print(root)
```

两个测试用例的结果一样，如下：

![tree_printer](https://user-images.githubusercontent.com/3950285/134381919-c3ca004a-52ca-4130-8434-c5946a43472d.png)

