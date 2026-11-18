import numpy as np

def diff_1d(f, x, h=1e-5):
    """中央差分法計算單變數微分 f'(x)"""
    return (f(x + h) - f(x - h)) / (2 * h)

def riemann_1d(f, low, high, n_steps=100000):
    """中點黎曼和計算單變數定積分 ∫f(x)dx"""
    dx = (high - low) / n_steps
    x = np.linspace(low + dx / 2, high - dx / 2, n_steps)
    return np.sum(f(x)) * dx

if __name__ == "__main__":
    print("=== 第 1 題：單變數數值微分與積分測試 ===")
    
    f1 = lambda x: x**3 + 2*x**2 - 5*x + 1
    print(f"[微分測試 1] f(x) = x^3 + 2x^2 - 5x + 1 在 x=2:")
    print(f"  數值解 = {diff_1d(f1, 2.0):.8f} | 理論值 = 15.00000000")
   
    f2 = lambda x: np.exp(2 * x)
    print(f"[微分測試 2] f(x) = e^(2x) 在 x=0:")
    print(f"  數值解 = {diff_1d(f2, 0.0):.8f} | 理論值 = 2.00000000")

    print(f"[積分測試 1] ∫sin(x)dx, x ∈ [0, pi]:")
    print(f"  數值解 = {riemann_1d(np.sin, 0, np.pi):.8f} | 理論值 = 2.00000000")

    f3 = lambda x: x**2
    print(f"[積分測試 2] ∫x^2 dx, x ∈ [0, 3]:")
    print(f"  數值解 = {riemann_1d(f3, 0, 3):.8f} | 理論值 = 9.00000000")