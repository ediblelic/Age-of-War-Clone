import random
class Enemy:
    def __init__(self, sword_man_cost, archer_cost):
        self.sword_man_cost = sword_man_cost
        self.archer_cost = archer_cost
        self.enemy_coins = 30
        self.shoutdown = 0
    def release_sprite(self):
        self.shoutdown += 0.1
        self.ai = random.randint(0, 100)
        if self.enemy_coins >= self.sword_man_cost and self.shoutdown >= 51 and self.ai == 22:
            self.shoutdown = 0
            self.enemy_coins -= self.sword_man_cost
            return "Sword_man"
        if self.enemy_coins >= self.archer_cost and self.shoutdown >= 61 and self.ai == 33:
            self.shoutdown = 0
            self.enemy_coins -= self.archer_cost
            return "Archer"
        return None
