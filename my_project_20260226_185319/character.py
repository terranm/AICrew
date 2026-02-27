# character.py

class Character:
    def __init__(self, name, description, initial_deck, skill):
        self.name = name
        self.description = description
        self.deck = initial_deck
        self.skill = skill
        self.health = 100

    def use_skill(self, target):
        print(f"{self.name} uses skill {self.skill} on {target.name}")

    def __repr__(self):
        return self.name