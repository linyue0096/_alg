# 蒙地卡羅隨機法

## 課堂繳交
## 程式碼使用gemini幫我寫，readme是利用Gemini說明再自己寫
## Gemini連結:https://share.gemini.google/HBmjZEuFyyx7
---

### 什麼是數值微分與積分？
1. **核心概念**：許多函數無法直接求得解析解，或積分難以手動計算，因此需仰賴數值方法進行近似求解，兩者的幾何意義、誤差來源與穩定性截然不同，數值積分是「把小誤差平均掉」，天生穩定；數值微分是「把小誤差放大」，天生敏感且容易不準
2. **數值微分**：
   - **中央差分法**：利用函數在目標點左右微小擾動 $\pm h$ 的斜率平均值逼近導數 $f'(x) \approx \frac{f(x+h) - f(x-h)}{2h}$，截斷誤差為 $O(h^2)$，精確度高於單邊差分
   - **多變數梯度**：對 $n$ 維向量的每個座標軸分別執行中央差分，求得函數上升最快的方向向量
3. **數值積分**：
   - **中點黎曼和**：將積分區間切分為多個等距子區間或 $n$ 維超立方體網格，取每個網格中點的函數值乘上子區間長度（或超體積）加總
   - **蒙地卡羅法**：在積分定義域內均勻隨機採樣 $N$ 個樣本點，計算樣本函數值的平均值並乘上定義域總長度（或總超體積）
4. **維度災難與收斂特性**：
   - **網格法瓶頸**：黎曼積分在 $n$ 維空間中，若每個維度切分 $k$ 格，總計算點數為 $k^n$。當維度升高（如 $n=100$）時，網格數量呈指數爆炸，導致記憶體與算力耗盡
   - **蒙地卡羅優勢**：誤差收斂速度為 $O(1/\sqrt{N})$，**與空間維度 $n$ 無關**，因此能有效克服高維度積分的維度災難

---

### 程式演算法

1. **單變數數值微分與黎曼積分**
   - `diff_1d`：採用中央差分法，預設步長 $h = 10^{-5}$，計算單變數函數在指定點的一階導數
   - `riemann_1d`：使用 `np.linspace` 建立區間中點陣列，以向量化運算快速求得單變數定積分

2. **單變數蒙地卡羅積分**
   - `mc_1d`：透過 `np.random.uniform` 在 $[low, high]$ 均勻抽取 $N$ 個樣本，計算 $(high - low) \times \frac{1}{N}\sum f(x_i)$

3. **多變數梯度與超體積黎曼積分**
   - `gradient_nd`：逐一對輸入向量 $\mathbf{x}$ 的第 $i$ 個分量加減 $h$，組合成完整梯度向量 $\nabla f(\mathbf{x})$
   - `riemann_nd`：利用 `itertools.product` 走訪所有 $n$ 維網格中點，累加函數值並乘以微小超立方體體積 $\prod dx_i$

4. **多變數蒙地卡羅積分**
   - `mc_nd`：生成形狀為 `(n_samples, n_dim)` 的均勻隨機樣本矩陣，計算平均函數值後乘上總超體積 $\prod (high_i - low_i)$

5. **高維度黎曼積分與維度災難防呆測試**
   - 內建網格上限保護機制（`n_steps ** n_dim > 1e7`），當維度過高（如 $n=100$ 需 $10^{100}$ 個網格點）時直接攔截並回傳維度災難提示，避免系統當機

6. **高維度蒙地卡羅積分（突破維度災難）**
   - 使用相同測試函數 $f(\mathbf{x}) = \sum_{i=1}^n x_i^2$，固定採樣數 $N = 200,000$，分別測試 $n \in \{1, 2, 5, 100\}$ 維空間，驗證高維度下的計算效率與準確度。

---

### 測試與實作驗證

