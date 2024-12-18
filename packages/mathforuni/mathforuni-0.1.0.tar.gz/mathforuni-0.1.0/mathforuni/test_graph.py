import unittest
from graphs import *

class TestGraphAlgorithms(unittest.TestCase):

    def test_minimum_spanning_tree(self):
        edges = [
            [1, 1, 2], [3, 1, 3], [2, 2, 3], [4, 2, 4], [5, 3, 4]
        ]

        mst_edges, total_weight = minimum_spanning_tree(edges)

        self.assertEqual(total_weight, 7)  # Ожидаем общий вес MST равным 7
        self.assertEqual(len(mst_edges), 3)  # Ожидаем 3 ребра в MST

        # Преобразуем mst_edges в кортежи для сравнения
        actual_edges = set((weight, u, v) for weight, u, v in mst_edges)

        # Ожидаемые рёбра в виде кортежей
        expected_edges = {(1, 1, 2), (2, 2, 3), (4, 2, 4)}

        self.assertTrue(actual_edges.issubset(expected_edges))  # Проверяем соответствие ожидаемым рёбрам

    def test_floyd_warshall(self):
        graph = [
            [0, 3, float('inf'), 7],
            [8, 0, 2, float('inf')],
            [5, float('inf'), 0, 1],
            [2, float('inf'), float('inf'), 0]
        ]
        distances = floyd_warshall(graph)
        self.assertEqual(distances[0][2], 5)  # Проверка кратчайшего пути


    def test_transitive_closure(self):
        graph = [
            [0, 1, 0],
            [0, 0, 1],
            [0, 0, 0]
        ]
        closure = transitive_closure(graph)
        expected_closure = [
            [0, 1, 1],
            [0, 0, 1],
            [0, 0, 0]
        ]
        self.assertEqual(closure, expected_closure)


    def test_find_eulerian_cycle(self):
        graph = {
            'A': ['B', 'C'],
            'B': ['A', 'D'],
            'C': ['A', 'D'],
            'D': ['B', 'C']
        }

        cycle = find_eulerian_cycle(graph)

        self.assertIsNotNone(cycle)  # Цикл должен существовать
        self.assertEqual(len(cycle), len(graph) + 1)  # Должен содержать все вершины + замыкание

        # Проверка, что все вершины присутствуют в цикле
        for vertex in graph:
            self.assertIn(vertex, cycle)

        # Проверка замыкания цикла
        self.assertEqual(cycle[0], cycle[-1])  # Цикл должен начинаться и заканчиваться в одной и той же вершине

    def test_hamiltonian_cycle(self):
        graph = {
            'A': ['B', 'C'],
            'B': ['A', 'C', 'D'],
            'C': ['A', 'B', 'D'],
            'D': ['B', 'C']
        }
        cycle = hamiltonian_cycle(graph)
        self.assertIsNotNone(cycle)  # Цикл должен существовать
        self.assertEqual(len(cycle), len(graph) + 1)  # Замкнутый цикл

    def test_dijkstra(self):
        graph = {
            'A': [('B', 1), ('C', 4)],
            'B': [('A', 1), ('C', 2), ('D', 5)],
            'C': [('A', 4), ('B', 2), ('D', 1)],
            'D': [('B', 5), ('C', 1)]
        }
        distances = dijkstra(graph, 'A')
        self.assertEqual(distances['D'], 4)  # Кратчайшее расстояние до D

    def test_prim(self):
        graph = {
            'A': [('B', 1), ('C', 3)],
            'B': [('A', 1), ('C', 2)],
            'C': [('A', 3), ('B', 2)]
        }
        mst_edges = prim(graph)
        self.assertEqual(len(mst_edges), 2)  # Должно быть два ребра в MST
        total_weight = sum(weight for _, _, weight in mst_edges)
        self.assertEqual(total_weight, 3)  # Общий вес MST

if __name__ == '__main__':
    unittest.main()
