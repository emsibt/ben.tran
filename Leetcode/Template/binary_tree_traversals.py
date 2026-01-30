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