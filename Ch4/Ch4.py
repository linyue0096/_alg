def solve_gauss_seidel(A, b, x0=None, tol=1e-7, max_iterations=100):
    """
    使用高斯-賽德爾法求解 Ax = b（純 Python 實作）
    
    :param A: 係數矩陣 (List[List[float]])，大小 n x n
    :param b: 常數項向量 (List[float])，長度 n
    :param x0: 初始猜測值 (List[float])，若為 None 則預設全為 0
    :param tol: 容許誤差 (Tolerance)
    :param max_iterations: 最大迭代次數
    :return: (解向量 x, 實際迭代次數)
    """
    n = len(b)
    
    # 檢查對角線是否有 0
    for i in range(n):
        if abs(A[i][i]) < 1e-15:
            raise ValueError(f"對角線元素 A[{i}][{i}] 為 0，無法直接套用高斯-賽德爾法。")
    
    # 初始化解向量（若無給定則初始為 0）
    x = [0.0] * n if x0 is None else [float(val) for val in x0]
    
    print(f"{'Iteration':<10} | {'x1':<12} | {'x2':<12} | {'x3':<12} | {'Error (L_inf)':<15}")
    print("-" * 70)
    print(f"{0:<10} | {x[0]:<12.6f} | {x[1]:<12.6f} | {x[2]:<12.6f} | {'-':<15}")

    for iteration in range(1, max_iterations + 1):
        max_diff = 0.0  # 用於記錄本輪變數更新的最大變動量（無窮範數）
        
        for i in range(n):
            old_xi = x[i]
            
            # 計算 sum_{j != i} A[i][j] * x[j]
            # 注意：當 j < i 時，x[j] 已經是「本輪最新值」；當 j > i 時，x[j] 仍為「上一輪舊值」
            # 這正是高斯-賽德爾法的原地更新特性
            sigma = 0.0
            for j in range(n):
                if j != i:
                    sigma += A[i][j] * x[j]
            
            # 更新 x[i]
            x[i] = (b[i] - sigma) / A[i][i]
            
            # 追蹤本維度的誤差
            diff = abs(x[i] - old_xi)
            if diff > max_diff:
                max_diff = diff
        
        # 印出每輪迭代收斂進度
        print(f"{iteration:<10} | {x[0]:<12.6f} | {x[1]:<12.6f} | {x[2]:<12.6f} | {max_diff:<15.6e}")
        
        # 達到收斂條件提早結束
        if max_diff < tol:
            print("-" * 70)
            print(f"在第 {iteration} 次迭代成功收斂！")
            return x, iteration

    print("-" * 70)
    print(f"達到最大迭代次數 {max_iterations}，未能收斂至指定容許誤差。")
    return x, max_iterations


# --- 執行求解 ---
if __name__ == "__main__":
    # 定義係數矩陣 A 與常數項向量 b
    A = [
        [ 4.0, -1.0,  1.0],
        [ 4.0, -8.0,  1.0],
        [-2.0,  1.0,  5.0]
    ]
    b = [7.0, -21.0, 15.0]

    # 執行高斯-賽德爾法
    solution, total_iters = solve_gauss_seidel(A, b, tol=1e-6)

    print("\n最終計算結果：")
    for idx, val in enumerate(solution, start=1):
        print(f"x_{idx} = {val:.8f}")