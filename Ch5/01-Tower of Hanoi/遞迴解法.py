def hanoi_recursive(n, source, target, auxiliary):
    """
    n: 盤子數量
    source: 來源柱（例如 'A'）
    target: 目標柱（例如 'C'）
    auxiliary: 輔助柱（例如 'B'）
    """
    if n == 1:
        print(f"Move disk 1 from {source} to {target}")
        return

    # 1. 將上面 n-1 個盤子從 source 移到 auxiliary
    hanoi_recursive(n - 1, source, auxiliary, target)
    
    # 2. 將第 n 個盤子從 source 移到 target
    print(f"Move disk {n} from {source} to {target}")
    
    # 3. 將 auxiliary 上的 n-1 個盤子移到 target
    hanoi_recursive(n - 1, auxiliary, target, source)

# 測試 3 個盤子從 A 移到 C
print("--- 遞迴解法 ---")
hanoi_recursive(3, 'A', 'C', 'B')