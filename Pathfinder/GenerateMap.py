import random
import time
import math

def main():

    for mapnum in range(0,5):
        # initialize map with all 1s
        random.seed(time.time())
        Map = [['1' for x in range(160)] for y in range(120)]

        # generate hard to traverse regions and store their center points
        hard_to_traverse = [(-1, -1) for x in range(8)]
        for hard_to_traverse_position in range(0, 8):
            x = -1
            y = -1

            # dont pick the same point twice
            while (x, y) in hard_to_traverse:
                x = random.randint(0, 159)
                y = random.randint(0, 119)

            hard_to_traverse[hard_to_traverse_position] = (x, y)

            # populate surrounding 31x31 with 2s, with a 50% probability
            col = x - 16
            row = y - 16
            for j in range(0, 31):
                for l in range(0, 31):
                    if (col + l <= 159 and col + l >= 0) and (row + j <= 119 and row + j >= 0):
                        r = random.randint(1, 2)
                        if r == 1:
                            Map[j + row][l + col] = '2'

        # copy of map to generate rivers on
        river_copy = [['1' for x in range(160)] for y in range(120)]
        for i in range(0, 120):
            for j in range(0, 160):
                river_copy[i][j] = Map[i][j]

        # generate 4 rivers
        river_counter = 0
        while river_counter < 5:

            #start position for the river
            river_start_pos = [(0, random.randint(0, 159)), (119, random.randint(0, 159)), (random.randint(0, 119), 0),
                               (random.randint(0, 119), 159)]
            river_start_pos = random.choice(river_start_pos)
            pos_counter = 0
            river_fail = False
            row_direction = -1
            col_direction = -1
            #river direction from start
            if river_start_pos[0] == 0:
                row_direction = 1
                col_direction = 0
            elif river_start_pos[0] == 119:
                row_direction = -1
                col_direction = 0
            elif river_start_pos[1] == 0:
                row_direction = 0
                col_direction = 1
            elif river_start_pos[1] == 159:
                row_direction = 0
                col_direction = -1

            #go through possible turns until 100 positions
            river_turns = 0
            while river_turns < 5:

                #failed river construction, restart
                if river_fail is True:
                    river_counter = 0
                    river_copy = [['1' for x in range(160)] for y in range(120)]
                    for i in range(0, 120):
                        for j in range(0, 160):
                            river_copy[i][j] = Map[i][j]
                    break

                for move in range(0, 20):

                    move_row = river_start_pos[0] + move * row_direction
                    move_col = river_start_pos[1] + move * col_direction

                    #at border, <100 filled
                    if ((move_row <= 0 or move_row >= 119) or (
                            move_col <= 0 or move_col >= 159)) and pos_counter < 100 and move != 0:
                        river_fail = True
                        river_turns = 0
                        break
                    #intersection occurs
                    if river_copy[move_row][move_col] == 'a' or river_copy[move_row][move_col] == 'b':
                        river_fail = True
                        river_turns = 0
                        break

                    if river_copy[move_row][move_col] == '1':
                        river_copy[move_row][move_col] = 'a'
                    else:
                        river_copy[move_row][move_col] = 'b'

                river_start_pos = (river_start_pos[0] + 20 * row_direction, river_start_pos[1] + 20 * col_direction)
                pos_counter += 1

                #20% change of a turn
                turn = random.randint(1, 10)
                if turn <= 2:
                    turn_direction = random.randint(1, 2)
                    if turn_direction == 1 and col_direction == 0:
                        row_direction = 0
                        col_direction = 1
                    elif turn_direction == 1 and row_direction == 0:
                        row_direction = 1
                        col_direction = 0
                    elif turn_direction == 2 and col_direction == 0:
                        row_direction = 0
                        col_direction = -1
                    elif turn_direction == 2 and row_direction == 0:
                        row_direction = -1
                        col_direction = 0
                river_turns += 1

            river_counter += 1

        #copy back into map
        for i in range(0, 120):
            for j in range(0, 160):
                Map[i][j] = river_copy[i][j]

        #set blocked cells
        blocked_cells = [(-1, -1) for x in range(3840)]
        for blocked_position in range(0, 3840):
            x = -1
            y = -1
            # dont pick the same point twice
            while (x, y) in blocked_cells:
                x = random.randint(0, 159)
                y = random.randint(0, 119)
                if Map[y][x] == 'a' or Map[y][x] == 'b':
                    x = -1
                    y = -1
            blocked_cells[blocked_position] = (x, y)
            Map[y][x] = '0'

        #generate start and goal cells
        start_cells = [(-1, -1) for x in range(10)]
        goal_cells = [(-1, -1) for x in range(10)]

        for start_goal_positions in range(0, 10):

            while True:
                possible_positions = [(random.randint(0, 159), random.randint(0, 19)),
                                      (random.randint(0, 159), random.randint(100, 119)),
                                      (random.randint(0, 19), random.randint(0, 119)),
                                      (random.randint(140, 159), random.randint(0, 119))]
                start = random.choice(possible_positions)
                possible_positions = [(random.randint(0, 159), random.randint(0, 19)),
                                      (random.randint(0, 159), random.randint(100, 119)),
                                      (random.randint(0, 19), random.randint(0, 119)),
                                      (random.randint(140, 159), random.randint(0, 119))]
                goal = random.choice(possible_positions)

                if Map[start[1]][start[0]] == '0' or Map[goal[1]][goal[0]] == '0':
                    continue
                distance = math.sqrt(math.pow(goal[1] - start[1], 2) + math.pow(goal[0] - start[0], 2))
                if distance < 100:
                    continue

                if start in start_cells or goal in goal_cells:
                    continue
                start_cells[start_goal_positions] = (start[0], start[1])
                goal_cells[start_goal_positions] = (goal[0], goal[1])
                break

        for filenum in range(0, 10):
            filestring = "map"+str(mapnum)+"_"+str(filenum)+".txt"
            file = open(filestring,'w+')
            file.write(str((start_cells[filenum])[0])+", "+str((start_cells[filenum])[1]))
            file.write('\n')
            file.write(str((goal_cells[filenum])[0])+", "+str((goal_cells[filenum])[1]))
            file.write('\n')
            for x in range(0,8):
                file.write(str((hard_to_traverse[x])[0])+", "+str((hard_to_traverse[x])[1]))
                file.write('\n')
            mapstring = ""
            for i in range(0, 120):
                for j in range(0, 160):
                    mapstring += Map[i][j]
                mapstring += '\n'
            file.write(mapstring)
            file.close()



if __name__ == '__main__':
    main()