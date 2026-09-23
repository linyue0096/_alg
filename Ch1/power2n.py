import sys
import time

sys.setrecursionlimit(2000)

# 方法 1：直接計算
def power2n_1(n):
    return 2**n

# 方法 2b：單遞迴
def power2n_2b(n):
    if n == 0:
        return 1
    return 2 * power2n_2b(n - 1)

# 方法 3：遞迴 + 查表
def power2n_3(n, memo=None):
    if memo is None:
        memo = {}
    if n == 0:
        return 1
    if n in memo:
        return memo[n]
    memo[n] = power2n_3(n - 1, memo) + power2n_3(n - 1, memo)
    return memo[n]

# 方法 2a：雙遞迴（無查表）
def power2n_2a(n):
    if n == 0:
        return 1
    return power2n_2a(n - 1) + power2n_2a(n - 1)


if __name__ == "__main__":
    n = 100
    print(f"=== 開始測試四種方法 (n = {n}) ===\n")

    # --- 1. 測試方法 1 ---
    t0 = time.perf_counter()
    ans1 = power2n_1(n)
    t1 = time.perf_counter()
    print(f"方法 1 耗時: {t1 - t0:.8f} 秒")

    # --- 2. 測試方法 2b ---
    t0 = time.perf_counter()
    ans2b = power2n_2b(n)
    t1 = time.perf_counter()
    print(f"方法 2b 耗時: {t1 - t0:.8f} 秒")

    # --- 3. 測試方法 3 ---
    t0 = time.perf_counter()
    ans3 = power2n_3(n)
    t1 = time.perf_counter()
    print(f"方法 3 耗時: {t1 - t0:.8f} 秒")

    # --- 4. 測試方法 2a ---
    print("\n--- 正在測試方法 2a ---")
    print("說明：因為計算量高達 2^101 次運算，程式將卡死在此處以證明『出不來』...")
    ans2a = power2n_2a(n)  # 這行會卡死
    print(f"方法 2a 耗時: {ans2a}")  # 永遠不會印出