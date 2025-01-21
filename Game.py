import math
import random
import time
import os

SEED = 2022

def calculateSD(data, p, matches_call):
    sum_data = 0.0
    z = 0.1
    for i in range(int(p)):
        sum_data += data[i]
        if data[i] == 0.0:
            z += 1
    if matches_call == 0:
        z = 0
    mean = sum_data / (p - z)
    sd = 0.0
    for i in range(int(p)):
        if (data[i] != 0.0) or (matches_call == 1):
            sd += (data[i] - mean) ** 2
    if p - z == 0:
        return 0
    else:
        return math.sqrt(sd / (p - z))

def output(best_round, n, rounds, ppg, players, names):
    BUFSIZE = 10 * players
    buf = ''
    with open("GameFiles/out", "r") as infile, \
         open("GameFiles/best", "w") as best_output, \
         open("GameFiles/f2", "w") as f2_output:
        
        print(f"\nBest round = {best_round}\n")
        f2_output.write(f"{n}\n{rounds}\n{ppg}\n")
        c = 1
        for line in infile:
            if not line.strip().isnumeric():
                continue
            elif int(line.strip()) == best_round:
                for _ in range(rounds):
                    buf = infile.readline()
                    best_output.write(f"Round {c}\n")
                    best_output.write(buf)
                    #best_output.write(names[int(buf) - 1])
                    """for char in buf:
                        if char.isdigit():
                            #FLAG 
                            #for i2 in range(2):
                            #    best_output.write(names[int(char) - 1][i2])

                            best_output.write(names[int(char) - 1])
                            # END FLAG
                        else:
                            best_output.write(char)
                            """
                    f2_output.write(buf)
                    print(buf)
                    c += 1
                break

def is_sitting(val, mod, sitters):
    for i in range(int(mod)):
        if val == sitters[i]:
            return True
    return False

def findMax(players, x, C, ppg, sitters):
    highest = -999
    index = 0
    for i in range(players):
        if (x[i] > highest) and (C[i] == True) and (not is_sitting(i, players % ppg, sitters)):
            
            highest = x[i]
            index = i

    return index

def findMin(players, ppg, sitters, x, C):
    lowest = 9999
    index = 0
    for i in range(players):
        if (x[i] < lowest) and (C[i] == True) and (not is_sitting(i, players % ppg, sitters)):
            lowest = x[i]
            index = i

    return index

