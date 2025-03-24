import heapq
import math
import copy

COLAB = 0

from matplotlib import rc

if COLAB:
    rc('animation', html='jshtml')
else:
    rc('animation')

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap


# node
class Node:
    def __init__(self, x, y) -> None:
        self.x, self.y = x, y
        self.g, self.h = 0, 0
        self.parent = None

    def f(self):
        return self.g + self.h  # *2 weight goes here

    def __lt__(self, other: "Node"):  # for frontier priority queue
        return self.f() < other.f()

    def __eq__(self, other: "Node"):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"({self.x}, {self.y})"


# heuristics
def h1(goal: "Node", node: "Node"):
    return math.sqrt((goal.x - node.x) ** 2 + (goal.y - node.y) ** 2)


# https://en.wikipedia.org/wiki/Taxicab_geometry
def h2(goal: "Node", node: "Node"):
    return abs(goal.x - node.x) + abs(goal.y - node.y)


# https://en.wikipedia.org/wiki/Chebyshev_distance
def h3(goal: "Node", node: "Node"):
    return max(abs(goal.x - node.x), abs(goal.y - node.y))


# algo
def astar(maze, start, goal, H=h1):
    """
    A* search

    Parameters:
    - maze: The 2D matrix that represents the maze with 0 represents empty space and 1 represents a wall
    - start: A tuple with the coordinates of starting position
    - goal: A tuple with the coordinates of finishing position

    Returns:
    - Number of steps from start to goal, equals -1 if the path is not found
    - Viz - everything required for step-by-step visualisation
    """

    start_node = Node(*start)
    goal_node = Node(*goal)

    frontier = []  # frontier - priority queue
    visited = []  # used as a set (required for vizualization)

    heapq.heappush(frontier, start_node)

    while frontier:  # while frontier is not empty
        curr_node = heapq.heappop(frontier)  # pick a node from a frontier
        visited.append(curr_node)  # mark the node as visited

        if curr_node.x == goal_node.x and curr_node.y == goal_node.y:  # if node is a goal
            path = []
            while curr_node:  # backtrack
                path.append((curr_node.x, curr_node.y))  # path is reversed here
                curr_node = curr_node.parent
            path.reverse()
            return len(path), (path, visited)

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # actions (down, right, up, left)
            next_node = Node(curr_node.x + dx, curr_node.y + dy)

            if next_node in visited:  # skip if already visited
                continue
            if next_node.x < 0 or next_node.y < 0 or next_node.x >= len(maze) or next_node.y >= len(
                    maze[0]):  # skip if out of borders
                continue
            if maze[next_node.x][next_node.y] == 1:  # skip if a wall
                continue

            if any((entry.x, entry.y) == (next_node.x, next_node.y) for entry in frontier): # skip if already in the frontier
                continue 

            next_node.parent = curr_node
            next_node.g = curr_node.g + 1
            next_node.h = H(goal_node, next_node)
            
            heapq.heappush(frontier, next_node)

    return -1, ([], visited)  # if no goal found


def vizualize(viz):
    """
    Vizualization function. Shows step by step the work of the search algorithm

    Parameters:
    - viz: everything required for step-by-step vizualization
    """

    path, visited = viz

    fig, ax = plt.subplots()
    ax.set_xticks([])
    ax.set_yticks([])

    # Define custom colormap
    colors = ['white', 'black', 'red', 'gold', 'lightblue']
    cmap = ListedColormap(colors)  # 4 = visited (blue)

    anim_maze = copy.deepcopy(maze)

    # Update maze display with the new colormap
    maze_display = ax.imshow(anim_maze, cmap=cmap, vmin=0, vmax=len(colors))

    # Animation function
    def update(frame):
        if frame < len(visited):
            node = visited[frame]
            anim_maze[node.x][node.y] = 4  # Mark visited path
        else:
            for node in path:
                anim_maze[node[0]][node[1]] = 3

        anim_maze[start_position[0]][start_position[1]] = 2
        anim_maze[finish_position[0]][finish_position[1]] = 2
        maze_display.set_data(anim_maze)

    anim = animation.FuncAnimation(fig, update, frames=len(visited) + 5, interval=100)

    # choose display format
    if not COLAB:
        anim.save('animation.mp4', writer='ffmpeg')
        # anim.save('animation.gif', writer='pillow')

    return anim


# Example usage:
# maze = [
#     [0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
#     [0, 1, 0, 1, 0, 1, 0, 1, 1, 0],
#     [0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
#     [1, 0, 1, 0, 0, 1, 0, 0, 0, 1],
#     [0, 0, 1, 1, 0, 0, 0, 1, 0, 0],
#     [0, 1, 0, 0, 0, 1, 1, 1, 0, 1],
#     [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 1, 0, 1, 1, 1, 1, 0],
#     [0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
#     [0, 0, 0, 1, 1, 0, 0, 0, 0, 0]
# ]

