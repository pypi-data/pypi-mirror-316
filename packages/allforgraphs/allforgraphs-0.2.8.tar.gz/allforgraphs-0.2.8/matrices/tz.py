def transitive_closure(edges, num_vertices):
    adjacency_matrix = [[0] * num_vertices for _ in range(num_vertices)]

    for _, i, j in edges:
        adjacency_matrix[i - 1][j - 1] = 1

    for k in range(num_vertices):
        for i in range(num_vertices):
            for j in range(num_vertices):
                adjacency_matrix[i][j] = adjacency_matrix[i][j] or (adjacency_matrix[i][k] and adjacency_matrix[k][j])

    return adjacency_matrix

if __name__ == "__main__":
    edges_input = [
        (5, 1, 2), (4, 2, 4), (4, 2, 3), (7, 3, 1)
    ]

    num_vertices = max(max(i, j) for _, i, j in edges_input)

    closure_matrix = transitive_closure(edges_input, num_vertices)

    print("Матрица транзитивного замыкания:")
    for row in closure_matrix:
        print(" ".join(map(str, row)))
 