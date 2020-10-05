from unit import Unit, Damage
from enum import Enum
import numpy as np
import copy


class ColumnHeaders(Enum):
    NAME = "name"
    HP = "hp"
    ARMOR = "armor"
    SHIELD = "shield"
    SIZE = "size"
    GROUND_ATTACK = "ground_attack"
    GROUND_UPGRADE = "ground_upgrade"
    AIR_ATTACK = "air_attack"
    AIR_UPGRADE = "air_upgrade"


class StarcraftColumn:
    def __init__(self, header: str, transform=lambda x: x):
        self.header = header
        self._transform = transform

    def get_data(self, v):
        return self._transform(v)


def damage_transform(s):
    amount = float(''.join(filter(str.isdigit, s)))
    type = ''.join(filter(str.isalpha, s))
    return Damage(amount, type)


# name size armor hp shield GA AA GU AU
COLUMNS = (
    StarcraftColumn(ColumnHeaders.NAME, transform=lambda x: x.replace('_', ' ')),
    StarcraftColumn(ColumnHeaders.SIZE),
    StarcraftColumn(ColumnHeaders.ARMOR, transform=int),
    StarcraftColumn(ColumnHeaders.HP, transform=int),
    StarcraftColumn(ColumnHeaders.GROUND_ATTACK, transform=damage_transform),
    StarcraftColumn(ColumnHeaders.AIR_ATTACK, transform=damage_transform),
    StarcraftColumn(ColumnHeaders.GROUND_UPGRADE, transform=int),
    StarcraftColumn(ColumnHeaders.AIR_UPGRADE, transform=int),
)

PROTOSS_COLUMNS = list(COLUMNS)
PROTOSS_COLUMNS.insert(4, StarcraftColumn(ColumnHeaders.SHIELD, transform=int))
PROTOSS_COLUMNS = tuple(PROTOSS_COLUMNS)


def import_race_data(race="protoss", path="protoss_stats.txt", columns=COLUMNS):
    race_data = open(path).read()
    units = {}

    for line in race_data.split('\n'):
        if not line:
            continue
        line = ' '.join(line.split()).split(' ')
        unit_map = {c.header.value: c.get_data(v) for c, v in zip(columns, line)}
        unit_map['race'] = race
        unit = Unit(**unit_map)
        units[unit.name] = unit

    return units


protoss = import_race_data(race="protoss", path="protoss_stats.txt", columns=PROTOSS_COLUMNS)
zerg = import_race_data(race="zerg", path="zerg_stats.txt")
terran = import_race_data(race="terran", path="terran_stats.txt")

flying = [protoss["Observer"], protoss["Shuttle"], protoss["Scout"], protoss["Carrier"], protoss["Arbiter"],
          protoss["Corsair"],
          zerg["Overlord"], zerg["Mutalisk"], zerg["Scourge"], zerg["Queen"], zerg["Guardian"], zerg["Devourer"],
          terran["Wraith"], terran["Dropship"], terran["Science Vessel"], terran["Battlecruiser"], terran["Valkyrie"]]

explosive_map = {'L': 1, 'M': .75, 'S': .5}
concussive_map = {'L': .5, 'M': .75, 'S': 1}


def calculate_shots(attacker: Unit, attack_upgrade, defender: Unit, armor_upgrade) -> int:
    shots = 0
    if defender in flying:
        damage = copy.deepcopy(attacker.air_attack)
        damage.amount += (attacker.air_upgrade * attack_upgrade)
    else:
        damage = copy.deepcopy(attacker.ground_attack)
        damage.amount += (attacker.ground_upgrade * attack_upgrade)

    armor = armor_upgrade * defender.armor
    shields = defender.shield

    while shields > 0:
        shots += 1
        shields -= damage.amount

    hp = defender.hp - shields

    if damage.type == 'e':
        damage.amount *= explosive_map[defender.size]
    elif damage.type == 'c':
        damage.amount *= concussive_map[defender.size]

    while hp > 0:
        shots += 1
        hp -= max((damage.amount + armor), .5)

    return shots


if __name__ == '__main__':
    units = {**terran, **protoss, **zerg}
    defender = units["Dragoon"]
    attacker = units["Siege Tank"]

    damage_table = np.zeros(16).reshape(4, 4)
    for i in range(4):
        for j in range(4):
            damage_table[i][j] = calculate_shots(defender, i, attacker, j)

    print(damage_table)
