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

def topological_sort(g: GraphDirected):
    """
    1. We look through all the in bound vertices of each vertex and keep a count of them in a vector,
       if the counter for any vertex is 0 it is added to the queue

    2. While the queue still has vertices we take the first one and append it to the topologically sorted graph
    3. Then we look through its out_bound vertices and for each decrement the counter
       if any of them reach 0 they are added to the queue

    :param g: a directed graph
    :return: None - if nr of vertices in top. sort. is smaller than  nr of vertices in graph
            else - the graph vertices sorted topologically
    """
    sort = []
    queue = []
    count = {}

    for x in g.in_bound.keys():
        count[x] = len(g.in_bound[x])
        if count[x] == 0:
            queue.append(x)

    while len(queue) != 0:
        x = queue.pop(0)
        sort.append(x)
        for y in g.out_bound[x]:
            count[y] -= 1
            if count[y] == 0:
                queue.append(y)
    if len(sort) < len(g.out_bound.keys()):
        return None
    return sort

def highest_cost_path(x, y, sort, g : GraphDirected):
    """
    1. Initializes the distances dictionary
    2. Go through the topol. sorted vertices till we reach x and start calculating the distances from there
    3. Look at every out bound vertex of each vertex in the sort vector starting with x and determining the
       longest distance for it so far.
       In case we discover a longer path we change it as well as the predecessor of that specific vertex
    4. When we reach the end vertex we reconstruct the path and return the necessary values

    :param x: starting vertex
    :param y: end vertex
    :param sort: the topologically sorted vertices
    :param g: the graph
    :return: the highest cost path between two vertices and the distance
    """
    dist = {}
    pred = {}
    for v in g.in_bound.keys():
        dist[v] = 0

    i = 0
    while sort[i] != x:
        if sort[i] == y:
            return sort, 0
        i += 1


    while i < len(sort):
        if sort[i] == y:
            break
        for v in g.out_bound[sort[i]]:
            if dist[v] < (dist[sort[i]] + g.edges[sort[i], v]):
                dist[v] = dist[sort[i]] + g.edges[sort[i], v]
                pred[v] = sort[i]
        i += 1

    path = [y]
    while y != x:
        y = pred[y]
        path.append(y)
    path.reverse()
    return path, dist[path[len(path) - 1]]

class ParseMenu:
    def __init__(self, g):
        self._graph = g
        self._command = {'d': self.print_graph, 'rd': self.read_directed_graph, 'ru': self.read_undirected_graph,
                         'fb': self.forward_shortest_path_bfs, 'bb': self.backward_shortest_path_bfs,
                         'bt': self.bfs_connected_components, 'dt': self.dfs_connected_components,
                         'fw': self.lowest_cost, 'tp': self.top_sort, 'hp': self.highest_cost}

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

        print("\n--- DIRECTION ACYCLIC GRAPH ---")
        print("  Topological sorting --> tp")
        print("  Highest cost path --> hp")

        print("\n  Display current graph --> d")
        print("  Exit program --> x")

    def top_sort(self):
        sort = topological_sort(self._graph)
        if sort is None:
            print("It's not a DAG")
        else:
            print(f"Topological sorting:\n     {sort}")

    def highest_cost(self):
        x = int(input("Start vertex: "))
        if not self._graph.is_vertex(x):
            print("Vertex doesn't exist")
            return
        y = int(input("End vertex: "))
        if not self._graph.is_vertex(y):
            print("Vertex doesn't exist")
            return

        sort = topological_sort(self._graph)
        if sort is None:
            print("It's not a DAG")
        else:
            path, dist = highest_cost_path(x, y, sort, self._graph)
            if dist == 0:
                print("No such possible path")
            else:
                print(f"Topological sorting:\n     {sort}")
                print(f"The highest cost path between two vertices:\n     {path}")
                print(f"The cost: {dist}")

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