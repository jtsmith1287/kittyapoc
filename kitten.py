"""
Module containing all kitten methods
"""


class Kitten(object):
    
    def __init__(self, name):
        
        self.name = name
        self.level = 1
        self.xp = [0.0, self.getXPToLevel()]
        
    def getXPToLevel(self):
        
        return 4.0 * self.level
    
    def displayInfo(self):
        
        bar = "#"* int(((self.xp[0] / self.xp[1]) * 100)/5)
        space = "-"* (20 - int(((self.xp[0] / self.xp[1]) * 100)/5))
        
        print(self.name + "%s [%s%s] %s".rjust(40 - len(self.name)) % (
                self.level, bar, space, self.level + 1))
    
    def levelUp(self):
        
        if self.xp[0] >= self.xp[1]:
            self.level += 1
            self.xp[0] = 0.0
            self.xp[1] = self.getXPToLevel()

