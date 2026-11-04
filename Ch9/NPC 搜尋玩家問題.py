import heapq

def a_star_search(grid, npc_pos, player_pos):
    rows, cols = len(grid), len(grid[0])
    
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    # 優先權佇列存入: (f_score, g_score, current_pos, path)
    open_set = []
    heapq.heappush(open_set, (heuristic(npc_pos, player_pos), 0, npc_pos, [npc_pos]))
    
    g_costs = {npc_pos: 0}

    while open_set:
        f, g, current, path = heapq.heappop(open_set)
        
        if current == player_pos:
            return path
            
        if g > g_costs.get(current, float('inf')):
            continue

        r, c = current
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            neighbor = (nr, nc)
            
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
                tentative_g = g + 1
                if tentative_g < g_costs.get(neighbor, float('inf')):
                    g_costs[neighbor] = tentative_g
                    f_cost = tentative_g + heuristic(neighbor, player_pos)
                    heapq.heappush(open_set, (f_cost, tentative_g, neighbor, path + [neighbor]))
                    
    return None

# 0: 可走, 1: 障礙物
grid = [
    [0, 0, 0, 1, 0],
    [1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0]
]
npc = (0, 0)
player = (0, 4)
print("NPC 追擊最短路徑:", a_star_search(grid, npc, player))