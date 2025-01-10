from MapGeneratation import MapGenerator
from PathFinding import StreetCleanerAI
import copy

mapGen = MapGenerator()
while True:
    mapGen.generateNew(20, 15, 5)
    mapGen.printMap()
    mapGen.printGraph()
    if input('Generate another map? (1/0) ') != '1':
        break
graphMap = copy.deepcopy(mapGen.graph)
numOfRobots = 1
while True:
    robot = StreetCleanerAI()
    start = int(input('Starting point for the robot #' + str(numOfRobots) + ' '))
    destination = int(input('End point for the robot #' + str(numOfRobots) + ' '))
    bestPath = robot.findPath(start, destination, graphMap)
    mapGen.printGraph()
    if input('Launch another robot? (1/0) ') != '1':
        break
    numOfRobots = numOfRobots + 1
    graphMap = robot.removePaths(graphMap, bestPath)