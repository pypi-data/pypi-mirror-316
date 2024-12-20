import unittest
from allforgraphs.algorithms.kr_max import *
from allforgraphs.algorithms.kr_min import *
from allforgraphs.algorithms.prima_max import *
from allforgraphs.algorithms.prima_min import *
from allforgraphs.algorithms.euler_gr import *
from allforgraphs.algorithms.dr import *
from allforgraphs.matrices.matr_sm import *
from allforgraphs.matrices.matr_inz import *
from allforgraphs.matrices.matr_vs import *
from allforgraphs.matrices.tz import *
from allforgraphs.matrices.wf import *


class TestGraphAlgorithms(unittest.TestCase):

    def test_kruskal_maximum_tree_algorithm(self):
        edges_input = [
            (9, 0, 1), (12, 0, 2), (10, 1, 2), (15, 1, 3), (5, 2, 3), (20, 2, 4), (25, 3, 4), (30, 4, 5)
        ]

        expected_result = [
            (30, 4, 5), (25, 3, 4), (20, 2, 4), (15, 1, 3), (12, 0, 2),
        ]

        expected_weight = sum(edge[0] for edge in expected_result)

        max_tree_edges, max_tree_weight = kruskal_maximum_tree(edges_input)

        self.assertEqual(max_tree_weight, expected_weight)
        self.assertEqual(len(max_tree_edges), len(expected_result))
        for edge in max_tree_edges:
            self.assertIn(edge, expected_result)

    def test_kruskal_minimum_tree_algorithm(self):

        edges_input = [
            (11, 3, 1), (5, 4, 3), (8, 5, 4), (12, 6, 5), (3, 8, 6),
            (14, 8, 20), (7, 19, 20), (2, 19, 7), (9, 2, 7), (4, 1, 2),
            (10, 7, 32), (6, 32, 31), (15, 32, 34), (13, 31, 7), (1, 34, 31),
            (8, 19, 21), (11, 21, 20), (7, 29, 8), (2, 29, 30), (5, 33, 29),
            (14, 8, 30), (6, 30, 33), (12, 31, 22), (3, 24, 22), (9, 22, 25),
            (5, 26, 24), (7, 25, 26), (13, 26, 23), (1, 23, 30), (4, 26, 27),
            (8, 27, 28), (2, 23, 28), (10, 11, 12), (15, 13, 14), (12, 16, 15), (6, 18, 17)
        ]
        expected_result = [
            (1, 34, 31), (1, 23, 30), (2, 19, 7), (2, 29, 30), (2, 23, 28),  (3, 8, 6), (3, 24, 22), (4, 1, 2), (4, 26, 27), (5, 4, 3),  (5, 33, 29), (5, 26, 24), (6, 32, 31),
            (6, 18, 17), (7, 19, 20), (7, 29, 8), (7, 25, 26), (8, 5, 4), (8, 19, 21), (8, 27, 28), (9, 2, 7), (10, 7, 32),  (10, 11, 12),  (11, 3, 1), (12, 6, 5),
            (12, 16, 15), (15, 13, 14)
        ]

        expected_weight = sum(edge[0] for edge in expected_result)

        min_tree_edges, min_tree_weight = kruskal_minimum_tree(edges_input)

        self.assertEqual(min_tree_weight, expected_weight)
        self.assertEqual(len(min_tree_edges), len(expected_result))
        for edge in min_tree_edges:
            self.assertIn(edge, expected_result)

    def test_prima_maximum_tree_algoritm(self):
        #входные рёбра для тестирования
        edges_input = [
            (18, 1, 2), (14, 2, 3), (23, 4, 5), (12, 5, 6), (16, 1, 6),
            (28, 6, 8), (24, 8, 9), (3, 9, 10), (17, 7, 8), (21, 7, 13),
            (1, 13, 14), (19, 14, 15), (7, 12, 15), (9, 11, 12), (25, 15, 16),
            (30, 16, 17), (8, 17, 18), (2, 18, 19), (6, 19, 20), (32, 20, 21),
            (3, 19, 23), (9, 22, 23), (22, 22, 24), (8, 24, 25), (15, 25, 26),
            (34, 24, 27), (20, 27, 28), (31, 28, 29), (11, 27, 30), (10, 30, 31),
            (34, 31, 32), (6, 30, 33), (12, 33, 34), (20, 34, 35), (1, 35, 36),
            (5, 36, 37), (11, 37, 38), (2, 38, 39), (13, 39, 40), (4, 40, 41),
            (15, 1, 41) ]

        #ожидаемый результат: рёбра минимального покрывающего дерева
        expected_result = [
            (34, 24, 27), (22, 22, 24), (20, 27, 28), (31, 28, 29), (11, 27, 30), (10, 30, 31),
            (34, 31, 32), (9, 22, 23), (8, 24, 25), (15, 25, 26), (6, 30, 33), (12, 33, 34),
            (20, 34, 35), (3, 19, 23), (6, 19, 20), (32, 20, 21), (2, 18, 19),
            (8, 17, 18), (30, 16, 17), (25, 15, 16), (19, 14, 15), (7, 12, 15), (9, 11, 12),
            (1, 13, 14), (21, 7, 13), (17, 7, 8), (28, 6, 8), (24, 8, 9), (16, 1, 6),
            (18, 1, 2), (15, 1, 41), (14, 2, 3), (12, 5, 6), (23, 4, 5), (4, 40, 41),
            (13, 39, 40), (3, 9, 10), (2, 38, 39), (11, 37, 38), (5, 36, 37) ]

        expected_weight = sum(edge[0] for edge in expected_result)

        #создаём граф и строим минимальное покрывающее дерево
        graph = Graph_1(edges_input)
        total_weight, max_tree_ribs = graph.prima_maximum_covering_tree()

        #проверка общего веса
        self.assertEqual(total_weight, expected_weight)

        #проверка количества рёбер
        self.assertEqual(len(max_tree_ribs), len(expected_result))

        #проверка, что все рёбра находятся в ожидаемом результате
        for edge in max_tree_ribs:
            u, v, weight = edge
            self.assertIn((weight, min(u, v), max(u, v)),
                          [(w, min(a, b), max(a, b)) for w, a, b in expected_result])

    def test_prima_minimum_tree_algoritm(self):
        #входные рёбра для тестирования
        edges_input = [
            (1, 1, 3), (1, 2, 6), (2, 2, 4), (3, 1, 5), (4, 3, 4),
            (5, 4, 5), (6, 3, 5), (7, 1, 2), (7, 4, 6) ]

        #ожидаемый результат: рёбра минимального покрывающего дерева
        expected_result = [
            (1, 1, 3), (3, 1, 5), (4, 3, 4), (2, 2, 4), (1, 2, 6) ]

        expected_weight = sum(edge[0] for edge in expected_result)

        #создаём граф и строим минимальное покрывающее дерево
        graph = Graph_2(edges_input)
        total_weight, min_tree_ribs = graph.prima_minimum_covering_tree()

        #проверка общего веса
        self.assertEqual(total_weight, expected_weight)

        #проверка количества рёбер
        self.assertEqual(len(min_tree_ribs), len(expected_result))

        #проверка, что все рёбра находятся в ожидаемом результате
        for edge in min_tree_ribs:
            u, v, weight = edge
            self.assertIn((weight, min(u, v), max(u, v)),
                          [(w, min(a, b), max(a, b)) for w, a, b in expected_result])

    def test_eulerian_cycle(self):
        #тест 1
        #список рёбер графа для тестирования
        edges = [
            (1, 2), (1, 5), (1, 7), (1, 4), (2, 3),
            (2, 5), (2, 6), (4, 5), (5, 6), (5, 7),
            (5, 8), (6, 7), (7, 8), (6, 8), (6, 9),
            (6, 3), (8, 9) ]

        #начальная вершина для поиска Эйлерова цикла
        start_vertex = 5

        #ожидаемый результат Эйлерова цикла
        expected_cycle = [5, 8, 9, 6, 3, 2, 6, 8, 7, 6, 5, 7, 1, 4, 5, 2, 1, 5]

        #нахождение Эйлерова цикла
        cycle = find_eulerian_cycle(edges, start_vertex)

        #проверка, что найденный цикл соответствует ожидаемому
        assert cycle == expected_cycle

    def test_find_shortest_path_algorithm(self):
        edges_input = [
            (11, 3, 1), (5, 4, 3), (8, 5, 4), (12, 6, 5), (3, 8, 6),
            (14, 8, 20), (7, 19, 20), (2, 19, 7), (9, 2, 7), (4, 1, 2),
            (10, 7, 32), (6, 32, 31), (15, 32, 34), (13, 31, 7), (1, 34, 31),
            (8, 19, 21), (11, 21, 20),
            (7, 29, 8), (2, 29, 30), (5, 33, 29), (14, 8, 30), (6, 30, 33),
            (12, 31, 22), (3, 24, 22), (9, 22, 25), (5, 26, 24), (7, 25, 26),
            (13, 26, 23), (1, 23, 30), (4, 26, 27), (8, 27, 28),
            (2, 23, 28), (10, 11, 12), (15, 13, 14), (12, 16, 15), (6, 18, 17)
        ]

        start_node = 34
        end_node = 8

        expected_distance = 61
        expected_path = [34, 31, 22, 25, 26, 23, 30, 33, 29, 8]

        distance, path = find_shortest_path(edges_input, start_node, end_node)

        self.assertEqual(distance, expected_distance)
        self.assertEqual(path, expected_path)

    def test_build_adjacency_matrix(self):
        edges_input = [
            (5, 1, 2),
            (0, 1, 3),
            (4, 2, 3),
            (3, 3, 4),
            (2, 4, 1),
            (0, 2, 4)
        ]

        expected_adjacency_matrix = [
            [0, 1, 0, 1],
            [1, 0, 1, 0],
            [0, 1, 0, 1],
            [1, 0, 1, 0]
        ]

        adjacency_matrix = build_adjacency_matrix(edges_input)
        self.assertEqual(adjacency_matrix, expected_adjacency_matrix)

    def test_build_incidence_matrix(self):
        edges_input = [
            (5, 1, 2),
            (0, 1, 3),
            (4, 2, 3),
            (3, 3, 4),
            (2, 4, 1),
            (0, 2, 4)
        ]

        expected_incidence_matrix = [
            [1, 0, 0, 0, 1, 0],
            [1, 0, 1, 0, 0, 0],
            [0, 0, 1, 1, 0, 0],
            [0, 0, 0, 1, 1, 0]
        ]

        incidence_matrix = build_incidence_matrix(edges_input)

        self.assertEqual(incidence_matrix, expected_incidence_matrix)

    def test_build_weight_matrix(self):
        edges_input = [
            (5, 1, 2),
            (10, 1, 3),
            (7, 3, 4),
            (2, 4, 1),
            (3, 2, 4)
    ]
        expected_weight_matrix = [
        [0, 5, 10, 2],
        [5, 0, float("inf"), 3],
        [10, float("inf"), 0, 7],
        [2, 3, 7, 0]

    ]
        weight_matrix = build_weight_matrix(edges_input)
        self.assertEqual(weight_matrix, expected_weight_matrix)

    def test_transitive_closure(self):
        edges_input = [
            (5, 1, 2),
            (4, 2, 4),
            (4, 2, 3),
            (7, 3, 1)
        ]

        num_vertices = 4
        expected_closure_matrix = [
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [0, 0, 0, 0]
        ]

        closure_matrix = transitive_closure(edges_input, num_vertices)
        self.assertEqual(closure_matrix, expected_closure_matrix)

    def test_floyd_warshall(self):
        edges_input = [
            (2, 1, 2),
            (1, 2, 3),
            (6, 2, 3),
            (1, 3, 1),
            (5, 1, 3)
        ]

        num_vertices = 3

        expected_matrix = [
            [4, 2, 3],
            [2, 4, 1],
            [1, 3, 4]
        ]

        result_matrix = floyd_warshall(edges_input, num_vertices)
        self.assertEqual(result_matrix, expected_matrix)

if __name__ == '__main__':
    unittest.main()
