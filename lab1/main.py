import heapq
import math
import copy

from matplotlib import rc
rc('animation') #, writer='ffmpeg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap


# Class for representing one node on a grid
class Node:
    def __init__(self, x, y) -> None:
        self.x, self.y = x, y
        self.g, self.h = 0, 0
        self.parent = None

    def f(self):
        return self.g + self.h

    def __lt__(self, other): # for priority queue
        return self.f() < other.f()

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"({self.x}, {self.y})"


def h1(goal, node):
    return math.sqrt((goal.x - node.x) ** 2 + (goal.y - node.y) ** 2) * 2


def h2(goal, node):
    return abs(goal.x - node.x) + abs(goal.y - node.y)


# Heuristic function - can be changed
def h(goal, node):
    return h1(goal, node)


def astar(maze, start, goal):
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
    visited = [] # set()

    heapq.heappush(frontier, start_node)

    while frontier:  # while frontier is not empty
        curr_node = heapq.heappop(frontier)  # pick a node from a frontier
        visited.append(curr_node)  # mark the node as visited

        if curr_node.x == goal_node.x and curr_node.y == goal_node.y:  # if node is a goal
            path = []
            while curr_node:  # backtrack
                path.append((curr_node.x, curr_node.y))  # path is reversed here
                curr_node = curr_node.parent
            return len(path), path, visited

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # actions (down, right, up, left)
            next_node = Node(curr_node.x + dx, curr_node.y + dy)

            if next_node in visited:  # skip if already visited
                continue
            if next_node.x < 0 or next_node.y < 0 or next_node.x >= len(maze) or next_node.y >= len(maze[0]):  # skip if out of borders
                continue
            if maze[next_node.x][next_node.y] == 1:  # skip if a wall
                continue

            next_node.parent = curr_node
            next_node.g = curr_node.g + 1
            next_node.h = h(goal_node, next_node)
            
            heapq.heappush(frontier, next_node) # push to the frontier
    return -1, [], visited  # if no goal found


def vizualize(maze, path, visited):
    """
    Vizualization function. Shows step by step the work of the search algorithm

    Parameters:
    - viz: everything required for step-by-step vizualization
    """

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

# start_position = Cell(0, 0)
# finish_position = Cell(9, 9)


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

num_steps, path, visited = astar(maze, start_position, finish_position)

# Print number of steps in path
if num_steps != -1:
    print(f"Path from {start_position} to {finish_position} using A* is {num_steps} steps.")

else:
    print(f"No path from {start_position} to {finish_position} exists.")

# Vizualize algorithm step-by-step even if the path was not found
vizualize(maze, path, visited)
