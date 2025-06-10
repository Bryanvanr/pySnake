import random

window_x = 720
window_y = 480

class Bot:
    def __init__(self, start_pos):
        self.start_pos = start_pos
        self.reset()

    def reset(self):
        x, y = self.start_pos
        self.pos = [x, y]
        self.body = [[x, y], [x + 10, y], [x + 20, y]]
        self.dir = 'LEFT'
        self.alive = True
        self.respawn_timer = 0
        self.respawn_delay = 180

        self.target_mode = 'food'
        self.target_timer = 0

    def pos_in_direction(self, direction):
        x, y = self.pos
        if direction == 'UP':
            return [x, y - 10]
        if direction == 'DOWN':
            return [x, y + 10]
        if direction == 'LEFT':
            return [x - 10, y]
        if direction == 'RIGHT':
            return [x + 10, y]

    def get_safe_directions(self, avoid):
        directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        safe = []
        for d in directions:
            new_pos = self.pos_in_direction(d)
            if new_pos[0] < 0 or new_pos[0] >= window_x or new_pos[1] < 0 or new_pos[1] >= window_y:
                continue
            if tuple(new_pos) in avoid:
                continue
            safe.append(d)
        return safe

    def get_direction(self, target_pos, avoid):
        safe_dirs = self.get_safe_directions(avoid)

        tx, ty = target_pos
        ax, ay = self.pos
        prioritized = []

        if ax < tx and 'RIGHT' in safe_dirs:
            prioritized.append('RIGHT')
        if ax > tx and 'LEFT' in safe_dirs:
            prioritized.append('LEFT')
        if ay < ty and 'DOWN' in safe_dirs:
            prioritized.append('DOWN')
        if ay > ty and 'UP' in safe_dirs:
            prioritized.append('UP')

        risky_prioritized = []
        if ax < tx and 'RIGHT' not in safe_dirs:
            risky_prioritized.append('RIGHT')
        if ax > tx and 'LEFT' not in safe_dirs:
            risky_prioritized.append('LEFT')
        if ay < ty and 'DOWN' not in safe_dirs:
            risky_prioritized.append('DOWN')
        if ay > ty and 'UP' not in safe_dirs:
            risky_prioritized.append('UP')

        if prioritized and random.random() < 0.7:
            return prioritized[0]
        if risky_prioritized and random.random() < 0.3:
            return risky_prioritized[0]
        if safe_dirs:
            return random.choice(safe_dirs)

        return self.dir

    def move(self):
        self.pos = self.pos_in_direction(self.dir)

    def update(self, food_list, all_bots, player_body):
        if not self.alive:
            self.respawn_timer -= 1
            if self.respawn_timer <= 0:
                self.reset()
            return

        # Switch targeting mode
        self.target_timer -= 1
        if self.target_timer <= 0:
            self.target_mode = random.choices(
                ['food', 'player', 'bot'],
                weights=[0.6, 0.2, 0.2],
                k=1
            )[0]
            self.target_timer = random.randint(90, 180)

        if not food_list:
            return

        # Create set of positions to avoid
        avoid = set()
        avoid.update(tuple(pos) for pos in self.body[1:])
        for b in all_bots:
            if b is not self:
                avoid.update(tuple(pos) for pos in b.body)
        avoid.update(tuple(pos) for pos in player_body)

        # Determine target position
        if self.target_mode == 'food' and food_list:
            target = food_list[0]
        elif self.target_mode == 'player' and player_body:
            target = player_body[0]
        elif self.target_mode == 'bot':
            min_dist = float('inf')
            target = food_list[0]  # fallback
            for b in all_bots:
                if b is not self and b.alive and b.body:
                    bx, by = b.body[0]
                    dist = abs(self.pos[0] - bx) + abs(self.pos[1] - by)
                    if dist < min_dist:
                        min_dist = dist
                        target = [bx, by]
        else:
            target = food_list[0]

        if random.random() < 0.2:
            pass  # Keep current direction
        else:
            self.dir = self.get_direction(target, avoid)

        self.move()
        self.body.insert(0, list(self.pos))
        if self.pos in food_list:
            food_list.remove(self.pos)
        else:
            self.body.pop()

    def die(self):
        self.alive = False
        self.respawn_timer = self.respawn_delay
        dropped = self.body.copy()
        self.body.clear()
        self.pos = [-100, -100]
        return dropped