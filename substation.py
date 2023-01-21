"""
The purpose of this module is to test and to understand the MST graph then to add an aggregation node.
The methods that compute the local connectivity, clustering, and highest degree centrality provide insight into the graph. 
The methods that compute highest degree, highest betweenness centrality and closeness centrality are used to find the aggregation node.
"""
from networkx.algorithms.connectivity import local_node_connectivity
from kruskal_algorithm import *


wind_park = WindParkGraph()
# because we are adding a substation we have 88 nodes (87 turbines and 1 substation)
while wind_park.G.number_of_nodes() < 88:
    x = floor(random.uniform(1000, 10000))
    y = floor(random.uniform(1000, 10000))
    wt = WindTurbine(x, y, wind_park.G.number_of_nodes())
    wind_park.add_turbine(wt)

for i in range(1, 89):
    for j in range(i+1, 89):
        wind_park.add_edge(i)


mst = kruskal(wind_park)

mst_graph = nx.Graph()
for u, v, w in mst:
    mst_graph.add_edge(u, v, weight=w)


# the local_connectivity is added just to test if we only have one connection between each 2 nodes (as it should for an MST)
def local_connectivity():

    connectivity = {}
    for u, v in mst_graph.edges():
        connectivity[(u, v)] = local_node_connectivity(mst_graph, u, v)

    print(f"The local_connectivity for all pairs of nodes in the MST are: {connectivity}.")

# test the connection of the network (for an MST it would be 0)
def compute_clustering():
    for u, v in mst_graph.edges():
        local_clustering = nx.clustering(mst_graph, u)

        print(f"The local clustering coefficient for node {u} is {local_clustering}.")

    global_clustering = nx.transitivity(mst_graph)
    print(f"The global clustering coefficient for the MST graph is {global_clustering}.")

    return local_clustering, global_clustering

def compute_degree_centrality():

    degree_cent = nx.degree_centrality(mst_graph)
    highest_cent = max(degree_cent.items(), key=lambda x: x[1])[0]

    print("The node with the highest centrality is: {} (in the MST graph represented as S) and has a centrality of {}".format(highest_cent, degree_cent[highest_cent]))

    return highest_cent

def compute_degree():

    candidates = []

    for node in mst_graph.nodes():
        if mst_graph.degree(node) >= 1:
            candidates.append(node)
 
    if not candidates:
        print("No candidate found, returning the first node as the aggregation node.")
        return mst_graph.nodes()[0]

    degrees = {n: mst_graph.degree(n) for n in candidates}

    return degrees

def compute_betweenness_centrality():
    betweenness_centrality = nx.betweenness_centrality(mst_graph)

    return betweenness_centrality

def compute_closeness_centrality():
    closeness_centrality = nx.closeness_centrality(mst_graph)

    return closeness_centrality

def find_aggregation_node():
    degree = compute_degree()
    betweenness_centrality = compute_betweenness_centrality()
    closeness_centrality = compute_closeness_centrality()

    for node in mst_graph.nodes():
        if node in degree and node in betweenness_centrality and node in closeness_centrality:
            print("The aggregation node is: {} (represented in the graph as S)".format(node))
            return node
    
    highest_degree = max(degree, key=degree.get)
    print("No intersection node found, returning the highest degree node in the network: ", highest_degree)
    return highest_degree

def draw_substation(mst):

    mst_graph = nx.Graph()

    for u, v, w in mst:
        mst_graph.add_edge(u, v, weight=w)

    pos = nx.kamada_kawai_layout(mst_graph, scale=500)

    aggregation_node = find_aggregation_node()

    mst_nodes = [node for node in mst_graph.nodes()]

    node_colors = ['orange' if node == aggregation_node else '#87CEEB' for node in mst_nodes]

    nx.draw(mst_graph, pos=pos, nodelist=mst_nodes, node_color=node_colors)

    # having S as a label for aggr_node and changing the order after it
    labels = {}
    for i, node in enumerate(mst_graph.nodes()):
        if node == aggregation_node:
            labels[node] = "S"
        else:
            labels[node] = "T" + str(i if i >= mst_nodes.index(aggregation_node) else i+1)

    nx.draw_networkx_labels(mst_graph, pos, labels, font_size=6, font_weight='bold')

    labels = nx.get_edge_attributes(mst_graph, 'weight')
    nx.draw_networkx_edge_labels(mst_graph, pos, edge_labels=labels, font_size=8, font_weight='bold')

    # draw a line from S to the shore (export cable)
    min_x, max_x = min(pos[n][0] for n in mst_graph.nodes()), max(pos[n][0] for n in mst_graph.nodes())
    min_y, max_y = min(pos[n][1] for n in mst_graph.nodes()), max(pos[n][1] for n in mst_graph.nodes())

    # to make sure that the point is outside the MST
    point_pos = (max_x + 1, min_y - 1) 

    s_node = [n for n in mst_graph.nodes() if n == aggregation_node][0]
    s_pos = pos[s_node]
    mst_graph = nx.Graph()


    plt.plot([s_pos[0], point_pos[0]], [s_pos[1], point_pos[1]], 'k--', linewidth=2, alpha=0.5, dashes=[5, 5])
    plt.text(point_pos[0], point_pos[1], "Shore (at 5 km)", fontsize=12, ha="center", va="center")


    plt.show()


if __name__ == "__main__":
    draw_substation(mst)