# Алгоритмы для работы с графами

def minimum_spanning_tree(edges):
    """
    Находит минимальное остовное дерево (MST) графа с использованием алгоритма Краскала.

    :param edges: Список рёбер графа, где каждое ребро представлено как [вес, вершина 1, вершина 2].
    :return: Кортеж, содержащий список рёбер в MST и общий вес MST.
    """
    # Сортировка рёбер по весу от меньшего к большему
    edges = sorted(edges, key=lambda x: x[0])

    mst = []  # Список для хранения рёбер в MST
    components = []  # Список для хранения множеств компонентов

    # Проходим по всем рёбрам
    for edge in edges:
        weight, u, v = edge

        component_u = None
        component_v = None

        # Проверяем принадлежность вершин к компонентам
        for component in components:
            if u in component:
                component_u = component
            if v in component:
                component_v = component

            # Если обе вершины уже в одной компоненте - пропускаем ребро
            if component_u is not None and component_v is not None:
                break

        # Если обе вершины уже в одной компоненте
        if component_u is not None and component_u == component_v:
            continue

        # Объединяем компоненты или создаем новую
        if component_u is not None and component_v is not None:
            # Объединяем две найденные компоненты
            component_u.update(component_v)
            components.remove(component_v)  # Удаляем объединенную компоненту
            mst.append(edge)
        elif component_u is not None:
            component_u.add(v)  # Добавляем v в компонент u
            mst.append(edge)
        elif component_v is not None:
            component_v.add(u)  # Добавляем u в компонент v
            mst.append(edge)
        else:
            # Если ни одна из вершин не входит в существующие компоненты
            new_component = {u, v}
            components.append(new_component)
            mst.append(edge)

    total_weight = sum(weight for weight, _, _ in mst)  # Считаем вес дерева
    return mst, total_weight


def floyd_warshall(graph):
    """
    Реализация алгоритма Флойда — Уоршелла для нахождения кратчайших путей между всеми парами вершин.

    :param graph: Матрица смежности графа, где graph[i][j] - вес ребра от i к j (или float('inf'), если ребра нет).
    :return: Матрица кратчайших расстояний между всеми парами вершин.
    """
    n = len(graph)
    distance = [row[:] for row in graph]  # Копируем оригинальную матрицу

    # Алгоритм Флойда-Уоршелла
    for k in range(n):
        for i in range(n):
            for j in range(n):
                distance[i][j] = min(distance[i][j], distance[i][k] + distance[k][j])

    return distance


def transitive_closure(graph):
    """
    Находит транзитивное замыкание графа.

    :param graph: Матрица смежности графа.
    :return: Матрица транзитивного замыкания.
    """
    n = len(graph)
    closure = [row[:] for row in graph]  # Копируем оригинальную матрицу

    for k in range(n):
        for i in range(n):
            for j in range(n):
                closure[i][j] = max(closure[i][j], closure[i][k] * closure[k][j])

    return closure


def find_eulerian_cycle(graph):
    """
    Находит Эйлеров цикл в графе.

    :param graph: Словарь, представляющий граф (ключи - вершины, значения - списки соседей).
    :return: Список вершин в Эйлеровом цикле или None, если цикл не существует.
    """
    # Проверка на наличие четной степени у всех вершин
    for vertex in graph:
        if len(graph[vertex]) % 2 != 0:
            return None  # Если хотя бы одна вершина имеет нечетную степень, цикл не существует

    cycle = []
    stack = []
    current_vertex = next(iter(graph))  # Начинаем с произвольной вершины
    stack.append(current_vertex)

    while stack:
        if graph[current_vertex]:
            stack.append(current_vertex)
            next_vertex = graph[current_vertex].pop()  # Берем следующее ребро
            graph[next_vertex].remove(current_vertex)  # Удаляем обратное ребро
            current_vertex = next_vertex  # Переходим к следующей вершине
        else:
            cycle.append(current_vertex)
            current_vertex = stack.pop()  # Возвращаемся назад

    return cycle[::-1]  # Возвращаем цикл в правильном порядке


def hamiltonian_cycle(graph):
    """
    Находит Гамильтонов цикл в графе.

    :param graph: Словарь, представляющий граф (ключи - вершины, значения - списки соседей).
    :return: Список вершин в Гамильтоновом цикле или None, если цикл не существует.
    """

    def backtrack(path):
        if len(path) == len(graph) and path[0] in graph[path[-1]]:
            return path + [path[0]]  # Замыкаем цикл

        for neighbor in graph[path[-1]]:
            if neighbor not in path:
                result = backtrack(path + [neighbor])
                if result:
                    return result

        return None

    for start in graph:
        result = backtrack([start])
        if result:
            return result

    return None


def dijkstra(graph, start):
    """
    Реализация алгоритма Дейкстры для нахождения кратчайших расстояний от начальной вершины до всех остальных.

    :param graph: Словарь, представляющий граф (ключи - вершины, значения - списки кортежей (сосед, вес)).
    :param start: Начальная вершина.
    :return: Словарь кратчайших расстояний от начальной вершины до всех остальных.
    """

    distances = {v: float('infinity') for v in graph}
    distances[start] = 0
    visited = set()

    while len(visited) < len(graph):
        current_v = min((v for v in distances if v not in visited), key=distances.get)

        for neighbor, weight in graph[current_v]:
            if neighbor not in visited:
                new_distance = distances[current_v] + weight
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance

        visited.add(current_v)

    return distances

def prim(graph):
    """
    Реализация алгоритма Прима для нахождения минимального остовного дерева.

    :param graph: Словарь, представляющий граф (ключи - вершины, значения - списки кортежей (сосед, вес)).
    :return: Список рёбер минимального остовного дерева.
    """
    start_v = next(iter(graph))
    mst_edges = []
    visited = set([start_v])

    edges = []

    # Добавляем все рёбра из начальной вершины в список рёбер
    for to, weight in graph[start_v]:
        edges.append((weight, start_v, to))

    while edges:
        # Находим ребро с минимальным весом
        edges.sort()  # Сортируем рёбра по весу
        weight, frm, to = edges.pop(0)  # Извлекаем наименьшее ребро

        if to not in visited:
            visited.add(to)
            mst_edges.append((frm, to, weight))

            # Добавляем все рёбра из новой вершины в список рёбер
            for next_to, next_weight in graph[to]:
                if next_to not in visited:
                    edges.append((next_weight, to, next_to))

    return mst_edges