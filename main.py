import math
import random
from enum import Enum, auto


class Style(Enum):  # value returns index of gear acc bonus, value+5 returns index of gear def bonus
    STAB = 0
    SLASH = auto()
    CRUSH = auto()
    RANGED = auto()
    MAGIC = auto()

class Stance(Enum): # invisible atk, def, strength boosts: strength last to match range/mage stances
    AGGRESSIVE = (0, 0, 3)
    ACCURATE = (3, 0, 0)
    DEFENSIVE = (0, 3, 0)
    CONTROLLED = (1, 1, 1)
    RAPID = (0, 0)
    LONGRANGE = (0, 3)
    LONGMAGE = (1, 3)

# TODO: try flag enum for attack styles on weapon classes

class Attribute(Enum):
    DEMON = auto()  # demonbane weapons/spells, holy water
    DRAGON = auto()  # dhcb/lance
    # Fiery = auto()
    # Golem = auto()
    # Kalphite = auto()  # keris
    # Penance = auto()  # ba attacks do +5
    PLAYER = auto()  # mage def is calculated differently
    # Shade = auto()
    SLAYER = auto()  # slayer helm and slayer dart (e) are calculated differently
    # Spectral = auto()
    UNDEAD = auto()  # salve does extra, crumble undead works
    # Vampyre = auto()  # only silver weapons deal damage, flails deal extra dmg
    WILDERNESS = auto()  # chainmace, craws bow, thammarons sceptre
    XERICIAN = auto()  # tbow capped to 350 instead of 250 magic

spell_max_hits = {
    'Wind Strike': 2,
    'Water Strike': 4,
    'Earth Strike': 6,
    'Fire Strike': 8,
    'Wind Bolt': 9,
    'Water Bolt': 10,
    'Earth Bolt': 11,
    'Fire Bolt': 12,
    'Wind Blast': 13,
    'Water Blast': 14,
    'Earth Blast': 15,
    'Fire Blast': 16,
    'Wind Wave': 17,
    'Water Wave': 18,
    'Earth Wave': 19,
    'Fire Wave': 20,
    'Wind Surge': 21,
    'Water Surge': 22,
    'Earth Surge': 23,
    'Fire Surge': 24,
    'Smoke Rush': 14,
    'Shadow Rush': 15,
    'Blood Rush': 16,
    'Ice Rush': 17,
    'Smoke Burst': 18,
    'Shadow Burst': 19,
    'Blood Burst': 21,
    'Ice Burst': 22,
    'Smoke Blitz': 23,
    'Shadow Blitz': 24,
    'Blood Blitz': 25,
    'Ice Blitz': 26,
    'Smoke Barrage': 27,
    'Shadow Barrage': 28,
    'Blood Barrage': 29,
    'Ice Barrage': 30,
    'Iban Blast': 25,
    'Magic Dart': 0,
    'Saradomin Strike': 20,
    'Flames of Zamorak': 20,
    'Claws of Guthix': 20,
    'Crumble Undead': 15
}
# spell types: fire (tome)

class Prayer:
    def __init__(self, name, numbers:[]):
        self.name = name
        self.mel_atk = numbers[0]
        self.mel_str = numbers[1]
        self.mel_def = numbers[2]
        self.rng_acc = numbers[3]
        self.rng_str = numbers[4]
        self.mg_acc = numbers[5]
        self.mg_str = numbers[6]
        self.mg_def = numbers[7]
        self.drain = numbers[8]

prayers_ = {
    # atk, str, def, range acc, range str, mage acc, mage str, mage def, drain
    'Clarity of Thought':   (0.05,0,0,0,0,0,0,0,3),
    'Improved Reflexes':    (0.1,0,0,0,0,0,0,0,6),
    'Incredible Reflexes':  (0.15,0,0,0,0,0,0,0,12),
    'Burst of Strength':    (0,0.05,0,0,0,0,0,0,3),
    'Superhuman Strength':  (0,0.1,0,0,0,0,0,0,6),
    'Ultimate Strength':    (0,0.15,0,0,0,0,0,0,12),
    'Thick Skin':           (0,0,0.05,0,0,0,0,0,3),
    'Rock Skin':            (0,0,0.1,0,0,0,0,0,6),
    'Steel Skin':           (0,0,0.15,0,0,0,0,0,12),
    'Chivalry':             (0.15,0.18,0.2,0,0,0,0,0,24),
    'Piety':                (0.2,0.23,0.25,0,0,0,0,0,24),
    'Mystic Will':          (0,0,0,0,0,0.05,0,0.05,3),
    'Mystic Lore':          (0,0,0,0,0,0,0.1,0.1,6),
    'Mystic Might':         (0,0,0,0,0,0,0.15,0.15,12),
    'Augury':               (0,0,0.25,0,0,0.25,0,0.25,24),
    'Sharp Eye':            (0,0,0,0.05,0.05,0,0,0,3),
    'Hawk Eye':             (0,0,0,0.1,0.1,0,0,0,6),
    'Eagle Eye':            (0,0,0,0.15,0.15,0,0,0,12),
    'Rigour':               (0,0,0.25,0.2,0.23,0,0,0,24)
}
prayers = {}
def init_prayers():
    for p in prayers_:
        prayers[p.lower()] = Prayer(p.lower(), prayers_[p])

