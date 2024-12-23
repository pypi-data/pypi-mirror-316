# Minimal Spanning Tree and Hamiltonian Cycle

This project implements algorithms for finding the minimum spanning tree (MST) and the Hamiltonian cycle in graphs. It includes three main classes: `Kruskal', `Hamilton` and `Primal_min', each of which provides different methods for working with graphs.

## Installation

To work with the project, you need to install the following libraries:

```bash
pip install networkx matplotlib
```

## Description of classes

### 1. Kruskal

The `Kruskal' class implements the Kruskal algorithm for finding the minimum spanning tree.

#### Constructor

```python
Kruskal(points, edges)
```

- `points`: A list of coordinates of graph vertices.
- `edges`: A list of graph edges, where each edge is represented as a tuple (u, v, weight).

#### Methods

- `draw_only(k)`: Displays the graph and its edges.
- `view(min_edges, max_edges, k)': Displays a graph with a minimum and maximum spanning tree.
- `kruskals_algorithm(edges)`: Implements the Kraskal algorithm for finding MST.
- `sort_edges_min()': Sorts the edges in ascending order of weight.
- `sort_edges_max()': Sorts the edges in descending order of weight.
- `result_weight(edges)`: Calculates and outputs the total weight of the tree.

### 2. Hamilton

The `Hamilton' class implements an algorithm for finding a Hamiltonian cycle.

#### Constructor

```python
Hamilton(points, edges)
```

- `points`: A list of coordinates of graph vertices.
- `edges`: A list of graph edges in the form of pairs of vertex indexes.

#### Methods

- `cycle_exist(cycle)`: Checks for a Hamiltonian cycle and outputs it.
- `draw()': Visualizes the graph.
- `avoidable()': Outputs the available vertices.
- `hamiltonian_cycle(start)': Finds a Hamiltonian cycle starting from a given vertex.
- `draw_graph(path=None)`: Displays a graph with a highlighted Hamiltonian cycle.

### 3. Primal_min

The `Primal_min' class implements the Prim algorithm for finding the minimum spanning tree.

#### Constructor

```python
Primal_min(graph)
```

- `graph': A graph in the form of a dictionary, where the keys are vertices and the values are lists of edges with weights.

#### Methods

- `run(begin)`: Starts the Prim algorithm, starting from the specified vertex.
- `min_tree()': Outputs the minimum spanning tree and its total weight.

## Usage example

```python
# Example of creating a graph and finding a minimum spanning tree
points = [(0, 0), (1, 1), (2, 0), (1, -1)]
edges = [(0, 1, 1.5), (0, 2, 1.0), (1, 3, 2.0), (2, 3, 1.0)]

kruskal = Kruskal(points, edges)
sorted_edges = kruskal.sort_edges_min()
mst = kruskal.alg_Kraskala(sorted_edges)
kruskal.view(mst, sorted_edges, 3)

# An example of finding a Hamiltonian cycle
hamilton = Hamilton(points, edges)
cycle = hamilton.hamiltonian_cycle(0)
hamilton.cycle_exist(cycle)
hamilton.draw_graph(cycle)
```

## License

This project is licensed under the MIT License. Please review the LICENSE file for more information.
``