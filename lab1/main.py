class Node:
    def __init__(self, state, parent, action):
        self.state = state # let's start with coordinates (row, col)
        self.parent = parent
        self.action = action

class QueueFrontier: # let's start with BFS
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

class MazeSolver:
    def __init__(self, maze, start, goal):
        self.walls = maze
        self.start = start
        self.goal = goal
        self.height = len(maze)
        self.width = len(maze[0])
        self.solution = None

    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                # if action is allowed i.e. we don't go out of maze or in the walls
                result.append((action, (r, c)))
        return result

    def solve(self):
        # Initialize frontier to just the starting position
        start = Node(state=self.start, parent=None, action=None)
        frontier = QueueFrontier()
        frontier.add(start)

        # Initialize an empty visited set
        self.visited = set()

        while True:
            # If nothing left in frontier, then no path
            if frontier.empty():
                raise Exception("empty frontier")

            # Choose a node from the frontier
            node = frontier.remove()

            # If node is the goal, then we have a solution
            if node.state == self.goal:
                # backtrack
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return

            # Mark node as explored
            self.visited.add(node.state)

            # Add neighbors to frontier
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.visited:
                    # if we haven't visited or are not to visit the node yet, add it to frontier
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)

    def output_image(self, filename, show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw

        cell_size = 50
        cell_border = 2

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):

                # Walls
                if col:
                    fill = (40, 40, 40) # GRAY

                # Start
                elif (i, j) == self.start:
                    fill = (255, 0, 0) # RED

                # Goal
                elif (i, j) == self.goal:
                    fill = (0, 171, 28) # GREEN

                # Solution
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (144, 238, 144) # LIGHT GREEN

                # Explored
                elif solution is not None and show_explored and (i, j) in self.visited:
                    fill = (220, 235, 113) # YELLOW

                # Empty cell
                else:
                    fill = (255, 255, 255) # WHITE

                # Draw cell
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )

        img.save(filename)

def astar(maze, start, finish):
    """
    A* search

    Parameters:
    - maze: The 2D matrix that represents the maze with 0 represents emptry space and 1 represents a wall
    - start: A tuple with the coordinates of starting position
    - finish: A tuple with the coordinates of finishing position

    Returns:
    - Number of steps from start to finish, equals -1 if the path is not found
    - Viz - everything required for step-by-step vizualization

    """


    solver = MazeSolver(maze, start, finish)
    solver.solve()
    solver.output_image("maze.png", show_explored=True)



def vizualize(viz):
    """
    Vizualization function. Shows step by step the work of the search algorithm

    Parameters:
    - viz: everything required for step-by-step vizualization
    """


# Example usage:
# grid = [
#     [0, 1, 0, 0, 0],
#     [0, 1, 0, 1, 0],
#     [0, 0, 0, 1, 0],
#     [1, 0, 1, 0, 0],
#     [0, 0, 0, 1, 0]
# ]
#
# start_position = (0, 0)
# finish_position = (4, 4)

grid = [
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
    [1, 0, 1, 0, 0, 1, 0, 0, 0, 1],
    [0, 0, 1, 1, 0, 0, 0, 1, 0, 0],
    [0, 1, 0, 0, 0, 1, 1, 1, 0, 1],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 0, 0, 0]
]

start_position = (0, 0)
finish_position = (9, 9)


num_steps, viz = astar(grid, start_position, finish_position)

# Print number of steps in path
if num_steps != -1:
    print(f"Path from {start_position} to {finish_position} using A* is {num_steps} steps.")

else:
    print(f"No path from {start_position} to {finish_position} exists.")

# Vizualize algorithm step-by-step even if the path was not found
vizualize(viz)