class Mob:
    def __init__(self, stats, potion, prayer, equipment, stance, attributes, custom):
        # stats: current and max (for dh, bludgeon)
        # potion
        # prayer
        self.stats = {
            "attack":   (99,99),
            "strength": (99,99),
            "defence":  (99,99),
            "ranged":   (99,99),
            "magic":    (99,99),
            "hp":       (99,99),
            "prayer":   (99,99)
        }
        # self.potion = []
        self.prayer:[Prayer] = [prayers['piety']]

        # spell that the attacker is using?

        # equipment
        self.equipment = {
            "head": None,
            "cape": None,
            "neck": None,
            "ammo": None,
            "weapon": None,
            "body": None,
            "legs": None,
            "offhand": None,
            "gloves": None,
            "boots": None,
            "ring": None,
            "custom": [0 for _ in range(0,14)]
        }
        self.gear = [0 for _ in range(0,14)]
        for item in self.equipment:
            if item is not None:
                for i,x in enumerate(item):
                    self.gear[i] += x

        # stance: assume NPCs use controlled
        self.stance:Stance = Stance.CONTROLLED

        # attributes
        self.attributes:[Attribute] = []

        # custom effects (ice, guards. verz p1? dmg reduction: dusk/dawn, kraken, zulrah)
            # cap (corp), reroll (zulrah, seren), double roll (verzik)
        self.custom_effects = []

        # custom max hits?

    def check_effects(self):
        effects = []
        for slot, item in self.equipment[0:-1]:
            if item is not None:
                if item.effects is not None:
                    # check that nulled items aren't on there: slayer helm & salve
                    pass # add to a list of effects
                if item.set_effects is not None:  # inq, void. crystal?
                    pass
        return effects

# json list of mobs with stats, attributes, special effects
# find out how to import them

class Item:
    def __init__(self, stats, slot):
        # stats: do a lookup from a table?
            # sl/st/cr/rng/mg acc, sl/st/cr/rng/mg def, mel/rng/mg str, pray
        self.stats = stats
        self.slot = slot
        # special effects
            # nulls: does not apply when X item is worn
        self.effects = []
        # set effects: when used with X other items add Y effect
            # which other items
            # effect when that happens
        self.set_effects = []
        # weight

class Weapon(Item):
    def __init__(self, stats, slot, speed, weapon_class):
        super().__init__(stats, slot)
        # speed
        self.speed = speed  # ticks
        # class: allowed attack options/stances
        self.weapon_class = weapon_class
        # special attack
            # cost, effect: acc increase, dmg increase
        self.special = None
        # custom max formula: tridents
        self.max = None
        # # custom accuracy formula
        # self.acc = None
        # # accuracy/damage multipliers
        # self.dmg_mult = None
        # self.acc_mult = None

class Potion(Enum):
#     Attack = ((lambda x: int (3 + 0.1 * x)), 0, 0, 0, 0)
#     Strength = (0, (lambda x: int (3 + 0.1 * x)), 0, 0, 0)
#     Defence = (0, 0, (lambda x: int (3 + 0.1 * x)), 0, 0)
#     Ranged = (0, 0, 0, (lambda x: int (3 + 0.1 * x)), 0)
#     Magic = (0, 0, 0, 0, 4)
#     Super_Attack = ((lambda x: int (5 + 0.15 * x)), 0, 0, 0, 0)
#     Super_Strength = (0, (lambda x: int (5 + 0.15 * x)), 0, 0, 0)
#     Super_Defence = (0, 0, (lambda x: int (5 + 0.15 * x)), 0, 0)
#     Super_Ranged = (0, 0, 0, (lambda x: int (5 + 0.15 * x)), 0)
#     Super_Magic = (0, 0, 0, 0, (lambda x: int (5 + 0.15 * x)))
    pass

# calcs accuracy given a mar and mdr
def calc_accuracy(mar: int, mdr: int) -> float:
    if mar > mdr:
        return 1 - (mdr+2)/(2*(mar+1))  # 1 - (d+2)/(2a+2)
    else:
        return mar/(2*(mdr+1))  # a/2d+2

