from typing import List, Set
def dfs(grid: List[List[int]], r: int, c: int, visited: Set[List[int]]):
    if r < 0 or c < 0 or r >= len(grid) or c >= len(grid[0]) or (r, c) in visited:
        return
    
    visited.add((r,c))
    dfs(grid, r+1, c)
    dfs(grid, r-1, c)
    dfs(grid, r, c+1)
    dfs(grid, r, c-1)

from collections import deque

directions = [(1,0), (-1,0), (0,1), (0,-1)]
def bfs(grid: List[List[int]], r: int, c: int):
    q = deque((r,c))
    visited = set((r,c))
    while q:
        r, c = q.popleft()
        for dr, dc in directions:
            nr, nc = r+dr, c+dc
            if nr < 0 or nc < 0 or nr >= len(grid) or nc >= len(grid[0]) or (nr,nc) in visited:
                continue

            visited.add((nr,nc))
            q.append((nr,nc))
