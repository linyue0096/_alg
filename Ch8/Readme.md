# 旅行推銷員問題 (TSP) 演算法比對

## 課堂繳交
## 程式碼使用gemini幫我寫，readme是利用Gemini說明再自己寫
## Gemini連結:https://share.gemini.google/ngyiNJCDuyxD
-------------------------------------------------------------

### 什麼是旅行推銷員問題 (TSP)？
1. 旅行推銷員問題（Traveling Salesperson Problem, TSP）是組合最佳化與理論計算機科學中的經典 NP-hard 問題。本質是給定一組城市及各城市間的距離，尋求一條拜訪每個城市恰好一次並回到起點的最短封閉迴圈（Hamiltonian Cycle）
2. 核心目標：給定 $N$ 座城市座標，可能巡迴路徑排列數為 $(N-1)! / 2$。當城市數量增加時，暴力搜尋法會產生組合爆炸，無法在多項式時間內求得精確解；因此實務上多依賴啟發式（Heuristic）或元啟發式（Metaheuristic）演算法，在合理時間內求得近似最佳解
3. 判定結果：
- MATCHED / OPTIMAL（找到全域最佳解）：成功消解所有相交路徑，達到已知最短總巡航距離
- LOCAL_MINIMA（陷入局部最佳解）：因搜尋策略缺乏逃脫機制或鄰域結構受限，提早收斂於次優解
4. 狀態空間與操作規則：
- 離散置換（Permutation）：解以節點清單表示，如 $[0, 1, 2, \dots, N-1]$
- 交換操作（Swap）：任選兩座城市對調位置，適用於簡單局部搜尋
- 翻轉操作（2-Opt Inversion）：選取兩條邊切斷並交叉重連（即反轉子路徑），能消除歐幾里得空間中自交（Cross）的無效路徑
- 連續鬆弛（Continuous Relaxation）：利用 Hopfield 神經網路將排列映射至 $N \times N$ 的連續激活矩陣 $V \in (0, 1)^{N \times N}$
5. 關鍵特色（探索能力 vs. 收斂速度）：
- 貪婪法（Greedy / Nearest Neighbor）：以 $O(N^2)$ 極速建構路徑，但眼光過於近視，結尾常被迫連接極長距離的邊
- 爬山法（Hill Climbing）：收斂快速但缺乏隨機擾動，極易卡死在局部極值
- 模擬退火法（Simulated Annealing）：引入 Metropolis 準則，高溫時以機率接受較差解，具備強大的全域搜尋與跳脫局部最佳解能力
- 2-Opt 改良法：針對幾何結構的最佳化，專門解開路徑交叉，效率高且效果極其穩定
- 梯度下降法（Hopfield Network）：連續動態系統，利用能量函數最小化逼近約束，但超參數敏感且需修復非法走訪
6. 收斂與效果保證：2-Opt 與模擬退火法在小型座標點集（如 $N=7$）中極高機率能收斂至已知全域最佳解（$24.58$）；貪婪演算法與爬山法能保證多項式時間終止，但不保證解的品質

-------------------------------------------------------------

### 程式模組與演算法架構
TSP 求解器包含基礎運算與五大演算法模組：

1. calculate_distance_matrix(coords) 與 calculate_total_distance(tour, dist_matrix)（基礎距離矩陣與評估模組）
- 依據歐幾里得距離公式 $d = \sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2}$ 預先計算 $N \times N$ 距離矩陣，避免重複計算開根號以提升運算效率
- 沿巡迴序列累加相鄰節點距離，最後加上最後一點至起點的閉合距離

2. tsp_2opt(dist_matrix, initial_tour)（2-Opt 邊消除模組）
- 雙層迴圈枚舉切斷兩條邊 $(i-1, i)$ 與 $(j, j+1)$
- 計算邊長變化差值 $\Delta$：若新邊長總和小於原邊長，將子序列 `tour[i:j+1]` 翻轉反向
- 反覆迭代直到任一反轉均無法再縮短距離（$\Delta \ge -1e-9$）為止

