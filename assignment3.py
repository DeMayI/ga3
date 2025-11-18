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
            self.head.next.prev = self.head
            return val
        else:
            return None
    def append(self, value):
        if(value == None):
            return
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
    tileGrid = []
    max_x = len(grid)
    max_y = len(grid[0])
    for i in range(max_x):
        tileGrid.append([])
        for j in range(max_y):
            tileGrid[i].append(Node("L"))
    shelter_location_x = 0
    shelter_location_y = 0
    #populates the dictionary with node objects
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            tileGrid[i][j] = Node(grid[i][j], -1, -1, i, j)
            if(grid[i][j] == "I"):
                distanceQueue.append((i, j))
                tileGrid[i][j].reach_turn = 0
            if(grid[i][j] == "W"):
                waterQueue.append((i, j))
                tileGrid[i][j].flood_turn = 0
            if(grid[i][j] == "S"):
                shelter_location_x = i
                shelter_location_y = j

    


    #simulates the water spread
    endOfQueueReach = False
    while not endOfQueueReach:
        value = waterQueue.pop()
        if(value != None):
            current_node = tileGrid[value[0]][value[1]]
            #attempts to flood every tile touching the current one
            
            waterQueue.append(flood_direction(current_node, tileGrid, -1, 0, max_x, max_y))
            waterQueue.append(flood_direction(current_node, tileGrid, 1, 0, max_x, max_y))
            waterQueue.append(flood_direction(current_node, tileGrid, 0, 1, max_x, max_y))
            waterQueue.append(flood_direction(current_node, tileGrid, 0, -1, max_x, max_y))
        else:
            endOfQueueReach = True
    #simulates the movement of the player
    endOfQueueReach = False
    while not endOfQueueReach:
        value = distanceQueue.pop()
        if(value != None):
            current_node = tileGrid[value[0]][value[1]]
            #attempts to move every direction touching the current tile
            distanceQueue.append(move_direction(current_node, tileGrid, -1, 0, max_x, max_y))
            distanceQueue.append(move_direction(current_node, tileGrid, 1, 0, max_x, max_y))
            distanceQueue.append(move_direction(current_node, tileGrid, 0, 1, max_x, max_y))
            distanceQueue.append(move_direction(current_node, tileGrid, 0, -1, max_x, max_y))
        else:
            endOfQueueReach = True


    '''
    for i in range(max_x):
        for j in range(max_y):
            print("Node:" + str(i) + ":" + str(j) + " State:" + "Water Turn: " + str(tileGrid[i][j].flood_turn) + " Reach Turn: " + str(tileGrid[i][j].reach_turn))
    '''
    return tileGrid[shelter_location_x][shelter_location_y].reach_turn

def move_direction(currentNode, tileGrid, xDir, yDir, max_x, max_y):
    #checks to see if the target tile is on the board
    if(currentNode.x + xDir < max_x and currentNode.x + xDir >= 0):
        if(currentNode.y + yDir < max_y and currentNode.y + yDir >= 0):
            target_node = tileGrid[currentNode.x + xDir][currentNode.y + yDir]
            nodeFlooded = False

            if(target_node.flood_turn != -1 and target_node.flood_turn <= currentNode.reach_turn + 1):
                nodeFlooded = True

            #checks to see if the target tile is floodable ie not a shelter, rock, and hasn't already been flooded
            if(target_node.reach_turn == -1 and not nodeFlooded):
                #floods the tile and stores the turn that it will be flooded
                
                tileGrid[currentNode.x + xDir][currentNode.y + yDir].reach_turn = currentNode.reach_turn + 1
                #adds the tile to the flood queue
                return (currentNode.x + xDir, currentNode.y + yDir)
    return None

def flood_direction(currentNode, tileGrid, xDir, yDir, max_x, max_y):
    #checks to see if the target tile is on the board
    if((currentNode.x + xDir) < max_x and (currentNode.x + xDir) >= 0):
        if((currentNode.y + yDir) < max_y and (currentNode.y + yDir) >= 0):
            
            target_node = tileGrid[currentNode.x + xDir][currentNode.y + yDir]
            #checks to see if the target tile is floodable ie not a shelter, rock, and hasn't already been flooded
            if((target_node.value != "S" and target_node.value != "R") and target_node.flood_turn == -1):
                #floods the tile and stores the turn that it will be flooded
                tileGrid[currentNode.x + xDir][currentNode.y + yDir].flood_turn = currentNode.flood_turn + 1
                #adds the tile to the flood queue
                return (currentNode.x + xDir, currentNode.y + yDir)
    return None

#print(min_steps_flood_escape(["ILLW", "LLRR", "LLLL", "LLLS"]))
#print(min_steps_flood_escape(["ILLW", "LRRL", "LRLL", "LLLS"]))

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
