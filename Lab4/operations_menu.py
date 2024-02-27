import graphdirected


class ModifyGraph:
    def __init__(self, g: graphdirected.GraphDirected):
        self._graph = g
        self._command = {'1': self.check_vertex_exists, '2': self.check_edge_exists, '3': self.vertex_info,
                         '4': self.in_bound_vertex, '5': self.out_bound_vertex, '6': self.get_cost_edge,
                         '7': self.vertex_add, '8': self.vertex_remove, '9': self.edge_add,
                         '10': self.edge_remove, '11': self.modify_cost}

    def operations_menu(self):
        print("\n---  OPERATIONS ON GRAPH  ---\n")
        print("  Check if vertex exists --> 1")
        print("  Check if edge exists --> 2")

        print("\n  Vertices information --> 3")
        print("  In bound of a vertex information --> 4")
        print("  Out bound of a vertex information --> 5")
        print("  Get cost of an edge --> 6")

        print("\n  Add a vertex --> 7")
        print("  Remove a vertex --> 8")
        print("  Add an edge --> 9")
        print("  Remove an edge --> 10")
        print("  Modify cost of an edge --> 11")


        print("\n  Display current graph --> d")
        print("  Print dictionaries --> p")
        print("  Go to main menu --> x")

    def check_vertex_exists(self):
        vertex = int(input("Vertex: "))
        if self._graph.is_vertex(vertex):
            print("YES - it's a vertex")
        else:
            print("NO - it's not a vertex")

    def check_edge_exists(self):
        print("Give edge coordinates")
        x = int(input("Edge X: "))
        y = int(input("Edge Y: "))
        if self._graph.is_edge(x, y):
            print("YES - it's an edge")
        else:
            print("NO - it's not an edge")

    def vertex_info(self):
        print(f"Currently have: {self._graph.nr_vert} vertices")
        print(f"Vertices: {list(self._graph.in_bound.keys())}")

    def in_bound_vertex(self):
        vertex = int(input("Vertex: "))
        if not self._graph.is_vertex(vertex):
            print("Vertex doesn't exist")
            return

        inb = self._graph.in_bound[vertex]
        print(f"The in degree of vertex {vertex} is {len(inb)}")

        if len(inb) > 0:
            print(f"The in bound edges: ")
            for y in inb:
                print(f"({y}, {vertex}) -> {self._graph.edges[(y, vertex)]}")

    def out_bound_vertex(self):
        vertex = int(input("Vertex: "))
        if not self._graph.is_vertex(vertex):
            print("Vertex doesn't exist")
            return

        outb = self._graph.out_bound[vertex]
        print(f"The out degree of vertex {vertex} is {len(outb)}")

        if len(outb) > 0:
            print(f"The out bound edges: ")
            for y in outb:
                print(f"({vertex}, {y}) -> {self._graph.edges[(vertex, y)]}")

    def get_cost_edge(self):
        print("Give edge coordinates")
        x = int(input("Edge X: "))
        y = int(input("Edge Y: "))
        if not self._graph.is_edge(x, y):
            print("There is no such edge")
        else:
            print(f"The cost is {self._graph.edges[(x, y)]}")

    def vertex_add(self):
        vertex = int(input("Vertex: "))
        if not self._graph.add_vertex(vertex):
            print("Vertex already exists")
        else:
            print("Vertex was added")

    def vertex_remove(self):
        vertex = int(input("Vertex: "))
        if not self._graph.del_vertex(vertex):
            print("Vertex doesn't exist")
        else:
            print("Vertex was removed")

    def edge_add(self):
        print("Give edge coordinates")

        x = int(input("Edge X: "))
        if not self._graph.is_vertex(x):
            print("Vertex doesn't exist")
            return
        y = int(input("Edge Y: "))
        if not self._graph.is_vertex(y):
            print("Vertex doesn't exist")
            return

        c = int(input("Edge cost: "))
        if not self._graph.add_edge(x, y, c):
            print("Edge already exists")
            return
        print("Edge was added")

    def edge_remove(self):
        print("Give edge coordinates")
        x = int(input("Edge X: "))
        y = int(input("Edge Y: "))
        if not self._graph.del_edge(x, y):
            print("Edge doesn't exist")
        else:

            print("Edge was removed")

    def modify_cost(self):
        print("Give edge coordinates")
        x = int(input("Edge X: "))
        y = int(input("Edge Y: "))
        if not self._graph.is_edge(x, y):
            print("Edge doesn't exist")
        else:
            c = int(input("Edge cost: "))
            self._graph.edges[(x, y)] = c
            print("The cost was modified")

    def print_dict(self):
        print("\nIn bound dict:")
        d = self._graph.in_bound
        for x in d.keys():
            print(f"{x} <- {d[x]}")

        print("\nOut bound dict:")
        d = self._graph.out_bound
        for x in d.keys():
            print(f"{x} -> {d[x]}")

        print("\nEdges dict:")
        d = self._graph.edges
        for x in d.keys():
            print(f"{x} -> {d[x]}")


    def start(self):

        while True:
            self.operations_menu()
            _choice = input("\nCommand: ")

            if _choice == "x":
                return

            if _choice == "d":
                print(self._graph)

            elif _choice == "p":
                self.print_dict()

            elif _choice not in self._command:
                print("Unidentifiable command")

            else:
                try:
                    self._command[_choice]()
                except Exception as ve:
                    print("Error: " + str(ve))
