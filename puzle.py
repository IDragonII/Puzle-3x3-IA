import os
import pygame
from heapq import heappush, heappop
import itertools
import time

SCREEN_SIZE = 500
TILE_SIZE = SCREEN_SIZE // 3

pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Puzle 3x3")

# dragon
image_folder = 'dragon'
# imagen
#image_folder = 'imagen'
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
    pygame.display.flip()

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

# dragon
goal_state = [[1, 2, 3], [0, 4, 5], [6, 7, 8]]
# imagen
#goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

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
        print("\nFrontier:")
        for f in frontier:
            print(f[3])
        print("\nExplored:")
        for e in explored:
            print(e)
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
    time.sleep(0.2)
    for move in solution:
        state = result(state, move)
        draw_board(state)
        time.sleep(0.2)
    font = pygame.font.SysFont(None, 48)

    text_background_rect = pygame.Rect(SCREEN_SIZE // 2 - 150, SCREEN_SIZE // 2 - 50, 350, 100)
    pygame.draw.rect(screen, (255, 255, 255), text_background_rect)
    
    text = font.render("Solución encontrada!", True, (0, 128, 0))
    screen.blit(text, (SCREEN_SIZE // 2 - text.get_width() // 2, SCREEN_SIZE // 2 - text.get_height() - 10))
    
    moves_text = font.render(f"Movimientos: {len(solution)}", True, (0, 128, 0))
    screen.blit(moves_text, (SCREEN_SIZE // 2 - moves_text.get_width() // 2, SCREEN_SIZE // 2 + 10))
    
    pygame.display.flip()

# dragon
initial_state = [[1, 5, 2], [0, 6, 3], [7, 4, 8]]
# imagen
#initial_state = [[1, 5, 2], [0, 3, 6], [7, 8, 4]]
solution = search(initial_state)

if solution:
    visualize_solution(solution, initial_state)
else:
    print("No se encontró solución")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()