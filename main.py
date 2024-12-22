from MapGeneratation import MapGenerator
from PathFinding import StreetCleanerAI

mapGen = MapGenerator()
choice = '1'
while choice == '1':
    mapGen.generateNew(20, 15, 5)
    mapGen.printMap()
    choice = input('Generate another map? (1/0) ')
start = int(input('Starting point for the robot '))
destination = int(input('End point for the robot '))
robot = StreetCleanerAI()
robot.findPath(start, destination, mapGen.graph)
print('')
mapGen.printMap()