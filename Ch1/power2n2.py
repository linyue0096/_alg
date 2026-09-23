import time

def power2n_2a(n):
    if n == 0:
        return 1
    return power2n_2a(n - 1) + power2n_2a(n - 1)

test_values_2a = [100]

print("--- 方法 2a 正確性與耗時測試 ---")
for n in test_values_2a:
    start = time.perf_counter()
    ans = power2n_2a(n)
    cost = time.perf_counter() - start
    print(f"2^{n:>2} = {ans:<10} (耗時: {cost:.6f} 秒)")