# start_position = (0, 0)
# finish_position = (9, 9)


maze = [
    [1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1],
    [1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0],
    [1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1],
    [1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0],
    [1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1],
    [1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1],
    [1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1],
    [0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1],
    [1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1],
    [1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0],
    [1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1],
    [1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1],
    [0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1],
    [1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0],
    [1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1],
    [1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1],
    [0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0]
]

start_position = (0, 0)
finish_position = (29, 29)

num_steps, viz = astar(maze, start_position,
                       finish_position)  # heuristics function can be added as a 4th argument; default h1

# Print number of steps in path
if num_steps != -1:
    print(f"Path from {start_position} to {finish_position} using A* is {num_steps} steps.")

else:
    print(f"No path from {start_position} to {finish_position} exists.")

# Vizualize algorithm step-by-step even if the path was not found
vizualize(viz)


#---------------------------------------------------------------------------------------------------------------
# tests
# --------------------------------------------------------------------------------------------------------------
import unittest
from main import astar, Node, h1, h2, h3

big_maze = [
    [1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1],
    [1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0],
    [1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1],
    [1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0],
    [1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1],
    [1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1],
    [1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1],
    [0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1],
    [1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1],
    [1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0],
    [1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1],
    [1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1],
    [0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1],
    [1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0],
    [1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1],
    [1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1],
    [0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0]
]

big_maze_2 = [
    [1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1],
    [1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0],
    [1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1],
    [1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0],
    [1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1],
    [1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1],
    [1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1],
    [0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1],
    [1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1],
    [1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0],
    [1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1],
    [1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1],
    [0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1],
    [1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0],
    [1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1],
    [1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1],
    [0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]
]

small_maze = [
    [0, 1, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 1],
    [0, 0, 0, 1, 0, 0, 0],
    [1, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 1, 0, 0, 0],
    [0, 1, 0, 0, 0, 1, 1],
    [0, 1, 1, 1, 0, 0, 0],
]

start_position = (0,0)

class TestAStart(unittest.TestCase):
# ---------------------------------------------------------------------------
# Basic functionality test
    def test_ok_small(self):
      finish_possible = (6, 6)
      path = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2), (0, 3),
       (0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (6, 5), (6, 6)]
      print("test_ok_small:")
      for h in [h1, h2, h3]:
        num_steps, viz = astar(small_maze, start_position, finish_possible, h)
        self.assertEqual(num_steps, 17)
        self.assertEqual(viz[0], path)
        print("--", h.__name__, "visited:", len(viz[1]))
# ---------------------------------------------------------------------------
# Test shows differences in the amound of visited nodes for different heuristics.
    def test_ok_big(self):
      finish = (29, 29)
      path = [(0, 0), (0, 1), (1, 1), (1, 2), (2, 2), (3, 2), (4, 2), (4, 3),
       (4, 4), (5, 4), (6, 4), (7, 4), (8, 4), (9, 4), (10, 4), (11, 4), (11, 5),
       (11, 6), (11, 7), (11, 8), (12, 8), (12, 9), (12, 10), (13, 10), (13, 11),
       (13, 12), (13, 13), (13, 14), (14, 14), (15, 14), (15, 15), (15, 16),
       (15, 17), (15, 18), (15, 19), (15, 20), (16, 20), (17, 20), (18, 20),
       (18, 19), (18, 18), (18, 17), (18, 16), (19, 16), (20, 16), (20, 17),
       (21, 17), (21, 18), (21, 19), (21, 20), (21, 21), (20, 21), (19, 21),
       (19, 22), (19, 23), (19, 24), (19, 25), (19, 26), (20, 26), (21, 26),
       (22, 26), (23, 26), (24, 26), (25, 26), (25, 27), (25, 28), (26, 28),
       (27, 28), (28, 28), (29, 28), (29, 29)]

      print("test_ok_big:")
      for h in [h1, h2, h3]:
        num_steps, viz = astar(big_maze, start_position, finish, h)
        self.assertEqual(num_steps, 71)
        self.assertEqual(viz[0], path)
        print("--", h.__name__, "visited:", len(viz[1]))

    def test_ok_big_2(self):
      start_position = (12, 12)
      finish_position = (29, 29)
      path = [(12, 12), (13, 12), (13, 13), (13, 14), (14, 14), (15, 14), 
       (15, 15), (15, 16), (15, 17), (15, 18), (15, 19), (15, 20), (16, 20), 
       (17, 20), (18, 20), (18, 19), (18, 18), (18, 17), (18, 16), (19, 16), 
       (20, 16), (20, 17), (21, 17), (21, 18), (21, 19), (21, 20), (21, 21), 
       (20, 21), (19, 21), (19, 22), (19, 23), (19, 24), (19, 25), (19, 26), 
       (20, 26), (21, 26), (22, 26), (23, 26), (24, 26), (25, 26), (25, 27), 
       (25, 28), (26, 28), (27, 28), (28, 28), (29, 28), (29, 29)]

      print("test_ok_big_2:")
      for h in [h1, h2, h3]:
        num_steps, viz = astar(big_maze_2, start_position, finish_position, h)
        self.assertEqual(num_steps, 47)
        self.assertEqual(viz[0], path)
        print("--", h.__name__, "visited:", len(viz[1]))