#### 1. 測試 1：單變數微分與中點黎曼積分
- **程式碼**：
```python
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
```
- **輸出**:
```
=== 第 1 題：單變數數值微分與積分測試 ===
[微分測試 1] f(x) = x^3 + 2x^2 - 5x + 1 在 x=2:
  數值解 = 15.00000000 | 理論值 = 15.00000000
[微分測試 2] f(x) = e^(2x) 在 x=0:
  數值解 = 2.00000000 | 理論值 = 2.00000000
[積分測試 1] ∫sin(x)dx, x ∈ [0, pi]:
  數值解 = 2.00000000 | 理論值 = 2.00000000
[積分測試 2] ∫x^2 dx, x ∈ [0, 3]:
  數值解 = 9.00000000 | 理論值 = 9.00000000
```
- 學習:
    - 高精度收斂：在單變數（1D）問題中，中央差分法與高網格密度的中點黎曼和皆能收斂至小數點後第 8 位完全貼合理論解析解

#### 2. 測試 2：用蒙地卡羅法算單變數積分
- **程式碼**：
```python
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
```
- **輸出**:
```
=== 第 2 題：蒙地卡羅法單變數積分測試 ===
[測試 1] ∫sin(x)dx, x ∈ [0, pi]:
  蒙地卡羅解 = 2.000906 | 理論值 = 2.000000
[測試 2] ∫(3x^2 + 2x)dx, x ∈ [1, 4]:
  蒙地卡羅解 = 78.057091 | 理論值 = 78.000000
```
- 學習:
    - 統計誤差特性：即使採樣 $500,000$ 點，蒙地卡羅法在 1D 積分上仍會因隨機抽樣變異而產生微幅波動（收斂速度 $O(1/\sqrt{N})$），精確度低於確定性網格法

#### 3. 測試 3：用數值方法算n變數微分和積分
- **程式碼**：
```python
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

    # 測試範例 1 (3變數梯度)：f(x, y, z) = x^2 + 2*y*z + z^3
    # 偏導數為 [2x, 2z, 2y + 3z^2]，代入 (1, 2, 3) 理論值為 [2, 6, 31]
    f_3d = lambda v: v[0]**2 + 2*v[1]*v[2] + v[2]**3
    grad_res = gradient_nd(f_3d, [1.0, 2.0, 3.0])
    print(f"[梯度測試] f(x,y,z) = x^2 + 2yz + z^3 在 (1, 2, 3):")
    print(f"  數值梯度 = {np.round(grad_res, 6)} | 理論值 = [ 2.  6. 31.]")

    # 測試範例 2 (2變數超體積積分)：f(x, y) = x + y 在 x∈[0, 2], y∈[0, 3]
    # 理論值 = ∫_0^3 ∫_0^2 (x+y) dx dy = 15
    f_2d = lambda v: v[0] + v[1]
    vol_2d = riemann_nd(f_2d, [0, 0], [2, 3], n_steps=60)
    print(f"[超體積測試 1] 2變數 ∫∫(x + y) dx dy, [0,2]x[0,3]:")
    print(f"  黎曼積分 = {vol_2d:.6f} | 理論值 = 15.000000")

    # 測試範例 3 (3變數超體積積分)：f(x, y, z) = x * y * z 在 [0, 1] x [0, 2] x [0, 3]
    # 理論值 = (1^2/2) * (2^2/2) * (3^2/2) = 0.5 * 2 * 4.5 = 4.5
    f_3d_vol = lambda v: v[0] * v[1] * v[2]
    vol_3d = riemann_nd(f_3d_vol, [0, 0, 0], [1, 2, 3], n_steps=40)
    print(f"[超體積測試 2] 3變數 ∫∫∫(x*y*z) dxdydz, [0,1]x[0,2]x[0,3]:")
    print(f"  黎曼積分 = {vol_3d:.6f} | 理論值 = 4.500000")
```
- **輸出**:
```
=== 第 3 題：n 變數數值微分(梯度)與積分(超體積)測試 ===
[梯度測試] f(x,y,z) = x^2 + 2yz + z^3 在 (1, 2, 3):
  數值梯度 = [ 2.  6. 31.] | 理論值 = [ 2.  6. 31.]
[超體積測試 1] 2變數 ∫∫(x + y) dx dy, [0,2]x[0,3]:
  黎曼積分 = 15.000000 | 理論值 = 15.000000
[超體積測試 2] 3變數 ∫∫∫(x*y*z) dxdydz, [0,1]x[0,2]x[0,3]:
  黎曼積分 = 4.500000 | 理論值 = 4.500000
```
- 學習:
    - 計算複雜度差異：數值梯度計算量僅與維度n成線性正比（$2n$ 次函數評估），適合用於高維最佳化；但 3 維網格積分即使每維僅切 40 格，總計算量已達 $40^3 = 64,000$ 次，隨維度呈指數膨脹

