"""Recursion is Banned
1. Using Stack
"""

from typing import List


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def preorderTraversa(root: TreeNode) -> List[TreeNode]:
    if not root:
        return []
    stack = [root]
    res = []
    while stack:
        node = stack.pop()
        res.append(node)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return res