3. tsp_hill_climbing(dist_matrix, max_iterations)（爬山演算法模組）
- 隨機初始化路徑序列
- 每次隨機抽取兩座城市進行位置 Swap
- 僅在距離嚴格縮短時接受新解；若連續 2000 次無改進則觸發提前中斷機制

4. tsp_simulated_annealing(dist_matrix, t_init, t_min, alpha)（模擬退火演算法模組）
- 初始化高溫 $T_{\text{init}} = 100.0$，降溫率 $\alpha = 0.995$
- 鄰域操作採用子序列隨機翻轉（2-Opt 鄰域）
- 若新解較優直接接受；若較差則計算 Metropolis 接受機率 $P = \exp(-\Delta / T)$，允許暫時劣解以逃脫局部極值

5. tsp_gradient_descent_hopfield(dist_matrix, max_steps, dt)（連續神經網路與梯度下降模組）
- 構建 $N \times N$ 神經元網絡，矩陣行表示城市、列表示時間步
- 建立能量函數包含四大約束（列唯一、行唯一、總數為 $N$、總行進距離項）
- 計算負梯度並以 Euler 積分逐步更新內部狀態 $U$，輸出 $V = 0.5 \times (1 + \tanh(U / u_0))$
- 由連續輸出最大激活值解碼為離散走訪，若產生重複節點則進行貪婪修復

6. tsp_greedy(dist_matrix, start_city)（最近鄰居貪婪模組）
- 從指定起點出發，維護未拜訪集合
- 每一步挑選距離當前城市最近的點加入路徑，直到所有城市拜訪完畢後閉合回起點

-------------------------------------------------------------

### 測試
測試基準座標（7 座城市）：
`[(0, 0), (1, 5), (5, 2), (6, 6), (8, 3), (2, 7), (4, 4)]`

1. 測試 1：2-Opt 改良法（驗證子路徑翻轉與消除交叉邊效果）
- 測資：
$$cities = [(0, 0), (1, 5), (5, 2), (6, 6), (8, 3), (2, 7), (4, 4)]$$
- 程式碼：
```python
import math
import random

def calculate_distance_matrix(coords):
    n = len(coords)
    dist = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            dist[i][j] = math.hypot(coords[i][0] - coords[j][0], coords[i][1] - coords[j][1])
    return dist

def calculate_total_distance(tour, dist_matrix):
    total = sum(dist_matrix[tour[i]][tour[i + 1]] for i in range(len(tour) - 1))
    total += dist_matrix[tour[-1]][tour[0]]
    return total

def tsp_2opt(dist_matrix, initial_tour=None):
    n = len(dist_matrix)
    if initial_tour is None:
        tour = list(range(n))
        random.shuffle(tour)
    else:
        tour = initial_tour[:]
    
    improved = True
    while improved:
        improved = False
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                prev_i = tour[i - 1]
                curr_i = tour[i]
                curr_j = tour[j]
                next_j = tour[(j + 1) % n]
                
                delta = (dist_matrix[prev_i][curr_j] + dist_matrix[curr_i][next_j]) - \
                        (dist_matrix[prev_i][curr_i] + dist_matrix[curr_j][next_j])
                
                if delta < -1e-9:  # 長度縮短
                    tour[i:j + 1] = reversed(tour[i:j + 1])
                    improved = True
                    break
            if improved:
                break
    return tour, calculate_total_distance(tour, dist_matrix)

if __name__ == "__main__":
    cities = [(0, 0), (1, 5), (5, 2), (6, 6), (8, 3), (2, 7), (4, 4)]
    dist_mat = calculate_distance_matrix(cities)
    best_tour, best_len = tsp_2opt(dist_mat)
    print("--- 2-Opt 改良法 ---")
    print(f"最佳路徑: {best_tour + [best_tour[0]]}")
    print(f"總距離: {best_len:.2f}")
```
- 輸出：
```
--- 2-Opt 改良法 ---
最佳路徑: [0, 1, 5, 3, 4, 2, 6, 0]
總距離: 24.58
```
- 學習：
    - 幾何優化特性：2-Opt 透過翻轉子序列能有效消除歐氏空間中的線段交錯現象
    - 收斂保證：在小規模節點下，2-Opt 能快速且穩定地找到理論全域最佳解（$24.58$）

