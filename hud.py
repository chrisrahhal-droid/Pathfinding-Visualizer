# hud.py
import pygame

CONTROLS = [
    ("Left click",  "Place start/end/walls"),
    ("Right click", "Erase node"),
    ("Space",       "Run algorithm"),
    ("P",           "Pause / Resume"),
    ("R",           "Reset grid"),
    ("G",           "Generate maze"),
    ("UP / DOWN",   "Change speed"),
]

ALGORITHMS = [
    ("1", "BFS"),
    ("2", "Dijkstra"),
    ("3", "A*"),
    ("4", "DFS"),
]

ALGO_COLORS = {
    "BFS":      (83, 140, 210),
    "Dijkstra": (210, 160, 83),
    "A*":       (83, 210, 140),
    "DFS":      (210, 83, 140),
}

def init_fonts():
    return {
        "badge": pygame.font.SysFont("consolas", 20, bold=True),
        "hint":  pygame.font.SysFont("monospace", 28),
    }

def draw_algo_badge(win, fonts, selected_algo, speed):
    badge_color = ALGO_COLORS.get(selected_algo, (150, 150, 150))
    label = fonts["badge"].render(f"  {selected_algo}  ", True, (240, 240, 240))
    bw, bh = label.get_width() + 8, label.get_height() + 8
    bx = win.get_width() - bw - 12
    by = 12
    pygame.draw.rect(win, badge_color, (bx, by, bw, bh), border_radius=6)
    win.blit(label, (bx + 4, by + 4))

    speed_label = fonts["badge"].render(f"  x{speed}  ", True, (240, 240, 240))
    tw, th = speed_label.get_width() + 8, speed_label.get_height() + 8
    tx = bx - tw - 8
    pygame.draw.rect(win, (60, 60, 80), (tx, by, tw, th), border_radius=6)
    win.blit(speed_label, (tx + 4, by + 4))

def draw_hint(win, fonts):
    win.blit(fonts["hint"].render("Press H for help", True, (150, 150, 150)),
             (10, win.get_height() - 40))

def _draw_section_header(win, font, text, px, py, pw, pad, line_h):
    s = font.render(text.upper(), True, (100, 140, 200))
    win.blit(s, (px + pad, py))
    line_y = py + s.get_height() + 3
    pygame.draw.line(win, (40, 50, 70), (px + pad, line_y), (px + pw - pad, line_y), 1)
    return line_y + int(line_h * 0.4)

