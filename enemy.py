"""
Module containing all enemy methods
"""


import random


NAMES = ["nomming", "gurgling", "drooling", "bloody", "filthy", "crawling",
         "aggressive", "frightening", "terrifying", "hungry", "famished",
         "leg-less", "arm-less", "one-armed", "moaning", "grotesque", "nasty",
         "gross", "one-eyed", "bad-breath", "growling", "rotting", "skinless",
         "putrid", "obnoxiously obese", "faceless", "decaying", "stinky", "smelly",
         "fragrant", "frenzied", "pocket protector", "awkward", "buff",
         "big McLarge-huge", "disgusting", "huge", "morbidly obese", "canine",
         "feline", "rat"]


class Zombie(object):
    
    def __init__(self, level, difficulty):
        
        self.name = random.choice(NAMES) + " zombie"
        self.level = level
        self.difficulty = difficulty
        self.debuffs = set([])
        self.boss = False
        self.rounds = 1
        self.burning_damage = 0
        self.health = int(round((0.7*self.level**2.0)* difficulty))
        self.m_health = self.health
        self._damage = (int(round(0.65 * level * difficulty)),
                        int(round(0.93 * level * difficulty)))
        
    def getDamage(self, player, is_random=True):
        """Returns total damage and mitigation value"""
        
        if "restrained" in self.debuffs:
            return 0, 0
        
        mitigation, num_cats = player.getCatBonus(player.defending_kittens,
                                                "defending")
        raw_dmg = random.randint(self._damage[0], self._damage[1])
        
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
    
        
class Boss(Zombie):
    
    def __init__(self, level, difficulty):
        super().__init__(level, difficulty)
        self.rounds = int(level / 5 + 1)
        self.boss = True

    def specialMove(self, player):
        
        total_cats = max_chance = len(player.kennel)
        if total_cats:
            max_chance = int(total_cats/self.rounds)
            if max_chance > total_cats:
                max_chance = len(player.kennel)
                
            dead_cats_list = random.sample(player.kennel, 
                    random.randint(1 if max_chance else 0, max_chance))
            dead_cat_names = [cat.name for cat in dead_cats_list]
            for cat in player.kennel:
                if cat.name in dead_cat_names:
                    player.kennel.remove(cat)
                    print(self.name, "just ate", cat.name)
                    less_attacking = random.randint(0, 1)
                    if less_attacking and player.attacking_kittens != 0:
                        player.attacking_kittens -= 1
                        if player.attacking_kittens < 0:
                            player.attacking_kittens = 0
                            player.defending_kittens -= 1
                    elif not less_attacking and player.defending_kittens != 0:
                        player.defending_kittens -= 1
                        if player.defending_kittens < 0:
                            player.defending_kittens = 0
                            player.attacking_kittens -= 1
        else:
            print("\n\tIt's just you and this guy...\n")
                
