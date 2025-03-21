import heapq
import math
import copy

from matplotlib import rc
rc('animation') #, writer='ffmpeg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap


# Class for representing one cell on a grid
class Cell:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.f, self.g, self.h = 0, 0, 0
        self.parent = None

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"({self.x}, {self.y})"


def h1(finish, cell):
    return math.sqrt((finish.x - cell.x) ** 2 + (finish.y - cell.y) ** 2) * 2


def h2(finish, cell):
    return abs(finish.x - cell.x) + abs(finish.y - cell.y)


# Heuristic function - can be changed
def H(finish, cell):
    return h1(finish, cell)


def astar(maze, start, finish):
    """
    A* search

    Parameters:
    - maze: The 2D matrix that represents the maze with 0 represents empty space and 1 represents a wall
    - start: A tuple with the coordinates of starting position
    - finish: A tuple with the coordinates of finishing position

    Returns:
    - Number of steps from start to finish, equals -1 if the path is not found
    - Viz - everything required for step-by-step visualisation
    """

    queue = []  # frontier
    visited = []

    heapq.heappush(queue, start)

    while queue:  # while frontier is not empty
        curr = heapq.heappop(queue)  # pick a cell from a frontier
        visited.append(curr)  # mark the cell as visited

        if curr.x == finish.x and curr.y == finish.y:  # if cell is a goal
            path = []
            while curr is not None:  # backtrack
                path.append((curr.x, curr.y))  # path is reversed here
                curr = curr.parent
            path.reverse()
            return len(path), path, visited

        deltas = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # actions (down, right, up, left)
        for delta in deltas:
            next_cell = Cell(curr.x + delta[0], curr.y + delta[1])

            if next_cell in visited:  # skip if already visited
                continue
            if next_cell.x < 0 or next_cell.y < 0 or next_cell.x >= len(maze) or next_cell.y >= len(
                    maze[0]):  # skip if out of borders
                continue
            if maze[next_cell.x][next_cell.y] == 1:  # skip if a wall
                continue

            next_cell.g = curr.g + 1  # update steps needed to reach this cell
            next_cell.h = H(finish, next_cell)
            next_cell.f = next_cell.g + next_cell.h * 2 # <- weight
            next_cell.parent = curr

            entry = next((q for q in queue if q.x == next_cell.x and q.y == next_cell.y),
                         None)  # queue entry with same coordinates if such exists or none
            if entry:
                # if it is possible to reach same cell (which is already in the queue) from a different (next_cell) path with a lower cost g
                if next_cell.g < entry.g:
                    entry.g, entry.h, entry.f = next_cell.g, next_cell.h, next_cell.f
                    entry.parent = next_cell.parent
                    heapq.heapify(queue)  # resort
            else:
                heapq.heappush(queue, next_cell)
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
            cell = visited[frame]
            anim_maze[cell.x][cell.y] = 4  # Mark visited path
        else:
            for cell in path:
                anim_maze[cell[0]][cell[1]] = 3

        anim_maze[start_position.x][start_position.y] = 2
        anim_maze[finish_position.x][finish_position.y] = 2
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

start_position = Cell(0, 0)
finish_position = Cell(29, 29)

num_steps, path, visited = astar(maze, start_position, finish_position)

# Print number of steps in path
if num_steps != -1:
    print(f"Path from {start_position} to {finish_position} using A* is {num_steps} steps.")

else:
    print(f"No path from {start_position} to {finish_position} exists.")

# Vizualize algorithm step-by-step even if the path was not found
vizualize(maze, path, visited)
