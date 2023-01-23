"""
This module contains the implementation of various graph analysis techniques that can be used to understand the properties of the original graph or the computed MST.

"""

from graph import *
from kruskal_algorithm import *
from networkx.algorithms.connectivity import local_node_connectivity


# create an instance of the WindParkGraph class
wind_park = WindParkGraph()

# add wind turbines to the graph until there are 87 nodes
while wind_park.G.number_of_nodes() < 87:
    x = floor(random.uniform(1000, 10000))
    y = floor(random.uniform(1000, 10000))
    wt = WindTurbine(x, y, wind_park.G.number_of_nodes())
    wind_park.add_turbine(wt)

# add edges between the wind turbines
for i in range(1, 88):
    for j in range(i+1, 88):
        wind_park.add_edge(i)

mst = kruskal(wind_park)

mst_graph = nx.Graph()
for u, v, w in mst:
    mst_graph.add_edge(u, v, weight=w)

# to analyse the MST graph use mst_graph instead of wind_park.G
class GraphAnalysis():
    def get_diameter(self):
        diameter = nx.diameter(wind_park.G)
        print("The diameter is: ", diameter)
        return diameter

    def get_average_shortest_path_length(self):
        avg_shortest_path = nx.average_shortest_path_length(wind_park.G)
        print("The average shortest path length is: ", avg_shortest_path)
        return avg_shortest_path

    def get_average_clustering(self):
        avg_clustering = nx.average_clustering(wind_park.G)
        print("The average clustering is: ", avg_clustering)
        return avg_clustering

    def get_eigenvector_centrality(self):
        eigenvector_centrality = nx.eigenvector_centrality(wind_park.G)
        print("The eigenvector centrality is: ", eigenvector_centrality)
        return eigenvector_centrality

    def get_degree_centrality(self):
        degree_cent = nx.degree_centrality(wind_park.G)
        highest_cent = max(degree_cent.items(), key=lambda x: x[1])[0]
        print("The node with the highest centrality is: {} (in the MST graph represented as S) and has a centrality of {}".format(highest_cent, degree_cent[highest_cent]))
        return highest_cent

    def subgraph_centrality(self):
        subgraph_centrality = nx.subgraph_centrality(wind_park.G)
        print("The subgraph centrality is: ", subgraph_centrality)
        return subgraph_centrality

    def connectivity(self):
        connected = nx.is_connected(wind_park.G)
        print("The connectivity is: ", connected)
        return connected

    def eccentricity(self):
        eccentricity = nx.eccentricity(wind_park.G)
        print("The eccentricity is: ", eccentricity)

    def radius_center(self):
        radius = nx.radius(wind_park.G)
        center = nx.center(wind_park.G)
        print("The Raduis is: ", radius)
        print("The center of the graph is: ", center)

    # check robustness of the MST
    def get_percolation(self, num_nodes_to_remove):
        original_num_nodes = len(mst_graph)
        largest_components = []
        for _ in range(num_nodes_to_remove):
            if not mst_graph.nodes():
                print(f"The network has failed after removing {num_nodes_to_remove} nodes")
                return
            node_to_remove = random.choice(list(mst_graph.nodes()))
            mst_graph.remove_node(node_to_remove)
            if mst_graph.number_of_nodes() == 0:
                print(f"The network has failed after removing {num_nodes_to_remove} nodes")
                return
            largest_component = max(nx.connected_components(mst_graph), key=len)
            largest_components.append(len(largest_component))
        percolation = max(largest_components) / original_num_nodes
        print(f"The percolation after removing {num_nodes_to_remove} nodes for the MST is: {percolation}")
        return percolation


analyze_graph = GraphAnalysis()

if __name__ == "__main__":
    #Depending on the property you want to check call it's method
    analyze_graph.get_diameter()
    analyze_graph.get_average_shortest_path_length()
    analyze_graph.get_average_clustering()
    analyze_graph.get_eigenvector_centrality()
    analyze_graph.subgraph_centrality()
    analyze_graph.get_degree_centrality()
    analyze_graph.connectivity()
    analyze_graph.eccentricity()
    analyze_graph.radius_center()
    analyze_graph.get_percolation(80)
    analyze_graph.get_percolation(3)
    analyze_graph.get_percolation(10)
    analyze_graph.get_percolation(25)


