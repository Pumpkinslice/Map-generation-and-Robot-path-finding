import matplotlib.pyplot as plt
from random import randint
import networkx as nx

class MapGenerator:
    map = []
    graph = []

    def checkNode(self, width, height):
        """
        Checks if created node is not on edge and doesn't have anything beside it
        """
        # check if within boundaries - 1
        if len(self.map[0]) - 1 > width > 0:
            if len(self.map) - 1 > height > 0:
                pass
            else:
                return False
        else:
            return False
        # check if everything around is empty
        if self.map[height-1][width-1] == 0 and self.map[height][width-1] == 0 and self.map[height+1][width-1] == 0:
            if self.map[height-1][width+1] == 0 and self.map[height][width+1] == 0 and self.map[height+1][width+1] == 0:
                if self.map[height-1][width] == 0 and self.map[height+1][width] == 0 and self.map[height][width] == 0:
                    return True
        return False

    def generateNew(self, width, height, initialNodeCount):
        """
        Generate new map, also creating grid map and graph tree based on it
        """
        # empty map of given scale
        self.map = []
        self.graph = []
        for i in range(height):
            self.map.append([0] * width)
        # place initial nodes and branch them out
        for i in range(initialNodeCount):
            nodeW, nodeH = randint(0, width - 1), randint(0, height - 1)
            while True:
                if self.checkNode(nodeW, nodeH):
                    break
                else:
                    nodeW, nodeH = randint(0, width - 1), randint(0, height - 1)
            self.map[nodeH][nodeW] = 2
            # place roads randomly in cardinal directions
            if randint(0, 2) != 0:  # left road
                step = nodeW
                while step > 0:
                    step = step - 1
                    if self.map[nodeH][step] == 1:
                        self.map[nodeH][step] = 2
                        if randint(0,2) == 0:
                            break
                    elif self.map[nodeH][step] == 2:
                        break
                    else:
                        self.map[nodeH][step] = 1
            if randint(0, 2) != 0:  # right road
                step = nodeW
                while step < width - 1:
                    step = step + 1
                    if self.map[nodeH][step] == 1:
                        self.map[nodeH][step] = 2
                        if randint(0,2) == 0:
                            break
                    elif self.map[nodeH][step] == 2:
                        break
                    else:
                        self.map[nodeH][step] = 1
            if randint(0, 2) != 0:  # top road
                step = nodeH
                while step > 0:
                    step = step - 1
                    if self.map[step][nodeW] == 1:
                        self.map[step][nodeW] = 2
                        if randint(0,2) == 0:
                            break
                    elif self.map[step][nodeW] == 2:
                        break
                    else:
                        self.map[step][nodeW] = 1
            if randint(0, 2) != 0:  # bottom road
                step = nodeH
                while step < height - 1:
                    step = step + 1
                    if self.map[step][nodeW] == 1:
                        self.map[step][nodeW] = 2
                        if randint(0,2) == 0:
                            break
                    elif self.map[step][nodeW] == 2:
                        break
                    else:
                        self.map[step][nodeW] = 1
        # differentiate nodes by IDs stating at 2
        nodeTotal = 2
        for h in range(height - 1, -1, -1):
            for w in range(width):
                if self.map[h][w] == 2:
                    self.map[h][w] = nodeTotal
                    nodeTotal = nodeTotal + 1
        print('Number of resulting nodes:', nodeTotal - 2)
        # make graph tree
        for h in range(height - 1, -1, -1):
            for w in range(width):
                if self.map[h][w] > 1:
                    edges = []
                    # going up
                    pathLength = h + 1
                    while pathLength != height:
                        if self.map[pathLength][w] > 1:
                            edges.append([self.map[pathLength][w] - 2, pathLength - h - 1])
                            break
                        pathLength = pathLength + 1
                    # going down
                    pathLength = h - 1
                    while pathLength != -1:
                        if self.map[pathLength][w] > 1:
                            edges.append([self.map[pathLength][w] - 2, h - pathLength - 1])
                            break
                        pathLength = pathLength - 1
                    # going right
                    pathLength = w + 1
                    while pathLength != width:
                        if self.map[h][pathLength] > 1:
                            edges.append([self.map[h][pathLength] - 2, pathLength - w - 1])
                            break
                        pathLength = pathLength + 1
                    # going right
                    pathLength = w - 1
                    while pathLength != -1:
                        if self.map[h][pathLength] > 1:
                            edges.append([self.map[h][pathLength] - 2, w - pathLength - 1])
                            break
                        pathLength = pathLength - 1
                    self.graph.append(edges)


    def printMap(self):
        """
        Print out map in console and 2 plots
        """
        fig, ax = plt.subplots()
        # grid map
        array0W, array0H, array1W, array1H, array2W, array2H = [], [], [], [], [], []
        for h in range(len(self.map) - 1, -1, -1):
            print(str(h) + 'h ' + str(self.map[h]))
            for w in range(len(self.map[h])):
                if self.map[h][w] == 0:
                    array0W.append(w)
                    array0H.append(h)
                if self.map[h][w] == 1:
                    array1W.append(w)
                    array1H.append(h)
                if self.map[h][w] > 1:
                    array2W.append(w)
                    array2H.append(h)
        ax.scatter(array0W, array0H, s=200, label='Empty', c='#737373', marker='s')
        ax.scatter(array1W, array1H, s=200, label='Road', c='#DBDBDB', marker='s')
        ax.scatter(array2W, array2H, s=200, label='Node', c='#FF9C1A', marker='s')
        plt.title("Generated map grid")
        plt.legend()
        plt.show()
        plt.close()
        # graph tree
        print('')
        tree = nx.Graph()
        for node in range(len(self.graph)):
            print(str(node) + 'n ' + str(self.graph[node]))
            for connection in range(len(self.graph[node])):
                tree.add_edge(node, self.graph[node][connection][0], weight=self.graph[node][connection][1])
        pos = nx.spring_layout(tree, seed=randint(1,10))
        nx.draw_networkx_nodes(tree, pos, node_color='orange')
        nx.draw_networkx_edges(tree, pos)
        nx.draw_networkx_labels(tree, pos)
        nx.draw_networkx_edge_labels(tree, pos, nx.get_edge_attributes(tree, "weight"))
        plt.title("Generated graph tree")
        plt.show()
        plt.close()