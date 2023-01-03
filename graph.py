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
        rotor_diameter=130

        for other_turbine in self.turbines:
            if turbine.distance(other_turbine) < 3*rotor_diameter:
                return

        # if the turbine passes the distance constraint, add it to the list and the graph
        self.turbines.append(turbine)
        self.G.add_node(turbine.ID, pos=(turbine.x, turbine.y))

        # add edges to the graph connecting the new turbine to all other turbines (followting distance constrain)
        for other_turbine in self.turbines:
            if turbine.ID != other_turbine.ID and turbine.distance(other_turbine) >= 3:
                self.G.add_edge(turbine.ID, other_turbine.ID, weight=turbine.distance(other_turbine))

        
    def add_edge(self, ID1):
        # check if the node does not exist in the graph
        if ID1 not in self.G:
            return

        # find the wind turbine with ID1 in the list
        turbine = None
        for t in self.turbines:
            if t.ID == ID1:
                turbine = t
                break

        # if the wind turbine was not found, return
        if turbine is None:
            return

        # loop over all the wind turbines in the list
        for other_turbine in self.turbines:
            # if the distance between the two turbines is at least 3 times the rotor diameter, add an edge to the graph
            if turbine.ID != other_turbine.ID and turbine.distance(other_turbine) >= 3:
                # check if there is already an edge between the two nodes
                if self.G.has_edge(turbine.ID, other_turbine.ID):
                    # update the weight of the existing edge
                    weight = floor(random.randint(300, 3000))
                    self.G[turbine.ID][other_turbine.ID]['weight'] = weight
                else:
                    # add a new edge with a random weight
                    weight = floor(random.randint(300, 3000))
                    self.G.add_edge(turbine.ID, other_turbine.ID, weight=weight)


    # sweep line algorithm to check if cables connecting overlap or touch:
    def check_cables(self):
        # sort the wind turbines by their x coordinate
        self.turbines.sort(key=lambda x: x.x)
        
        # initialize an empty list to store the intersecting cables
        intersecting_cables = []
        
        # scan the sweep line across the wind park
        for turbine in self.turbines:
            # get the cable connecting the wind turbine to its nearest neighbor on the left or right
            if turbine.ID == 0:
                cable = self.G[turbine.ID][self.turbines[turbine.ID+1].ID]['weight']
            elif turbine.ID == len(self.turbines)-1:
                cable = self.G[turbine.ID][self.turbines[turbine.ID-1].ID]['weight']
            else:
                left_cable = self.G[turbine.ID][self.turbines[turbine.ID-1].ID]['weight']
                right_cable = self.G[turbine.ID][self.turbines[turbine.ID+1].ID]['weight']
                if left_cable < right_cable:
                    cable = left_cable
                else:
                    cable = right_cable
            
            # check whether the cable intersects any of the intersecting cables
            for intersecting_cable in intersecting_cables:
                if self.check_intersection(cable, intersecting_cable):
                    return True
            
            # add the cable to the list of intersecting cables
            intersecting_cables.append(cable)
        
        # if no intersecting cables were found, return False
        return False
    
    def check_intersection(self, cable1, cable2):
        # calculate the x and y coordinates of the two endpoints of the cables
        x1, y1 = self.get_coordinates(cable1)
        x2, y2 = self.get_coordinates(cable2)
        
        # check whether the cables intersect
        if min(x1, x2) <= max(x1, x2) and min(y1, y2) <= max(y1, y2):
            return True
        else:
            return False

    def get_coordinates(self, cable):
        # get the IDs of the wind turbines to which the cable is attached
        ID1, ID2 = self.G.edges[cable]['weight']
        
        # get the x and y coordinates of the wind turbines
        x1, y1 = self.G.nodes[ID1]['pos']
        x2, y2 = self.G.nodes[ID2]['pos']
        
        return (x1, y1, x2, y2)
    
    # to check the connectivity (in the network_structure module)
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


    def check_num(self):
            num_nodes = self.G.number_of_nodes()
            num_edges = self.G.number_of_edges()
            weights = list(self.G.edges(data='weight'))
            print("The number of nodes is: {}, and the number of edges is: {}. \nA list containing nodes, edges and weights: {}".format(num_nodes, num_edges, weights))


# create an instance of the WindParkGraph class and add 87 wind turbines to it
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

### just for debugging:
### to check the number of nodes and edges (with a weighted edges list) 
#print(wind_park.check_num())

### to check if all the turbines ID if they are added in add_turbine()
###  add this to the add_trubine print(f"Adding turbine with ID {turbine.ID} to the graph")
#print(wind_park.add_trubine())
 
### to get the positions of the nodes in the graph 
#pos = nx.get_node_attributes(wind_park.G, 'pos')
#print(pos)

if __name__ == "__main__":
    wind_park.draw()