from collections import deque

def is_valid(state):
    farmer, wolf, goat, cabbage = state
    if wolf == goat and farmer != wolf:
        return False
    if goat == cabbage and farmer != goat:
        return False
    return True

def river_crossing_bfs():
    start = (0, 0, 0, 0)
    goal = (1, 1, 1, 1)
    
    queue = deque([(start, [start])])
    visited = {start}
    
    while queue:
        current, path = queue.popleft()
        if current == goal:
            return path
        
        f, w, g, c = current
        next_f = 1 - f
        
        # 移動候選：農夫自己走，或帶與農夫同岸的物品
        candidates = [(next_f, w, g, c)]  # 單獨走
        if w == f: candidates.append((next_f, next_f, g, c))
        if g == f: candidates.append((next_f, w, next_f, c))
        if c == f: candidates.append((next_f, w, g, next_f))
        
        for nxt in candidates:
            if is_valid(nxt) and nxt not in visited:
                visited.add(nxt)
                queue.append((nxt, path + [nxt]))
                
    return None

steps = river_crossing_bfs()
print(f"最少步數需 {len(steps) - 1} 步：")
for s in steps:
    print(f"農:{s[0]}, 狼:{s[1]}, 羊:{s[2]}, 菜:{s[3]}")