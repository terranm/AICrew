# user.py

class User:
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.gold = 100
        self.deck = []

    def add_card_to_deck(self, card):
        self.deck.append(card)

    def remove_card_from_deck(self, card):
        self.deck.remove(card)

    def gain_gold(self, amount):
        self.gold += amount

    def lose_gold(self, amount):
        self.gold -= amount