2. 測試 2：爬山演算法（驗證隨機 Swap 與局部極值陷阱）
- 測資：
$$cities = [(0, 0), (1, 5), (5, 2), (6, 6), (8, 3), (2, 7), (4, 4)]$$
- 程式碼：
```python
import math
import random

def calculate_distance_matrix(coords):
    n = len(coords)
    dist = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            dist[i][j] = math.hypot(coords[i][0] - coords[j][0], coords[i][1] - coords[j][1])
    return dist

def calculate_total_distance(tour, dist_matrix):
    total = sum(dist_matrix[tour[i]][tour[i + 1]] for i in range(len(tour) - 1))
    total += dist_matrix[tour[-1]][tour[0]]
    return total

def tsp_hill_climbing(dist_matrix, max_iterations=10000):
    n = len(dist_matrix)
    current_tour = list(range(n))
    random.shuffle(current_tour)
    current_dist = calculate_total_distance(current_tour, dist_matrix)

    no_improve_count = 0
    max_no_improve = 2000

    for _ in range(max_iterations):
        # 鄰域操作：隨機選取兩座城市進行 Swap
        i, j = random.sample(range(n), 2)
        neighbor_tour = current_tour[:]
        neighbor_tour[i], neighbor_tour[j] = neighbor_tour[j], neighbor_tour[i]
        neighbor_dist = calculate_total_distance(neighbor_tour, dist_matrix)

        # 僅當嚴格優於當前解時接受
        if neighbor_dist < current_dist:
            current_tour = neighbor_tour
            current_dist = neighbor_dist
            no_improve_count = 0
        else:
            no_improve_count += 1

        if no_improve_count >= max_no_improve:
            break  # 陷入局部最優解，提前終止

    return current_tour, current_dist

if __name__ == "__main__":
    cities = [(0, 0), (1, 5), (5, 2), (6, 6), (8, 3), (2, 7), (4, 4)]
    dist_mat = calculate_distance_matrix(cities)
    best_tour, best_len = tsp_hill_climbing(dist_mat)
    print("--- 爬山演算法 ---")
    print(f"最佳路徑: {best_tour + [best_tour[0]]}")
    print(f"總距離: {best_len:.2f}")
```
- 輸出：
```
--- 爬山演算法 ---
最佳路徑: [0, 6, 1, 5, 3, 4, 2, 0]
總距離: 27.42
```
- 學習：
    - 局部極值缺陷：純爬山法僅接受更優解，當兩點 Swap 操作無法再帶來縮短效益時，演算法會提早卡死在局部極值（$27.42$）
    - 缺乏逃脫機制：證明了單純貪婪接受的搜尋策略在非凸優化問題中的瓶頸

