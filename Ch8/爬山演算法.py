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