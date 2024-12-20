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


def kruskal_maximum_tree(edges_input):
    edges_input.sort(key=lambda x: x[0], reverse=True)

    num_vertices = max(max(u, v) for _, u, v in edges_input) + 1
    ds = DisjointSet(num_vertices)

    max_tree_weight = 0
    max_tree_edges = []

    for weight, u, v in edges_input:
        if ds.find(u) != ds.find(v):
            ds.union(u, v)
            max_tree_edges.append((weight, u, v))
            max_tree_weight += weight

    return max_tree_edges, max_tree_weight


if __name__ == "__main__":
    edges_input = [
        (9, 0, 1), (12, 0, 2), (10, 1, 2), (15, 1, 3),
        (5, 2, 3), (20, 2, 4), (25, 3, 4), (30, 4, 5)
    ]

    max_tree_edges, max_tree_weight = kruskal_maximum_tree(edges_input)

    print('Максимальное покрывающее дерево:')
    for edge in max_tree_edges:
        print(f'Вес: {edge[0]}, Вершины: ({edge[1]}, {edge[2]})')

    print('Общий вес максимального покрывающего дерева:', max_tree_weight)