# ---------------------------------------------------------------------------
# Goal node is unreachable.
    def test_unreachable(self):
      finish_unreachable = (0, 6)
      vizited_unreachable = {h1: 31, h2: 31, h3: 31}
      for h in [h1, h2, h3]:
        num_steps, viz = astar(small_maze, start_position, finish_unreachable, h)
        self.assertEqual(num_steps, -1)
        self.assertEqual(viz[0], [])
        self.assertEqual(len(viz[1]), vizited_unreachable[h])
# ---------------------------------------------------------------------------
# Goal node is out of range of the maze.
    def test_out_of_range(self):
      finish_out_of_range = (10, 10)
      vizited_out_of_range = 31 # all reachable nodes
      for h in [h1, h2, h3]:
        num_steps, viz = astar(small_maze, start_position, finish_out_of_range, h)
        self.assertEqual(num_steps, -1)
        self.assertEqual(viz[0], [])
        self.assertEqual(len(viz[1]), vizited_out_of_range)
# ---------------------------------------------------------------------------
# Goal node is the same as starting node. For every heuristic it is found in 1 step.
    def test_zero(self):
      finish_zero = (0, 0)
      vizited_zero = 1
      for h in [h1, h2, h3]:
        num_steps, viz = astar(small_maze, start_position, finish_zero, h)
        self.assertEqual(num_steps, 1)
        self.assertEqual(viz[0], [(0, 0)])
        self.assertEqual(len(viz[1]), vizited_zero)
# ---------------------------------------------------------------------------
# Goal node is in the wall - same behaviour as for unreachable node.
    def test_in_wall(self):
      finish_in_wall = (5, 6)
      vizited_in_wall = 31 # all reachable nodes
      for h in [h1, h2, h3]:
        num_steps, viz = astar(small_maze, start_position, finish_in_wall, h)
        self.assertEqual(num_steps, -1)
        self.assertEqual(viz[0], [])
        self.assertEqual(len(viz[1]), vizited_in_wall)
# ---------------------------------------------------------------------------
# For this type of maze, algorithm will iterate over all zeros achieveble from
# the start before understanding that the finish is unreachable, which can be
# considered a drawback of the algorithm.
    def test_many_zeros(self):
      maze = [
          [0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0],
          [0, 0, 0, 1, 1],
          [0, 0, 0, 1, 0],
      ]
      start_position = (0,0)
      finish_possible = (4, 4)
      for h in [h1, h2, h3]:
        num_steps, viz = astar(maze, start_position, finish_possible, h)
        self.assertEqual(num_steps, -1)
        self.assertEqual(viz[0], [])
        self.assertEqual(len(viz[1]), 21) # visit all zeros
# ---------------------------------------------------------------------------
# Without applying heuristics, the A* algorithm is simply a Dijkstra's algorithm.
# As can be sees from visualization, all reachable nodes was visited for this case.
    def test_no_heuristics(self):
      def bad_h(goal: 'Node', node: 'Node'):
        return 0
      finish = (29, 29)
      num_steps, viz = astar(big_maze, start_position, finish, bad_h)
      self.assertEqual(num_steps, 71)
      self.assertEqual(len(viz[1]), 182) # <- the amount of visited nodes is much higher than with heuristics

# ---------------------------------------------------------------------------
# Bad heuristics result in visiting much more nodes (potentially all reachable).
    def test_no_heuristics(self):
      def bad_h(goal: 'Node', node: 'Node'):
        return node.x + node.y # heuristic does not extimate distance to the goal

      finish = (29, 29)
      num_steps, viz = astar(big_maze, start_position, finish, bad_h)
      self.assertEqual(num_steps, 71)
      self.assertEqual(len(viz[1]), 182) # <- the amount of visited nodes is much higher than with heuristics

# unittest.main(argv=[''], verbosity=2, exit=False) #<-- uncomment to run tests
