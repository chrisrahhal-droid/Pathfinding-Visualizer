import pygame
import random
from colors import *
WEIGHT_FONT = None

def get_weight_font():
    global WEIGHT_FONT
    if WEIGHT_FONT is None:
        WEIGHT_FONT = pygame.font.SysFont('Arial', 22)
    return WEIGHT_FONT

class Node:
    def __init__(self, row, col, size):
        self.row = row
        self.col = col
        self.size = size
        self.x = col * size
        self.y = row * size

        self.color = WHITE
        self.state = "empty"
        self.neighbors = []
        self.parent = None

        self.g = float('inf')
        self.h = float('inf')
        self.f = float('inf')
        self.weight = random.randint(1, 1)

    def draw(self, win, selected_algo):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size))
        
        if selected_algo in ["Dijkstra", "A*"] and self.state != "wall":
            weight_text = str(self.weight) if self.weight != float('inf') else '∞'
            font = get_weight_font()
            text_color = BLACK if self.state in ["empty", "start", "end"] else WHITE
            text_surf = font.render(weight_text, True, text_color)
            text_rect = text_surf.get_rect(center=(self.x + self.size // 2, self.y + self.size // 2))
            win.blit(text_surf, text_rect)

    def make_wall(self):
        self.color = BLACK
        self.state = "wall"
        self.weight = float('inf')

    def make_start(self):
        self.color = GREEN
        self.state = "start"
        self.weight = 0  

    def make_end(self):
        self.color = RED
        self.state = "end"
        self.weight = 0  

    def generate_weight(self):
        self.weight = random.randint(1, 1)

    def reset(self):
        self.color = WHITE
        self.state = "empty"
        
    def is_wall(self):
        return self.state == "wall"

    def make_visited(self):
        self.color = BLUE
        self.state = "visited"

    def make_frontier(self):
        self.color = YELLOW
        self.state = "frontier"

    def make_path(self):
        self.color = PURPLE
        self.state = "path"

    def update_neighbors(self, grid):
        self.neighbors = []
        rows = len(grid)
        cols = len(grid[0])
        if self.row > 0 and not grid[self.row-1][self.col].is_wall():
            self.neighbors.append(grid[self.row-1][self.col])
        if self.row < rows - 1 and not grid[self.row+1][self.col].is_wall():
            self.neighbors.append(grid[self.row+1][self.col])
        if self.col > 0 and not grid[self.row][self.col-1].is_wall():
            self.neighbors.append(grid[self.row][self.col-1])
        if self.col < cols - 1 and not grid[self.row][self.col+1].is_wall():
            self.neighbors.append(grid[self.row][self.col+1])