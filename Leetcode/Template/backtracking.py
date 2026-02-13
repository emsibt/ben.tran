def backtracking_template(nums):
    res = []

    def backtrack(start_index, current_path):
        if is_solution(current_path):
            res.append(current_path[:])
            return 
        
        for i in range(start_index, len(nums)):
            current_path.append(nums[i])

            backtrack(i, current_path)

            current_path.pop()
    backtrack(0, [])
    return res