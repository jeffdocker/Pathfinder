from queue import PriorityQueue

# uncomment for colored map
from colorama import Fore
from colorama import Style

import math
import time



#cell object
class cell:
    def __init__(self, x_coordinate, y_coordinate, type):
        self.position = (x_coordinate,y_coordinate) #position of cell
        self.type = type #'1','2','a','b', or '0'
        self.type_val = float("inf")
        #typeval used to calculate cost of paths
        if type == '1':
            self.type_val = 1
        elif type == '2':
            self.type_val = 2
        elif type == 'a':
            self.type_val = 0.25
        elif type == 'b':
            self.type_val = 0.5
        #parent
        self.parent = None
        self.g = float("inf")
        self.h = float("inf")
        self.f = float("inf")

    def __lt__(self, other):
        return self.f < other.f

def main():

    #open file, read first 2 lines as start and goal
    file = input("File Name:")
    file = open(str(file),"r")
    sstart = eval(file.readline())
    sgoal = eval(file.readline())
    #skip lines for the hard to traverse regions
    for i in range(0,8):
        file.readline()

    #ask for user generated start and goal
    rand_pos = input("Random start/goal? [y/n]:")
    if(rand_pos=="n"):
        input_start = input("Enter Start [x, y]:")
        sstart = eval(input_start)
        input_goal = input("Enter Goal [x, y]:")
        sgoal = eval(input_goal)

    #ask for weight for heuristic.
    #If 0, f = g (uniform search)
    #If 1, f = g + h (A*)
    #If w, f = g + w*h (weighted A*)
    weight = input("Weight (0 if uniform, 1 if unweighted):")
    weight = float(weight)

    #select heuristic (add more later)
    print("0 = manhattan ")
    print("1 = euclidean ")
    print("2 = euclidean squared ")
    print("3 = diagonal ")
    print("4 = chebyshev ")
    h_func = input("Enter Heuristic Number: ")
    h_func = int(h_func)

    #grid of cell objects
    Map = [[None for x in range(160)] for y in range(120)]

    #populating grid from file + calculating heuristic for each
    for row in range(0,120):
        line = file.readline()
        for col in range(0,160):
            Map[row][col] = cell(col,row,line[col])
            (Map[row][col]).h = h(col,row,sgoal[0],sgoal[1],h_func)


    #setting goal and start cells
    sstart = Map[sstart[1]][sstart[0]]
    sgoal = Map[sgoal[1]][sgoal[0]]

    #flag for valid path from sstart to sgoal
    path_found = False

    #initialize start cell, fringe, set to keep track of what is in fringe, and closed set
    sstart.g = 0
    sstart.f = sstart.g + weight*sstart.h
    sstart.parent = None
    fringe = PriorityQueue()
    fringe_set = set()
    fringe.put(sstart)
    fringe_set.add(sstart)
    closed = set()

    cells_expanded = 0
    start_time = time.time()
    #keep taking from fringe
    while(fringe.empty() is False):

        #take cell with minimal f value out of fringe
        s = fringe.get()
        fringe_set.remove(s)

        #if we take goal cell out, done
        if s.position[0] == sgoal.position[0] and s.position[1] == sgoal.position[1]:
            path_found = True
            break
        #add taken cell from fringe into closed set
        closed.add(s)

        cells_expanded+=1

        #itterate over 8 neighbor cells of cell that was taken out
        for r in range(-1,2):
            for c in range(-1,2):
                #bounds check
                if (s.position)[0]+c<=159 and (s.position)[0]+c>=0 and (s.position)[1]+r<=119 and (s.position)[1]+r>=0:
                    #neighbor cell sp
                    sp = Map[(s.position)[1]+r][(s.position)[0]+c]
                    if sp not in closed:
                        #if neighbor cell not yet expanded, update its f value if needed and add to fringe
                        update(s,sp,r,c,fringe,fringe_set,weight)


    print("Time: "+str((time.time() - start_time))+" seconds")
    if path_found:
        print("Path Found")
    else:
        print("Path Not Found")


    #collect verticies in the path
    path_length = 0
    path  = set()
    current = sgoal
    while current.parent != None:
        path.add(current)
        current = current.parent
        path_length+=1

    print("Path Length: " + str(path_length))
    print("Path Cost: " + str(sgoal.g))
    print("Cells Expanded: "+ str(cells_expanded))

    #uncomment for colored map
    for row in range(0,120):
        for col in range(0,160):
            if Map[row][col] == sstart or Map[row][col] == sgoal:
                print(f"{Fore.MAGENTA}"+Map[row][col].type+f"{Style.RESET_ALL}",end='')
            elif Map[row][col] in path:
                print(f"{Fore.LIGHTRED_EX}"+Map[row][col].type+f"{Style.RESET_ALL}",end='')
            elif Map[row][col].g != float("inf"):
                print(f"{Fore.CYAN}"+Map[row][col].type+f"{Style.RESET_ALL}",end='')
            elif Map[row][col].type == '1':
                print(f"{Fore.LIGHTGREEN_EX}" + Map[row][col].type + f"{Style.RESET_ALL}", end='')
            elif Map[row][col].type == '2':
                print(f"{Fore.GREEN}" + Map[row][col].type + f"{Style.RESET_ALL}", end='')
            elif Map[row][col].type == 'a':
                print(f"{Fore.BLUE}" + Map[row][col].type + f"{Style.RESET_ALL}", end='')
            elif Map[row][col].type == 'b':
                print(f"{Fore.LIGHTBLUE_EX}" + Map[row][col].type + f"{Style.RESET_ALL}", end='')
            elif Map[row][col].type == '0':
                print(f"{Fore.BLACK}" + Map[row][col].type + f"{Style.RESET_ALL}", end='')
        print("")

    # print map
    # # comment for colored map
    # for row in range(0,120):
    #     for col in range(0,160):
    #         if Map[row][col] in path:
    #             print("X",end='')
    #         else:
    #             print(Map[row][col].type,end='')
    #     print("")

    print("Get values for specific cells using [f, g, or h] [x coordinate] [y coordinate]")
    while True:
        command = input("Command:")
        command = command.split()

        if command[0] == "f":

            print("f value at ("+command[1]+","+command[2]+") = "+str((Map[int(command[2])][int(command[1])]).f))

        elif command[0] == "g":

            print("g value at ("+command[1]+","+command[2]+") = "+str((Map[int(command[2])][int(command[1])]).g))

        elif command[0] == "h":

            print("h value at ("+command[1]+","+command[2]+") = "+str((Map[int(command[2])][int(command[1])]).h))

