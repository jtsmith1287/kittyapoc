"""
Module containing all player methods and data
"""

import random


INTRO = """
    You've entered a world where everyone is dead. You're the only one left
and you're also almost dead. You're also borderline insane and have an
infatuation with kittens that is rivaled by none. Armed with your purse, and 
your lack of wits, you decide to venture off into the darkness.

The question is, are you being brave, or are you insane?
"""

BRAVE_OR_CRAZY = "('brave' or 'insane')\n:"

CRAZY_WORDS = ["nuts", "crazy", "insane", "bonkers",]
BRAVE_WORDS = ["brave", "courageous", "tough",]

LEVEL_UP_TEXT = """
Coming out of that, it's hard to tell if you're more %s or %s than before. What 
do you think?
""" 


class Player(object):
    
    def __init__(self):

        self._insanity = 10
        self._courage = 10
        self.health = self._courage * 2
        self.kennel = []
        self.special_kennel = []
        self.attacking_kittens = 0
        self.defending_kittens = 0
        self.inventory = []
        self._weapon = None
        self.level = 1
        self.xp = [0, 1]
        
    def __len__(self):
        
        return len(self.kennel)
    
    def kittenCount(self):
        
        return len(self.kennel)
    
    def updateInsanity(self, mod=0):
        
        self._insanity += mod
        return self._insanity
    
    def updateCourage(self, mod=0):
        
        self._courage += mod
        return self._courage
    
    def updateHealth(self, mod=0):
        
        if self.health > self._courage * 2:
            self.health = self._courage * 2
        else:
            self.health += mod
        return self.health
    
    def equip(self, item):
        
        self._weapon = item
    
    def getBonusDamageFromInsanity(self):
        
        return int(round((self._insanity ** 2)/50)) -1
    
    def getCatBonus(self, count):
        
        total = 0
        for i in range(count):
            total += random.choice(self.kennel).level
        return total
    
    def getDamage(self):
        """Returns total damage and number of attacking kittens"""
        
        weapon_dmg = self._weapon.getDamage()
        cat_bonus = self.getCatBonus(self.attacking_kittens)
        bonus = random.randint(0, cat_bonus)
        true_dmg = weapon_dmg + bonus + self.getBonusDamageFromInsanity()
        return true_dmg, bonus
        
    def adoptKitten(self, kitten, special=False):
        
        if special:
            self.special_kennel.append(kitten)
        else:
            self.kennel.append(kitten)
    
    def checkInventory(self):
        
        items = {}
        for item in self.inventory:
            if item.name in items:
                items[item.name] += 1
            else:
                items[item.name] = 1
        return items
    
    def insanityChanceBonus(self):
        
        return self._insanity * 0.01
    
    def getKittenCourageBonus(self):
        
        return self._courage * 0.01
    
    def healthBar(self):
        
        bar = "#"* int(((float(self.health) / (self._courage*2)) * 100)/5)
        space = "-"* (20 - int(((float(self.health) / (self._courage*2) * 100)/5)))
        
        return "You: %s [%s%s] %s" % (self.health, bar, space, self._courage * 2)
    
    def newStats(self):
        
        good = False
        while not good:
            answer = input(BRAVE_OR_CRAZY)
            if answer == "brave":
                self.updateCourage(1)
                print("You go, Grandma!\n")
                good = True
            elif answer == "insane":
                self.updateInsanity(1)
                print("Ya, thought so...\n")
                good = True
            else:
                print("Sorry, what now?")
        
        self.health = self._courage * 2
    
    def startLevelUp(self):
        
        if self.xp[0] >= self.xp[1]:
            print(LEVEL_UP_TEXT % (random.choice(CRAZY_WORDS),
                                   random.choice(BRAVE_WORDS)))
            self.newStats()
            self.xp = [0, self.xp[1] * 2]
            self.level += 1
        self.checkKittenLevels()
    
    def checkKittenLevels(self):
        
        for cat in self.kennel:
            cat.levelUp()
        
        for special_cat in self.special_kennel:
            special_cat.levelUp()
    
    def intro(self):
        
        print(INTRO)
        while (self._courage == 10 and self._insanity == 10):
            self.newStats()
        
        return self
        