def draw_help_panel(win):
    WW, WH = win.get_width(), win.get_height()
    PW, PH = int(WW * 0.30), int(WH * 0.55)
    PX, PY = int(WW * 0.02), int(WH * 0.05)
    PAD     = int(PW * 0.06)
    TITLE_H = int(PH * 0.09)
    LINE_H  = int(PH * 0.062)
    SEC_GAP = int(PH * 0.04)
    SMALL   = max(14, int(PH * 0.038))
    LABEL_W = int(PW * 0.38)

    font_label  = pygame.font.SysFont("consolas", SMALL)
    font_value  = pygame.font.SysFont("consolas", SMALL)
    font_header = pygame.font.SysFont("consolas", max(11, int(SMALL * 0.78)))
    font_title  = pygame.font.SysFont("consolas", int(SMALL * 1.1), bold=True)

    bg = pygame.Surface((PW, PH), pygame.SRCALPHA)
    bg.fill((15, 15, 20, 245))
    win.blit(bg, (PX, PY))
    pygame.draw.rect(win, (80, 80, 100), (PX, PY, PW, PH), 1, border_radius=6)

    title_bar = pygame.Surface((PW, TITLE_H), pygame.SRCALPHA)
    title_bar.fill((60, 52, 137, 220))
    win.blit(title_bar, (PX, PY))
    pygame.draw.line(win, (100, 90, 180), (PX, PY + TITLE_H), (PX + PW, PY + TITLE_H), 1)

    t = font_title.render("HELP", True, (206, 203, 246))
    win.blit(t, (PX + PAD, PY + (TITLE_H - t.get_height()) // 2))
    hint = font_header.render("H to close", True, (120, 110, 180))
    win.blit(hint, (PX + PW - hint.get_width() - PAD, PY + (TITLE_H - hint.get_height()) // 2))

    cy = PY + TITLE_H + SEC_GAP
    cy = _draw_section_header(win, font_header, "Controls", PX, cy, PW, PAD, LINE_H)
    for key, desc in CONTROLS:
        win.blit(font_label.render(key,  True, (120, 120, 140)), (PX + PAD, cy))
        win.blit(font_value.render(desc, True, (210, 210, 210)), (PX + PAD + LABEL_W, cy))
        cy += LINE_H

    cy += SEC_GAP
    cy = _draw_section_header(win, font_header, "Algorithms", PX, cy, PW, PAD, LINE_H)
    col_w = (PW - PAD * 2) // 2
    for i, (key, name) in enumerate(ALGORITHMS):
        col_x = PX + PAD + (i % 2) * col_w
        row_y = cy + (i // 2) * LINE_H
        badge = pygame.Surface((int(SMALL * 1.4), int(SMALL * 1.4)), pygame.SRCALPHA)
        badge.fill((83, 74, 183, 130))
        win.blit(badge, (col_x, row_y))
        bk = font_label.render(key, True, (206, 203, 246))
        win.blit(bk, (col_x + (badge.get_width() - bk.get_width()) // 2,
                      row_y + (badge.get_height() - bk.get_height()) // 2))
        n = font_value.render(name, True, (210, 210, 210))
        win.blit(n, (col_x + badge.get_width() + 8,
                     row_y + (badge.get_height() - n.get_height()) // 2))

def draw_results_panel(win, phase, nodes_visited, path_cost, elapsed_time, ran_algo):
    WW, WH = win.get_width(), win.get_height()
    PW, PH = int(WW * 0.16), int(WH * 0.32)
    PX, PY = WW - PW - int(WW * 0.02), int(WH * 0.05)
    PAD     = int(PW * 0.08)
    TITLE_H = int(PH * 0.14)
    LINE_H  = int((PH - TITLE_H) / 5.5)
    SMALL   = max(12, int(PH * 0.058))

    font_label = pygame.font.SysFont("consolas", SMALL)
    font_value = pygame.font.SysFont("consolas", SMALL, bold=True)
    font_title = pygame.font.SysFont("consolas", int(SMALL * 1.05), bold=True)

    bg = pygame.Surface((PW, PH), pygame.SRCALPHA)
    bg.fill((15, 15, 20, 245))
    win.blit(bg, (PX, PY))
    pygame.draw.rect(win, (60, 100, 80), (PX, PY, PW, PH), 1, border_radius=6)

    bar_color = (15, 80, 65, 220) if phase == "complete" else (100, 50, 10, 220)
    title_bar = pygame.Surface((PW, TITLE_H), pygame.SRCALPHA)
    title_bar.fill(bar_color)
    win.blit(title_bar, (PX, PY))
    pygame.draw.line(win, (60, 150, 110), (PX, PY + TITLE_H), (PX + PW, PY + TITLE_H), 1)

    t = font_title.render("RESULTS", True, (159, 225, 203))
    win.blit(t, (PX + PAD, PY + (TITLE_H - t.get_height()) // 2))
    algo_hint = font_label.render(ran_algo, True, (100, 160, 130))
    win.blit(algo_hint, (PX + PW - algo_hint.get_width() - PAD,
                         PY + (TITLE_H - algo_hint.get_height()) // 2))

    is_complete = phase == "complete"
    rows = [
        ("Phase",         phase),
        ("Nodes visited", str(nodes_visited)),
        ("Path cost",     str(path_cost)  if is_complete else "—"),
        ("Time",          f"{elapsed_time:.2f}s"),
    ]

    cy = PY + TITLE_H + int(LINE_H * 0.4)
    for i, (label, value) in enumerate(rows):
        win.blit(font_label.render(label, True, (120, 120, 140)), (PX + PAD, cy))
        val = font_value.render(value, True, (210, 210, 210))
        win.blit(val, (PX + PW - val.get_width() - PAD, cy))
        if i < len(rows) - 1:
            div_y = cy + LINE_H - int(LINE_H * 0.15)
            pygame.draw.line(win, (35, 45, 40), (PX + PAD, div_y), (PX + PW - PAD, div_y), 1)
        cy += LINE_H