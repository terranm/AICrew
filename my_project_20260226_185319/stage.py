# stage.py

class Stage:
    def __init__(self, name, description, enemy, boss, reward):
        self.name = name
        self.description = description
        self.enemy = enemy
        self.boss = boss
        self.reward = reward

    def start(self):
        print(f"Starting {self.name}: {self.description}")

    def end(self):
        print(f"Stage {self.name} cleared. Reward: {self.reward}")