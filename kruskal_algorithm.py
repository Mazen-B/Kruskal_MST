from graph import *

def kruskal(G, distance_threshold):
    mst = []

    # sort the edges of the graph by weight in ascending order
    edges = list(G.G.edges(data='weight'))
    sorted_edges = sorted(edges, key=lambda x: x[2])

    ds = DisjointSet()

    for v in G.G.nodes():
        ds.make_set(v)

    for u, v, w in sorted_edges:
        w = floor(w)
        # If the endpoints of the edge belong to different connected components, add the edge to the MST and union the connected components
        if ds.find(u) != ds.find(v) and w > distance_threshold:
            mst.append((u, v, w))
            ds.union(u, v)

    return mst

def draw_mst(mst, G):
    mst_graph = nx.Graph()

    for u, v, w in mst:
        mst_graph.add_edge(u, v, weight=w)

    # use the Kamada-Kawai layout, which uses a force-directed approach to positioning the nodes:
    # scale parameter controls the overall spacing between all the nodes in the layout
    pos = nx.kamada_kawai_layout(mst_graph, scale=100)

    nx.draw(mst_graph, pos, with_labels=False, font_weight='bold', node_size=350)

    labels = {}
    for i in range(87):
        labels[i] = "T" + str(i+1)

    nx.draw_networkx_labels(mst_graph, pos, labels, font_size=6, font_weight='bold')

    labels = nx.get_edge_attributes(mst_graph, 'weight')
    nx.draw_networkx_edge_labels(mst_graph, pos, edge_labels=labels, font_size=8, font_weight='bold')

    plt.show()


# initialize a disjoint-set data structure to keep track of the connected components in the MST
class DisjointSet:
    def __init__(self):
        self.parent = {}
    
    def make_set(self, x):
        self.parent[x] = x
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        x_root = self.find(x)
        y_root = self.find(y)
        if x_root != y_root:
            self.parent[x_root] = y_root


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
        wind_park.add_edge(i, j)


mst = kruskal(wind_park, distance_threshold=2000)



if __name__ == "__main__":
    print(mst)
    print(len(mst)) # mst should return |V|-1
    draw_mst(mst, wind_park.G)
    mst_degrees = nx.degree(mst)
