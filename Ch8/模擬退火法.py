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