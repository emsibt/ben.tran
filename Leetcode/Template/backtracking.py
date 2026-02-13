def backtracking_template(nums):
    res = []

    def backtrack(start_index, curr_path):
        if is_solution():
            res.append(curr_path[:])
            return
        
        for i in range(start_index, len(nums)):
            curr_path.append(nums[i])
            backtrack(i, curr_path)
            curr_path.pop()
    backtrack(0, [])
    return res