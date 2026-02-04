def solveDP(n, choices):
    dp = [gia_tri_mac_dinh] * (n+1)
    dp[0] = 0

    for i in range(1, n+1):
        for choice in choices:
            if i >= choices:
                # min
                dp[i] = min(dp[i], dp[i-choice] + 1)
                #max
                dp[i] = max(dp[i], dp[i-choice] + value)
                # Dang dem so cach
                dp[i]+=dp[i-choice]
    return dp[n]