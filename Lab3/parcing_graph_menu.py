from graphdirected import GraphDirected
from graphundirected import GraphUndirected

def bfs_forward(g: GraphDirected, start):
    prev = {start: None}
    visited = [start]
    dist = {start: 0}
    queue = [start]

    while len(queue) > 0:
        node = queue[0]
        queue.pop(0)
        for neighbour in g.out_bound[node]:
            print("\n")
            if neighbour not in visited:
                prev[neighbour] = node
                visited.append(neighbour)
                dist[neighbour] = dist[node] + 1
                queue.append(neighbour)

    return prev, visited, dist

def bfs_backward(g: GraphDirected, start):
    prev = {start: None}
    visited = [start]
    dist = {start: 0}

    queue = [start]
    while len(queue) > 0:
        node = queue[0]
        queue.pop(0)
        for neighbour in g.in_bound[node]:
            if neighbour not in visited:
                prev[neighbour] = node
                visited.append(neighbour)
                dist[neighbour] = dist[node] + 1
                queue.append(neighbour)

    return prev, visited, dist

def bfs_connected(g: GraphUndirected, start):
    con = [start]
    lis = [start]
    while len(lis) > 0:
        x = lis[0]
        lis = lis[1:]
        for y in g.connected[x]:
            if y not in con:
                con.append(y)
                lis.append(y)
    return con

def print_matrix(mat, maxN):
    for i in mat:
        for j in i:
            if j == maxN:
                print("-", end=" ")
            else:
                print(j, end=" ")
        print()
    print()

def dfs_connected(g: GraphUndirected, start, visited):
    """
    At the beginning we add it to visited with value 1
    Then we call the function again (recursively) with the x as the new node
    when we go through all neighbours of a node and all the neighbour's neighbours
    and only then we change the node's value to 2 as it was completely visited and analysed
    :param g:
    :param start:
    :param visited:
    :return: visited - which nodes where visited
    """
    visited[start] = 1

    for x in g.connected[start]:
        if x not in visited.keys():
            dfs_connected(g, x, visited)

    visited[start] = 2
    return visited

def Floyd_Warshall(g: GraphDirected):
    """
    1. We firstly initialize the distance matrix with 0 and the previous matrix with "-"
    2. After we give the corresponding initial values by checking if the created edge exists or not:
        if edge exists - dist will take the cost and prev the out vertex
        if not - the dist will take the established maximum value
    3. After we go through every possible path between two vertices and if a path is a smaller cost appears we
       change it in the dist matrix

    :param g: a directed graph with non-negative costs
    :return: the prev and dist matrices, and the maximum value established
    """
    maxN = 10
    for i in g.edges.values():
        maxN += i

    dist = [[0 for i in range(g.nr_vert)] for j in range(g.nr_vert)]
    prev = [["-" for i in range(g.nr_vert)] for j in range(g.nr_vert)]

    for i in range(g.nr_vert):
        for j in range(g.nr_vert):
            if i != j:
                if g.is_edge(i, j):
                    dist[i][j] = g.edges[i, j]
                    prev[i][j] = i
                else:
                    dist[i][j] = maxN

    print("-- ORIGINAL --\nDistance: \n")
    print_matrix(dist, maxN)
    print("Previous: \n")
    print_matrix(prev, maxN)

    for k in range(g.nr_vert):
        print(f"\n k = {k}\n")
        for i in range(g.nr_vert):
            for j in range(g.nr_vert):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    prev[i][j] = prev[k][j]

        print("Distance: \n")
        print_matrix(dist, maxN)
        print("Previous: \n")
        print_matrix(prev, maxN)

    return dist, prev, maxN

