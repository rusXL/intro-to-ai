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
      vizited = {h1: 24, h2: 25, h3: 23}
      for h in [h1, h2, h3]:
        num_steps, viz = astar(small_maze, start_position, finish_possible, h)
        self.assertEqual(num_steps, 17)
        self.assertEqual(viz[0], path)
        self.assertEqual(len(viz[1]), vizited[h])
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

      # For this graph, heuristics h1 performs better.
      vizited = {h1: 115, h2: 121, h3: 168}
      for h in [h1, h2, h3]:
        num_steps, viz = astar(big_maze, start_position, finish, h)
        self.assertEqual(num_steps, 71)
        self.assertEqual(viz[0], path)
        self.assertEqual(len(viz[1]), vizited[h])
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
      vizited_out_of_range = {h1: 31, h2: 31, h3: 31}
      for h in [h1, h2, h3]:
        num_steps, viz = astar(small_maze, start_position, finish_out_of_range, h)
        self.assertEqual(num_steps, -1)
        self.assertEqual(viz[0], [])
        self.assertEqual(len(viz[1]), vizited_out_of_range[h])
# ---------------------------------------------------------------------------
# Goal node is the same as starting node. For every heuristic it is found in 1 step.
    def test_zero(self):
      finish_zero = (0, 0)
      vizited_zero = {h1: 1, h2: 1, h3: 1}
      for h in [h1, h2, h3]:
        num_steps, viz = astar(small_maze, start_position, finish_zero, h)
        self.assertEqual(num_steps, 1)
        self.assertEqual(viz[0], [(0, 0)])
        self.assertEqual(len(viz[1]), vizited_zero[h])
# ---------------------------------------------------------------------------
# Goal node is in the wall - same behaviour as for unreachable node.
    def test_in_wall(self):
      finish_in_wall = (5, 6)
      vizited_in_wall = {h1: 31, h2: 31, h3: 31}
      for h in [h1, h2, h3]:
        num_steps, viz = astar(small_maze, start_position, finish_in_wall, h)
        self.assertEqual(num_steps, -1)
        self.assertEqual(viz[0], [])
        self.assertEqual(len(viz[1]), vizited_in_wall[h])
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

unittest.main(argv=[''], verbosity=2, exit=False)