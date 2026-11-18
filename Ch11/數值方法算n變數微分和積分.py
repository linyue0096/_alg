import numpy as np
import itertools

def gradient_nd(f, x, h=1e-5):
    """計算 n 變數函數在點 x 的梯度向量 ∇f(x)"""
    x = np.array(x, dtype=float)
    grad = np.zeros_like(x)
    for i in range(len(x)):
        x_plus = x.copy()
        x_minus = x.copy()
        x_plus[i] += h
        x_minus[i] -= h
        grad[i] = (f(x_plus) - f(x_minus)) / (2 * h)
    return grad

def riemann_nd(f, low, high, n_steps=40):
    """計算 n 變數函數在超矩形區間內的定積分 (超體積)"""
    low = np.array(low, dtype=float)
    high = np.array(high, dtype=float)
    dx = (high - low) / n_steps
    axes = [np.linspace(l + d/2, h - d/2, n_steps) for l, h, d in zip(low, high, dx)]
    
    total = 0.0
    for point in itertools.product(*axes):
        total += f(np.array(point))
    return total * np.prod(dx)

if __name__ == "__main__":
    print("=== 第 3 題：n 變數數值微分(梯度)與積分(超體積)測試 ===")

    f_3d = lambda v: v[0]**2 + 2*v[1]*v[2] + v[2]**3
    grad_res = gradient_nd(f_3d, [1.0, 2.0, 3.0])
    print(f"[梯度測試] f(x,y,z) = x^2 + 2yz + z^3 在 (1, 2, 3):")
    print(f"  數值梯度 = {np.round(grad_res, 6)} | 理論值 = [ 2.  6. 31.]")

    f_2d = lambda v: v[0] + v[1]
    vol_2d = riemann_nd(f_2d, [0, 0], [2, 3], n_steps=60)
    print(f"[超體積測試 1] 2變數 ∫∫(x + y) dx dy, [0,2]x[0,3]:")
    print(f"  黎曼積分 = {vol_2d:.6f} | 理論值 = 15.000000")

    f_3d_vol = lambda v: v[0] * v[1] * v[2]
    vol_3d = riemann_nd(f_3d_vol, [0, 0, 0], [1, 2, 3], n_steps=40)
    print(f"[超體積測試 2] 3變數 ∫∫∫(x*y*z) dxdydz, [0,1]x[0,2]x[0,3]:")
    print(f"  黎曼積分 = {vol_3d:.6f} | 理論值 = 4.500000")