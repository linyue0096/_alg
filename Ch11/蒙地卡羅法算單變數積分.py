import numpy as np

def mc_1d(f, low, high, n_samples=500000):
    """蒙地卡羅法計算單變數定積分"""
    x = np.random.uniform(low, high, n_samples)
    return (high - low) * np.mean(f(x))

if __name__ == "__main__":
    np.random.seed(42)
    print("=== 第 2 題：蒙地卡羅法單變數積分測試 ===")

    res1 = mc_1d(np.sin, 0, np.pi, n_samples=500000)
    print(f"[測試 1] ∫sin(x)dx, x ∈ [0, pi]:")
    print(f"  蒙地卡羅解 = {res1:.6f} | 理論值 = 2.000000")

    f_poly = lambda x: 3 * (x**2) + 2 * x
    res2 = mc_1d(f_poly, 1, 4, n_samples=500000)
    print(f"[測試 2] ∫(3x^2 + 2x)dx, x ∈ [1, 4]:")
    print(f"  蒙地卡羅解 = {res2:.6f} | 理論值 = 78.000000")