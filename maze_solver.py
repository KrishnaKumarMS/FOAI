"""
Maze Solver with A* Search
---------------------------
Model: Informed (heuristic) graph search.
- Each cell in the grid is a node.
- g(n) = actual cost from start to node n (steps taken so far).
- h(n) = heuristic estimate from n to goal (Manhattan distance, since
         movement is restricted to 4 directions).
- f(n) = g(n) + h(n)  -> A* always expands the node with lowest f(n).

'#' = wall, '.' = open path, 'S' = start, 'G' = goal, '*' = solution path.
"""

import heapq

WALL = '#'
OPEN = '.'
START = 'S'
GOAL = 'G'
PATH = '*'

DEFAULT_MAZE = [
    "S.#.....",
    "..#.##..",
    "........",
    ".......#",
    "...##.##",
    "#...#..#",
    "..#.....",
    "#...#..G",
]


def parse_maze(maze_lines):
    grid = [list(row) for row in maze_lines]
    start = goal = None
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == START:
                start = (r, c)
            elif ch == GOAL:
                goal = (r, c)
    return grid, start, goal


def heuristic(a, b):
    # Manhattan distance: admissible for 4-directional grid movement
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def neighbors(grid, node):
    r, c = node
    rows, cols = len(grid), len(grid[0])
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != WALL:
            yield (nr, nc)


def a_star(grid, start, goal):
    """Returns the solution path as a list of (row, col), or None."""
    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal), 0, start))
    came_from = {}
    g_score = {start: 0}
    visited = set()

    while open_set:
        f, g, current = heapq.heappop(open_set)

        if current == goal:
            # reconstruct path
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path, visited

        if current in visited:
            continue
        visited.add(current)

        for nxt in neighbors(grid, current):
            tentative_g = g_score[current] + 1
            if nxt not in g_score or tentative_g < g_score[nxt]:
                g_score[nxt] = tentative_g
                f_score = tentative_g + heuristic(nxt, goal)
                came_from[nxt] = current
                heapq.heappush(open_set, (f_score, tentative_g, nxt))

    return None, visited


def print_solution(grid, path):
    display = [row[:] for row in grid]
    for (r, c) in path:
        if display[r][c] not in (START, GOAL):
            display[r][c] = PATH
    for row in display:
        print("".join(row))


def solve(maze_lines=None):
    maze_lines = maze_lines or DEFAULT_MAZE
    grid, start, goal = parse_maze(maze_lines)
    if start is None or goal is None:
        print("Maze must contain a start 'S' and goal 'G'.")
        return

    print("Maze:")
    for row in maze_lines:
        print(row)

    result, visited = a_star(grid, start, goal)
    print(f"\nCells explored by A*: {len(visited)}")

    if result:
        print(f"Path found! Length: {len(result) - 1} steps\n")
        print_solution(grid, result)
    else:
        print("No path exists between start and goal.")


if __name__ == "__main__":
    solve()