def roll_accuracy(mar: int, mdr: int) -> bool:
    return random.randint(0, mar) > random.randint(0, mdr)

def default_max(style:Style, level:dict, prayer:Prayer, gear_bonus:int, stance: Stance) -> int:
    if style in [Style.STAB, Style.SLASH, Style.CRUSH]:
        pray_boost = prayer.mel_str
        stance_boost = stance.value[2]
        lvl = level['attack']
    elif style == Style.RANGED:
        pray_boost = prayer.rng_str
        stance_boost = stance.value[0]
        lvl = level['ranged']
    elif style == Style.MAGIC:
        # raise warning if it tries the default max hit formula because it should have used a custom one already?
        # pray_boost = prayer.mg_str
        # stance_boost = 0
        print("WARNING: default max hit formula is being used for mage - make sure this is a NPC")
        pray_boost = prayer.mg_str
        stance_boost = stance.value[0]
        lvl = level['magic']
    else:
        print("max hit: style is invalid?" + style.__str__())
        raise
    effective_level = int(lvl * (1+ pray_boost)) + stance_boost + 8
    # void modifies effective level
    max_hit = int (0.5 + effective_level * (gear_bonus + 64) / 640)
    return max_hit

# calcs mar. additional effects not yet factored
def max_atk_roll(style:Style, level:int, prayer:Prayer, gear,
                 stance:Stance):
    if style in (Style.STAB, Style.SLASH, Style.CRUSH):
        pray_boost = prayer.mel_atk
        stance_boost = stance.value[0]
    elif style == Style.RANGED:
        pray_boost = prayer.rng_acc
        stance_boost = stance.value[0]
    elif style == Style.MAGIC:
        pray_boost = prayer.mg_acc
        stance_boost = stance.value[0]
        # if gear.weapon.weapon_class == trident:
        #     stance_boost = stance.value[1]
    else:
        print("mar: style is invalid?" + style.__str__())
        raise
    effective_level = (math.trunc(level * (1 + pray_boost)) + stance_boost) + 8
    # then void bonus then floor

    # for effect in effects:
    #   effective_level *= (1 + effect)

    base_mar = effective_level * (gear + 64)
    # slayer helm, salve etc. multiply at the end
    return base_mar

def max_def_roll(style:Style, level:(int, int), prayer:Prayer, gear,
                 stance:Stance, APlayer:bool, BPlayer:bool):
    #TODO: why is level a tuple?

    # Calc melee def: not necessary if magic pvm
    effective_def_level = int (level[0] * (1 + prayer.mel_def)) + stance.value + 8
    # other effects here: torags with aotd?

    # Calc magic accuracy if style is magic
    if style == Style.MAGIC:
        pray_boost = prayer.mg_def
        stance_boost = stance.value[1]
        effective_magic_level = (math.trunc(level[0] * (1 + prayer.mel_def)) + stance.value) + 8
        # other effects: none currently

        # if APlayer and BPlayer:  # pvp: 50/50 mage and def (apparently never happened?)
        #     effective_def_level = int (0.5 * effective_magic_level + 0.5 * effective_def_level)
        # elif not APlayer and

        if BPlayer:  # 70/30 mage and def
            effective_def_level = math.trunc(0.7 * effective_magic_level) + math.trunc(0.3 * effective_def_level)
        else: effective_def_level = effective_magic_level

    mdr = effective_def_level * (gear + 64)
    # other effects here: are there any?
    return mdr

def hit(style, spell, A:Mob, D:Mob):
    get_max(1,1,A)
    pass

def get_max(style, spell, mob:Mob):
    if spell is not None:
        base_max_hit = spell_max_hits[spell.lower()]
        # apply modifiers like chaos gauntlets
        for effect in mob.check_effects():
            # apply the effect if it goes here. how to know? priority?
            # tick off the effect as having been applied
            pass
        return base_max_hit
    # elif mob.equipment['weapon'].max is not None:  # has custom damage formula
    #     return parse_max(mob.equipment['weapon'].max)
    else:
        max_hit = default_max(style, mob.stats, mob.prayer[0], mob.gear[max(11, style.value+8)], mob.stance)
        for effect in mob.check_effects():
            # apply the effect if it goes here. how to know? priority?
            # tick off the effect as having been applied
            pass
        return max_hit


def main():
    if __name__ == "__main__":
        print("main function")
        print(calc_accuracy(13223, 3231))


init_prayers()

a = 'slash'
print(Style[a.upper()].value)

# asdf = Mob()