import copy

class StreetCleanerAI:
    capacity = 20

    def removeEdge(self, nodeA, nodeB, Map):
        """
        Set edge's weight to 0 on both paths from A to B, and from B to A
        """
        for i in range(len(Map[nodeA])):
            if Map[nodeA][i][0] == nodeB:
                Map[nodeA][i][1] = 0
                break
        for i in range(len(Map[nodeB])):
            if Map[nodeB][i][0] == nodeA:
                Map[nodeB][i][1] = 0
                break
        return Map

    def findPath(self, start, destination, Map):
        """
        Find path from start to destination, while trying to maximise capacity
        """
        validPaths = []
        # recursive depth search
        for i in range(len(Map[start])):
            newMap = self.removeEdge(start, Map[start][i][0], copy.deepcopy(Map))
            path = self.checkPath(Map[start][i][0], destination, self.capacity - Map[start][i][1], newMap)
            if path is not None:
                path.append(start)
                validPaths.append(path)
        # print out the best path
        print('Found best path:')
        maxPath = 0
        for i in range(len(validPaths)):
            if validPaths[maxPath][0] > validPaths[i][0]:
                maxPath = i
        print(str(validPaths[maxPath][1:]) + ' , used capacity - ' + str(self.capacity - validPaths[maxPath][0]))


    def checkPath(self, curr, dest, fill, changedMap):
        """
        Recursive step trying to find the best path
        """
        validPaths = []
        if curr != dest:
            # continue recursive search
            for i in range(len(changedMap[curr])):
                if changedMap[curr][i][1] != 0:
                    newCapacity = fill - changedMap[curr][i][1]
                    if newCapacity >= 0:
                        newMap = self.removeEdge(curr, changedMap[curr][i][0], copy.deepcopy(changedMap))
                        newPath = self.checkPath(changedMap[curr][i][0], dest, newCapacity, newMap)
                        if newPath is not None:
                            newPath.append(curr)
                            validPaths.append(newPath)
            # decide the best path from valid ones
            if len(validPaths) == 0:
                return None
            else:
                maxPath = 0
                for i in range(len(validPaths)):
                    if validPaths[maxPath][0] > validPaths[i][0]:
                        maxPath = i
                return validPaths[maxPath]
        else:
            # destination reached
            return [fill, dest]