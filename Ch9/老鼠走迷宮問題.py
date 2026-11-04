def solve_maze_dfs(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    visited = set()
    path = []

    def dfs(r, c):
        if (r, c) == end:
            path.append((r, c))
            return True
        
        visited.add((r, c))
        path.append((r, c))

        # 上、右、下、左
        for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if maze[nr][nc] == 0 and (nr, nc) not in visited:  # 0 代表通路，1 代表牆壁
                    if dfs(nr, nc):
                        return True

        path.pop()  # 回溯
        return False

    return path if dfs(start[0], start[1]) else None

# 範例測試 (0: 路, 1: 牆)
maze = [
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [1, 1, 0, 0, 0]
]
print("迷宮路徑:", solve_maze_dfs(maze, (0, 0), (3, 4)))