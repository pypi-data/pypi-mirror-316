def floyd_warshall(edges, num_vertices):
    INF = float('inf')
    distance_matrix = [[INF] * num_vertices for _ in range(num_vertices)]

    for w, i, j in edges:
        distance_matrix[i - 1][j - 1] = min(distance_matrix[i - 1][j - 1], w)

    for k in range(num_vertices):
        for i in range(num_vertices):
            for j in range(num_vertices):
                distance_matrix[i][j] = min(distance_matrix[i][j], distance_matrix[i][k] + distance_matrix[k][j])

    return distance_matrix


if __name__ == "__main__":
    edges_input = [
        (2, 1, 2), (1, 2, 3), (6, 2, 3), (1, 3, 1), (5, 1, 3)
    ]

    num_vertices = max(max(i, j) for _, i, j in edges_input)
    shortest_paths_matrix = floyd_warshall(edges_input, num_vertices)

    print("Матрица кратчайших расстояний:")
    for row in shortest_paths_matrix:
        print(" ".join(map(lambda x: f"{x:5}" if x != float('inf') else "  INF", row)))
