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