import networkx as nx
import matplotlib.pyplot as plt

class Kruskal:
	def __init__(self, points, edges):
		self.points = points
		self.edges = edges

	def draw_only(self, k):
		def add_edge_to_graph(G, e1, e2, w):
			G.add_edge(e1, e2, weight=w)

		G_original = nx.Graph()  # создание графа
		for i in range(len(self.edges)):  # добавляем ребра для исходного графа
			add_edge_to_graph(G_original, self.points[self.edges[i][0]], self.points[self.edges[i][1]], self.edges[i][2])

		# Создание рисунка
		plt.figure(figsize=(9, 9))
		pos = {point: point for point in self.points}  # позиции вершин
		nx.draw(G_original, pos=pos, node_color='k', node_size=80)  # контур вершины
		nx.draw(G_original, pos=pos, node_color='w', node_size=40, width=3)  # заливка вершины

		# Подписи вершин
		labels = {point: str(i) for i, point in enumerate(self.points)}
		label_pos = {point: (x, y + 0.3) for point, (x, y) in pos.items()}  # порядковый номер
		nx.draw_networkx_labels(G_original, pos=label_pos, labels=labels, font_size=10)  # рисование подписей
		edge_labels = nx.get_edge_attributes(G_original, 'weight')
		nx.draw_networkx_edge_labels(G_original, pos, edge_labels=edge_labels, font_size=6)  # вес ребер

		# Настройка графика
		plt.title("Граф с минимальным покрывающим деревом", fontsize=12)
		plt.xlim(0, k)
		plt.ylim(0, k)
		plt.grid(True)
		plt.show()


	def view(self, min_edges, max_edges, k):
		def add_edge_to_graph(G, e1, e2, w):
			G.add_edge(e1, e2, weight=w)

		# ----------------------------------------------------------------------------------

		G_min = nx.Graph()  # создание графа
		for i in range(len(min_edges)):  # добавляем ребра для исходного графа
			add_edge_to_graph(G_min, self.points[min_edges[i][0]], self.points[min_edges[i][1]], min_edges[i][2])

		# Создание рисунка
		fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 9))  # два графика в одном окне

		# Первый график (мин)
		pos = {point: point for point in self.points}  # позиции вершин
		nx.draw(G_min, pos=pos, node_color='k', node_size=80, ax=ax1)  # контур вершины
		nx.draw(G_min, pos=pos, node_color='w', node_size=40, ax=ax1, width=3)  # заливка вершины

		# Подписи вершин
		labels = {point: str(i) for i, point in enumerate(self.points)}
		label_pos = {point: (x, y + 0.3) for point, (x, y) in pos.items()}  # порядковый номер
		nx.draw_networkx_labels(G_min, pos=label_pos, labels=labels, ax=ax1, font_size=10)  # рисование подписей
		edge_labels = nx.get_edge_attributes(G_min, 'weight')
		nx.draw_networkx_edge_labels(G_min, pos, edge_labels=edge_labels, ax=ax1, font_size=6)  # вес ребер

		# Настройка графика
		ax1.set_title("Граф с минимальным покрывающим деревом", fontsize=12)
		ax1.set_xlim(0, k)
		ax1.set_ylim(0, k)
		ax1.grid(True)

		# ----------------------------------------------------------------------------------

		G_max = nx.Graph()  # создание графа для MST (Minimum/Maximum Spanning Tree)
		for u, v, w in max_edges:  # добавляем ребра
			add_edge_to_graph(G_max, self.points[u], self.points[v], w)

		# Второй график (макс)
		nx.draw(G_max, pos=pos, node_color='k', node_size=80, ax=ax2)  # контур вершины
		nx.draw(G_max, pos=pos, node_color='w', node_size=40, ax=ax2, width=3)  # заливка вершины

		# Подписи вершин
		nx.draw_networkx_labels(G_max, pos=label_pos, labels=labels, ax=ax2, font_size=10)  # порядковый номер
		edge_labels = nx.get_edge_attributes(G_max, 'weight')
		nx.draw_networkx_edge_labels(G_max, pos, edge_labels=edge_labels, ax=ax2, font_size=6)  # вес ребер

		# Настройка графика
		ax2.set_title("Граф с максимальным покрывающим деревом", fontsize=12)
		ax2.set_xlim(0, k)
		ax2.set_ylim(0, k)
		ax2.grid(True)

		# ----------------------------------------------------------------------------------

		plt.tight_layout()  # Автоматически подгоняем подграфики
		plt.show()


	def find(self, bouquets, i):
		for idx, bouquet in enumerate(bouquets):  # Находим индекс букета, в котором находится искомая вершина i (в edges она на втором месте)
			if i in bouquet:  # если вершина нашлась в букете, возвращаем индекс букета
				return idx
		return -1  # если элемент не найден


	def union(self, bouquets, x, y):
		index_x = self.find(bouquets, x)  # ищем букет в котором есть вершина x
		index_y = self.find(bouquets, y)  # ищем букет в котором есть вершина y

		if index_x != -1 and index_y != -1 and index_x != index_y:  # если букеты нашлись и они не равны
			bouquets[index_x].extend(bouquets[index_y])  # то объединяем их
			bouquets[index_y] = []  # очищаем старый букет
			bouquets[index_x].sort()  # сортируем по возрастанию
			# print(f"({x}, {y}) Объединение букета {index_x+1} и букета {index_y+1}: {bouquets[index_x]}")  # отладочное сообщение, очень полезная штука


	def kruskals_algorithm(self, edges):
		bouquets = []  # массив со всеми букетами
		edge_colors = ["Не обработано"] * len(edges)  # цвета ребер изначально не обработаны

		for node in range(len(self.points)):  # всего букетов ровно столько же, сколько и вершин (потому что не знаю как посчитать максимальное количество букетов...)
			bouquets.append([node])  # заполняем букеты от нуля до конечной вершины (позже в консоль будут выводиться "-" если ячейка состоит только из одной вершины. Заморочилась, зато работает nwn)

		result = []  # массив с итоговыми вершинами, которые войдут в ответ
		e = 0  # ребра, добавленные в результат
		i = 0  # пронумеровали ребра, анализируем по очереди каждое, в зависимости от ребер данных на вводе (для минимума или для максимума)

		while e < len(self.points) - 1:  # пока результат не превысил количество вершин минус один (минус один потому что вершины соединяются между собой и логично что ребер должно быть меньше. Потому что мы строим дерево без лишних веток)
			if i >= len(edges):  # если порядковый номер ребра превышает количество ребер
				print("Все ребра обработаны, но не достигнуто необходимое количество ребер в MST")
				break  # останавливаем цикл

			u, v, w = edges[i]  # назначаем первому ребру букву u, v - второе ребро, w - вес
			x = self.find(bouquets, u)  # ищем букет в котором есть первая вершина в исследуемом ребре
			y = self.find(bouquets, v)  # ищем букет в котором есть вторая вершина в исследуемом ребре

			if x == y:  # если ранее был найден один и тот же букет, значит эти вершины уже объединены
				edge_colors[i] = "Оранжевый"  # окрашиваем в оранжевый
			else:  # иначе были найдены разные букеты
				self.union(bouquets, u, v)  # объединяем вершины в один букет
				edge_colors[i] = "Синий"  # окрашиваем в синий
				result.append((u, v, w))  # добавляем в результат
				e += 1  # увеличиваем счетчик ребер в результате на 1
			i += 1  # продолжаем анализировать остальные ребра

			# Выводим информацию о текущем состоянии
			if e == 1:  # выводим заголовок только один раз
				print(f"{'Ребро':<15}{'Цвет':<15}", end='')
				for j in range(len(bouquets)):  # выводим все букеты по порядку (в моем случае их столько же, сколько и вершин)
					print(f"{f'Букет {j + 1}':<15}", end='')
				print()

			# Выводим текущее ребро, цвет и букеты
			print(f"{f'({u}, {v}, {w})':<15}{f'{edge_colors[i - 1]}':<15}", end='')
			for bouquet in bouquets:  # выводим каждый букет по порядку
				if len(bouquet) == 1 or len(bouquet) == 0:  # если букет состоит из одного элемента или он пустой (в моем коде это сделано нарочно), то выводится прочерк
					print(f"{'-':<15}", end='')
				else:
					print(f"{str(bouquet):<15}", end='')  # в ином случае выводим букет
			print()

			# Проверка на количество уникальных букетов
			unique_bouquets = [b for b in bouquets if b]  # список непустых букетов
			if len(unique_bouquets) == 1:  # если в списке остался только один букет, значит все вершины объединились и можно завершить цикл
				print("Все вершины включены в один букет. Завершение алгоритма")  # на самом деле это даже не нужно. Но если хотите посмотреть анализ абсолютно всех ребер, напишите в цикле условие e < len(edges) и удалите "break" ниже
				break
		return result  # возвращаем массив с обработанными ребрами


	def sort_edges_min(self):  # сорт по мин
		sorted_edges = sorted(self.edges, key=lambda item: (item[2], item[0]))  # сортируем ребра по возрастанию веса, а затем по возрастанию первой вершины в ребре
		return sorted_edges


	def sort_edges_max(self):  # сорт по макс
		sorted_edges = sorted(self.edges, key=lambda item: (-item[2], item[0]))  # сортируем ребра по убыванию веса, а затем по возрастанию первой вершины в ребре
		return sorted_edges


	def result_weight(self, edges):  # итоговый вес дерева
		total_weight = 0

		for i, (u, v, w) in enumerate(edges):  # перебираем рёбра и выводим их веса
			print(w, end=" ")  # выводим вес ребра
			total_weight += w  # суммируем веса
			if i < len(edges) - 1:  # проверяем не последнее ли это ребро
				print("+", end=" ")  # выводим "+" только если это не последнее ребро

		print("=", total_weight)  # выводим итоговую сумму
		return total_weight