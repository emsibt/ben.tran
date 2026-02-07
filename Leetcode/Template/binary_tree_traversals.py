# DSF - recursion
def preorder(root: TreeNote) -> None:
    if not root: return
    print(root.val)
    preorder(root.left)
    preorder(root.right)

def inorder(root: TreeNote) -> None:
    if not root: return
    inorder(root.left)
    print(root.val)
    inorder(root.right)

def postorder(root: TreeNote) -> None:
    if not root: return
    postorder(root.left)
    postorder(root.right)
    print(root.val)

def dfs_top_down(node, param):
    if not node:
        return True

    if not check_logic(node, param):
        return False

    new_param_left = update(param, node.val)
    new_param_right = update(param, node.val)
    return dfs_top_down(node.left, new_param_left) and dfs_top_down(node.right, new_param_right)

def dfs_bottom_up(node):
    if not node:
        return 0
    
    left_result = dfs_bottom_up(node.left)
    right_result = dfs_bottom_up(node.right)

    my_res = process(node.val, left_result, right_result)
    return my_res

# BFS - deque
from collections import deque

def bfs(root: TreeNote) -> None:
    queue = deque([root])
    while queue:
        size = len(queue)
        for i in range(size):
            node = queue.popleft()
            print(node.val)
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)

        print or return