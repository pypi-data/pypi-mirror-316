from .Kruskals_algorithm import Kruskal
from .Hamiltonian_cycle import Hamilton
from .Primal import Primal_min
import sys
import os
from contextlib import contextmanager

@contextmanager
def suppress_stdout():
    """Контекстный менеджер для подавления вывода на консоль."""
    original_stdout = sys.stdout  # Сохраняем оригинальный stdout
    sys.stdout = open(os.devnull, 'w')  # Перенаправляем stdout в "черную дыру"
    try:
        yield  # Позволяем выполнять код внутри блока
    finally:
        sys.stdout.close()  # Закрываем "черную дыру"
        sys.stdout = original_stdout  # Восстанавливаем оригинальный stdout


def test(points, edges):
	points = [(1, 5), (1, 3), (3, 3), (3, 5)]  # (x,y) координаты
	edges = [(0, 1, 4), (1, 2, 8), (1, 2, 1), (1, 3, 5), (0, 2, 2), (0, 3, 1), (0, 3, 8), (2, 3, 6)]
	return points, edges, 6


def drawing(points, edges):
	# (x,y) - координаты вершин. Нужны исключительно для вывода рисунка через матплотлиб + количество вершин через len
	points = [(10, 1), (15, 4), (17, 7), (18, 8), (17, 9), (13, 13), (17, 10), (16, 11.5), (14, 15), (10, 19.5),
			(16, 13), (9.5, 19), (9.2, 17), (9, 16), (7, 16), (3, 17.5), (2.6, 17), (5.3, 12), (4.8, 11), (5, 10.5),
			(5, 10), (5.2, 9.5), (3.5, 6.5), (4, 6), (5.3, 5), (8, 5.5), (10, 7), (8.5, 3.5), (10, 2),
			(10, 5), (14, 8.5), (11, 10), (7, 7), (6, 7.5), (4.9, 7), (5, 6.5), (4.5, 6), (12, 14), (11, 15.5),
			(9.5, 14.5), (8.5, 11), (8, 10.2), (7.5, 10), (6.5, 15.5), (7, 10.5), (6.6, 10.5), (7.1, 11.5), (6, 11),
			(5.5, 10.2), (6, 9), (5, 7.5), (5.5, 12.5), (3.3, 16.3), (5.8, 15), (6, 14)]

	# (первая вершина, вторая вершина с которой соединяется, вес) - ребра. В "дано" они сразу отсортированы так, что сначала идет меньший индекс вершины, потом больший. Петель нет, но в алгоритме это учтено
	edges = [(0, 1, 5), (1, 2, 2), (2, 3, 8), (3, 4, 1), (4, 6, 7), (6, 7, 3),
			(8, 9, 14), (8, 10, 6), (7, 10, 11), (9, 11, 4), (11, 12, 9),
			(12, 14, 13), (14, 15, 15), (15, 16, 12), (16, 17, 10), (17, 18, 1),
			(18, 19, 3), (19, 20, 2), (20, 21, 6), (21, 22, 7), (22, 23, 8),
			(23, 24, 5), (24, 25, 9), (25, 27, 2), (27, 28, 4), (0, 28, 8),
			(4, 5, 15), (2, 5, 11), (7, 8, 3), (12, 13, 6), (25, 26, 7),
			(26, 29, 1), (27, 29, 14), (28, 29, 12), (26, 30, 5), (5, 30, 10),
			(28, 30, 2), (1, 28, 4), (1, 30, 9), (5, 8, 3), (30, 31, 15),
			(31, 32, 11), (32, 33, 6), (33, 34, 12), (34, 35, 7), (35, 36, 14),
			(23, 36, 1), (22, 34, 5), (5, 37, 10), (37, 38, 13), (9, 38, 8),
			(13, 39, 12), (38, 39, 3), (31, 37, 9), (31, 39, 6), (31, 40, 11),
			(31, 41, 4), (40, 41, 15), (40, 44, 2), (41, 42, 7), (42, 44, 1),
			(44, 45, 8), (45, 46, 10), (40, 46, 3), (47, 48, 14), (45, 47, 6),
			(19, 48, 5), (21, 48, 12), (45, 49, 11), (44, 49, 9), (42, 49, 2),
			(49, 50, 7), (34, 50, 13), (17, 51, 10), (51, 52, 4), (16, 52, 3),
			(51, 52, 8), (52, 53, 6), (53, 54, 1), (43, 54, 15), (14, 43, 12),
			(39, 54, 9), (51, 54, 2), (39, 47, 7), (47, 54, 11), (11, 39, 5)]
	return points, edges, 20

