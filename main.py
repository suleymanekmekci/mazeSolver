import sys,copy
maze, mazehealth, healthTime,outputName = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
defaultMaze = []

with open(maze,"r") as mazeFile:
    for line in mazeFile:
        mazeRow = [element for element in line.strip("\n")]
        defaultMaze.append(mazeRow)
    mazeFile.close()

secondMaze = copy.deepcopy(defaultMaze)
outputFile = open(outputName,"w")
outputFile.close()

def findPoint(defaultMaze,startPoints = False):
    startPoint = []
    healthPoints = []
    for row in defaultMaze:
        for letter in row:
            a = defaultMaze.index(row)
            b = row.index(letter)
            if letter == "S":
                startPoint.append(a)
                startPoint.append(b)
            elif letter == "H":
                healthPoints.append([a,b])
    if startPoints:
        return startPoint
    else:
        return healthPoints
startPoint = findPoint(defaultMaze,startPoints=True)
def move(a,b,healthTime,finishGame = False):
    global defaultMaze

    if defaultMaze[a][b] == "S" or defaultMaze[a][b] == "F" :
        pass
    else:
        defaultMaze[a][b] = "1"

    if healthTime >= 0 and defaultMaze[a][b] == "F":
        finishGame = True

    elif healthTime <= 0 and defaultMaze[a][b] != "F":
        print("Maze cannot be solved")
        finishGame = True

    
    if finishGame:
        
        for outputRow in defaultMaze:
            for outputElement in outputRow:
                if outputElement == "W" or outputElement == "P":
                    a = defaultMaze.index(outputRow)
                    b = outputRow.index(outputElement)
                    defaultMaze[a][b] = "0"
        if healthPoints:
            for healths in healthPoints:
                x, y = healths[0],healths[1]
                defaultMaze[x][y] = "H"
        with open(outputName,"a+") as outputFile:
            for rw in defaultMaze:
                outputFile.write(", ".join(rw))
                outputFile.write("\n")
            outputFile.write("\n")
            outputFile.close()
                       
        
    else:
        pathsAndWalls = {}
        walls = []
        paths = []
        healths = []
        finish = []
        try:
            if a-1 < 0:
                raise IndexError
            elif defaultMaze[a-1][b] == "W":
                walls.append([a-1,b])
            elif defaultMaze[a-1][b] == "P":
                paths.append([a-1,b])
            elif defaultMaze[a-1][b] == "H":
                healths.append([a-1,b])
            if defaultMaze[a-1][b] == "F":
                finish.append([a-1,b])
        except IndexError:
            walls.append([a-1,b])
        try:
            if b-1 < 0:
                raise IndexError
            elif defaultMaze[a][b-1] == "W":
                walls.append([a,b-1])
            elif defaultMaze[a][b-1] == "P":
                paths.append([a,b-1])
            elif defaultMaze[a][b-1] == "H":
                healths.append([a,b-1])
            if defaultMaze[a][b-1] == "F":
                finish.append([a,b-1])
        except IndexError:
            walls.append([a,b-1])
        try:
            
            if defaultMaze[a][b+1] == "W":
                walls.append([a,b+1])
            elif defaultMaze[a][b+1] == "P":
                paths.append([a,b+1])
            elif defaultMaze[a][b+1] == "H":
                healths.append([a,b+1])
            if defaultMaze[a][b+1] == "F":
                finish.append([a,b+1])
        except IndexError:
            walls.append([a,b+1])
        try:
            if defaultMaze[a+1][b] == "W":
                walls.append([a+1,b])
            elif defaultMaze[a+1][b] == "P":
                paths.append([a+1,b])
            elif defaultMaze[a+1][b] == "H":
                healths.append([a+1,b])
            if defaultMaze[a+1][b] == "F":
                finish.append([a+1,b])
        except IndexError:
            walls.append([a+1,b])
        
        pathsAndWalls["W"] = walls
        pathsAndWalls["P"] = paths
        pathsAndWalls["F"] = finish
        pathsAndWalls["H"] = healths
        
        if pathsAndWalls["H"]:
            x, y = pathsAndWalls["H"][0][0],pathsAndWalls["H"][0][1]
            healthTime = mainHealth
            return move(x,y,healthTime)

        elif not pathsAndWalls["P"] and not pathsAndWalls["F"]:
            secondMaze[a][b] = "W"
            defaultMaze = copy.deepcopy(secondMaze)
            healthTime = mainHealth
            return move(startPoint[-2],startPoint[-1],healthTime)


        elif len(pathsAndWalls["P"]) == 1:
            x, y =pathsAndWalls["P"][0][0],pathsAndWalls["P"][0][1]
            healthTime -= 1
            return move(x,y,healthTime)
        
        elif pathsAndWalls["F"]:
            x, y= pathsAndWalls["F"][0][0],pathsAndWalls["F"][0][1]
            healthTime -= 1
            return move(x,y,healthTime,finishGame = True)
        
        elif len(pathsAndWalls["P"]) > 1:
            healthPoints2 = findPoint(defaultMaze)
            if healthPoints2:
                ranges = []
                
                for coordinates in healthPoints2:                    
                    c, d = coordinates[0],coordinates[1]

                    for option in pathsAndWalls["P"]:
                        distance = abs(option[0] - c) + abs(option[1] - d)
                        ranges.append(distance)
                
                if len(pathsAndWalls["P"]) == 2:

                    ind = ranges.index(min(ranges))

                    if ind % 2 == 0:
                        x, y = pathsAndWalls["P"][0][0], pathsAndWalls["P"][0][1]
                        healthTime -= 1
                        return move(x,y,healthTime)
                    elif ind % 2 != 0:
                        x, y = pathsAndWalls["P"][1][0], pathsAndWalls["P"][1][1]
                        healthTime -= 1
                        return move(x,y,healthTime)
                        
                elif len(pathsAndWalls["P"]) == 3:
                   
                    ind = ranges.index(min(ranges))
                    
                    if ind % 3 == 0:
                        x, y = pathsAndWalls["P"][0][0], pathsAndWalls["P"][0][1]
                        healthTime -= 1
                        return move(x,y,healthTime)

                    elif ind % 3 == 1:
                        x, y = pathsAndWalls["P"][1][0], pathsAndWalls["P"][1][1]
                        healthTime -= 1
                        return move(x,y,healthTime)
                    
                    elif ind % 3 == 2:
                        x, y = pathsAndWalls["P"][2][0], pathsAndWalls["P"][2][1]
                        healthTime -= 1
                        return move(x,y,healthTime)
            else:
                
                x, y = pathsAndWalls["P"][0][0], pathsAndWalls["P"][0][1]
                healthTime -= 1
                return move(x,y,healthTime)
        
healthPoints = []
mainHealth = 50000
move(startPoint[-2],startPoint[-1],50000)

with open(mazehealth,"r") as mazeFile:
    defaultMaze.clear()
    secondMaze.clear()
    for line in mazeFile:
        mazeRow = [element for element in line.strip("\n")]
        defaultMaze.append(mazeRow)
    mazeFile.close()

secondMaze = copy.deepcopy(defaultMaze)
healthPoints = findPoint(defaultMaze)
startPoint = findPoint(secondMaze,startPoints=True)

mainHealth = healthTime
move(startPoint[-2],startPoint[-1],healthTime)
