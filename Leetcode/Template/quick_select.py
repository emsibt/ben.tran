"""Find the Top/Least Kth element
1. QuickSelect: O(n) average, O(n2) worst
2. Heap: O(n log k)
"""

from typing import List


def kClosest(points: List[List[int]], k: int) -> List[List[int]]:
    def dist(index):
        return points[index][0] ** 2 + points[index][1] ** 2

    def partition(nums, l, r):
        p, pivot = r, dist(r)
        i = l
        while i < p:
            if dist(i) < pivot:
                nums[i], nums[p - 1] = nums[p - 1], nums[i]
                nums[p], nums[p - 1] = nums[p - 1], nums[p]
                i -= 1
                p -= 1
            i += 1
        return p

    def quick_select(nums, l, r):
        if l >= r:
            return
        p = partition(nums, l, r)
        if p < k:
            return quick_select(nums, p + 1, r)
        if p > k:
            return quick_select(nums, l, p - 1)
        return

    quick_select(points, 0, len(points) - 1)
    return points[:k]
