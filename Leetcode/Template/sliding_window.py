from typing import List
def longestWindow(nums: List[int]) -> int:
    j = 0
    res = 0
    for i in range(len(nums)):
        # using nums[i] update state
        while invalid():
            # using nums[j] update state
            j+=1
        res = max(res, i - j + 1)
    return res