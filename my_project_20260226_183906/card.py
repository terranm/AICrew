
class Card:
    def __init__(self, name, attack, defense):
        self.name = name
        self.attack = attack
        self.defense = defense

    def use(self, target):
        print(f"{self.name} 카드를 사용해서 {target.name}을 공격합니다!")
        target.take_damage(self.attack)


