'''
grid = [['1','2','3','4','5'],['1','2','3','4','5']]
for x in grid[0]:
    for y in grid[1]:
        print(x, y)

'''
import random
def maze():
    grid = [[0,1,2,3,4], [0,1,2,3,4]]
    cells = []
    for x in grid[0]:
        for y in grid[1]:
            cells.append({"position": [x, y],
            "walls": {
                'top': True,
                'bottom': True,
                'left': True,
                'right': True
            } 
            })
    return cells

my_maze = maze()

vis = my_maze[0]

def remove_wall(CuCe, neig):
    if CuCe["position"][0] > neig["position"][0]:
        CuCe['walls'].update({'left': False})
        neig['walls'].update({'right': False})
    elif CuCe["position"][0] < neig["position"][0]:
        CuCe['walls'].update({'right': False})
        neig['walls'].update({'left': False})
    elif CuCe["position"][1] > neig["position"][1]:
        CuCe['walls'].update({'top': False})
        neig['walls'].update({'bottom': False})
    elif CuCe["position"][1] < neig["position"][1]:
        CuCe['walls'].update({'bottom': False})
        neig['walls'].update({'top': False})
    print(CuCe)
    print(neig)

remove_wall(my_maze[0], my_maze[1])



def neighbors():#    X Axis↴             Y Axis↴
    positions = [[0, 1, 2, 3, 4,] , [0, 1, 2, 3, 4,] ] # index positions in X and Y
    path = [] # The path the algorithm have taken
    visitedPositons = [] 
    abPositions = [] # Abalible postions (abalible neighbors)
    X = random.choice(positions[0]) #random start point
    Y = random.choice(positions[1]) #random start point
    visitedPositons.append([X, Y])
    path.append([X, Y])
    while True:
        if(len(path) == 0): # End function
            print(" YOU REACH THE END.")
            print(path)
            return visitedPositons
        if (path[-1][0] in positions[0]) == True and (path[-1][1] in positions[1]) == True: #Check if the coordinates are correct 
            if (path[-1][0]-1 in positions[0]) == True: #Check if there is a neighbor to the of LEFT the current cell
                abPositions.append([path[-1][0]-1,path[-1][1]])
            
            if (path[-1][0]+1 in positions[0]) == True: #Check if there is a neighbor to the RIGHT of the current cell
                abPositions.append([path[-1][0]+1,path[-1][1]])
            
            if (path[-1][1]-1 in positions[1]) == True: #Check if there is a neighbor in TOP of the current cell
                abPositions.append([path[-1][0],path[-1][1]-1])
            
            if (path[-1][1]+1 in positions[1]) == True: #Check if there is a neighbor in BOTTOM of the current cell
                abPositions.append([path[-1][0],path[-1][1]+1])
            for x in visitedPositons: #Discart all the already visited positions from the current abalible neighbors list
                if x in abPositions:
                    abPositions.remove(x)
            if(len(abPositions) == 0): #If there is not any abalible neighbor go back (Backtracking)
                path.pop()
                abPositions.clear()
                continue
            if ((len(abPositions) == 0) == False): #If there is one or more abalible neighbors move to one randomly and beguin again.
                choice = random.choice(abPositions)
                X = choice[0]
                Y = choice[1]
                visitedPositons.append([X, Y])
                path.append([X, Y])
                abPositions.clear()
            print(visitedPositons)
        else:
            print('ERROR')

result = neighbors()

print("Total visited:", len(result))
print("Unique positions:", len(set(tuple(p) for p in result)))


'''
print("""
+---+---+---+---+---+
|   |   |   |   |   |
+---+---+---+---+---+
|   |   |   |   |   |
+---+---+---+---+---+
|   |   |   |   |   |
+---+---+---+---+---+
|   |   |   |   |   |
+---+---+---+---+---+
|   |   |   |   |   |
+---+---+---+---+---+
""")
'''