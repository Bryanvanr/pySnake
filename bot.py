# bot.py

import random

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

    def get_direction(self, food_pos):
        ax, ay = self.pos
        fx, fy = food_pos
        new_dir = self.dir

        # Prefer horizontal moves
        if ax < fx and self.dir != 'LEFT':
            new_dir = 'RIGHT'
        elif ax > fx and self.dir != 'RIGHT':
            new_dir = 'LEFT'
        elif ay < fy and self.dir != 'UP':
            new_dir = 'DOWN'
        elif ay > fy and self.dir != 'DOWN':
            new_dir = 'UP'

        self.dir = new_dir

    def move(self):
        if self.dir == 'UP':
            self.pos[1] -= 10
        elif self.dir == 'DOWN':
            self.pos[1] += 10
        elif self.dir == 'LEFT':
            self.pos[0] -= 10
        elif self.dir == 'RIGHT':
            self.pos[0] += 10

    def update(self, food_list):
        if not self.alive:
            self.respawn_timer -= 1
            if self.respawn_timer <= 0:
                self.reset()
            return

        if not food_list:
            return

        self.get_direction(food_list[0])
        self.move()

        # Eat food or move forward
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