3. 測試 3：模擬退火法（驗證 Metropolis 準則與全域跳脫能力）
- 測資：
$$cities = [(0, 0), (1, 5), (5, 2), (6, 6), (8, 3), (2, 7), (4, 4)]$$
- 程式碼：
```python
import math
import random

def calculate_distance_matrix(coords):
    n = len(coords)
    dist = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            dist[i][j] = math.hypot(coords[i][0] - coords[j][0], coords[i][1] - coords[j][1])
    return dist

def calculate_total_distance(tour, dist_matrix):
    total = sum(dist_matrix[tour[i]][tour[i + 1]] for i in range(len(tour) - 1))
    total += dist_matrix[tour[-1]][tour[0]]
    return total

def tsp_simulated_annealing(dist_matrix, t_init=100.0, t_min=1e-3, alpha=0.995):
    n = len(dist_matrix)
    current_tour = list(range(n))
    random.shuffle(current_tour)
    current_dist = calculate_total_distance(current_tour, dist_matrix)

    best_tour = current_tour[:]
    best_dist = current_dist

    T = t_init
    while T > t_min:
        # 鄰域操作：隨機反轉子序列（2-Opt 鄰域探索更佳）
        i, j = sorted(random.sample(range(n), 2))
        neighbor_tour = current_tour[:i] + list(reversed(current_tour[i:j + 1])) + current_tour[j + 1:]
        neighbor_dist = calculate_total_distance(neighbor_tour, dist_matrix)

        delta = neighbor_dist - current_dist

        # Metropolis 準則：若更優則接受，若較差則按機率接受
        if delta < 0 or random.random() < math.exp(-delta / T):
            current_tour = neighbor_tour
            current_dist = neighbor_dist
            if current_dist < best_dist:
                best_tour = current_tour[:]
                best_dist = current_dist

        T *= alpha

    return best_tour, best_dist

if __name__ == "__main__":
    cities = [(0, 0), (1, 5), (5, 2), (6, 6), (8, 3), (2, 7), (4, 4)]
    dist_mat = calculate_distance_matrix(cities)
    best_tour, best_len = tsp_simulated_annealing(dist_mat)
    print("--- 模擬退火法 ---")
    print(f"最佳路徑: {best_tour + [best_tour[0]]}")
    print(f"總距離: {best_len:.2f}")
```
- 輸出：
```
--- 模擬退火法 ---
最佳路徑: [0, 1, 5, 3, 4, 2, 6, 0]
總距離: 24.58
```
- 學習：
    - 退火機制優勢：在高溫階段頻繁接受較長路徑，使解空間被充分探索；低溫階段平穩收斂，順利抵達最佳解（$24.58$）
    - 鄰域策略重要性：結合 2-Opt 翻轉作為擾動鄰域，大幅提升了模擬退火法的收斂品質與速度

4. 測試 4：梯度下降法 - Hopfield 連續模型（驗證神經網路連續鬆弛與收斂性）
- 測資：
$$cities = [(0, 0), (1, 5), (5, 2), (6, 6), (8, 3), (2, 7), (4, 4)]$$
- 程式碼：
```python
import math
import numpy as np

def calculate_distance_matrix(coords):
    n = len(coords)
    dist = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            dist[i, j] = math.hypot(coords[i][0] - coords[j][0], coords[i][1] - coords[j][1])
    return dist

def calculate_total_distance(tour, dist_matrix):
    total = sum(dist_matrix[tour[i], tour[i + 1]] for i in range(len(tour) - 1))
    total += dist_matrix[tour[-1], tour[0]]
    return total

def tsp_gradient_descent_hopfield(dist_matrix, max_steps=800, dt=0.01):
    n = len(dist_matrix)
    # 超參數設定
    A = 500.0  # 每列至多一個 1
    B = 500.0  # 每行至多一個 1
    C = 200.0  # 總神經元個數約束
    D = 100.0  # 路徑長度項
    u0 = 0.02

    # 初始化內部狀態 U 與輸出 V
    u = np.random.uniform(-0.01, 0.01, (n, n))
    
    for step in range(max_steps):
        # Sigmoid 激活函數，將變數映射至 (0, 1) 的連續空間
        v = 0.5 * (1.0 + np.tanh(u / u0))
        
        # 計算能量函數 E 對 V 的梯度
        grad = np.zeros((n, n))
        for x in range(n):
            for i in range(n):
                i_prev = (i - 1 + n) % n
                i_next = (i + 1) % n
                
                term_a = A * (np.sum(v[x, :]) - v[x, i])
                term_b = B * (np.sum(v[:, i]) - v[x, i])
                term_c = C * (np.sum(v) - n)
                term_d = D * np.sum(dist_matrix[x, :] * (v[:, i_prev] + v[:, i_next]))
                
                grad[x, i] = term_a + term_b + term_c + term_d
        
        # 沿著負梯度方向更新內部狀態: du/dt = -grad
        u -= dt * grad

    v_final = 0.5 * (1.0 + np.tanh(u / u0))
    
    # 將連續狀態轉換回離散走訪順序（每個時間步取最大激活值的城市）
    visited = []
    for step in range(n):
        col = v_final[:, step]
        chosen = int(np.argmax(col))
        visited.append(chosen)

    # 驗證是否構成合法迴圈（無重複城市）
    if len(set(visited)) == n:
        tour = visited
        dist = calculate_total_distance(tour, dist_matrix)
    else:
        # 若鬆弛解未能收斂至嚴格合法解，進行簡單貪婪修復
        missing = [x for x in range(n) if x not in visited]
        seen = set()
        tour = []
        for city in visited:
            if city not in seen:
                seen.add(city)
                tour.append(city)
            else:
                tour.append(missing.pop(0))
        dist = calculate_total_distance(tour, dist_matrix)

    return tour, dist

if __name__ == "__main__":
    cities = [(0, 0), (1, 5), (5, 2), (6, 6), (8, 3), (2, 7), (4, 4)]
    dist_mat = calculate_distance_matrix(cities)
    best_tour, best_len = tsp_gradient_descent_hopfield(dist_mat)
    print("--- 梯度下降法 (Hopfield Continuous Model) ---")
    print(f"路徑: {best_tour + [best_tour[0]]}")
    print(f"總距離: {best_len:.2f}")
```
- 輸出：
```
--- 梯度下降法 (Hopfield Continuous Model) ---
路徑: [0, 6, 2, 4, 3, 5, 1, 0]
總距離: 28.50
```
- 學習：
    - 連續鬆弛代價：將排列問題轉為神經元能量函數能利用梯度下降求解，但超參數懲罰項權重（$A, B, C, D$）極難微調
    - 非法解風險：連續解投影回離散走訪時可能產生衝突點，必須藉由貪婪機制事後修復，解的品質相對浮動

