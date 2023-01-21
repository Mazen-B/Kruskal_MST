"""
This module contains the implementation of various graph analysis techniques that can be used to understand the properties of a graph.

"""

from graph import *


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
        eigenvector_centrality = nx.average_clustering(wind_park.G)
        print("The eigenvectorcentrality is: ", eigenvector_centrality)
        return eigenvector_centrality

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


analyze_graph = GraphAnalysis()

if __name__ == "__main__":
    # Depending on the property you want to check call it's method
    analyze_graph.get_diameter()
    analyze_graph.get_average_shortest_path_length()
    analyze_graph.get_average_clustering()
    analyze_graph.get_eigenvector_centrality()
    analyze_graph.subgraph_centrality()
    analyze_graph.connectivity()
    analyze_graph.eccentricity()
    analyze_graph.radius_center()

