import random
from random import randint
import parcing_graph_menu
from graphdirected import GraphDirected
import operations_menu

def generate_random_graph(n, m):
    gr = GraphDirected()
    cr = []

    for i in range(n):
        gr.add_vertex(i)
        for j in range(n):
            cr.append((i, j))

    counter = 0
    while counter < m:
        group = random.choice(cr)
        c = randint(-10, 10)
        gr.add_edge(group[0], group[1], c)
        cr.remove(group)
        counter += 1
    return gr

def copy_graph(g: GraphDirected):
    copy = GraphDirected()

    for i in g.in_bound.keys():
        copy.add_vertex(i)

    for edge in g.edges.keys():
        copy.add_edge(edge[0], edge[1], g.edges[edge])

    return copy


class MainMenu:
    def __init__(self, g: GraphDirected):
        self._graph = g
        self._command = {'r': self.read_graph_file, 'd': self.print_graph, 's': self.save_graph_file,
                         'g': self.create_random_graph, 'c': self.make_copy,'m': self.modify_menu,
                         'p': self.parse_menu}

    def print_menu(self):
        print("\n--- GRAPH OPERATIONS --- ")
        print("  Display current graph --> d")
        print("  Read graph from file --> r")
        print("  Save graph to file --> s")
        print("  Generate a random graph --> g")
        print("  Make a copy --> c")
        print("\n  Modify the graph --> m")
        print("  Parse the graph --> p")
        print("  Exit program --> x")

    def modify_menu(self):
        op = operations_menu.ModifyGraph(self._graph)
        op.start()

    def parse_menu(self):
        parse = parcing_graph_menu.ParseMenu(self._graph)
        parse.start()

    def make_copy(self):
        copy = copy_graph(self._graph)
        fout = open("copy.txt", "wt")
        fout.write(f"{copy.nr_vert} {copy.nr_edge}\n")

        for x in copy.out_bound.keys():
            if (len(copy.out_bound[x]) == 0) and (len(copy.in_bound[x]) == 0):
                line = f"{x} -1\n"
                fout.write(line)
            else:
                for y in copy.out_bound[x]:
                    line = f"{x} {y} {copy.edges[(x, y)]}\n"
                    fout.write(line)

        fout.close()

    def read_graph_file(self):
        g = GraphDirected()
        file_name = input("\nFile name: ")
        g.load_file(file_name)
        self._graph = g

    def print_graph(self):
        print(self._graph)

    def save_graph_file(self):
        file_name = input("\nFile name: ")
        self._graph.save_file(file_name)

    def create_random_graph(self):
        ver = int(input("\nNr of vertices: "))
        edge = int(input("\nNr of edges: "))
        if edge > ver * ver:
            print("Too many edges for this many vertices")
        else:
            self._graph = generate_random_graph(ver, edge)

    def start(self):
        while True:
            self.print_menu()
            _choice = input("\nCommand: ")

            if _choice == "x":
                break

            if _choice  not in self._command:
                print("Unidentifiable command")

            else:
                try:
                    self._command[_choice]()
                except Exception as ve:
                    print("Error: " + str(ve))

        print("\n---  END PROGRAM  ---")


if __name__ == '__main__':
    grap = GraphDirected()
    ui = MainMenu(grap)
    ui.start()