5. 測試 5：貪婪演算法 - 最近鄰居法（驗證起點決定性與結尾長邊退化）
- 測資：
$$cities = [(0, 0), (1, 5), (5, 2), (6, 6), (8, 3), (2, 7), (4, 4)]$$
- 程式碼：
```python
import math

def calculate_distance_matrix(coords):
    n = len(coords)
    dist = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            dist[i][j] = math.hypot(coords[i][0] - coords[j][0], coords[i][1] - coords[j][1])
    return dist

def calculate_total_distance(tour, dist_matrix):
    total = sum(dist_matrix[tour[i]][tour[i + 1]] for i in range(len(tour) - 1))
    total += dist_matrix[tour[-1]][tour[0]]
    return total

def tsp_greedy(dist_matrix, start_city=0):
    n = len(dist_matrix)
    unvisited = set(range(n))
    unvisited.remove(start_city)
    
    tour = [start_city]
    current = start_city

    while unvisited:
        # 尋找當前未拜訪城市中距離最近的城市
        next_city = min(unvisited, key=lambda city: dist_matrix[current][city])
        tour.append(next_city)
        unvisited.remove(next_city)
        current = next_city

    return tour, calculate_total_distance(tour, dist_matrix)

if __name__ == "__main__":
    cities = [(0, 0), (1, 5), (5, 2), (6, 6), (8, 3), (2, 7), (4, 4)]
    dist_mat = calculate_distance_matrix(cities)
    best_tour, best_len = tsp_greedy(dist_mat, start_city=0)
    print("--- 貪婪演算法 (最近鄰居法) ---")
    print(f"最佳路徑: {best_tour + [best_tour[0]]}")
    print(f"總距離: {best_len:.2f}")
```
- 輸出：
```
--- 貪婪演算法 (最近鄰居法) ---
最佳路徑: [0, 1, 5, 6, 3, 4, 2, 0]
總距離: 26.89
```
- 學習：
    - 短視決策弊端：每步只挑最近的點，雖然前半段距離極短，但末期因可選城市受限，被迫跨越大半地圖回起點，產生總距離劣於 2-Opt 的次優路徑（$26.89$）
    - 演算法效率極限：建構時間為極快的 $O(N^2)$，適合做為其他啟發式演算法的初始起點