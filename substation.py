"""
This module aims to find the most important node (an aggregation node) and then draw it as a substation (S) in the MST graph.
The methods that compute the highest degree, highest betweenness centrality and closeness centrality are used to find the aggregation node.
"""
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

    degree_sorted = sorted(degree.items(), key=lambda x: x[1], reverse=True)
    betweenness_centrality_sorted = sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)
    closeness_centrality_sorted = sorted(closeness_centrality.items(), key=lambda x: x[1], reverse=True)

    for aggregation_node, _ in degree_sorted:
        for node_betweenness, _ in betweenness_centrality_sorted:
            for node_closeness, _ in closeness_centrality_sorted:
                if aggregation_node == node_betweenness and aggregation_node == node_closeness:
                    print("The aggregation node is: {} (represented in the graph as S)".format(aggregation_node))
                    return aggregation_node
      
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