def drawing2(points, edges):
	points = [
		(7, 0), (8, 1), (7, 1), (8.5, 4.5), (9, 5), (8.5, 5.5),
		(8.5, 7.5), (7.5, 6.5), (7, 6.5), (6.5, 6.5), (5.5, 7.5),
		(5.5, 5.5), (5, 5), (5.5, 4.5), (4.5, 3), (4, 1.5),
		(5, 0.5), (7, 3.5)
	]

	# Обновлённые рёбра для ориентированного графа с Гамильтоновым циклом
	edges = [
		(0, 1), (1, 2), (2, 3), (4, 3), (5, 4), (6, 5), (7, 6), (8, 7),
		(9, 8), (10, 9), (11, 10), (12, 11), (13, 12), (13, 14), (14, 15),
		(15, 16), (16, 0),  # Гамильтонов цикл: последняя вершина соединяется с начальной
		(14, 2), (13, 2), (17, 2), (2, 0), (3, 17), (17, 13), (4, 14)  # Дополнительные рёбра
	]
	return points, edges

def drawing3():
	graf = {
		'1': [(2, '2'), (1, '25')],
		'2': [(2, '1'), (3, '3'), (2, '25')],
		'3': [(3, '2'), (1, '3'), (2, '4')],
		'4': [(2, '3'), (1, '5')],
		'5': [(1, '4'), (4, '6')],
		'6': [(4, '5'), (3, '8'), (2, '24'), (3, '24')],
		'7': [(1, '8'), (2, '20'), (3, '22')],
		'8': [(3, '6'), (1, '7'), (1, '9'), (2, '9')],
		'9': [(1, '8'), (2, '8'), (1, '10'), (2, '19')],
		'10': [(1, '9'), (1, '11'), (3, '17')],
		'11': [(1, '10'), (1, '12'), (3, '13')],
		'12': [(1, '11'), (1, '13'), (4, '13')],
		'13': [(3, '11'), (1, '12'), (4, '12'), (1, '14'), (3, '15')],
		'14': [(1, '13'), (1, '15'), (1, '16')],
		'15': [(3, '13'), (1, '14'), (2, '16')],
		'16': [(1, '14'), (2, '15'), (3, '17'), (1, '18')],
		'17': [(3, '10'), (3, '16'), (1, '19')],
		'18': [(1, '16'), (3, '19'), (3, '21')],
		'19': [(2, '9'), (1, '17'), (3, '18'), (3, '20')],
		'20': [(2, '7'), (3, '19'), (1, '22')],
		'21': [(3, '18'), (1, '22'), (2, '23')],
		'22': [(3, '7'), (1, '20'), (1, '21'), (1, '23')],
		'23': [(2, '21'), (1, '22'), (1, '24')],
		'24': [(2, '6'), (3, '6'), (1, '23'), (1, '25')],
		'25': [(1, '1'), (2, '2'), (1, '24')],
	}
	return graf
def get_elements_Kruskal(points, edges):
	graph_instance = Kruskal(points, edges)
	sorted_edges_min = graph_instance.sort_edges_min()
	sorted_edges_max = graph_instance.sort_edges_max()
	with suppress_stdout():
		mst_edges_min = graph_instance.kruskals_algorithm(sorted_edges_min)
		mst_edges_max = graph_instance.kruskals_algorithm(sorted_edges_max)
		Tmin = graph_instance.result_weight(mst_edges_min)
		Tmax = graph_instance.result_weight(mst_edges_max)
	return Tmin, Tmax

def test_Kruskal(out):
	# Тест 1: Проверка функции test
	points, edges, k = test([], [])
	Tmin, Tmax = get_elements_Kruskal(points, edges)
	assert len(points) == 4, f"Тест 1 не пройден: ожидается 4 точки, но получено {len(points)}"
	assert len(edges) == 8, f"Тест 1 не пройден: ожидается 8 рёбер, но получено {len(edges)}"
	assert k == 6, f"Тест 1 не пройден: ожидается k = 6, но получено {k}"
	assert Tmin == 4, f"Тест 1 не пройден: ожидается Tmin == 4, но получено {Tmin}"
	assert Tmax == 22, f"Тест 1 не пройден: ожидается Tmin == 22, но получено {Tmin}"
	if out:	print('Тест 1 завершён')

	# Тест 2: Проверка функции drawing
	points, edges, k = drawing([], [])
	Tmin, Tmax = get_elements_Kruskal(points, edges)
	graph = Kruskal(points, edges)
	assert len(points) == 55, f"Тест 2 не пройден: ожидается 55 точек, но получено {len(points)}"
	assert len(edges) == 86, f"Тест 2 не пройден: ожидается 86 рёбер, но получено {len(edges)}"
	assert k == 20, f"Тест 2 не пройден: ожидается k = 20, но получено {k}"
	assert Tmin == 279, f"Тест 2 не пройден: ожидается Tmin == 279, но получено {Tmin}"
	assert Tmax == 533, f"Тест 2 не пройден: ожидается Tmax == 533, но получено {Tmax}"
	assert isinstance(graph, Kruskal), "Тест 2 не пройден: объект не является экземпляром класса Kruskal"
	if out:	print('Тест 2 завершён')

	# Тест 4: Проверка вычисления
	test_points = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]
	test_edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3), (3, 4, 4)]
	Tmin, Tmax = get_elements_Kruskal(test_points, test_edges)
	assert len(test_points) == 5, f"Тест 3 не пройден: ожидается 5 точек, но получено {len(points)}"
	assert len(test_edges) == 4, f"Тест 3 не пройден: ожидается 4 ребра, но получено {len(edges)}"
	assert Tmin == 10, f"Тест 3 не пройден: ожидается Tmin == 10, но получено {Tmin}"
	assert Tmax == 10, f"Тест 3 не пройден: ожидается Tmax == 10, но получено {Tmax}"
	if out:	print('Тест 3 завершён')
	return True


