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

# Game over function
def g_over():
    font = pygame.font.SysFont('times new roman', 50)
    g_over_surface = font.render('Score : ' + str(score), True, red)
    g_over_rect = g_over_surface.get_rect()
    g_over_rect.midtop = (window_x / 2, window_y / 4)
    g_window.blit(g_over_surface, g_over_rect)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    quit()

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
                print(f"Bot collided with another bot!")
                food_list.extend(b1.die())
                break
            # Head-on collision between bots
            if b1.pos == b2.pos:
                print("Bots collided head-on!")
                food_list.extend(b1.die())
                food_list.extend(b2.die())


# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                change_to = 'UP'
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                change_to = 'DOWN'
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                change_to = 'LEFT'
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                change_to = 'RIGHT'

    # Update bots
    for b in bots:
        b.update(food_list)

    # Update player direction and movement
    dir = s_pos_update(dir)
    s_pos = s_movement_update(dir)

    # --- Player eats food ---
    s_body.insert(0, list(s_pos))
    player_ate = False
    for food in food_list:
        if s_pos == food:
            score += 10
            food_list.remove(food)
            player_ate = True
            break
    if not player_ate:
        s_body.pop()

    # --- Ensure food is present ---
    if len(food_list) < 1:
        food_list.append(spawn_food())

    g_window.fill(black)

    # Draw player
    for pos in s_body:
        pygame.draw.rect(g_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

    # Draw all bots
    for b in bots:
        for part in b.body:
            pygame.draw.rect(g_window, blue, pygame.Rect(part[0], part[1], 10, 10))

    # Draw food
    for food in food_list:
        pygame.draw.rect(g_window, white, pygame.Rect(food[0], food[1], 10, 10))

    # Wall collisions
    if s_pos[0] < 0 or s_pos[0] > window_x - 10 or s_pos[1] < 0 or s_pos[1] > window_y - 10:
        g_over()

    # Player self-collision
    for block in s_body[1:]:
        if s_pos == block:
            g_over()

    # Player hits any bot
    for b in bots:
        for part in b.body:
            if s_pos == part:
                g_over()

    # Bot hits player
    for b in bots:
        if b.alive and b.pos in s_body:
            food_list.extend(b.die())
    
    # Check bot on bot collision      
    check_bot_collisions(bots, food_list)

    # Head-on collision
    for b in bots:
        if b.alive and b.pos == s_pos:
            g_over()

    show_score(1, white, 'times new roman', 20)
    pygame.display.update()
    fps.tick(s_speed)