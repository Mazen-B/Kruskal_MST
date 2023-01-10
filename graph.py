from math import sqrt, floor
import random
import networkx as nx
from networkx import kamada_kawai_layout
import matplotlib.pyplot as plt


class WindTurbine:
    def __init__(self, x, y, ID):
        self.x = x
        self.y = y
        self.ID = ID
    
    # Pythagorean theorem
    def distance(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return sqrt(dx**2 + dy**2)

class WindParkGraph:
    def __init__(self):
        self.turbines = []
        self.G = nx.Graph()

    def add_turbine(self, turbine):
        rotor_diameter=154

        for other_turbine in self.turbines:
            if turbine.distance(other_turbine) < 4*rotor_diameter:
                return

        # if the turbine passes the distance constraint, add it to the list and the graph
        self.turbines.append(turbine)
        self.G.add_node(turbine.ID, pos=(turbine.x, turbine.y))

    def add_edge(self, ID1):
        turbine1 = None
        for t in self.turbines:
            if t.ID == ID1:
                turbine1 = t
                break
        
        if turbine1 is None:
            return "Turbine with ID{} was not found in the list".format(ID1)

        for turbine2 in self.turbines:
            # avoid self-loops
            if turbine1.ID != turbine2.ID:
                if self.G.has_edge(turbine1.ID, turbine2.ID):
                    # Update the weight of the existing edge
                    weight = turbine1.distance(turbine2)
                    self.G[turbine1.ID][turbine2.ID]['weight'] = weight
                else:
                    # Add a new weighted edge
                    weight = turbine1.distance(turbine2)
                    self.G.add_edge(turbine1.ID, turbine2.ID, weight=weight)

        if self.check_cables():
            return "The new cable intersects with an existing one"

    # sweep line algorithm to check if cables connecting overlap or touch:
    def check_cables(self):
        self.turbines.sort(key=lambda x: x.x)
        
        for turbine in self.turbines:
            try:
                # if ID1 = 0 then ID2 is the second element of the list (right ID)
                if turbine.ID == 0:
                    ID1 = turbine.ID
                    ID2 = self.turbines[turbine.ID+1].ID
                # if ID1 is the last ID then ID2 is the second to last element of the list (left ID)
                elif turbine.ID == len(self.turbines)-1:
                    ID1 = turbine.ID
                    ID2 = self.turbines[turbine.ID-1].ID
                # else check the weight of the cable to compare the length of the cable (weight) 
                else:
                    left_ID1 = turbine.ID
                    left_ID2 = self.turbines[turbine.ID-1].ID
                    right_ID1 = turbine.ID
                    right_ID2 = self.turbines[turbine.ID+1].ID
                    left_cable = self.G[turbine.ID][self.turbines[turbine.ID-1].ID]['weight']
                    right_cable = self.G[turbine.ID][self.turbines[turbine.ID+1].ID]['weight']
                    if left_cable < right_cable:
                        ID1 = left_ID1
                        ID2 = left_ID2
                    else:
                        ID1 = right_ID1
                        ID2 = right_ID2

                # check if the cables intersect or touch
                if self.check_intersection(ID1, ID2):
                    return True
            except:
                continue
        return False

    def check_intersection(self, ID1, ID2):
        # check if the cables intersect using the line intersection formula
        x1, y1 = self.turbines[ID1].x, self.turbines[ID1].y
        x2, y2 = self.turbines[ID2].x, self.turbines[ID2].y
        for other_turbine in self.turbines:
            if other_turbine.ID == ID1 or other_turbine.ID == ID2:
                continue
            x3, y3 = other_turbine.x, other_turbine.y
            for other_other_turbine in self.turbines:
                if other_other_turbine.ID == ID1 or other_other_turbine.ID == ID2 or other_other_turbine.ID == other_turbine.ID:
                    continue
                x4, y4 = other_other_turbine.x, other_other_turbine.y
                d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
                if d == 0:
                    continue
                uA = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / d
                uB = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / d
                if uA > 0 and uA < 1 and uB > 0 and uB < 1:
                    return True
        return False

    # needed to compute the local connectivity (in the substation module)
    def is_directed(self):
        return False

    def draw(self):
        pos = kamada_kawai_layout(self.G)

        labels = {}
        node_colors = []
        for i in range(self.G.number_of_nodes()):
            labels[i] = f"T{i + 1}"
            if i == 0 or i == self.G.number_of_nodes() - 1:
                node_colors.append("red")
            else:
                node_colors.append("blue")
        nx.draw(self.G, pos, with_labels=True, labels=labels, node_color=node_colors, node_size=300, font_size=8, font_weight="bold")

        plt.show()

    # this method checks if we have a random graph with p=1
    def check_topology(self):
            num_nodes = self.G.number_of_nodes()
            num_edges = self.G.number_of_edges()
            weights = list(self.G.edges(data='weight'))
            print("The number of nodes is: {}, and the number of edges is: {}.\nA list containing nodes, edges and weights: {}".format(num_nodes, num_edges, weights))

            # average degree 
            candidates = []
            for node in self.G.nodes():
                if self.G.degree(node) >= 1:
                    candidates.append(node)
            degrees = {n: self.G.degree(n) for n in candidates}
            k = sum(degrees.values())/len(degrees.values())
            print("The average degree (<k>) is: ", k)

            # Random failure for an ER-network
            fc=1-(1/k)
            print("The fc for this graph is: ", fc)

# create an instance of the WindParkGraph class
wind_park = WindParkGraph()

# add wind turbines to the graph until there are 87 nodes
while wind_park.G.number_of_nodes() < 87:
    x = floor(random.uniform(1000, 10000))
    y = floor(random.uniform(1000, 10000))
    ID = wind_park.G.number_of_nodes()
    wt = WindTurbine(x, y, ID)
    wind_park.add_turbine(wt)

# add edges between the wind turbines
for i in range(1, 88):
    for j in range(i+1, 88):
        wind_park.add_edge(i)

### just for debugging:
### to check the network topology
#print(wind_park.check_topology())

### to check if all the turbines ID if they are added in add_turbine()
###  add this to the add_trubine print(f"Adding turbine with ID {turbine.ID} to the graph")
#print(wind_park.add_trubine())
 
### to get the positions of the nodes in the graph 
#pos = nx.get_node_attributes(wind_park.G, 'pos')
#print(pos)

if __name__ == "__main__":
    wind_park.draw()