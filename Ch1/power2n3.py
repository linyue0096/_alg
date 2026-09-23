import time

def power2n_2b(n):
    if n == 0:
        return 1
    return 2 * power2n_2b(n - 1)

if __name__ == "__main__":
    n = 100
    
    t_start = time.perf_counter()
    
    result = power2n_2b(n)
    
    t_end = time.perf_counter()
    
    print(f"計算 2^{n} 完成！")
    print(f"結果：{result}")
    print(f"耗時：{t_end - t_start:.6f} 秒")