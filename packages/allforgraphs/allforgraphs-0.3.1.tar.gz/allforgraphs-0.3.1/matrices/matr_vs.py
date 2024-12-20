def build_weight_matrix(edges):
    if not edges:
        return None

    max_vertex = 0
    for w, u, v in edges:
        max_vertex = max(max_vertex, u, v)

    num_vertices = max_vertex

    weight_matrix = [[float('inf')] * num_vertices for _ in range(num_vertices)]
    for i in range(num_vertices):
        weight_matrix[i][i] = 0

    for w, u, v in edges:
        if w <= 0:
            continue
        weight_matrix[u - 1][v - 1] = min(weight_matrix[u - 1][v - 1], w)
        weight_matrix[v - 1][u - 1] = min(weight_matrix[v - 1][u - 1], w)

    return weight_matrix

if __name__ == "__main__":
    edges = [
        (5, 1, 2),
        (10, 1, 3),
        (0, 2, 3),
        (7, 3, 4),
        (2, 4, 1),
        (3, 2, 4)
    ]

    def print_weight_matrix(matrix):
        num_vertices = len(matrix)

        print(" ", end="")
        for i in range(num_vertices):
            print(f"{i + 1:3}", end="")
        print()

        print("-" * (num_vertices * 4 + 3))
        for i in range(num_vertices):
            print(f"{i + 1:3}|", end="")
            for j in range(num_vertices):
                if matrix[i][j] == float('inf'):
                    print(" ∞ ", end="")
                else:
                    print(f"{matrix[i][j]:3}", end="")
            print("|")


    weight_matrix = build_weight_matrix(edges)

    if weight_matrix:
        print_weight_matrix(weight_matrix)
    else:
        print("Список рёбер пуст.")

