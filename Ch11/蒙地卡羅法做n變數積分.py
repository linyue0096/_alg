import numpy as np
import time

def integral(f, low, high, n_samples=300000):
    """蒙地卡羅法計算 n 變數積分（n 為 low, high 的陣列長度）"""
    low = np.array(low, dtype=float)
    high = np.array(high, dtype=float)
    n_dim = len(low)
    
    samples = np.random.uniform(low, high, size=(n_samples, n_dim))
    volume = np.prod(high - low)
    return float(volume * np.mean(f(samples)))

if __name__ == "__main__":
    np.random.seed(42)
    print("=== 第 6 題：蒙地卡羅法 integral(f, low, high) 多維度測試 ===")
    f_test = lambda x: np.sum(np.asarray(x)**2, axis=-1)

    for n in [1, 2, 5, 100]:
        low = [0] * n
        high = [1] * n
        t0 = time.time()
        ans = integral(f_test, low, high, n_samples=300000)
        elapsed = time.time() - t0
        print(f"n = {n:3d} 維 | 理論值: {n/3:8.4f} | 蒙地卡羅結果: {ans:8.4f} | 耗時: {elapsed:.4f}s")