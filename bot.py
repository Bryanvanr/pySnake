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
            # Stay in bounds
            if new_pos[0] < 0 or new_pos[0] >= window_x or new_pos[1] < 0 or new_pos[1] >= window_y:
                continue
            # Avoid collisions
            if tuple(new_pos) in avoid:
                continue
            safe.append(d)
        return safe

    def get_direction(self, food_pos, avoid):
        safe_dirs = self.get_safe_directions(avoid)

        # Simple pathfinding: prefer safe directions toward food
        fx, fy = food_pos
        ax, ay = self.pos
        prioritized = []

        if ax < fx and 'RIGHT' in safe_dirs:
            prioritized.append('RIGHT')
        if ax > fx and 'LEFT' in safe_dirs:
            prioritized.append('LEFT')
        if ay < fy and 'DOWN' in safe_dirs:
            prioritized.append('DOWN')
        if ay > fy and 'UP' in safe_dirs:
            prioritized.append('UP')

        for d in prioritized:
            return d

        if safe_dirs:
            return random.choice(safe_dirs)

        return self.dir  # No safe move, continue current dir

    def move(self):
        self.pos = self.pos_in_direction(self.dir)

    def update(self, food_list, all_bots, player_body):
        if not self.alive:
            self.respawn_timer -= 1
            if self.respawn_timer <= 0:
                self.reset()
            return

        if not food_list:
            return

        # Create set of positions to avoid
        avoid = set()
        avoid.update(tuple(pos) for pos in self.body[1:])  # self
        for b in all_bots:
            if b is not self:
                avoid.update(tuple(pos) for pos in b.body)
        avoid.update(tuple(pos) for pos in player_body)

        # Decide direction and move
        self.dir = self.get_direction(food_list[0], avoid)
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
