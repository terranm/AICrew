# battle.py

class Battle:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy

    def start_battle(self):
        print(f"Battle start: {self.player.name} vs {self.enemy.name}")

    def end_battle(self):
        print("Battle end")