#!/usr/bin/env python

import string
import sys

class COLORS:
    START = '\033[34m'
    GOAL = '\033[32m'
    PATH = '\033[33m'
    WALL = '\033[1m'
    ENDC = '\033[0m'
    
COORDS = "NSEW"

#this holds the text representation of the maze. It can work with the
#text to decide legal moves, where the goal position is, etc.
class MazeText():

###########################################################################
##  Maze Text Initialization
###########################################################################

    #initialize the maze
    def __init__(self, text=None, filename=None):
        self.startText = "A"
        self.goalText = "B"
        self.wallText = "#"
        self.solveText = "+"
    
        self.maze = []
        if filename is not None:
            textFile = open(filename)
            text = textFile.read()
            textFile.close()
            
        if text is None:
            raise Exception("No maze text or file")
            
        for line in text.splitlines():
            if (line[-1] == "\n"):
                self.maze.append(line[:-1])
            else:
                self.maze.append(line)
        
        self.height = 0
        self.width = 0
        self.moveTime = 0
        if (len(self.maze) > 0):
            self.height = len(self.maze)
            self.width = len(self.maze[0])
        
        self.start = (1, 1)
        self.goal = (self.width-2, self.height-2)
                
        self.checkStartGoalPosition()

    def checkMazeFormat(self):
        if self.wallText not in self.getText():
            raise Exception("Bad maze format")

    def checkStartGoalPosition(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.maze[i][j] == self.startText:
                    self.setStartPosition((j,i))
                if self.maze[i][j] == self.goalText:
                    self.setGoalPosition((j,i))

    #this sets a custom position for the start
    def setStartPosition(self, x_y):
        x, y = x_y
        if (self.validPosition((x, y)) and self.maze[y][x] != self.wallText):
            self.start = (x, y)

    #this sets a custom position for the end
    def setGoalPosition(self, x_y):
        x, y = x_y
        if (self.validPosition((x, y)) and self.maze[y][x] != self.wallText):
            self.goal = (x, y)
            
    def setWallText(self, wall):
        wall = str(wall)
        if (len(wall) == 1):
            self.wallText = wall
    
    def setPathText(self, path):
        path = str(path)
        if (len(path) == 1):
            self.pathText = path

    def setStartText(self, text):
        text = str(text)
        if (len(text) == 1):
            self.startText = text
            self.checkStartGoalPosition()

    def setGoalText(self, text):
        text = str(text)
        if (len(text) == 1):
            self.goalText = text
            self.checkStartGoalPosition()
    
###########################################################################
##  Maze Text Game Solving
###########################################################################

    #this gets the valid moves from a position
    def getValidMoves(self, x_y):
        x, y = x_y
        #the current position can't be on or outside boundary walls
        
        #note that height is downwards

        #because the left wall and top line are defined by
        #underscores, valid values begin at position (2, 2) and
        #run to (self.width-1, self.height-1)
        
        #note also that arrays and strings are 0 based, but self.width
        #and self.height are not
        if (not self.validPosition((x, y))):
            return []
        else:
            moves = [None,None,None,None]
            (current, N, S, E, W) = self.lookAround((x, y))
            #now that we've gotten the definitions all sewn up, do
            #position checks
            
            if (N != self.wallText):
                moves[0] = (x, y-1)
            if (S != self.wallText):
                moves[1] = (x, y+1)
            if (E != self.wallText):
                moves[2] = (x+1, y)
            if (W != self.wallText):
                moves[3] = (x-1, y)

            return moves

    #this gets all the characters in the area
    def lookAround(self, x_y):
        x, y = x_y
        #North: y+1, x
        #South: y-1, x
        #East:  y, x+1
        #West:  y, x-1
        
        #return in order South, East, West, North, because I'm
        #assuming the path will start in the top left corner and
        #go to the bottom right corner
        current = self.maze[y][x]
        N = self.wallText
        S = self.wallText
        E = self.wallText
        W = self.wallText
        if (self.validPosition((x,y-1))):
            N = self.maze[y-1][x]
        if (self.validPosition((x,y+1))):
            S = self.maze[y+1][x]
        if (self.validPosition((x+1,y))):
            E = self.maze[y][x+1]
        if (self.validPosition((x-1,y))):
            W = self.maze[y][x-1]

        return (current, N, S, E, W)
    
###########################################################################
##  Maze Text Helper and info functions
###########################################################################

    #this returns if the given position is a valid one
    def validPosition(self, x_y):
        x, y = x_y
        return (not (x >= self.width or y >= self.height or \
                     x < 0 or y < 0))

    #return if the position is the goal
    def isGoal(self, x_y):
        x, y = x_y
        return (x == self.goal[0] and y == self.goal[1])

    #return the position of the start
    def getStartPosition(self):
        return self.start

    #return the position of the goal
    def getGoalPosition(self):
        return self.goal

    #return a text representation of the maze
    def getText(self):
        return "\n".join(self.maze)

    def getMazeInfo(self):
        self.checkMazeFormat()
        return self.height, self.width, self.start, self.goal

    def normalize(lines):
        maze = []
        for i in range(len(lines)):
            line = lines[i].rstrip('\n')

            if i == 0:
                # if there is are Spaces in corners
                if line[0] == " ":
                    line = "#"+line[1:]
                if line[-1] == " ":
                    line = line[:-1]+"#"
                
                second_line = lines[1].rstrip('\n')
                diff = len(second_line)-len(line)
                if diff > 0:
                    line = line+"#"*(diff)

                # if there are other Spaces in line0, they are starting points
                if " " in line:
                    space_count = line.count(" ")
                    if space_count > 1 and " "*space_count in line:
                        line = line.replace(" "*space_count,"A"+"#"*space_count)
                    else:
                        raise Exception("too many spaces in line0")

                maze.append(line.replace("_","#").replace("|","#"))
                continue

            if i == len(lines)-1:
                maze.append(line.replace("_"," ").replace("|","#"))
                
                if " " in line:
                    space_count = line.count(" ")
                    if space_count > 1 and " "*space_count in line:
                        line = line.replace(" "*space_count,"B"+"#"*space_count)
                    else:
                        raise Exception("too many spaces in line"+len(lines))

                maze.append(line.replace("_","#").replace("|","#"))
                continue

            next_line = lines[i+1]
            for i in range(len(next_line)-1):
                c1 = next_line[i]
                c0 = line[i]
                if c1 == "|" and c0 == " ":
                    line = line[:i] + "_" + line[i+1:]

            maze.append(line.replace("_"," ").replace("|","#"))
            maze.append(line.replace("_","#").replace("|","#"))

        return maze

###########################################################################
##  Maze Text Heuristics
###########################################################################

    #return the manhattan distance to the goal
    def manHeuristic(self, x_y):
        x, y = x_y
        (goalX, goalY) = self.getGoalPosition()
        return abs(goalX - x) + abs(goalY - y)

    #return the euclidean heuristic the goal
    #I'm not sure this is useful given the manhattan heuristic, but
    #it's here because it could be and when it becomes useful it'll
    #already be here.
    def eucHeuristic(self, x_y):
        x, y = x_y
        import math
        (goalX, goalY) = self.getGoalPosition()
        return math.sqrt(math.pow((goalX - x), 2) + math.pow((goalY - y), 2))

###########################################################################
##  Maze Text Drawing
###########################################################################
    
    def drawPoint(self, x_y, text):
        x, y = x_y
        line = self.maze[y]
        line = list(line)
        if line[x] is self.wallText:
            raise Exception("Can't draw on a Wall")
        if line[x] is not self.goalText:
            line[x] = text
        line = ''.join(line)
        self.maze[y] = line
    
    def drawSolution(self, solution):
        for point in solution:
            self.drawPoint(point,self.solveText)

    def resetMaze(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.maze[i][j] == self.solveText:
                    self.drawPoint((j,i)," ")

    def drawMaze(self):
        self.checkMazeFormat()
        text = ""
        for i in range(self.height):
            for j in range(self.width):
                if self.maze[i][j] == self.solveText:
                    text += COLORS.PATH + self.solveText + COLORS.ENDC
                elif self.maze[i][j] == self.wallText:
                    text += COLORS.WALL + self.wallText + COLORS.ENDC
                elif self.maze[i][j] == self.startText:
                    text += COLORS.START + self.startText + COLORS.ENDC
                elif self.maze[i][j] == self.goalText:
                    text += COLORS.GOAL + self.goalText + COLORS.ENDC
                else:
                    text += " "
            text += "\n"
        print(text)

class MazeSolver():

###########################################################################
##  Program search functions
###########################################################################

    def __init__(self, maze):
        self.maze = maze

    def solve(self):
        # default solve with aStar
        return self.aStar()

    def aStar(self):
        if (self.maze == None):
            return

        self.maze.checkMazeFormat()

        import time, heapq

        self.maze.resetMaze()
        
        class Node:
            def __init__(self, _node, _cost, _hcost, _coord):
                self.path = []
                self.sequence = ""
                self.node = _node
                self.cost = _cost
                self.hcost = _hcost
                self.coord = COORDS[_coord]
                
            #this is for sorting
            def __lt__(self, other):
                if (self.hcost < other.hcost):
                    return True
                else:
                    return self.cost < other.cost

            
        dejavu = []
        start = self.maze.getStartPosition()

        global path, forward, back
        
        #if we're done, then we're done
        if (self.maze.isGoal(start)):
            return

        heuristic = self.maze.manHeuristic
        startNode = Node(start, 0, heuristic(start), -1)

        def solve(queue):
            while (len(queue) > 0):
                item = heapq.heappop(queue)
                if self.maze.isGoal(item.node):
                    return item.path, item.sequence
                else:
                    children = self.maze.getValidMoves(item.node)
                    for i in range(len(children)):
                        child = children[i]
                        if (child is not None and child not in dejavu):
                            if self.maze.isGoal(child):
                                return item.path + [child], item.sequence + COORDS[i]
                                
                            dejavu.append(child)
                            cost = item.cost + 1 #+1 because all steps cost 1
                            hcost = item.cost + heuristic(child)
                            node = Node(child, cost, hcost, i)
                            node.path = item.path + [child]
                            node.sequence = item.sequence + COORDS[i]
                            heapq.heappush(queue, node)
        
        try:
            solution, sequence = solve([startNode])
        except TypeError as e:
            solution = None

        if solution is None:
            raise Exception("No solution found")
        if (len(solution) > 0):
            self.maze.drawSolution(solution)
            return sequence

###########################################################################
##  Program file processing functions
###########################################################################

    def autoSolveMaze(text=None,filename=None):
        maze = MazeText(text=text,filename=filename)
        height, width, startPoint, goalPoint = maze.getMazeInfo()
        print("Maze - Size: {}x{}, Start at {}, Goal at {}".format(height, width, startPoint, goalPoint))
        maze.drawMaze()
        solver = MazeSolver(maze)
        sequence = solver.solve()
        print("Solved with sequence: {}".format(sequence))
        maze.drawMaze()


class MazeConvert():
    def convert(filename=None,lines=None):
        if filename:
            if filename[-4:] == ".lay":
                maze_file = open(filename, "r")
                lines = maze_file.readlines()
                maze_file.close()
        if lines:
            normalized_maze = MazeText.normalize(lines)
            normalized_maze = '\n'.join(normalized_maze)
            return normalized_maze
        return None


if __name__ == "__main__":
    del sys.argv[0]
    for mazeFile in sys.argv:
        MazeSolver.autoSolveMaze(filename=mazeFile)
        
