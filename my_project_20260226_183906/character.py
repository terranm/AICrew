
class Character:
    def __init__(self, name, health, attack, defense):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack = attack
        self.defense = defense

    def take_damage(self, damage):
        actual_damage = max(0, damage - self.defense)
        self.health -= actual_damage
        print(f"{self.name}이(가) {actual_damage}의 데미지를 입었습니다. 현재 체력: {self.health}")
        if self.health <= 0:
            print(f"{self.name}이(가) 쓰러졌습니다!")

    def is_alive(self):
        return self.health > 0
