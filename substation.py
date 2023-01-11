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

# the local_connectivity is added just to test if we only have one connection between each 2 nodes (as it should for an MST)
def local_connectivity(G, mst):
    mst_graph = nx.Graph()
    for u, v, w in mst:
        mst_graph.add_edge(u, v, weight=w)

    connectivity = {}
    for u, v in mst_graph.edges():
        connectivity[(u, v)] = local_node_connectivity(mst_graph, u, v)

    print(f"The local_connectivity for all pairs of nodes in the MST are: {connectivity}.")


def compute_degree(G, mst):

    mst_graph = nx.Graph()
    for u, v, w in mst:
        mst_graph.add_edge(u, v, weight=w)
    candidates = []

    for node in mst_graph.nodes():
        if mst_graph.degree(node) >= 1:
            candidates.append(node)
 
    if not candidates:
        print("No candidate found, returning the first node as the aggregation node.")
        return mst_graph.nodes()[0]

    degrees = {n: mst_graph.degree(n) for n in candidates}
    highest_degree = max(degrees, key=degrees.get)

    print("The node with the highest degree is: {} (in the MST graph represented as S) and has a degree of {}".format(highest_degree, degrees[highest_degree]))

    return highest_degree

def compute_centrality():
    mst_graph = nx.Graph()

    for u, v, w in mst:
        mst_graph.add_edge(u, v, weight=w)

    degree_cent = nx.degree_centrality(mst_graph)
    highest_cent = max(degree_cent.items(), key=lambda x: x[1])[0]

    print("The node with the highest centrality is: {} (in the MST graph represented as S) and has a centrality of {}".format(highest_cent, degree_cent[highest_cent]))

    return highest_cent

def draw_substation(mst, G):

    mst_graph = nx.Graph()

    for u, v, w in mst:
        mst_graph.add_edge(u, v, weight=w)

    pos = nx.kamada_kawai_layout(mst_graph, scale=500)

    aggregation_node = compute_degree(G, mst)

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
    ### to also compute the local connectivity
    #local_connectivity(wind_park, mst)

    compute_degree(wind_park, mst)
    compute_centrality()
    draw_substation(mst, wind_park)




