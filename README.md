# Wind Park Graph
This project provides a solution to model a wind park as a graph, where each wind turbine is a node and the cables connecting them are the edges. The distance between two wind turbines is constrained to be at least four times their rotor diameter. The wind park graph also includes a method to check if any two cables intersect or touch. 

The created graph is a random graph with a probability of 1 because we are interesed in a complete graph.

# The project consists of 4 main modules:
1. *graph.py* creates then draws a graph representing a wind parks (in my example of 87 wind turbines). The graph respects the distance and overlapping constrains (mentioned above). Also a check topology method can be called to get information about the topoloy of the graph and to make sure that the created graph is a random graph with p = 1.
    <figure>
    <img src="./Figures/wp_graph.png" alt="Alt text">
    <figcaption>Figure 1: Output when calling the draw method in graph.py</figcaption>
    </figure>
2. *graph_analyis.py* contains the implementation of various graph analysis techniques that can be used to better understand the properties of the created graph.

3. *kruskal_algorithm.py* uses the kryskal algorithm to compute the MST for the graph created in graph.py. Using a disjoint-set data structure and union to merge the sets.
    <figure>
    <img src="./Figures/kruskal.png" alt="Alt text">
    <figcaption>Figure 2: Output when running the draw method in kruskal_algorithm.py</figcaption>
    </figure>
4. *substation.py* computes the highest degree, highest betweenness centrality and closeness centrality of the MST graph. These methods are used to find the aggregation node, which serves as the central point of connection for all the other nodes in the network.
    <figure>
    <img src="./Figures/substation.png" alt="Alt text">
    <figcaption>Figure 3: Output when running the draw method in substation.py</figcaption>
    </figure>

This project is a part of a university course project for the Systems and Network Analysis course.