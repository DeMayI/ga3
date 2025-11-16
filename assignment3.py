'''
    This file contains the template for Assignment3. For testing it, I will place it
    in a different directory, call the function <min_steps_flood_escape>, and check its output.
    So, you can add/remove  whatever you want to/from this file. But, don't change the name
    of the file or the name/signature of the following function.

    I will use <python3> to run this code.
'''

class Node:
    def __init__(self, value, flood_turn = -1,  reach_turn = -1, x = None, y = None):
        self.value = value
        self.flood_turn = flood_turn
        self.reach_turn = reach_turn
        self.x = x
        self.y = y

class QueueNode:
    def __init__(self, value= None):
        self.value = value
        
    
class Queue:
    def __init__(self):
        self.head = QueueNode()
        self.tail = QueueNode()
        self.head.next = self.tail
        self.tail.prev = self.head
    def pop(self):
        if(self.head.next != self.tail):
            val = self.head.next.value
            self.head.next = self.head.next.next
            return val
        else:
            return None
    def append(self, value):
        newNode = QueueNode(value)
        newNode.next = self.tail
        newNode.prev = self.tail.prev
        self.tail.prev.next = newNode
        self.tail.prev = newNode





def min_steps_flood_escape(grid: list[str]) -> int:
    '''
    Compute the minimum number of steps to reach the shelter, in a board specified by
    a list of strings; grid[i] is the ith row of the grid.  grid[i][j] is the character
    at the intersection of row i and column j.

    @param grid: list[str] - representing the board.
    Output: minium number of steps to reach from the initial point top-left to the
    shelter bottom-right.
    '''

    # Your code here :)
    waterQueue = Queue()
    distanceQueue = Queue()
    tileDict = {}
    max_x = len(grid)
    max_y = len(grid[0])
    shelter_location = ""
    #populates the dictionary with node objects
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            tileDict[str(i) + ":" + str(j)] = Node(grid[i][j], -1, -1, i, j)
            if(grid[i][j] == "I"):
                distanceQueue.append(str(i) + ":" + str(j))
                tileDict[str(i) + ":" + str(j)].reach_turn = 0
            if(grid[i][j] == "W"):
                waterQueue.append(str(i) + ":" + str(j))
                tileDict[str(i) + ":" + str(j)].flood_turn = 0
            if(grid[i][j] == "S"):
                shelter_location = str(i) + ":" + str(j)

    #simulates the water spread
    endOfQueueReach = False
    while not endOfQueueReach:
        value = waterQueue.pop()
        if(value != None):
            current_node = tileDict[value]
            #attempts to flood every tile touching the current one
            flood_direction(waterQueue, current_node, tileDict, -1, 0, max_x, max_y)
            flood_direction(waterQueue, current_node, tileDict, 1, 0, max_x, max_y)
            flood_direction(waterQueue, current_node, tileDict, 0, 1, max_x, max_y)
            flood_direction(waterQueue, current_node, tileDict, 0, -1, max_x, max_y)
        else:
            endOfQueueReach = True
    #simulates the movement of the player
    endOfQueueReach = False
    while not endOfQueueReach:
        value = distanceQueue.pop()
        if(value != None):
            current_node = tileDict[value]
            #attempts to move every direction touching the current tile
            move_direction(distanceQueue, current_node, tileDict, -1, 0, max_x, max_y)
            move_direction(distanceQueue, current_node, tileDict, 1, 0, max_x, max_y)
            move_direction(distanceQueue, current_node, tileDict, 0, 1, max_x, max_y)
            move_direction(distanceQueue, current_node, tileDict, 0, -1, max_x, max_y)
        else:
            endOfQueueReach = True

    return tileDict[shelter_location].reach_turn

def move_direction(distanceQueue, currentNode, tileDict, xDir, yDir, max_x, max_y):
    #checks to see if the target tile is on the board
    if(currentNode.x + xDir < max_x and currentNode.x + xDir > 0):
        if(currentNode.y + yDir < max_y and currentNode.y + yDir > 0):
            target_node = tileDict[str(currentNode.x + xDir) + ":" + str(currentNode.y + yDir)]
            nodeFlooded = False

            if(target_node.flood_turn != -1 and target_node.flood_turn <= currentNode.reach_turn + 1):
                nodeFlooded = True

            #checks to see if the target tile is floodable ie not a shelter, rock, and hasn't already been flooded
            if(target_node.reach_turn == -1 and not nodeFlooded):
                #floods the tile and stores the turn that it will be flooded
                tileDict[str(currentNode.x + xDir) + ":" + str(currentNode.y + yDir)].flood_turn = currentNode.flood_turn + 1
                #adds the tile to the flood queue
                distanceQueue.append(str(currentNode.x + xDir) + ":" + str(currentNode.y + yDir))

def flood_direction(waterQueue, currentNode, tileDict, xDir, yDir, max_x, max_y):
    #checks to see if the target tile is on the board
    if(currentNode.x + xDir < max_x and currentNode.x + xDir > 0):
        if(currentNode.y + yDir < max_y and currentNode.y + yDir > 0):
            target_node = tileDict[str(currentNode.x + xDir) + ":" + str(currentNode.y + yDir)]
            #checks to see if the target tile is floodable ie not a shelter, rock, and hasn't already been flooded
            if((target_node.value != "S" or target_node.value != "R") and target_node.flood_turn == -1):
                #floods the tile and stores the turn that it will be flooded
                tileDict[str(currentNode.x + xDir) + ":" + str(currentNode.y + yDir)].flood_turn = currentNode.flood_turn + 1
                #adds the tile to the flood queue
                waterQueue.append(str(currentNode.x + xDir) + ":" + str(currentNode.y + yDir))

print(min_steps_flood_escape(["ILLW", "LLRR", "LLLL", "LLLS"]))


'''
MyQueue = Queue()

for i in range(10):
    MyQueue.append(i)
endOfQueueReach = False
while not endOfQueueReach:
    value = MyQueue.pop()
    if(value != None):
        print(value)
    else:
        endOfQueueReach = True
'''