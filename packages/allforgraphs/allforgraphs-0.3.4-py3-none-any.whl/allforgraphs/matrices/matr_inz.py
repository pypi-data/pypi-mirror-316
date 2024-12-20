def build_incidence_matrix(edges):
    if not edges:
        return None
    max_vertex = 0
    for weight, u, v in edges:
        max_vertex = max(max_vertex, u, v)

    num_vertices = max_vertex
    num_edges = len(edges)

    incidence_matrix = [[0 for _ in range(num_edges)] for _ in range(num_vertices)]

    for i, (weight, u, v) in enumerate(edges):
        if weight == 0:
            continue
        if u == v:
            incidence_matrix[u - 1][i] = 2
        else:
            incidence_matrix[u - 1][i] = 1
            incidence_matrix[v - 1][i] = 1

    return incidence_matrix


if __name__ == "__main__":
    edges = [
        (5, 1, 2),
        (0, 1, 3),
        (4, 2, 3),
        (3, 3, 4),
        (2, 4, 1),
        (0, 2, 4)
    ]


    def print_incidence_matrix(matrix, edges):
        num_vertices = len(matrix)
        num_edges = len(matrix[0])

        print(" ", end="")
        for i in range(num_edges):
            print(f"E{i + 1}({edges[i][0]}) ", end="")
        print()
        print("-" * (10 + 8 * num_edges))

        for i in range(num_vertices):
            print(f"V{i + 1} |", end="")
            for j in range(num_edges):
                print(f" {matrix[i][j]} ", end="")
            print()


    incidence_matrix = build_incidence_matrix(edges)

    if incidence_matrix:
        print_incidence_matrix(incidence_matrix, edges)
    else:
        print("Список рёбер пуст.")