#### 4. 測試 4：用蒙地卡羅法算n變數積分
- **程式碼**：
```python
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
```
- **輸出**:
```
=== 第 4 題：蒙地卡羅法 n 變數積分(超體積)測試 ===
[測試 1] 2變數 ∫∫(x + y) dx dy, [0,2]x[0,3]:
  蒙地卡羅解 = 15.001432 | 理論值 = 15.000000
[測試 2] 3變數 ∫∫∫(x*y*z) dxdydz, [0,1]x[0,2]x[0,3]:
  蒙地卡羅解 = 4.501577 | 理論值 = 4.500000
```
- 學習:
    - 架構簡潔性：蒙地卡羅法無需撰寫多重巢狀迴圈，無論輸入空間為 2 維或 3 維，均只需生成 (n_samples, n_dim) 隨機矩陣並計算樣本均值乘上總超體積就好

#### 5. 測試 5：黎曼積分法
- **程式碼**：
```python
import numpy as np
import time

def integral(f, low, high, n_steps=10):
    """黎曼積分法計算 n 變數積分（n 為 low, high 的陣列長度）"""
    low = np.array(low, dtype=float)
    high = np.array(high, dtype=float)
    n_dim = len(low)
    
    # 安全防呆：避免 100 維產生 10^100 個網格點導致記憶體溢位與死機
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
```
- **輸出**:
```
=== 第 5 題：黎曼積分法 integral(f, low, high) 多維度測試 ===
n =   1 維 | 理論值:   0.3333 | 黎曼積分結果:   0.3325 | 耗時: 0.0001s
n =   2 維 | 理論值:   0.6667 | 黎曼積分結果:   0.6650 | 耗時: 0.0001s
n =   5 維 | 理論值:   1.6667 | 黎曼積分結果:   1.6625 | 耗時: 0.0030s
n = 100 維 | 理論值:  33.3333 | 黎曼積分結果: 無法計算（需 10^100 個網格點，觸發維度災難）
```
- 學習:
    - 防呆：網格點數隨維度呈指數爆炸（$10^1 \to 10^2 \to 10^5 \to 10^{100}$），在 $n=100$ 維時超出物理算力與記憶體極限，觸發安全攔截機制

#### 6. 測試 6：蒙地卡羅法
- **程式碼**：
```python
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
```
- **輸出**:
```
=== 第 6 題：蒙地卡羅法 integral(f, low, high) 多維度測試 ===
n =   1 維 | 理論值:   0.3333 | 蒙地卡羅結果:   0.3338 | 耗時: 0.0041s
n =   2 維 | 理論值:   0.6667 | 蒙地卡羅結果:   0.6673 | 耗時: 0.0099s
n =   5 維 | 理論值:   1.6667 | 蒙地卡羅結果:   1.6645 | 耗時: 0.0201s
n = 100 維 | 理論值:  33.3333 | 蒙地卡羅結果:  33.3290 | 耗時: 0.3701s
```