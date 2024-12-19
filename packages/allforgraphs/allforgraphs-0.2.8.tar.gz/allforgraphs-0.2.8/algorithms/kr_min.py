class DisjointSet:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, u):
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])
        return self.parent[u]

    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)

        if root_u != root_v:
            if self.rank[root_u] > self.rank[root_v]:
                self.parent[root_v] = root_u
            elif self.rank[root_u] < self.rank[root_v]:
                self.parent[root_u] = root_v
            else:
                self.parent[root_v] = root_u
                self.rank[root_u] += 1


def kruskal_minimum_tree(edges_input):
    edges_input.sort(key=lambda x: x[0])


    num_vertices = max(max(u, v) for _, u, v in edges_input) + 1
    ds = DisjointSet(num_vertices)

    min_tree_weight = 0
    min_tree_edges = []

    for weight, u, v in edges_input:
        if ds.find(u) != ds.find(v):
            ds.union(u, v)
            min_tree_edges.append((weight, u, v))
            min_tree_weight += weight

    return min_tree_edges, min_tree_weight

if __name__ == "__main__":
    edges_input = [
        (11, 3, 1), (5, 4, 3), (8, 5, 4), (12, 6, 5), (3, 8, 6),
        (14, 8, 20), (7, 19, 20), (2, 19, 7), (9, 2, 7), (4, 1, 2),
        (10, 7, 32), (6, 32, 31), (15, 32, 34), (13, 31, 7), (1, 34, 31),
        (8, 19, 21), (11, 21, 20), (7, 29, 8), (2, 29, 30), (5, 33, 29), (14, 8, 30), (6, 30, 33),
        (12, 31, 22), (3, 24, 22), (9, 22, 25), (5, 26, 24), (7, 25, 26),
        (13, 26, 23), (1, 23, 30), (4, 26, 27), (8, 27, 28),
        (2, 23, 28), (10, 11, 12), (15, 13, 14), (12, 16, 15), (6, 18, 17)
    ]

    min_tree_edges, min_tree_weight = kruskal_minimum_tree(edges_input)

    print('Минимальное покрывающее дерево:')
    for edge in min_tree_edges:
        print(f'Вес: {edge[0]}, Вершины: ({edge[1]}, {edge[2]})')

    print('Общий вес минимального покрывающего дерева:', min_tree_weight)