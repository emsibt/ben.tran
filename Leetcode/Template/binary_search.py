"""Input Array is Sorted
1. Binary Search: O(log n)
2. Two Pointers: O(n)
"""

from typing import List


def binary_search(nums: List[int], target: int) -> int:
    # sorted array
    l, r = 0, len(nums) - 1
    while l <= r:
        m = l + ((r - l) // 2)
        if nums[m] == target:
            return m
        elif nums[m] < target:
            l = m + 1
        else:
            r = m - 1
    return -1
