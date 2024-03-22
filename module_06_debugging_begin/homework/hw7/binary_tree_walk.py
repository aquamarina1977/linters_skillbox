"""
Помимо того чтобы логи писать, нужно их ещё и уметь читать,
иначе мы будем как в известном анекдоте, писателями, а не читателями.

Для вас мы написали простую функцию обхода binary tree по уровням.
Также в репозитории есть файл с логами, написанными этой программой.

Напишите функцию restore_tree, которая принимает на вход путь до файла с логами
    и восстанавливать исходное BinaryTree.

Функция должна возвращать корень восстановленного дерева

def restore_tree(path_to_log_file: str) -> BinaryTreeNode:
    pass

Примечание: гарантируется, что все значения, хранящиеся в бинарном дереве уникальны
"""
import itertools
import logging
import random
from collections import deque
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger("tree_walk")


@dataclass
class BinaryTreeNode:
    val: int
    left: Optional["BinaryTreeNode"] = None
    right: Optional["BinaryTreeNode"] = None

    def __repr__(self):
        return f"<BinaryTreeNode[{self.val}]>"


def walk(root: BinaryTreeNode):
    queue = deque([root])

    while queue:
        node = queue.popleft()

        logger.info(f"Visiting {node!r}")

        if node.left:
            logger.debug(
                f"{node!r} left is not empty. Adding {node.left!r} to the queue"
            )
            queue.append(node.left)

        if node.right:
            logger.debug(
                f"{node!r} right is not empty. Adding {node.right!r} to the queue"
            )
            queue.append(node.right)


counter = itertools.count(random.randint(1, 10 ** 6))


def get_tree(max_depth: int, level: int = 1) -> Optional[BinaryTreeNode]:
    if max_depth == 0:
        return None

    node_left = get_tree(max_depth - 1, level=level + 1)
    node_right = get_tree(max_depth - 1, level=level + 1)
    node = BinaryTreeNode(val=next(counter), left=node_left, right=node_right)


    return node

# TODO можно такой вариант логики использовать
# def restore_tree(walk_log_path: str) -> BinaryTreeNode:
#     import re
#
#     tree: dict[int, BinaryTreeNode] = {}
#     PATTERN: str = r"\d+"
#
#     with open(walk_log_path) as log:
#         for line in log.readlines():
#             values: list[int] = list(map(int, re.findall(PATTERN, line)))
#             if "INFO" in line and values[0] not in tree:
#                 tree[values[0]] = BinaryTreeNode(val=values[0])
#             elif "left" in line:
#                 left = BinaryTreeNode(val=values[1])
#                 tree[values[1]] = left
#                 tree[values[0]].left = tree[values[1]]
#             elif "right" in line:
#                 right = BinaryTreeNode(val=values[1])
#                 tree[values[1]] = right
#                 tree[values[0]].right = tree[values[1]]
#
#     return next(iter(tree.values()))

def restore_tree(path_to_log_file: str = "walk_log_1.txt") -> BinaryTreeNode:
    nodes = {}

    with open(path_to_log_file, 'r') as file:
        for line in file:
            parts = line.strip().split()
            node_val = int(parts[1])
            left_val = int(parts[2]) if parts[2] != 'None' else None
            right_val = int(parts[3]) if parts[3] != 'None' else None

            node = BinaryTreeNode(node_val)
            nodes[node_val] = node

            if left_val:
                node.left = BinaryTreeNode(left_val)
                nodes[left_val] = node.left

            if right_val:
                node.right = BinaryTreeNode(right_val)
                nodes[right_val] = node.right

    print(nodes[1])


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(levelname)s:%(message)s",
        filename="walk_log_4.txt",
    )

    root = get_tree(7)
    walk(root)

