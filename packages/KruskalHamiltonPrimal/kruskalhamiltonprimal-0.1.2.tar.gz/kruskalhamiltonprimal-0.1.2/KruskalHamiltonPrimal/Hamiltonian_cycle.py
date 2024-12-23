import networkx as nx
import matplotlib.pyplot as plt
import string

class Hamilton:
    def __init__(self, points, edges):
        """
        Инициализирует граф Hamilton.

        Args:
            points (list): Список координат вершин графа.
            edges (list): Список рёбер графа в виде пар индексов вершин.
        """
        self.points = points
        self.edges = edges
        self.num_vertices = len(points)
        self.vertex_labels = list(string.ascii_lowercase)[:self.num_vertices]
        self.edges_with_labels = [(self.vertex_labels[u], self.vertex_labels[v]) for u, v in self.edges]
        self.adjacency_matrix = self.create_adjacency_matrix()

    def cycle_exist(self, cycle):
        if cycle and cycle != "Нет цикла":  # Если цикл найден
            print("Гамильтонов цикл найден: ",
                  [self.vertex_labels[v] for v in cycle])  # Выводим цикл с буквами
        else:
            print("Гамильтонов цикл не найден")  # Иначе сообщаем, что цикла нет

    def draw(self):
        # Визуализируем граф
        G = nx.DiGraph()  # Создаём объект ориентированного графа
        for i, coord in enumerate(self.points):  # Добавляем вершины в граф
            G.add_node(self.vertex_labels[i], pos=coord)
        G.add_edges_from(self.edges_with_labels)  # Добавляем рёбра в граф

        plt.figure(figsize=(8, 10))  # Увеличиваем размеры графика
        pos = nx.get_node_attributes(G, 'pos')  # Получаем позиции вершин для отображения
        nx.draw(G, pos, with_labels=True, node_color='orange', node_size=500, edge_color='orange', font_size=10,
                arrows=True)
        plt.title("Ориентированный граф с заданными координатами")  # Добавляем заголовок графика
        plt.show()  # Отображаем граф

    def aviable(self):
        print("Доступные вершины:")  # Выводим список доступных вершин
        for i, coord in enumerate(self.points):  # Перебираем индексы и координаты
            print(f"Вершина {self.vertex_labels[i]}: {coord}")  # Печатаем букву и координаты вершины

    def create_adjacency_matrix(self):
        """Создаёт матрицу смежности из количества вершин и рёбер."""
        matrix = [[0] * self.num_vertices for _ in range(self.num_vertices)]
        for u, v in self.edges:
            matrix[u][v] = 1
        return matrix

    def hamiltonian_cycle(self, start):
        """
        Находит Гамильтонов цикл в графе.

        Args:
            start (int): Индекс начальной вершины для поиска цикла.

        Returns:
            list or str: Список вершин в Гамильтоновом цикле или сообщение "Нет цикла".
        """
        used = [False] * self.num_vertices
        path = []

        def hamilton(v):
            path.append(v)
            if len(path) == self.num_vertices:
                if self.adjacency_matrix[path[-1]][path[0]] == 1:
                    return path
                else:
                    path.pop()
                    return None

            used[v] = True
            for next_v in range(self.num_vertices):
              if self.adjacency_matrix[v][next_v] == 1 and (not used[next_v] or (next_v == start and len(path) == self.num_vertices - 1)):
                  result = hamilton(next_v)
                  if result is not None:
                      return result

            used[v] = False
            path.pop()
            return None

        result = hamilton(start)
        return result if result is not None else "Нет цикла"

    def draw_graph(self, path=None):
      """
      Отображает граф с заданным Гамильтоновым циклом.

      Args:
          path (list, optional): Список индексов вершин, составляющих Гамильтонов цикл.
              Если задан, цикл будет выделен. Defaults to None.
      """
      graph = nx.DiGraph()
      graph.add_edges_from(self.edges_with_labels)
      pos = dict(zip(self.vertex_labels, self.points)) # Связываем метки вершин с их координатами

      if path: # Если передан гамильтонов цикл
          path_edges = [(self.vertex_labels[path[i]], self.vertex_labels[path[(i+1)%len(path)]]) for i in range(len(path))] # Преобразуем путь в список ребер
          nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color='red', width=2, arrowsize=20) # Рисуем ребра цикла красным
          nx.draw_networkx_edges(graph, pos, edgelist=[edge for edge in self.edges_with_labels if edge not in path_edges],
                  edge_color='gray', width=1, arrowsize=10) # Рисуем остальные ребра серым
      else:
        nx.draw_networkx_edges(graph, pos, edge_color='gray', width=1, arrowsize=10) # Рисуем все ребра серым

      nx.draw_networkx_nodes(graph, pos, node_color='skyblue', node_size=800) # Рисуем узлы
      nx.draw_networkx_labels(graph, pos, labels=dict(zip(self.vertex_labels, self.vertex_labels)), font_size=12) # Рисуем подписи узлов

      plt.title('Hamiltonian Cycle Graph') # Добавляем заголовок
      plt.show() # Отображаем граф

