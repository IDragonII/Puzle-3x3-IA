import os
import pygame
from heapq import heappush, heappop
import itertools
import time
import random

SCREEN_SIZE = 500
TILE_SIZE = SCREEN_SIZE // 3

pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Puzle 3x3")

image_folder = 'dragon'
images = []
for i in range(9):
    image_path = os.path.join(image_folder, f"image{i}.png")
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
    images.append(image)

def draw_board(state):
    screen.fill((255, 255, 255))
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            if value != 0:
                screen.blit(images[value], (j*TILE_SIZE, i*TILE_SIZE))

def draw_buttons(buttons):
    for button in buttons:
        pygame.draw.rect(screen, button['color'], button['rect'])
        screen.blit(button['text'], (button['rect'].x + (button['rect'].width - button['text'].get_width()) // 2,
                                     button['rect'].y + (button['rect'].height - button['text'].get_height()) // 2))

def find_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

def get_possible_actions(state):
    blank_row, blank_col = find_blank(state)
    actions = []
    if blank_row > 0:
        actions.append('up')
    if blank_row < 2:
        actions.append('down')
    if blank_col > 0:
        actions.append('left')
    if blank_col < 2:
        actions.append('right')
    return actions

def result(state, action):
    blank_row, blank_col = find_blank(state)
    new_state = [row[:] for row in state]
    if action == 'up':
        new_state[blank_row][blank_col], new_state[blank_row-1][blank_col] = new_state[blank_row-1][blank_col], new_state[blank_row][blank_col]
    elif action == 'down':
        new_state[blank_row][blank_col], new_state[blank_row+1][blank_col] = new_state[blank_row+1][blank_col], new_state[blank_row][blank_col]
    elif action == 'left':
        new_state[blank_row][blank_col], new_state[blank_row][blank_col-1] = new_state[blank_row][blank_col-1], new_state[blank_row][blank_col]
    elif action == 'right':
        new_state[blank_row][blank_col], new_state[blank_row][blank_col+1] = new_state[blank_row][blank_col+1], new_state[blank_row][blank_col]
    return new_state

goal_state = [[1, 2, 3], [0, 4, 5], [6, 7, 8]]

def goal_test(state):
    return state == goal_state

def path_cost(cost_so_far):
    return cost_so_far + 1

def manhattan_distance(state):
    total_distance = 0
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            if value != 0:
                target_row, target_col = divmod(value - 1, 3)
                total_distance += abs(i - target_row) + abs(j - target_col)
    return total_distance

def search(initial_state):
    frontier = []
    explored = set()
    counter = itertools.count()
    heappush(frontier, (manhattan_distance(initial_state), 0, next(counter), initial_state, []))

    while frontier:
        _, cost, _, state, path = heappop(frontier)

        if goal_test(state):
            return path
        
        explored.add(tuple(tuple(row) for row in state))
        for action in get_possible_actions(state):
            new_state = result(state, action)
            new_cost = path_cost(cost)
            state_tuple = tuple(tuple(row) for row in new_state)
            if state_tuple not in explored:
                heappush(frontier, (new_cost + manhattan_distance(new_state), new_cost, next(counter), new_state, path + [action]))

    return None

def visualize_solution(solution, initial_state):
    state = initial_state
    draw_board(state)
    pygame.display.flip()
    time.sleep(0.2)
    for move in solution:
        state = result(state, move)
        draw_board(state)
        pygame.display.flip()
        time.sleep(0.2)
    
    font = pygame.font.SysFont(None, 48)
    text_background_rect = pygame.Rect(SCREEN_SIZE // 2 - 150, SCREEN_SIZE // 2 - 50, 350, 100)
    pygame.draw.rect(screen, (255, 255, 255), text_background_rect)
    
    text = font.render("¡Solución encontrada!", True, (0, 128, 0))
    screen.blit(text, (SCREEN_SIZE // 2 - text.get_width() // 2, SCREEN_SIZE // 2 - text.get_height() - 10))
    
    moves_text = font.render(f"Movimientos: {len(solution)}", True, (0, 128, 0))
    screen.blit(moves_text, (SCREEN_SIZE // 2 - moves_text.get_width() // 2, SCREEN_SIZE // 2 + 10))
    
    pygame.display.flip()
    time.sleep(3)

def shuffle_state(state):
    actions = get_possible_actions(state)
    for _ in range(100):
        action = random.choice(actions)
        state = result(state, action)
        actions = get_possible_actions(state)
    return state

def game_loop():
    initial_state = [[1, 2, 3], [0, 4, 5], [6, 7, 8]]
    state = [row[:] for row in initial_state]

    font = pygame.font.SysFont(None, 48)
    solve_button_text = font.render("Resolver", True, (255, 255, 255))
    shuffle_button_text = font.render("Revolver", True, (255, 255, 255))
    back_button_text = font.render("Regresar", True, (255, 255, 255))

    buttons = [
        {'rect': pygame.Rect(SCREEN_SIZE // 2 - 75, SCREEN_SIZE // 2 + 50, 150, 60), 'color': (0, 128, 0), 'text': solve_button_text},
        {'rect': pygame.Rect(SCREEN_SIZE // 2 - 75, SCREEN_SIZE // 2 + 120, 150, 60), 'color': (0, 128, 255), 'text': shuffle_button_text},
        {'rect': pygame.Rect(SCREEN_SIZE // 2 - 75, SCREEN_SIZE // 2 + 190, 150, 60), 'color': (255, 0, 0), 'text': back_button_text}
    ]

    while True:
        screen.fill((255, 255, 255))
        draw_board(state)
        draw_buttons(buttons)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[0]['rect'].collidepoint(event.pos):
                    solution = search(state)
                    if solution:
                        visualize_solution(solution, state)
                        state = [row[:] for row in initial_state]
                    else:
                        print("No se encontró solución")
                if buttons[1]['rect'].collidepoint(event.pos):
                    state = shuffle_state([row[:] for row in initial_state])
                if buttons[2]['rect'].collidepoint(event.pos):
                    return

def main_menu():
    font = pygame.font.SysFont(None, 72)
    button_font = pygame.font.SysFont(None, 48)
    
    title_text = font.render("Puzle 3x3", True, (0, 0, 0))
    start_button_text = button_font.render("Iniciar", True, (255, 255, 255))
    exit_button_text = button_font.render("Salir", True, (255, 255, 255))
    
    buttons = [
        {'rect': pygame.Rect(SCREEN_SIZE // 2 - 75, SCREEN_SIZE // 2 + 50, 150, 60), 'color': (0, 128, 0), 'text': start_button_text},
        {'rect': pygame.Rect(SCREEN_SIZE // 2 - 75, SCREEN_SIZE // 2 + 120, 150, 60), 'color': (255, 0, 0), 'text': exit_button_text}
    ]
    
    while True:
        screen.fill((173, 216, 230))
        screen.blit(title_text, (SCREEN_SIZE // 2 - title_text.get_width() // 2, SCREEN_SIZE // 2 - 150))
        draw_buttons(buttons)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[0]['rect'].collidepoint(event.pos):
                    game_loop()
                if buttons[1]['rect'].collidepoint(event.pos):
                    pygame.quit()
                    exit()

main_menu()
