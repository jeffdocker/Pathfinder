from queue import PriorityQueue
import math
import time

times = []
lengths = []
expanded = []
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

    for a in range(0, 5):
        for b in range(0, 10):
            file = open("map" + str(a) + "_" + str(b) + ".txt", "r")
            s_start = eval(file.readline())
            s_goal = eval(file.readline())
            for i in range(0, 8):
                file.readline()
            Map = [[None for l in range(160)] for m in range(120)]
            for row in range(0, 120):
                line = file.readline()
                for col in range(0, 160):
                    Map[row][col] = cell(col, row, line[col])
            print("map" + str(a) + "_" + str(b) + ".txt")
            print("========================================================================")
            Map_uniform = [[None for p in range(160)] for q in range(120)]
            for row in range(0, 120):
                for col in range(0, 160):
                    Map_uniform[row][col] = cell(col,row,Map[row][col].type)
            print("uniform:")
            a_star(Map_uniform, 0, 0, s_start, s_goal)

            for x in range(0, 5):
                Map_A = [[None for r in range(160)] for s in range(120)]
                for row in range(0, 120):
                    for col in range(0, 160):
                        Map_A[row][col] = cell(col,row,Map[row][col].type)
                print("A* heuristic " + str(x) + ":")
                a_star(Map_A, x, 1, s_start, s_goal)

            for y in range(0, 5):
                Map_W_125 = [[None for t in range(160)] for u in range(120)]
                for row in range(0, 120):
                    for col in range(0, 160):
                        Map_W_125[row][col] = cell(col,row,Map[row][col].type)
                print("Weighted A* heuristic " + str(y) + " weight 1.25:")
                a_star(Map_W_125, y, 1.25, s_start, s_goal)

            for z in range(0, 5):
                Map_W_2 = [[None for f in range(160)] for g in range(120)]
                for row in range(0, 120):
                    for col in range(0, 160):
                        Map_W_2[row][col] = cell(col,row,Map[row][col].type)
                print("Weighted A* heuristic " + str(z) + " weight 2:")
                a_star(Map_W_2, z, 2, s_start, s_goal)
            print("========================================================================")

    time_sum = 0
    for t in times:
        time_sum += t
    print("time avg: " + str(time_sum / 800))

    length_sum = 0
    for l in lengths:
        length_sum += l
    print("length avg: " + str(length_sum / 800))

    expanded_sum = 0
    for e in expanded:
        expanded_sum += e
    print("expanded avg: " + str(expanded_sum / 800))

def a_star(Map, h_func, weight, sstart, sgoal):

    for row in range(0,120):
        for col in range(0,160):
            (Map[row][col]).h = h(col,row,sgoal[0],sgoal[1],h_func)

    sstart = Map[sstart[1]][sstart[0]]
    sgoal = Map[sgoal[1]][sgoal[0]]


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


    runtime = time.time()-start_time
    print("runtime: "+str(runtime),end=',')
    path_length = 0
    current = sgoal
    while current.parent != None:
        current = current.parent
        path_length+=1
    print("path length: "+str(path_length),end=",")
    print("path cost: "+str(sgoal.g),end=",")
    print("cells expanded: "+str(cells_expanded))
    times.append(runtime)
    lengths.append(path_length)
    expanded.append(cells_expanded)




# heuristic function
def h(curr_x, curr_y, goal_x, goal_y, h_func):
    # manhattan distance
    if h_func == 0:
        manhattan_distance = 0.25 * (abs(goal_x - curr_x) + abs(goal_y - curr_y))
        return manhattan_distance

    # euclidean distance
    elif h_func == 1:
        euclidean_distance = float(
            math.sqrt(((curr_x - goal_x) * (curr_x - goal_x)) + ((curr_y - goal_y) * (curr_y - goal_y))))

        return euclidean_distance

    # euclidean distance squared
    elif h_func == 2:
        euclidean_sqr = float((((curr_x - goal_x) * (curr_x - goal_x)) + ((curr_y - goal_y) * (curr_y - goal_y))))

        return euclidean_sqr

    # diagonal distance
    elif h_func == 3:
        dist = (abs(abs(curr_x - goal_x) - abs(curr_y - goal_y)))

        if abs(curr_x - goal_x) > abs(curr_y - goal_y):
            diagDist = float(math.sqrt(2) * abs(curr_y - goal_y))
        else:
            diagDist = float(math.sqrt(2) * abs(curr_x - goal_x))

        diagonal_distance = float(0.25 * (diagDist + dist))

        return diagonal_distance

    # chebyshev distance
    elif h_func == 4:
        straight = (abs(curr_x - goal_x) + abs(curr_y - goal_y))

        if abs(curr_x - goal_x) > abs(curr_y - goal_y):
            diag = abs(curr_y - goal_y)
        else:
            diag = abs(curr_x - goal_x)

        chebyshev_distance = float(0.25 * (straight - diag))

        return chebyshev_distance


def update(curr_cell, neighbor_cell, r, c, fringe, fringe_set, weight):
    # cost from current cell to neighbor cell
    cost_of_move = cost(curr_cell, neighbor_cell, r, c)

    # if neighbor cell is blocked, skip
    if cost_of_move == float("inf"):
        return

    # update neighbor cell and add to finge
    if curr_cell.g + cost_of_move < neighbor_cell.g:
        neighbor_cell.g = curr_cell.g + cost_of_move
        neighbor_cell.parent = curr_cell

        # if already in fringe, take it out
        if neighbor_cell in fringe_set:

            # remove from fringe set, reset fringe, add everything from fringe set back in
            fringe_set.remove(neighbor_cell)
            fringe = PriorityQueue()
            for x in fringe_set:
                fringe.put(x)

        # update f, put back into fringe and fringe set
        neighbor_cell.f = neighbor_cell.g + weight * neighbor_cell.h
        fringe.put(neighbor_cell)
        fringe_set.add(neighbor_cell)


def cost(curr_cell, neighbor_cell, r, c):
    if r == 0 or c == 0:

        return (curr_cell.type_val + neighbor_cell.type_val) / 2

    else:

        return (math.sqrt(2 * math.pow(curr_cell.type_val, 2)) + math.sqrt(2 * math.pow(neighbor_cell.type_val, 2))) / 2



if __name__ == '__main__':
    main()