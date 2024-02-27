class GraphDirected:
    def __init__(self):
        self.__nr_vert = 0
        self.__nr_edge = 0
        self.__in_bound = {}
        self.__out_bound = {}
        self.__edges = {}

    @property
    def nr_vert(self):
        return self.__nr_vert

    @property
    def nr_edge(self):
        return self.__nr_edge

    @property
    def in_bound(self):
        return self.__in_bound

    @property
    def out_bound(self):
        return self.__out_bound

    @property
    def edges(self):
        return self.__edges

    def is_vertex(self, x) -> bool:
        return x in self.__in_bound

    def is_edge(self, x, y) -> bool:
        return (x, y) in self.__edges

    def add_vertex(self, x) -> bool:
        if self.is_vertex(x):
            return False
        self.__nr_vert += 1
        self.__out_bound[x] = []
        self.__in_bound[x] = []
        return True

    def add_edge(self, x, y, c) -> bool:
        if self.is_edge(x, y):
            return False
        self.__nr_edge += 1
        self.__out_bound[x].append(y)
        self.__in_bound[y].append(x)
        self.__edges[(x, y)] = c
        return True

    def del_edge(self, x, y) -> bool:
        if not self.is_edge(x, y):
            return False
        self.__nr_edge -= 1
        self.__out_bound[x].remove(y)
        self.__in_bound[y].remove(x)
        self.__edges.pop((x, y))
        return True

    def del_vertex(self, x) -> bool:
        if not self.is_vertex(x):
            return False
        for y in self.__in_bound.keys():
            if x in self.__in_bound[y]:
                self.del_edge(x, y)

        for y in self.__out_bound.keys():
            if x in self.__out_bound[y]:
                self.del_edge(y, x)

        self.__in_bound.pop(x)
        self.__out_bound.pop(x)
        self.__nr_vert -= 1
        return True

    def load_file(self, file_name):
        fin = open(file_name, "rt")
        lines = fin.readlines()
        fin.close()

        line = lines[0].split(" ")
        vertex = int(line[0])
        lines.pop(0)

        for i in range(vertex):
            self.add_vertex(i)

        for line in lines:
            edge_line = line.split(" ")
            self.add_edge(int(edge_line[0]), int(edge_line[1]), int(edge_line[2]))

    def save_file(self, file_name):
        fout = open(file_name, "wt")
        fout.write(f"{self.__nr_vert} {self.__nr_edge}\n")

        for x in self.__edges.keys():
            line = f"{x[0]} {x[1]} {self.__edges[x]}\n"
            fout.write(line)

        fout.close()

    def __str__(self):
        final = f"\n{self.__nr_vert} {self.__nr_edge}"
        for x in self.__edges.keys():
            final += f"\n{x[0]} {x[1]} {self.__edges[x]}"
        return final

