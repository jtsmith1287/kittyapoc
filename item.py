"""
Module containing item info and methods
"""


import random


WEAPON_LIST = [
               ("Purse", (1, 1), None),
               ("walking Stick", (1, 2), None),
               ("Brick", (2, 3), None),
               ("Shovel", (3, 4), None)
             ]

FOOD_LIST = [
             ("stale bread", None, (1,2)),
             ("rotten apple", None, (2, 2)),
             ("dog chewed steak", None, (3, 5)),
             ("Snapple", None, (3, 4)),
             ("granola bar", None, (4, 7)),
             ("still hot pizza?", None, (10, 10)),
             ]


def generateNextWeapon():
    
    name, dmg, hlg = WEAPON_LIST.pop(0)
    item = Item(name, dmg, hlg)
    return item

def getRandomFood():
    
    name, dmg, hlg = random.choice(FOOD_LIST)
    item = Item(name, dmg, hlg)
    return item


class Item(object):
    
    def __init__(self, name, damage=None, healing=None):
        
        self.name = name
        self._damage = damage
        self._healing = healing
    
    def __str__(self):
        
        return self.name
    
    def getDamage(self):
        
        return random.randint(self._damage[0], self._damage[1])
    
    def getHealing(self):
        
        return random.randint(self._healing[0], self._healing[1])

