# deck.py

class Deck:
    def __init__(self, cards=None):
        if cards is None:
            self.cards = []
        else:
            self.cards = cards

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self, card):
        self.cards.remove(card)

    def shuffle(self):
        import random
        random.shuffle(self.cards)

    def __repr__(self):
        return f"Deck with {len(self.cards)} cards"
