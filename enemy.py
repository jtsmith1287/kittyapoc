"""
Module containing all enemy methods
"""


import random


NAMES = ["Nomming", "Gurgling", "Drooling", "Bloody", "Filthy", "Crawling",
         "Aggressive", "Frightening", "Terrifying", "Hungry", "Famished",
         "Leg-less", "Arm-less", "One-armed", "Moaning",]


class Zombie(object):
    
    def __init__(self, level, difficulty):
        
        self.name = random.choice(NAMES) + " Zombie"
        self.level = level
        self.difficulty = difficulty
        self.health = int(round(1.49 * level * difficulty))
        self.m_health = self.health
        self._damage = (1 * level, int(1.3 * level))
        
    def getDamage(self, mitigation, is_random=True):
        """Returns total damage and mitigation value"""
        
        raw_dmg = random.randint(int(self._damage[0] * self.difficulty),
                                 int(self._damage[1] * self.difficulty))
        if is_random:
            mitigation = random.randint(0, mitigation)
        
        true_dmg = raw_dmg - mitigation
        if true_dmg < 0:
            true_dmg = 0
            
        return true_dmg, mitigation
    
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
        
    
    