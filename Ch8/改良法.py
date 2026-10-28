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

def tsp_2opt(dist_matrix, initial_tour=None):
    n = len(dist_matrix)
    if initial_tour is None:
        tour = list(range(n))
        random.shuffle(tour)
    else:
        tour = initial_tour[:]
    
    improved = True
    while improved:
        improved = False
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                # 原始邊長度: (i-1 -> i) 與 (j -> (j+1)%n)
                # 翻轉後邊長度: (i-1 -> j) 與 (i -> (j+1)%n)
                prev_i = tour[i - 1]
                curr_i = tour[i]
                curr_j = tour[j]
                next_j = tour[(j + 1) % n]
                
                delta = (dist_matrix[prev_i][curr_j] + dist_matrix[curr_i][next_j]) - \
                        (dist_matrix[prev_i][curr_i] + dist_matrix[curr_j][next_j])
                
                if delta < -1e-9:  # 長度縮短
                    tour[i:j + 1] = reversed(tour[i:j + 1])
                    improved = True
                    break
            if improved:
                break
    return tour, calculate_total_distance(tour, dist_matrix)

if __name__ == "__main__":
    cities = [(0, 0), (1, 5), (5, 2), (6, 6), (8, 3), (2, 7), (4, 4)]
    dist_mat = calculate_distance_matrix(cities)
    best_tour, best_len = tsp_2opt(dist_mat)
    print("--- 2-Opt 改良法 ---")
    print(f"最佳路徑: {best_tour + [best_tour[0]]}")
    print(f"總距離: {best_len:.2f}")