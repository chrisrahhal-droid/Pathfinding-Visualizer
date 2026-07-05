import random
from algorithms.dfs import dfs
from algorithms.maze import generate_maze
import pygame
import time
import sys
from grid.grid import make_grid, draw_grid, get_clicked_pos
from algorithms.bfs import bfs
from algorithms.dijkstra import dijkstra
from algorithms.a_star import a_star
from algorithms.utils import reconstruct_path
from itertools import count  # needed for A* tie-breaker
from colors import *
from hud import init_fonts, draw_algo_badge, draw_hint, draw_help_panel, draw_results_panel
import os, sys, socket

lock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
try:
    lock.bind('\0pathfinder_lock')
except OSError:
    sys.exit()  # already running
os.environ['SDL_VIDEO_WAYLAND_APP_ID'] = 'pathfinder'
os.environ['SDL_VIDEO_X11_WMCLASS'] = 'pathfinder'
pygame.init()
info = pygame.display.Info()
WIDTH = info.current_w
HEIGHT = info.current_h
CELL_SIZE = 48
ROWS = int(HEIGHT * 0.8) // CELL_SIZE
COLS = int(WIDTH * 0.8) // CELL_SIZE
WIN = pygame.display.set_mode((COLS * CELL_SIZE, ROWS * CELL_SIZE))
pygame.display.set_caption("Pathfinder")

def full_reset(ROWS, COLS, CELL_SIZE):
    return {
        "grid": make_grid(ROWS, COLS, CELL_SIZE),
        "start": None, "end": None,
        "algo_gen": None, "maze_gen": None,
        "running": False, 
        "nodes_visited": 0, "path_len": 0,
        "start_time": 0, "elapsed_time": 0,
        "timer_started": False, "phase": "idle"
    }

def reset_for_run(grid):
    for row in grid:
        for node in row:
            node.update_neighbors(grid)

            node.parent = None
            node.distance = float('inf')
            node.g = float('inf')
            node.f = float('inf')

            if node.state not in ("start", "end", "wall"):
                node.reset()
                node.generate_weight()

            if node.state == "end" and node.color != RED:
                node.color = RED

def main(win):
    grid = make_grid(ROWS, COLS, CELL_SIZE)
    start = None
    end = None
    algo_gen = None
    running = False
    global selected_algo
    selected_algo = "BFS"
    speed = 1
    phase = "idle"
    show_help = False
    maze_gen= None
    timer_started = False
    counter = count()
    clock = pygame.time.Clock()
    fonts = init_fonts()
    while True:
        clock.tick(60)

        if running and phase not in ("idle", "complete", "unreachable"):
            elapsed_time = time.time() - start_time
 
        draw_grid(win, grid, selected_algo)

        draw_algo_badge(win, fonts, selected_algo, speed)
        if show_help:
            draw_help_panel(win)
        if phase in ("complete", "unreachable"):
            draw_results_panel(win, phase, nodes_visited, path_cost, elapsed_time, ran_algo)
        if not show_help:
            draw_hint(win, fonts)
        pygame.display.flip()
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
         
            if phase in ("idle", "complete", "unreachable"):
                if pygame.mouse.get_pressed()[0]:
                    row, col = get_clicked_pos(pygame.mouse.get_pos(), CELL_SIZE, WIDTH, HEIGHT)
                    if row is None: continue
                    node = grid[row][col]
                    if not start and node != end:
                        start = node
                        start.make_start()
                    elif not end and node != start:
                        end = node
                        end.make_end()
                    elif node != start and node != end:
                        node.make_wall()
    
                elif pygame.mouse.get_pressed()[2]:
                    row, col = get_clicked_pos(pygame.mouse.get_pos(), CELL_SIZE, WIDTH, HEIGHT)
                    if row is None: continue
                    node = grid[row][col]
                    if node == start:
                        start = None
                    elif node == end:
                        end = None
                    node.reset()
                    node.generate_weight()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end and not running:
                    reset_for_run(grid)
                    if selected_algo == "BFS":
                        algo_gen = bfs(grid, start, end)
                    elif selected_algo == "Dijkstra":
                        algo_gen = dijkstra(grid, start, end, counter)
                    elif selected_algo == "A*":
                        algo_gen = a_star(grid, start, end, counter)
                    elif selected_algo == "DFS":
                        algo_gen = dfs(grid, start, end)
                    ran_algo = selected_algo
                    running = True
                    nodes_visited = 0
                    path_cost = 0
                    start_time = 0
                    elapsed_time = 0
                    timer_started = False
                    phase = "searching"

                elif event.key == pygame.K_p:
                    running = not running
                elif event.key == pygame.K_r:
                    state = full_reset( ROWS, COLS, CELL_SIZE)
                    grid, start, end = state["grid"], state["start"], state["end"]
                    algo_gen, maze_gen = state["algo_gen"], state["maze_gen"]
                    running = state["running"]
                    phase = state["phase"]
                elif event.key == pygame.K_h:
                        show_help = not show_help
                allowed_phases = {"idle", "complete", "unreachable"}
                if phase in allowed_phases:
                    if event.key == pygame.K_1:
                        selected_algo = "BFS"
                    elif event.key == pygame.K_2:
                        selected_algo = "Dijkstra"
                    elif event.key == pygame.K_3:
                        selected_algo = "A*"
                    elif event.key == pygame.K_4:
                        selected_algo = "DFS"
                    elif event.key == pygame.K_UP:
                        speed = min(speed+1, 10)
                    elif event.key == pygame.K_DOWN:
                        speed = max(speed-1, 1)
                    elif event.key == pygame.K_g :
                            phase = "idle"
                            for row in grid:
                                for node in row:
                                    node.reset()
                            # start = None
                            # end = None
                            maze_gen = generate_maze(grid, ROWS, COLS)
        if running and algo_gen:
            if not timer_started:
                start_time = time.time()
                timer_started = True
            try:
                for _ in range(speed):
                    if phase == "searching":
                        action, node = next(algo_gen)
 
                        if action == "visit":
                            nodes_visited += 1
                        if node.state not in ["start", "end"]:
                            if action == "visit":
                                node.make_visited()
                            else:
                                node.make_frontier()
                               
            except StopIteration:
                if phase == "searching":
                    elapsed_time = time.time() - start_time
                    if end and end.parent:
                        algo_gen = reconstruct_path(end, lambda: draw_grid(win, grid, selected_algo))
                        phase = "pathfinding"
                        running = False
                        path_cost = 0
                        current = end
                        while current.parent:
                            if ran_algo in ("BFS", "DFS"):
                                path_cost += 1
                            else:
                                path_cost += current.weight
                            current = current.parent
                    else:
                        phase = "unreachable"
                        running = False
                        if end:
                            end.color = ORANGE
 
        if not running and algo_gen and phase == "pathfinding":
            try:
                next(algo_gen)
            except StopIteration:
                phase = "complete"

        if not running  and maze_gen:
            try:
                for _ in range(speed * 4):
                    next(maze_gen)
            except StopIteration:
                maze_gen = None
                empty_nodes = []
                for row in grid:
                    for node in row:
                        if node.state != "wall":
                            empty_nodes.append(node)
                
                start = random.choice(empty_nodes)
                start.make_start()
                end = random.choice(empty_nodes)
                while end == start:
                    end = random.choice(empty_nodes)
                end.make_end()
if __name__ == "__main__":        
    main(WIN)
