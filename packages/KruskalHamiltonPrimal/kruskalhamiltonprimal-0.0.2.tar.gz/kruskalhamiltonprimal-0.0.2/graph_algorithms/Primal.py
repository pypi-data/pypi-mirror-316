class Primal_min:
    def __init__(self, graph):
        self.graph = graph  # Сохраняем граф в виде словаря
        self.tree = []  # Список рёбер минимального остовного дерева
        self.visited = set()  # Множество посещённых вершин
        self.apexs = []  # Список всех доступных рёбер
        self.min_weight = 0  # Суммарный мин. вес дерева

    def run(self, begin):
        # Добавляем начальную вершину в множество посещённых
        self.visited.add(begin)
        # Добавляем все рёбра, исходящие из начальной вершины, в список доступных рёбер
        self.apexs.extend((weight, begin, neighbor) for weight, neighbor in self.graph[begin])

        while self.apexs:
            # Сортируем список рёбер по весу (в порядке возрастания) и выбираем минимальное
            self.apexs.sort()
            weight, from_peak, to_peak = self.apexs.pop(0)  # Берем ребро с мин. весом

            # Проверяем, не принадлежит ли конечная вершина уже построенному дереву
            if to_peak not in self.visited:
                # Добавляем вершину в множество посещённых
                self.visited.add(to_peak)
                # Добавляем ребро в мин. дерево
                self.tree.append((from_peak, to_peak, weight))
                # Увеличиваем суммарный вес дерева
                self.min_weight += weight

                # Вывод отладочной информации
                print(f"Добавлено в дерево: {from_peak} -> {to_peak}, вес: {weight}")
                print(f"Посещённые вершины: {self.visited}")

                # Добавляем в список доступных рёбер все рёбра, исходящие из новой вершины
                for apex_weight, neighbor in self.graph[to_peak]:
                    if neighbor not in self.visited:
                        # Отладочный вывод для каждого нового доступного ребра
                        print(f"Новое ребро доступно: {to_peak} -> {neighbor}, вес: {apex_weight}")
                        self.apexs.append((apex_weight, to_peak, neighbor))

        # Итоговый вывод построенного дерева
        print(f"Минимальное покрывающее дерево: {self.tree}")
        return self.tree, self.min_weight

    def min_tree(self):
        # Вывод минимального остовного дерева и его суммарного веса
        print("Минимальное покрывающее дерево:")
        for from_peak, to_peak, weight in self.tree:
            print(f"{from_peak} <-> {to_peak}, вес: {weight}")
