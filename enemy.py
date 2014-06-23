"""
Module containing all enemy methods
"""


import random


NAMES = ["nomming", "gurgling", "drooling", "bloody", "filthy", "crawling",
         "aggressive", "frightening", "terrifying", "hungry", "famished",
         "leg-less", "arm-less", "one-armed", "moaning", "grotesque,", "nasty",
         "gross", "one-eyed", "bad-breath", "growling", "rotting", "skinless",
         "putrid", "obnoxiously obese", "faceless", "decaying", "stinky", "smelly",
         "fragrant", "frenzied", "pocket protector", "awkward", "buff",
         "big McLarge-huge", "disgusting", "huge", "morbidly obese"]


class Zombie(object):
    
    def __init__(self, level, difficulty):
        
        self.name = random.choice(NAMES) + " zombie"
        self.level = level
        self.difficulty = difficulty
        self.debuffs = set([])
        self.burning_damage = 0
        self.health = int(round(2.9 * level * difficulty))
        self.m_health = self.health
        self._damage = (int(round(0.7 * level * difficulty)),
                        int(round(1.0 * level * difficulty)))
        
    def getDamage(self, player, is_random=True):
        """Returns total damage and mitigation value"""
        
        if "restrained" in self.debuffs:
            return 0, 0
        
        def_cats, num_cats = player.getCatBonus(player.defending_kittens)
        mitigation = sum([i.level for i in def_cats])
        raw_dmg = random.randint(int(self._damage[0] * self.difficulty),
                                 int(self._damage[1] * self.difficulty))
        
        true_dmg = raw_dmg - mitigation
        if true_dmg < 0:
            true_dmg = 0
        
        return true_dmg, num_cats
    
    def healthBar(self):
        
        bar = "#"* int(((float(self.health) / self.m_health) * 100)/5)
        space = "-"* (20 - int(((float(self.health) / self.m_health) * 100)/5))
        
        return "%s: %s [%s%s] %s" % (self.name, self.health, bar, space, self.m_health)
    
    def updateHealth(self, mod=0):
        
        if self.health + mod < 0:
            self.health = 0
        else:
            self.health += mod
        
        return self.health
        
    
    
