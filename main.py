import pygame
import time
import random

# Bot settings etc
import bot
# Init multiple bots
bots = [
    bot.Bot([650, 400]),
    bot.Bot([400, 300]),
    bot.Bot([300, 100])
]

s_speed = 10
window_x = 720
window_y = 480

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 10, 10)
green = pygame.Color(0, 255, 10)
blue = pygame.Color(0, 0, 255)

pygame.init()
pygame.display.set_caption('snek')
g_window = pygame.display.set_mode((window_x, window_y))
fps = pygame.time.Clock()

# Player snake variables
s_pos = [50, 50]
s_body = [[50, 50], [40, 50], [30, 50]]
dir = 'RIGHT'
change_to = dir
score = 0

# Food variables
def spawn_food():
    return [random.randrange(1, (window_x // 10)) * 10,
            random.randrange(1, (window_y // 10)) * 10]

food_list = [spawn_food()]

# Show score function
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    g_window.blit(score_surface, score_rect)
    
# Update player direction
def s_pos_update(dir):
    if change_to == 'UP' and dir != 'DOWN':
        dir = 'UP'
    if change_to == 'DOWN' and dir != 'UP':
        dir = 'DOWN'
    if change_to == 'LEFT' and dir != 'RIGHT':
        dir = 'LEFT'
    if change_to == 'RIGHT' and dir != 'LEFT':
        dir = 'RIGHT'
    return dir

# Update player movement
def s_movement_update(dir):
    if dir == 'UP':
        s_pos[1] -= 10
    if dir == 'DOWN':
        s_pos[1] += 10
    if dir == 'LEFT':
        s_pos[0] -= 10
    if dir == 'RIGHT':
        s_pos[0] += 10
    return s_pos

# Bot on Bot collision check
def check_bot_collisions(bots, food_list):
    for b1 in bots:
        if not b1.alive:
            continue
        for b2 in bots:
            if b1 == b2 or not b2.alive:
                continue
            # Bot head hits other bot body
            if b1.pos in b2.body:
                food_list.extend(b1.die())
                break
            # Head-on collision between bots
            if b1.pos == b2.pos:
                food_list.extend(b1.die())
                food_list.extend(b2.die())

# Input handling
def handle_input():
    global change_to
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            key_map = {
                pygame.K_UP: 'UP', pygame.K_w: 'UP',
                pygame.K_DOWN: 'DOWN', pygame.K_s: 'DOWN',
                pygame.K_LEFT: 'LEFT', pygame.K_a: 'LEFT',
                pygame.K_RIGHT: 'RIGHT', pygame.K_d: 'RIGHT',
            }
            change_to = key_map.get(event.key, change_to)
# Bot update logic
def update_bots():
    for b in bots:
        b.update(food_list, bots, s_body)

# Player movement/eating
def update_player():
    global dir, s_pos, score
    dir = s_pos_update(dir)
    s_pos = s_movement_update(dir)

    s_body.insert(0, list(s_pos))

    for food in food_list:
        if s_pos == food:
            score += 10
            food_list.remove(food)
            return
    s_body.pop()

# Draw game objects
def draw_elements():
    g_window.fill(black)
    for pos in s_body:
        pygame.draw.rect(g_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

    for b in bots:
        for part in b.body:
            pygame.draw.rect(g_window, blue, pygame.Rect(part[0], part[1], 10, 10))

    for food in food_list:
        pygame.draw.rect(g_window, white, pygame.Rect(food[0], food[1], 10, 10))

# Game over condition check
def check_game_over():
    if s_pos[0] < 0 or s_pos[0] > window_x - 10 or s_pos[1] < 0 or s_pos[1] > window_y - 10:
        return True
    if s_pos in s_body[1:]:
        return True
    for b in bots:
        if s_pos in b.body:
            return True
        if b.alive and b.pos in s_body:
            food_list.extend(b.die())
        if b.alive and b.pos == s_pos:
            return True
    check_bot_collisions(bots, food_list)
    return False

# Game over screen
def show_game_over():
    font = pygame.font.SysFont('times new roman', 50)
    g_window.fill(black)
    game_over_surface = font.render('Game Over', True, red)
    game_over_rect = game_over_surface.get_rect(center=(window_x / 2, window_y / 4))
    g_window.blit(game_over_surface, game_over_rect)

    score_surface = font.render('Score: ' + str(score), True, white)
    score_rect = score_surface.get_rect(center=(window_x / 2, window_y / 2))
    g_window.blit(score_surface, score_rect)

    restart_surface = pygame.font.SysFont('times new roman', 30).render('Press R to Restart or Q to Quit', True, white)
    restart_rect = restart_surface.get_rect(center=(window_x / 2, window_y * 3 / 4))
    g_window.blit(restart_surface, restart_rect)

    pygame.display.flip()

    # Wait for player input
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()


# Main loop
def main_game_loop():
    global s_pos, s_body, dir, change_to, score, food_list, bots

    # Reset state
    s_pos = [50, 50]
    s_body = [[50, 50], [40, 50], [30, 50]]
    dir = 'RIGHT'
    change_to = dir
    score = 0
    food_list = [spawn_food()]
    bots = [bot.Bot([650, 400]), bot.Bot([400, 300]), bot.Bot([300, 100])]

    while True:
        handle_input()
        update_bots()
        update_player()

        if len(food_list) < 1:
            food_list.append(spawn_food())

        draw_elements()

        if check_game_over():
            show_game_over()
            return

        show_score(1, white, 'times new roman', 20)
        pygame.display.update()
        fps.tick(s_speed)

# Start the script
if __name__ == "__main__":
    while True:
        main_game_loop()