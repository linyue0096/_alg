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