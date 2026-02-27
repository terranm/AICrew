# card.py

class Card:
    def __init__(self, name, description, attack, defense, skill):
        self.name = name
        self.description = description
        self.attack = attack
        self.defense = defense
        self.skill = skill

    def use_skill(self, target):
        print(f"{self.name} uses {self.skill} on {target.name}")

    def __repr__(self):
        return self.name