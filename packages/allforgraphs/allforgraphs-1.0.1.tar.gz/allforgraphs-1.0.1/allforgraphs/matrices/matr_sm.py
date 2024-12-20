def build_adjacency_matrix(edges):
    if not edges:
        return None

    max_vertex = 0
    for weight, u, v in edges:
        if weight == 0:
            continue
        max_vertex = max(max_vertex, u, v)

    num_vertices = max_vertex

    adjacency_matrix = [[0 for _ in range(num_vertices)] for _ in range(num_vertices)]

    for weight, u, v in edges:
        if weight == 0:
            continue
        adjacency_matrix[u - 1][v - 1] = 1
        adjacency_matrix[v - 1][u - 1] = 1

    return adjacency_matrix

if __name__ == "__main__":
    edges = [
        (5, 1, 2),
        (0, 1, 3),
        (4, 2, 3),
        (3, 3, 4),
        (2, 4, 1),
        (0, 2, 4)
    ]

    def print_adjacency_matrix(matrix):
        num_vertices = len(matrix)

        print(" ", end="")
        for i in range(num_vertices):
            print(f"V{i + 1} ", end="")
        print()
        print("-" * (8 + 5 * num_vertices))

        for i in range(num_vertices):
            print(f"V{i + 1} |", end="")
            for j in range(num_vertices):
                print(f" {matrix[i][j]:2} ", end="")
            print()


    adjacency_matrix = build_adjacency_matrix(edges)

    if adjacency_matrix:
        print_adjacency_matrix(adjacency_matrix)
    else:
        print("Список рёбер пуст.")