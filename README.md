# pyMazeRunner

*This project is heavily based on https://github.com/asinck/Ascii-Art-Maze-Solver*

## Maze Solver

This takes an ascii art maze as input, and solves it.

Instead of [Ascii-Art-Maze-Solver](https://github.com/asinck/Ascii-Art-Maze-Solver) this project:
 - doesn't have a GUI
 - it's lightweight, fast and CLI-friendly
 - can be used as a library
 - use a 1-char format
 - returns a string of coordinates as a solution
 - can convert a non-1-char maze to 1-char maze (to a certain degree)

## Usage

If your maze is already in the default format (wall = `#`, path = ` `, start = `A`, goal = `B`) you can simply run:

`python3 MazeRunner.py <mazefile>`

Otherwise you need to write a simple python3 script to set those parameters like:

```python
from MazeRunner import MazeText, MazeSolver

maze = MazeText(filename="maze.lay")
maze.setPathText(".")
maze.setStartText("@")
maze.setGoalText("*")
maze.setWallText("+")
MazeSolver(maze).solve()
maze.drawMaze()
```

For more example see the [tests.py]() file

## 1-char format

Every wall and path in the maze must take up exactly 1-char.  
In a non-1-char maze, one char is used as a wall and a path at the same time.

Example for non-1-char format compatible maze (note the `_` char)

```
 _____
|A   _|
| |_|B|
|_____|
```

Same maze above as a 1-char format maze

```
#######
#A    #
# # ###
# # #B#
# ### #
#     #
#######
```

## Search Algorithm

There are currently four search algorithms inplemented:
* A*, which expands the search node with the minimum path cost + heuristic estimate.

### A*

A UCS (Uniform Cost Search) would will search down the path that has the lowest total cost to traverse. Because the mazes don't have path costs, this is approximately equivalent to a BFS. This algorithm is also guaranteed to find the shortest path from the start to the goal, but doesn't necessarily find that path quickly.

An A* search is similar to a UCS, except that it factors in a heuristic for how far that path is from the goal. For a given path, the estimated cost of that path is the total cost so far (the "walking distance" to that point) plus the estimated "walking distance" back. The heuristic used for estimating the "walking distance" back is the manhattan distance (for (x1, y1) and (x2, y2), the manhattan distance is abs(x1-x2) + abs(y1-y2)). A* will go down the path that has the lowest estimated cost. 

The A* is also guaranteed to find the shortest path from the start to the goal, but also doesn't necessarily find that path quickly.
