"""Input is a Binary Tree
1. DFS(Preorder, Inorder, Postorder): O(n)
2. BFS(Leval Order): O(n)
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def dfs_top_down(root: TreeNode, param) -> None:
    if not root:
        return True
    if not check_logic(root, param):
        return False

    new_param_l = update(param, root.val)
    new_param_r = update(param, root.val)
    return dfs_top_down(root.left, new_param_l) and dfs_top_down(
        root.right, new_param_r
    )


def dfs_bottom_up(root: TreeNode) -> int:
    if not root:
        return 0

    l_res = dfs_bottom_up(root.left)
    r_res = dfs_bottom_up(root.right)

    res = process(root.val, l_res, r_res)

    return res


from collections import deque


def bfs(root: TreeNode) -> None:
    q = deque([root])
    while q:
        size = len(q)
        for i in range(size):
            node = q.popleft()
            print(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)

        # process