class ParseMenu:
    def __init__(self, g):
        self._graph = g
        self._command = {'d': self.print_graph, 'rd': self.read_directed_graph, 'ru': self.read_undirected_graph,
                         'fb': self.forward_shortest_path_bfs, 'bb': self.backward_shortest_path_bfs,
                         'bt': self.bfs_connected_components, 'dt': self.dfs_connected_components,
                         'fw': self.lowest_cost}

    def print_menu(self):
        print("\n--- LOWEST LENGTH PATH ---")
        print("  Read directed graph --> rd")
        print("  Forward breadth-first search --> fb")
        print("  Backward breadth-first search --> bb")


        print("\n--- CONNECTED COMPONENTS ---")
        print("  Read undirected graph --> ru")
        print("  Depth-first traversal --> dt")
        print("  Breadth-first traversal --> bt")

        print("\n--- LOWEST COST WALK ---")
        print("  Floyd-Warshall algorithm --> fw")

        print("\n  Display current graph --> d")
        print("  Exit program --> x")

    def lowest_cost(self):
        x = int(input("Start vertex: "))
        if not self._graph.is_vertex(x):
            print("Vertex doesn't exist")
            return
        y = int(input("End vertex: "))
        if not self._graph.is_vertex(y):
            print("Vertex doesn't exist")
            return

        dist, prev, maxN = Floyd_Warshall(self._graph)
        if dist[x][y] == maxN:
            print(f"No possible walks from {x} to {y}")
        else:
            print(f"The minimum cost is {dist[x][y]}")
            path = [y]
            while y != x:
                y = prev[x][y]
                path.append(y)
            path.reverse()
            print(f"The path is: {path}")

    def forward_shortest_path_bfs(self):
        x = int(input("Start vertex: "))
        if not self._graph.is_vertex(x):
            print("Vertex doesn't exist")
            return
        y = int(input("End vertex: "))
        if not self._graph.is_vertex(y):
            print("Vertex doesn't exist")
            return

        parents, visited, dist = bfs_forward(self._graph, x)
        if y not in visited:
            print("No such possible paths")
            return
        path = []
        print(f"\nThe minimum distance is {dist[y]}")
        while y is not None:
            path.append(y)
            y = parents[y]
        path.reverse()
        print(f"Shortest path possible is: {path}")

    def backward_shortest_path_bfs(self):
        x = int(input("Start vertex: "))
        if not self._graph.is_vertex(x):
            print("Vertex doesn't exist")
            return
        y = int(input("End vertex: "))
        if not self._graph.is_vertex(y):
            print("Vertex doesn't exist")
            return

        parents, visited, dist = bfs_backward(self._graph, y)
        if x not in visited:
            print("No such possible paths")
            return
        path = []
        print(f"\nThe minimum distance is {dist[x]}")
        while x is not None:
            path.append(x)
            x = parents[x]
        print(f"Shortest path possible is: {path}")

    def bfs_connected_components(self):
        ver = list(self._graph.connected.keys())
        while len(ver) > 0:
            con = bfs_connected(self._graph, ver[0])
            print(f"Connected components: {con}")
            for x in con:
                ver.remove(x)

    def dfs_connected_components(self):
        """
        Ver - keeps track of what nodes where visited and if it's not empty call the function with
        the first of the remaining elements
        in visited we get the visited components and as long as their value is 2 we delete the mode from ver
        :return:
        """
        ver = list(self._graph.connected.keys())
        while len(ver) > 0:
            con = []
            visited = dfs_connected(self._graph, ver[0], {})
            for x in visited.keys():
                if visited[x] == 2:
                    con.append(x)
                    ver.remove(x)
            print(f"Connected components: {con}")

    def read_directed_graph(self):
        g = GraphDirected()
        file_name = input("\nFile name: ")
        g.load_file(file_name)
        self._graph = g

    def read_undirected_graph(self):
        g = GraphUndirected()
        file_name = input("\nFile name: ")
        g.load_file(file_name)
        self._graph = g

    def print_graph(self):
        print(self._graph)

    def start(self):
        while True:
            self.print_menu()
            _choice = input("\nCommand: ")

            if _choice == "x":
                return

            if _choice  not in self._command:
                print("Unidentifiable command")

            else:
                try:
                    self._command[_choice]()
                except Exception as ve:
                    print("Error: " + str(ve))



# g = GraphUndirected()
# g.load_file("uGraph2.txt")
# ui = ParseMenu(g)
# ui.start()