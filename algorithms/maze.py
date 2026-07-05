import random


def generate_maze(grid, rows, cols):
    for r in range(0, rows ):
        for c in range(0, cols ):
            if grid[r][c].state not in ("start", "end"):
                grid[r][c].make_wall()

    visited = set()
    visited.add((0, 0))
    grid[0][0].reset()

    stack = [(0, 0)]

    while stack:
        r, c = stack[-1]

        neighbors = []
        for dr, dc in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows   and 0 <= nc < cols   and (nr, nc) not in visited:
                neighbors.append((nr, nc, dr, dc))

        if neighbors:
            nr, nc, dr, dc = random.choice(neighbors)
            visited.add((nr, nc))
            wr, wc = r + dr // 2, c + dc // 2
            grid[wr][wc].reset()
            grid[nr][nc].reset()
            yield
            stack.append((nr, nc))
        else:
            stack.pop()
            