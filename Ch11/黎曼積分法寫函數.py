import numpy as np
import time

def integral(f, low, high, n_steps=10):
    """黎曼積分法計算 n 變數積分（n 為 low, high 的陣列長度）"""
    low = np.array(low, dtype=float)
    high = np.array(high, dtype=float)
    n_dim = len(low)
    
    if n_steps ** n_dim > 1e7:
        return f"無法計算（需 {n_steps}^{n_dim} 個網格點，觸發維度災難）"
        
    dx = (high - low) / n_steps
    axes = [np.linspace(l + d/2, h - d/2, n_steps) for l, h, d in zip(low, high, dx)]
    grid = np.meshgrid(*axes, indexing='ij')
    points = np.stack(grid, axis=-1).reshape(-1, n_dim)
    
    return float(np.sum(f(points)) * np.prod(dx))

if __name__ == "__main__":
    print("=== 第 5 題：黎曼積分法 integral(f, low, high) 多維度測試 ===")
    
    f_test = lambda x: np.sum(np.asarray(x)**2, axis=-1)

    for n in [1, 2, 5, 100]:
        low = [0] * n
        high = [1] * n
        t0 = time.time()
        ans = integral(f_test, low, high, n_steps=10)
        elapsed = time.time() - t0
        
        if isinstance(ans, float):
            print(f"n = {n:3d} 維 | 理論值: {n/3:8.4f} | 黎曼積分結果: {ans:8.4f} | 耗時: {elapsed:.4f}s")
        else:
            print(f"n = {n:3d} 維 | 理論值: {n/3:8.4f} | 黎曼積分結果: {ans}")