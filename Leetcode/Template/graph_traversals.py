"""Input is a Graph
1. DFS(Recursion, Stack): O(n)
2. BFS(Queue): O(n)
"""

from typing import List, Dict, Set
from collections import deque


def dfs(graph: Dict[int, List[int]], cur: int, visited: Set[int]):
    if cur in visited:
        return
    visited.add(cur)
    for next in graph[cur]:
        dfs(graph, next, visited)


def bfs(graph: Dict[int, List[int]], node: int):
    q = deque([node])
    visited = set([node])
    while q:
        cur = q.popleft()
        for next in graph[cur]:
            if next in visited:
                continue

            q.append(next)
            visited.add(next)
