import numpy as np

def mc_nd(f, low, high, n_samples=500000):
    """蒙地卡羅法計算 n 變數定積分 (超體積)"""
    low = np.array(low, dtype=float)
    high = np.array(high, dtype=float)
    n_dim = len(low)
    
    samples = np.random.uniform(low, high, size=(n_samples, n_dim))
    values = np.apply_along_axis(f, 1, samples)
    volume = np.prod(high - low)
    return volume * np.mean(values)

if __name__ == "__main__":
    np.random.seed(42)
    print("=== 第 4 題：蒙地卡羅法 n 變數積分(超體積)測試 ===")

    f_2d = lambda v: v[0] + v[1]
    res_2d = mc_nd(f_2d, [0, 0], [2, 3], n_samples=500000)
    print(f"[測試 1] 2變數 ∫∫(x + y) dx dy, [0,2]x[0,3]:")
    print(f"  蒙地卡羅解 = {res_2d:.6f} | 理論值 = 15.000000")

    f_3d = lambda v: v[0] * v[1] * v[2]
    res_3d = mc_nd(f_3d, [0, 0, 0], [1, 2, 3], n_samples=500000)
    print(f"[測試 2] 3變數 ∫∫∫(x*y*z) dxdydz, [0,1]x[0,2]x[0,3]:")
    print(f"  蒙地卡羅解 = {res_3d:.6f} | 理論值 = 4.500000")