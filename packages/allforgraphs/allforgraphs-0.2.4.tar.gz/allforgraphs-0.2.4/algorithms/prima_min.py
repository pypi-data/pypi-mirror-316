#определение класса графа
class Graph_2:

    #инициализация графа с заданными рёбрами
    def __init__(self, ribs):
        self.ribs = ribs #список рёбер графа (каждое ребро - кортеж: вес, узел1, узел2)
        self.nodes = self._get_nodes() #вызываем метод для получения всех уникальных узлов графа
        self.tree_ribs = [] #список рёбер, которые войдут в максимальное покрывающее дерево
        self.total_weight = 0 #общий вес минимального покрывающего дерева

    #метод для извлечения всех уникальных вершин из списка рёбер
    def _get_nodes(self):
        nodes = set() #создаём пустое множество для хранения вершин
        for ribs in self.ribs: #проходим по всем рёбрам графа
            nodes.add(ribs[1]) #добавляем первую вершину ребра
            nodes.add(ribs[2]) #добавляем вторую вершину ребра
        return nodes #возвращаем множество всех вершин

    #метод построения минимального покрывающего дерева
    def prima_minimum_covering_tree(self):
        #сортируем рёбра по возрастанию веса. При равных весах — по меньшему номеру первой и второй вершины.
        sorted_ribs = sorted(self.ribs, key=lambda x: (x[0], min(x[1], x[2]), max(x[1], x[2])))
        bouquet = set() #множество вершин, уже включённых в дерево
        remaining_ribs = set(sorted_ribs) #множество всех оставшихся рёбер

        #шаг 1: обработка первого ребра
        while sorted_ribs:
            weight, u, v = sorted_ribs.pop(0) #берём первое (наибольшее) ребро
            if u not in bouquet and v not in bouquet: #проверяем, чтобы вершины не были в дереве
                self.tree_ribs.append((u, v, weight)) #добавляем ребро в дерево
                self.total_weight += weight #увеличиваем общий вес дерева
                bouquet.add(u) #добавляем вершины ребра в множество дерева
                bouquet.add(v)

            #шаг 2: добавляем рёбра, инцидентные текущему дереву
            while sorted_ribs:
                #флаг, указывающий, было ли добавлено ребро на текущем шаге
                ribs_found = False
                for ribs in sorted_ribs: #проходим по оставшимся рёбрам
                    weight, u, v = ribs
                    if u in bouquet or v in bouquet: #проверяем, инцидентно ли ребро текущему дереву
                        if self.cycle(u, v): #проверяем, образует ли ребро цикл
                            remaining_ribs.discard(ribs) #удаляем ребро из оставшихся
                            sorted_ribs.remove(ribs) #удаляем ребро из списка для обработки
                            break
                        else: #если цикл не образуется
                            self.tree_ribs.append((u, v, weight)) #добавляем ребро в дерево
                            self.total_weight += weight #увеличиваем общий вес дерева
                            bouquet.add(u) #добавляем вершины ребра в множество дерева
                            bouquet.add(v)
                            remaining_ribs.discard(ribs)  #удаляем ребро из оставшихся
                            sorted_ribs.remove(ribs) #удаляем ребро из списка для обработки
                            ribs_found = True #отмечаем, что ребро было добавлено
                            break

                if not ribs_found: #если ни одно ребро не было добавлено, выходим из цикла
                    break

        return self.total_weight, self.tree_ribs #возвращаем общий вес и рёбра минимального дерева

    #метод для проверки, образует ли добавляемое ребро цикл
    def cycle(self, u, v):
        visited = set() #множество посещённых вершин

        #вспомогательная функция для поиска в глубину
        def depth_first_search(node):
            if node in visited: #если вершина уже посещена, значит, цикл найден
                return False
            visited.add(node) #отмечаем вершину как посещённую
            for ribs in self.tree_ribs: #проходим по всем рёбрам текущего дерева
                if ribs[0] == node and ribs[1] not in visited: #если вершина инцидентна текущей
                    if depth_first_search(ribs[1]): #рекурсивно проверяем соседнюю вершину
                        return True
                elif ribs[1] == node and ribs[0] not in visited: #обратное направление
                    if depth_first_search(ribs[0]): #рекурсивно проверяем соседнюю вершину
                        return True
            return False #если цикл не найден, возвращаем False

        depth_first_search(u) #запускаем поиск в глубину из первой вершины ребра
        return v in visited #если вторая вершина посещена, значит, цикл образован


if __name__ == "__main__":
    #задаём граф в виде списка рёбер (вес, вершина1, вершина2)
    E = [ (1, 1, 3), (1, 2, 6), (2, 2, 4), (3, 1, 5), (4, 3, 4),
          (5, 4, 5), (6, 3, 5), (7, 1, 2), (7, 4, 6) ]

    graph = Graph_2(E) #создаём граф на основе заданных рёбер
    total_weight, min_tree_ribs = graph.prima_minimum_covering_tree() #строим минимальное покрывающее дерево

    print("Общий вес минимального покрывающего дерева:", total_weight) #выводим общий вес минимального покрывающего дерева
    print("Рёбра минимального покрывающего дерева:") #выводим рёбра минимального покрывающего дерева
    for u, v, weight in min_tree_ribs:
        print(f"Вес: {weight}, Ребро: ({u}, {v})")
