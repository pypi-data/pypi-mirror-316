import networkx as nx
import heapq
def find_shortest_path(edges_input, start_node, end_node):
    def dijkstra(graph, start, end):
        distances = {node: float('infinity') for node in graph.nodes()}
        distances[start] = 0
        previous_nodes = {node: None for node in graph.nodes()}
        priority_queue = [(0, start)]

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)

            if current_node == end:
                break

            for neighbor, weight in graph[current_node].items():
                distance = current_distance + weight['weight']
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor))

        path = []
        current_node = end
        while current_node is not None:
            path.append(current_node)
            current_node = previous_nodes[current_node]
        path.reverse()

        return distances[end], path
    G = nx.DiGraph()
    for weight, e1, e2 in edges_input:
        G.add_edge(e1, e2, weight=weight)
    distance, path = dijkstra(G, start_node, end_node)

    return distance, path

if __name__ == "__main__":
    edges_input = [
        (11, 3, 1), (5, 4, 3), (8, 5, 4), (12, 6, 5), (3, 8, 6), (14, 8, 20), (7, 19, 20), (2, 19, 7), (9, 2, 7), (4, 1, 2),
        (10, 7, 32), (6, 32, 31), (15, 32, 34), (13, 31, 7), (1, 34, 31), (8, 19, 21), (11, 21, 20), (7, 29, 8), (2, 29, 30),
        (5, 33, 29), (14, 8, 30), (6, 30, 33), (12, 31, 22), (3, 24, 22), (9, 22, 25), (5, 26, 24), (7, 25, 26), (13, 26, 23),
        (1, 23, 30), (4, 26, 27), (8, 27, 28),(2, 23, 28), (10, 11, 12), (15, 13, 14), (12, 16, 15), (6, 18, 17)
    ]
    start_node = 34
    end_node = 8

    distance, path = find_shortest_path(edges_input, start_node, end_node)
    print(f"Кратчайшее расстояние от {start_node} до {end_node}: {distance}")
    print(f"Путь: {' -> '.join(map(str, path))}")