def game(players, rounds, TESTSIZE, ppg, names):
    random.seed(SEED)
    start = time.process_time()
    
    outFile = open("GameFiles/out", "w")
    print("Players: ",players, "Rounds: ",rounds, "TESTSIZE: ",TESTSIZE, "ppg: ",ppg, "Names: ",names)
    C = [False] * players
    sitting = (players % ppg != 0)
    HIT_MAX = False
    r1 = r2 = r3 = r4 = r5 = r6 = r7 = index = best_round = sit = w_count = 0
    best = [[0] * players for _ in range(players)]
    stdev = -1.0
    stdevs = [0] * players
    stdev_new = 0
    matches = [[0] * players for _ in range(players)]
    data = [0] * (players * players)
    dummy = [999] * 7
    sit_out_count = [0] * players
    sitters = [0] * (players % ppg)
    
    SIT_MAX = math.ceil((players % ppg) * rounds / players)
    
    if sitting:
        print("People have to sit out.\n")
    else:
        print("Nobody is sitting out.\n")
    
    #if players == ppg:
    #    TESTSIZE = players + 1
    
    for test_count in range(players + 1, TESTSIZE + 1):
        
        outFile.write(f"{test_count}")
        HIT_MAX = False
        
        # Clearing The Array
        for i in range(players):
            sit_out_count[i] = 0
            for j in range(players):
                matches[i][j] = 0
        
        # Running Simulation
        for j in range(rounds):
            for i in range(players):
                C[i] = True
            
            if sitting:
                count = 0
                while count < players % ppg:
                    if HIT_MAX:
                        sit_random = findMin(players, ppg, dummy, sit_out_count, C)
                        sitters[count] = sit_random
                        C[sit_random] = False
                        sit_out_count[sit_random] += 1
                        count += 1
                    else:
                        sit_random = random.randint(0, players - 1)
                        if (sit_out_count[sit_random] < SIT_MAX) and (C[sit_random] == True):
                            sitters[count] = sit_random
                            C[sit_random] = False
                            sit_out_count[sit_random] += 1
                            if sit_out_count[sit_random] == SIT_MAX:
                                HIT_MAX = True
                            count += 1
            else:
                sit = 9999
            
            outFile.write("\n")
            w_count = players
            for z in range(players):
               stdevs[z] = calculateSD(matches[z], float(players), 1)

            while w_count >= ppg:
                r1 = findMax(players, stdevs, C, ppg, sitters)
                C[r1] = False
                r2 = findMin(players, ppg, sitters, matches[r1], C)
                C[r2] = False
                if ppg > 2:
                    r3 = findMin(players, ppg, sitters, matches[r1], C)
                    C[r3] = False
                if ppg > 3:
                    r4 = findMin(players, ppg, sitters, matches[r1], C)
                    C[r4] = False
                if ppg > 4:
                    r5 = findMin(players, ppg, sitters, matches[r1], C)
                    C[r5] = False
                if ppg > 5:
                    r6 = findMin(players, ppg, sitters, matches[r1], C)
                    C[r6] = False
                if ppg > 6:
                    r7 = findMin(players, ppg, sitters, matches[r1], C)
                    C[r7] = False
                """
                if j > 0:
                    print("J\n")
                    if sitting and (w_count == players):
                        r1 = (j + 1) % players
                    else:
                        r1 = findMax(players, stdevs, C, ppg, sitters)
                    C[r1] = False
                    r2 = findMin(players, ppg, sitters, matches[r1], C)
                    C[r2] = False
                    if ppg > 2:
                        r3 = findMin(players, ppg, sitters, matches[r1], C)
                        C[r3] = False
                    if ppg > 3:
                        r4 = findMin(players, ppg, sitters, matches[r1], C)
                        C[r4] = False
                    if ppg > 4:
                        r5 = findMin(players, ppg, sitters, matches[r1], C)
                        C[r5] = False
                    if ppg > 5:
                        r6 = findMin(players, ppg, sitters, matches[r1], C)
                        C[r6] = False
                    if ppg > 6:
                        r7 = findMin(players, ppg, sitters, matches[r1], C)
                        C[r7] = False
                else:
                    print("ELSE\n")
                    r1 = 0 + (players - w_count)
                    if sitting: r1 += 1
                    C[r1] = False
                    r2 = 1 + (players - w_count)
                    if sitting: r2 += 1
                    C[r2] = False
                    if ppg > 2:
                        r3 = 2 + (players - w_count)
                        if sitting: r3 += 1
                        C[r3] = False
                    if ppg > 3:
                        r4 = 3 + (players - w_count)
                        if sitting: r4 += 1
                        C[r4] = False
                    if ppg > 4:
                        r5 = 4 + (players - w_count)
                        if sitting:
                            r5 += 1
                        C[r5] = False

                    if ppg > 5:
                        r6 = 5 + (players - w_count)
                        if sitting:
                            r6 += 1
                        C[r6] = False

                    if ppg > 6:
                        r7 = 6 + (players - w_count)
                        if sitting:
                            r7 += 1
                        C[r7] = False
                """
                outFile.write(f" {r1 + 1} vs {r2 + 1}")
                if ppg > 2:
                    outFile.write(f" vs {r3 + 1}")
                if ppg > 3:
                    outFile.write(f" vs {r4 + 1}")
                if ppg > 4:
                    outFile.write(f" vs {r5 + 1}")
                if ppg > 5:
                    outFile.write(f" vs {r6 + 1}")
                if ppg > 6:
                    outFile.write(f" vs {r7 + 1}")
                outFile.write(" -")

                matches[r2][r1] += 1
                matches[r1][r2] += 1
                w_count -= 2

                if ppg > 2:
                    matches[r3][r1] += 1
                    matches[r3][r2] += 1
                    matches[r1][r3] += 1
                    w_count -= 1

                if ppg > 3:
                    matches[r4][r1] += 1
                    matches[r4][r2] += 1
                    matches[r4][r3] += 1
                    matches[r1][r4] += 1
                    matches[r2][r4] += 1
                    matches[r3][r4] += 1
                    w_count -= 1

                if ppg > 4:
                    matches[r5][r1] += 1
                    matches[r5][r2] += 1
                    matches[r5][r3] += 1
                    matches[r5][r4] += 1
                    matches[r1][r5] += 1
                    matches[r2][r5] += 1
                    matches[r3][r5] += 1
                    matches[r4][r5] += 1
                    w_count -= 1

                if ppg > 5:
                    matches[r6][r1] += 1
                    matches[r6][r2] += 1
                    matches[r6][r3] += 1
                    matches[r6][r4] += 1
                    matches[r6][r5] += 1
                    matches[r1][r6] += 1
                    matches[r2][r6] += 1
                    matches[r3][r6] += 1
                    matches[r4][r6] += 1
                    matches[r5][r6] += 1
                    w_count -= 1

                if ppg > 6:
                    matches[r7][r1] += 1
                    matches[r7][r2] += 1
                    matches[r7][r3] += 1
                    matches[r7][r4] += 1
                    matches[r7][r5] += 1
                    matches[r7][r6] += 1
                    matches[r1][r7] += 1
                    matches[r2][r7] += 1
                    matches[r3][r7] += 1
                    matches[r4][r7] += 1
                    matches[r5][r7] += 1
                    matches[r6][r7] += 1
                    w_count -= 1

        for k in range(players):
            for k2 in range(players):
                data[index] = matches[k][k2]
                index += 1

        index = 0
        zero_count = 0
        for i in range(int(pow(players, 2))):
            if data[i] == 0.0:
                zero_count += 1

        if zero_count <= players or players >= rounds:
            stdev_new = calculateSD(data, float(pow(players, 2)), 0)

        if stdev_new < stdev or stdev == -1.0:
            stdev = stdev_new
            best_round = test_count
            for x in range(players):
                for y in range(players):
                    best[x][y] = matches[x][y]

        outFile.write(f"\n{test_count}\n")

    print("\n\n", end="")
    for x in range(players):
        print(f"\n{x + 1}:", end="")
        for y in range(players):
            print(f" {best[x][y]}", end="")

    output(best_round, players, rounds, ppg, players, names)
    """
    end = clock()
    cpu_time_used = (end - start) / CLOCKS_PER_SEC
    print(f"Time: {cpu_time_used:.3f} \n")
    """
    
    C = None

