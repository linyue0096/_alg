import time

def power2n_3(n, memo=None):
    if memo is None:
        memo = {}
    if n == 0:
        return 1
    if n in memo:
        return memo[n]
    memo[n] = power2n_3(n - 1, memo) + power2n_3(n - 1, memo)
    return memo[n]

if __name__ == "__main__":
    n = 100
    
    t0 = time.perf_counter()
    ans = power2n_3(n)
    t1 = time.perf_counter()
    
    print(f"2^{n} 計算成功！")
    print(f"結果位數: {len(str(ans))} 位數")
    print(f"耗費時間: {t1 - t0:.6f} 秒")