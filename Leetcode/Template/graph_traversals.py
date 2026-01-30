from typing import List, Dict, Set
def dfs(graph: Dict[int, List[int]], cur: int, visited: Set[int]):
    if cur in visited: return

    visited.add(cur)

    for next in graph[cur]:
        dfs(graph, next, visited)

from collections import deque
def bfs(graph: Dict[int, List[int]], node: int):
    queue = deque([node])
    visited = set([node])
    while queue:
        cur = queue.popleft()

        for next in graph[cur]:
            if next in visited:
                continue
                
            queue.append(next)
            visited.add(next)