def get_elements_Hamilton(points, edges, start_vertex_label):
	hamilton_instance = Hamilton(points, edges)
	n = len(points)  # Количество вершин графа
	start_vertex = hamilton_instance.vertex_labels.index(start_vertex_label)  # Преобразуем букву в индекс
	cycle = hamilton_instance.hamiltonian_cycle(start_vertex)  # Ищем Гамильтонов цикл
	with suppress_stdout():
		hamilton_instance.cycle_exist(cycle)  # проверяем, существует ли цикл
	answer = [hamilton_instance.vertex_labels[v] for v in cycle]
	return answer


def test_Hamilton(out=False):
	points, edges = drawing2([], [])
	start_vertex_label = 'a'
	answer = get_elements_Hamilton(points, edges, start_vertex_label)
	assert answer == ['a', 'b', 'c', 'd', 'r', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f', 'e', 'o', 'p', 'q'], f"Тест 1 не пройден: получено {answer}"
	if out:	print('Тест 1 завершён')

	points, edges = drawing2([], [])
	start_vertex_label = 'r'
	answer = get_elements_Hamilton(points, edges, start_vertex_label)
	assert answer == ['r', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f', 'e', 'o', 'p', 'q', 'a', 'b', 'c', 'd'], f"Тест 2 не пройден: получено {answer}"
	if out:	print('Тест 2 завершён')


	points, edges = drawing2([], [])
	start_vertex_label = 'n'
	answer = get_elements_Hamilton(points, edges, start_vertex_label)
	assert answer == ['n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f', 'e', 'o', 'p', 'q', 'a', 'b', 'c', 'd', 'r'], f"Тест 3 не пройден: получено {answer}"
	if out:	print('Тест 3 завершён')
	return True


def test_Primal_min(out=False):
	# Тест 1: Проверка корректности минимального остовного дерева
	graph = {
		'1': [(1, '2'), (4, '3')],
		'2': [(1, '1'), (2, '3'), (5, '4')],
		'3': [(4, '1'), (2, '2'), (3, '4')],
		'4': [(5, '2'), (3, '3')]
	}
	start_vertex = '1'
	primal_min_instance = Primal_min(graph)
	tree, min_weight = primal_min_instance.run(start_vertex)
	expected_tree = [('1', '2', 1), ('2', '3', 2), ('3', '4', 3)]
	expected_weight = 6
	assert tree == expected_tree, f"Тест 1 не пройден: получено {tree}"
	assert min_weight == expected_weight, f"Тест 1 не пройден: получен {min_weight}"
	if out: print('Тест 1 завершён')

	# Тест 2: Проверка на пустом графе
	empty_graph = {}
	primal_min_instance_empty = Primal_min(empty_graph)
	# Проверяем, что дерево и вес равны начальным значениям
	assert primal_min_instance_empty.tree == [], "Тест 2 не пройден: дерево не пустое"
	assert primal_min_instance_empty.min_weight == 0, "Тест 2 не пройден: ненулевой вес"
	if out: print('Тест 2 завершён')

	# Тест 3: Проверка на графе с одним узлом
	single_node_graph = {'1': []}
	primal_min_instance_single = Primal_min(single_node_graph)
	tree_single, min_weight_single = primal_min_instance_single.run('1')
	assert tree_single == [], "Тест 3 не пройден: получено не пустое дерево"
	assert min_weight_single == 0, "Тест 3 не пройден: получен ненулевой вес"
	if out: print('Тест 3 завершён')

	return True

if __name__ == '__main__':
	test_Kruskal(False)
	test_Hamilton(False)
	test_Primal_min(False)
