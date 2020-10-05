class Damage:
    def __init__(self, amount: float, type: str):
        self.amount = amount
        self.type = type

    def __str__(self):
        return str(self.amount) + self.type

class Unit:
    def __init__(self, name: str, race: str, hp: int, armor: int,
                size: str, ground_attack: Damage, air_attack: Damage,
                ground_upgrade: str, air_upgrade: str, shield: int = 0):
        self.name = name
        self.race = race
        self.hp = hp
        self.armor = armor
        self.shield = shield
        self.size = size
        self.ground_attack = ground_attack
        self.air_attack = air_attack
        self.ground_upgrade = ground_upgrade
        self.air_upgrade = air_upgrade

    def describe(self):
        return ' '.join([str(i) for i in (self.race, self.name, "has hp and shields", self.hp, self.shield,
              "does ground attack", self.ground_attack, "+", self.ground_upgrade,
              "with air attack", self.air_attack, "+", self.air_upgrade,
              "and size", self.size)])

    def __str__(self):
        return self.describe()
