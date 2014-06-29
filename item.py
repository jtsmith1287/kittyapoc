"""
Module containing item info and methods
"""


import random


weapon_list = [
               ("Purse", (1, 1), None),
               ("Walking Stick", (1, 2), None),
               ("Brick", (2, 3), None),
               ("Shovel", (3, 4), None),
               ("Revolver", (5, 7), None),
               ("Crossbow", (10, 12), None),
               ("Shotgun", (12, 14), None),
               ("AR-15 Assult Rifle", (14, 17), None),
               ("Katana", (18, 20), None),
               ("Chainsaw", (21, 25), None),
               ("Rocket Launcher", (30, 30), None),
             ]

food_list = [
             ("stale bread", None, (3,5)),
             ("stale bagels", None, (3,5)),
             ("rotten apple", None, (4, 5)),
             ("rotten banana", None, (4, 5)),
             ("dog chewed steak", None, (5, 7)),
             ("half-eaten pie", None, (5, 7)),
             ("Snapple", None, (5, 6)),
             ("prune juice", None, (4, 6)),
             ("California raisins", None, (4, 5)),
             ("Werther's Originals", None, (2, 5)),
             ("Beer", None, (5, 6)),
             ("granola bar", None, (6, 8)),
             ("cliff bar", None, (6, 8)),
             ("still hot pizza?", None, (12, 15)),
             ("5-Hour Energy Drink", None, (17, 20))
             ]


def generateNextWeapon(current_weapon):

    if weapon_list:
        weapon = None
        for i, entry in enumerate(weapon_list):
            if current_weapon and entry[0] == current_weapon.name:
                if len(weapon_list) > i + 1:
                    weapon = weapon_list[i + 1]; break
                else:
                    weapon = weapon_list[-1]; break
            else:
                weapon = weapon_list[0]; break
        name, dmg, hlg = weapon
        item = Item(name, dmg, hlg)
        return item

def getRandomFood():
    
    name, dmg, hlg = random.choice(food_list)
    item = Item(name, dmg, hlg)
    return item


class Item(object):
    
    def __init__(self, name=None, damage=None, healing=None):
        
        self.name = name
        self._damage = damage
        self._healing = healing
    
    def __str__(self):
        
        return self.name
    
    def getDamage(self):
        
        return random.randint(self._damage[0], self._damage[1])
    
    def getHealing(self):
        
        return random.randint(self._healing[0], self._healing[1])

