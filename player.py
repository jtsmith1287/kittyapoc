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

        self.difficulty = None

        self._insanity = 10
        self._courage = 10
        self.health = self._courage * 2
        self.kennel = []
        self.special_kennel = []
        self.attacking_kittens = 0
        self.defending_kittens = 0
        self.inventory = []
        self.weapon = None
        self.level = 1
        self.xp = [0, 1]
        self.boss_fights = [i*5 + 5 for i in range(10)]
        
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
    
    def setMaxHealth(self, mod=0):

        self.health = self._courage * 2 + self.level + mod
    
    def updateHealth(self, mod=0):
        
        if self.health + mod >= (self._courage * 2) + self.level:
            self.setMaxHealth()
        else:
            self.health += mod
        return self.health
    
    def equip(self, item):
        
        self.weapon = item
    
    def getBonusDamageFromInsanity(self):
        
        return int(round((self._insanity ** 2)/50)) -1
    
    def getCatBonus(self, count, state):
        
        allocated = self.__dict__["%s_kittens" % state]
        
        stats = {"attacking": int(round(self._insanity/6))-1,
                "defending": int(round(self._courage/6))-1}

        number_of_cats = random.randint(0, count if count >= 0 else 0)
        if allocated:
            if stats[state] + number_of_cats > allocated:
                number_of_cats = allocated
            else:
                number_of_cats += stats[state]
            cat_sample = random.sample(self.kennel, number_of_cats)
            cat_bonus = sum([i.level for i in cat_sample])
            return cat_bonus, number_of_cats
        else:
            return 0, 0
    
    def getDamage(self):
        """Returns total damage and number of attacking kittens"""
        
        weapon_dmg = self.weapon.getDamage()
        cat_bonus, att_cats = self.getCatBonus(self.attacking_kittens,
                                               "attacking")
        true_dmg = weapon_dmg + cat_bonus + self.getBonusDamageFromInsanity()
        return true_dmg, att_cats
        
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
        
        return self._courage * 0.0075

    def experienceBar(self):

        bar = "#"* int(((float(self.xp[0]) / (self.xp[1])) * 100)/5)
        space = "-"* (20 - int(((float(self.xp[0]) / (self.xp[1]) * 100)/5)))
        
        return "XP: %s [%s%s] %s" % (self.xp[0], bar, space, self.xp[1])
    
    def healthBar(self):
        
        bar = "#"* int(((float(self.health) / (self._courage*2 + self.level)) * 100)/5)
        space = "-"* (20 - int(((float(self.health) / (self._courage*2 + self.level) * 100)/5)))
        
        name = "You:"
        full_bar = "%s [%s%s] %s" % (self.health, bar, space, self._courage * 2 + self.level)
        
        return name + full_bar.rjust(60-len(name))
    
    def newStats(self):
        
        good = False
        while not good:
            answer = input(BRAVE_OR_CRAZY)
            if answer == "brave":
                self.updateCourage(2)
                print("You go, Grandma!\n")
                good = True
            elif answer == "insane":
                self.updateInsanity(2)
                print("Ya, thought so...\n")
                good = True
            else:
                print("Sorry, what now?")
        
        self.setMaxHealth(1)
    
    def startLevelUp(self, rewards=None):
        
        if self.xp[0] >= self.xp[1]:
            if rewards:
                for reward in rewards:
                    reward()
            print(LEVEL_UP_TEXT % (random.choice(CRAZY_WORDS),
                                   random.choice(BRAVE_WORDS)))
            self.newStats()
            self.level += 1
            self.xp = [0, self.level]
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
        
