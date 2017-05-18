#!/usr/bin/env python3

import inspect
import logging
import os
import sys
import unittest
import glob

from MazeRunner import MazeText, MazeSolver, MazeConvert

class UpdateTest(unittest.TestCase):

    def testCustomMazes(self):
        mazes = []
        
        maze = MazeText(filename="tests/custom1.nlay")
        maze.setPathText(".")
        mazes.append(maze)

        maze = MazeText(filename="tests/custom2.nlay")
        maze.setPathText(".")
        mazes.append(maze)
        
        maze = MazeText(filename="tests/custom3.nlay")
        maze.setPathText(".")
        mazes.append(maze)

        maze = MazeText(filename="tests/custom4.nlay")
        maze.setPathText(".")
        maze.setStartText("@")
        maze.setGoalText("*")
        mazes.append(maze)

        maze = MazeText(filename="tests/custom5.nlay")
        maze.setStartText("X")
        maze.setGoalText("O")
        mazes.append(maze)

        for m in mazes:
            height, width, startPoint, goalPoint = m.getMazeInfo()
            print("Maze - Size: {}x{}, Start at {}, Goal at {}".format(height, width, startPoint, goalPoint))
            solver = MazeSolver(m)
            sequence = solver.solve()
            print("Solved with sequence: {}".format(sequence))
            m.drawMaze()
        
    def testMazeFromText(self):
        with open("tests/tiny.nlay",'r') as f:
            maze = MazeText(text=f.read())
            height, width, startPoint, goalPoint = maze.getMazeInfo()
            print("Maze - Size: {}x{}, Start at {}, Goal at {}".format(height, width, startPoint, goalPoint))
            solver = MazeSolver(maze)
            sequence = solver.solve()
            print("Solved with sequence: {}".format(sequence))
            maze.drawMaze()

    def testConversion(self):
        # converting
        for mazeFile in glob.glob("tests/*.lay"):
            m = MazeConvert.convert(mazeFile)
            with open(mazeFile[:-4]+"_e.nlay",'w') as f:
                f.write(m)

        # solving
        for mazeFile in glob.glob("tests/*_e.nlay"):
            maze = MazeText(filename=mazeFile)
            height, width, startPoint, goalPoint = maze.getMazeInfo()
            print("Maze {} - Size: {}x{}, Start at {}, Goal at {}".format(mazeFile, height, width, startPoint, goalPoint))
            solver = MazeSolver(maze)
            sequence = solver.solve()
            print("Solved with sequence: {}".format(sequence))
            maze.drawMaze()
            # clean converted mazeFile
            os.remove(mazeFile)


if __name__ == "__main__":
    newSuite = unittest.TestSuite()
    newSuite.addTest(unittest.makeSuite(UpdateTest))
    unittest.main()