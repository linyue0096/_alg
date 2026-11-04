def solve_n_queens(n=8):
    solutions = []
    
    def is_safe(queens, row, col):
        for r, c in enumerate(queens):
            if c == col or abs(c - col) == abs(r - row):
                return False
        return True

    def dfs(row, current_queens):
        if row == n:
            solutions.append(list(current_queens))
            return
        
        for col in range(n):
            if is_safe(current_queens, row, col):
                current_queens.append(col)
                dfs(row + 1, current_queens)
                current_queens.pop()  # 回溯

    dfs(0, [])
    return solutions

solutions = solve_n_queens(8)
print(f"8 皇后問題共有 {len(solutions)} 組解。")
print("第一組解（各列欄位）：", solutions[0])