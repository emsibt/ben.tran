"""Sort
1. Quick Sort: O(n log n) average, O(n2) worst
2. Merge Sort: O (n log n)
3. Build-in Sort: O (n log n)
"""

from typing import List


def quick_sort(nums: List[int]) -> None:
    def partition(nums, l, r):
        p, pivot = r, nums[r]
        i = l
        while i < p:
            if nums[i] < pivot:
                nums[i], nums[p - 1] = nums[p - 1], nums[i]
                nums[p], nums[p - 1] = nums[p - 1], nums[p]
                i -= 1
                p -= 1
            i += 1
        return p

    def quick_sort_helper(nums, l, r):
        if l >= r:
            return
        p = partition(nums, l, r)
        quick_sort_helper(nums, l, p - 1)
        quick_sort_helper(nums, p + 1, r)

    quick_sort_helper(nums, 0, len(nums) - 1)
