import pygame
from .node import Node
from colors import WHITE, GREY

def make_grid(rows, cols, cell_size):
    grid = []
    for r in range(rows):
        row = []
        for c in range(cols):
            node = Node(r, c, cell_size)
            row.append(node)
        grid.append(row)
    return grid

def draw_grid(win, grid, selected_algo):
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win, selected_algo)
            pygame.draw.rect(win, GREY, (node.x, node.y, node.size, node.size), 1)

def get_clicked_pos(pos, cell_size, width, height):
    x, y = pos
    if y < 0 or y >= height or x < 0 or x >= width:
        return None, None
    return y // cell_size, x // cell_size