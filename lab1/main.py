import random

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
        self.step = 0  # Step counter for visualization
        self.visited = set()
        self.frontier = QueueFrontier()

    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]


        # random.shuffle(candidates)

        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                # if action is allowed i.e. we don't go out of maze or in the walls
                result.append((action, (r, c)))

        return result

    def solve(self):
        # Initialize frontier to just the starting position
        start = Node(state=self.start, parent=None, action=None)

        self.frontier.add(start)


        while True:
            # If nothing left in frontier, then no path
            if self.frontier.empty():
                raise Exception("empty frontier")

            # Choose a node from the frontier
            node = self.frontier.remove()
            # Mark node as explored
            self.visited.add(node.state)

            self.output_image(f"step_{self.step}.png", current=node.state)
            self.step += 1 # step is now 42

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

            # Add neighbors to frontier
            for action, state in self.neighbors(node.state):
                if not self.frontier.contains_state(state) and state not in self.visited:
                    # if we haven't visited or are not to visit the node yet, add it to frontier
                    child = Node(state=state, parent=node, action=action)
                    self.frontier.add(child)

    def output_image(self, filename, show_solution=True, show_explored=True, current=None):
        from PIL import Image, ImageDraw

        cell_size = 50
        cell_border = 2

        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    fill = (40, 40, 40)  # Wall (Gray)
                elif (i, j) == self.start:
                    fill = (255, 0, 0)  # Start (Red)
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)  # Goal (Green)
                elif solution and show_solution and (i, j) in solution:
                    fill = (144, 238, 144)  # Solution Path (Light Green)
                elif show_explored and (i, j) in self.visited:
                    fill = (220, 235, 113)  # Explored (Yellow)
                else:
                    fill = (255, 255, 255)  # Empty Cell (White)

                if current and (i, j) == current:
                    fill = (0, 0, 255)  # Current Node (Blue)

                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )

        img.save(filename)

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

solver = MazeSolver(grid, start_position, finish_position)
solver.solve()