import time

def power2n_1(n):
    return 2**n

test_values = [100]

print("--- 方法 1 正確性測試 ---")
for n in test_values:
    print(f"2^{n} = {power2n_1(n)}")

# 效能測試
start = time.perf_counter()
ans = power2n_1(25)
cost = time.perf_counter() - start
print(f"\n效能測試 (n=25): 結果 = {ans}, 耗時 = {cost:.8f} 秒")