#heuristic function
def h(curr_x, curr_y, goal_x, goal_y, h_func):

#manhattan distance
    if h_func == 0:
        manhattan_distance = 0.25 * (abs(goal_x - curr_x) + abs(goal_y - curr_y))
        return manhattan_distance
        
#euclidean distance
    elif h_func == 1:
        euclidean_distance =  float(math.sqrt(((curr_x - goal_x) * (curr_x - goal_x)) + ((curr_y - goal_y) *(curr_y - goal_y))))

        return euclidean_distance

#euclidean distance squared
    elif h_func == 2:
        euclidean_sqr = float((((curr_x - goal_x) * (curr_x - goal_x)) + ( (curr_y - goal_y) *(curr_y - goal_y))))

        return euclidean_sqr

#diagonal distance
    elif h_func == 3:
        dist = (abs(abs(curr_x - goal_x) - abs(curr_y - goal_y)))

        if abs(curr_x - goal_x) > abs(curr_y - goal_y):
            diagDist = float(math.sqrt(2)*abs(curr_y - goal_y))
        else:
            diagDist = float(math.sqrt(2)*abs(curr_x - goal_x))

        diagonal_distance = float(0.25*(diagDist + dist))

        return diagonal_distance

#chebyshev distance
    elif h_func == 4:
        straight = (abs(curr_x - goal_x) + abs(curr_y - goal_y))

        if abs(curr_x - goal_x) > abs(curr_y - goal_y):
            diag = abs(curr_y - goal_y)
        else:
            diag = abs(curr_x - goal_x)

        chebyshev_distance = float(0.25*(straight - diag))

        return chebyshev_distance

def update(curr_cell, neighbor_cell, r, c, fringe, fringe_set, weight):

    #cost from current cell to neighbor cell
    cost_of_move = cost(curr_cell, neighbor_cell, r, c)

    #if neighbor cell is blocked, skip
    if cost_of_move == float("inf"):
        return

    #update neighbor cell and add to finge
    if curr_cell.g + cost_of_move < neighbor_cell.g:
        neighbor_cell.g = curr_cell.g + cost_of_move
        neighbor_cell.parent = curr_cell

        #if already in fringe, take it out
        if neighbor_cell in fringe_set:

            #remove from fringe set, reset fringe, add everything from fringe set back in
            fringe_set.remove(neighbor_cell)
            fringe = PriorityQueue()
            for x in fringe_set:
                fringe.put(x)

        #update f, put back into fringe and fringe set
        neighbor_cell.f = neighbor_cell.g + weight*neighbor_cell.h
        fringe.put(neighbor_cell)
        fringe_set.add(neighbor_cell)


def cost(curr_cell, neighbor_cell, r, c):

    if r == 0 or c == 0:

        return (curr_cell.type_val+neighbor_cell.type_val)/2

    else:

        return (math.sqrt(2*math.pow(curr_cell.type_val,2))+math.sqrt(2*math.pow(neighbor_cell.type_val,2)))/2


if __name__ == '__main__':
    main()