# bot.py

def get_ai_direction(ai_pos, ai_dir, food_pos):
    ax, ay = ai_pos
    fx, fy = food_pos

    new_dir = ai_dir

    # Prefer horizontal moves
    if ax < fx and ai_dir != 'LEFT':
        new_dir = 'RIGHT'
    elif ax > fx and ai_dir != 'RIGHT':
        new_dir = 'LEFT'
    elif ay < fy and ai_dir != 'UP':
        new_dir = 'DOWN'
    elif ay > fy and ai_dir != 'DOWN':
        new_dir = 'UP'

    return new_dir

# Update bot movement
def bot_movement_update(ai_dir, ai_pos):
    if ai_dir == 'UP':
        ai_pos[1] -= 10
    if ai_dir == 'DOWN':
        ai_pos[1] += 10
    if ai_dir == 'LEFT':
        ai_pos[0] -= 10
    if ai_dir == 'RIGHT':
        ai_pos[0] += 10
    return ai_pos