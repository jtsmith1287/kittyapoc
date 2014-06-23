"""
Main module to run all other game components.
"""


import player
import enemy
import kitten
import special
import names
from item import getRandomFood, generateNextWeapon
import time
import random
import sys
import platform


SHOW_STATS_STRING = """
Your current health is %s
You are level %s.
%s
Your courage is %s.
Your insanity is %s.
You are wielding a %s.
You have %s kittens in your kennel.
You possess the following items:
%s
"""

INVALID = "Invalid choice, please try again.\n"

COMBAT_ATTACK = """
    With %s in hand, you and %s kittens attack the %s for %s damage!
"""
COMBAT_DEFEND = """    The %s attacks you and %s kittens for %s damage in return!
"""
ZOMBIE_RESTRAINED = """The zombie begins to recover...
"""

END_COMBAT = """
The %s crumples to the ground. Holy smokes that is wild. I think it's dead. 
Let's get out of here.
"""

GAME_OVER = """
Well, that's it. You finally kicked the bucket. You had to know this was
going to happen eventually. R.I.P., you old hag."""

DETAILED_INFO_TEXT = """
Your insanity (%s) pushes you to do really dumb things, like digging through
old dumpsters and breaking into dark and eerie animal shelters in search for
kittens in need of rescuing. You are more apt to flailing uncontrollably during
combat which proves to be quite effective against zombies (+%s bonus dmg).

Your courage (%s) is your fortitude. It's what's keeping you pushing forward
and enables you to stand strong when you're toe to toe with the flesh eating
undead. Without it you'd surely die. Only the brave are willing to risk their
lives for their kittens (+%s%% kitten protection)
"""

CAT_HERDING = """
Would you like to attempt to herd your cats? If so, type in 
the number you'd prefer to attack followed by the number to defend you. 
(eg '4 8'). Otherwise, press <ENTER> to skip.\n:
"""

CAT_HERDING_CONFIRM = """
Ok, so that's %s attacking, and %s defending. You've got %s kittens left.
"""


class Game(object):
    
    def __init__(self):
        
        self.running = True
        self.difficulty = [1, 1.25, 1.5]
        self.find_kitten_chance = 0.3
        self.find_item_chance = 0.10
        self.find_food_chance = 0.92
        self.kitten_death_chance = 0.3
        
        self._turn_choices = {"1) Venture further into the darkness?": self._venture,
                              "2) Check yourself out in a mirror?": self._showPlayerStats,
                              "3) Use an item?": self._useItem,
                              "4) Poke your cats?": self._pokeCats,
                              "5) How am I doing?": self.detailed_info}
        
        self.player = player.Player()
        self.player.equip(generateNextWeapon())
    
    def _setDifficulty(self):
        
        print("Choose a difficulty")
        while type(self.difficulty) == type([]):
            dif_list = ["1: Easy", "2: Normal", "3: Your Grave\n"]
            dif = input("\n".join([d for d in dif_list]))
            if dif.isdigit() and int(dif) -1 in range(len(dif_list)):
                self.difficulty = self.difficulty[int(dif)-1]
                print("\nDifficulty set to %s" % (dif_list[int(dif)-1].split()[-1]))
            else:
                print(INVALID)
            
    def beginningOfTurnPrompt(self):
        
        print
        for k in sorted(self._turn_choices):
            print(k)
    
    def acquireItem(self):
        
        item_chance = random.random()
        # determine whether a weapon or food was found
        if item_chance < self.find_food_chance - self.player.insanityChanceBonus():
            item = getRandomFood()
            self.player.inventory.append(item)
            print("You found a %s" % item.name)
        else:
            item = generateNextWeapon()
            print("You found a %s" % item.name)
            print("You toss your %s to the ground in favor of your new %s!" % (
                    self.player._weapon, item))
            self.player.equip(item)
    
    def _findKitten(self):
        
        print("You found a wee kitty! Awwww.")
        chance = random.random()
        if len(self.player.special_kennel) == 4:
          chance = 1
        if chance > 0.16:
            name = names.generateName()
            print("The kitty mews at you and you see a collar with a tag reading: %s" % (
                    name))
            new_kitten = kitten.Kitten(name)
            self.player.adoptKitten(new_kitten)
        else:
            new_kitten = special.spawnSpecialKitty()
            print("But this is no ordinary kitten!!! It's %s!" % new_kitten.name)
            self.player.adoptKitten(new_kitten, True)
    
    def specialCatStuff(self, zombie, post=False):
    
        for cat in self.player.special_kennel:
            if cat.post == post and random.random() < cat.activation_chance:
                cat.specialMove(cat, player=self.player, zombie=zombie)
    
    def _findZombie(self):
        
        zombie = enemy.Zombie(self.player.level, self.difficulty)
        print("Aaannd now you're being attacked by a %s" % zombie.name)
        in_combat = True
        while in_combat:
            
            time.sleep(2)
            self.specialCatStuff(zombie, False)
            time.sleep(2)
            
            dmg_dealt, attacking_kittens = self.player.getDamage()
            dmg_recv, defending_kittens = zombie.getDamage(self.player)
            print(COMBAT_ATTACK % (self.player._weapon, attacking_kittens,
                                   zombie.name, dmg_dealt))
            
            if "burning" in zombie.debuffs:
                print("%s is on fire! It burns for %s damage!" % (zombie.name, zombie.burning_damage))
            if "restrained" in zombie.debuffs:
                print(ZOMBIE_RESTRAINED)
                zombie.debuffs.discard("restrained")
            else:
                print(COMBAT_DEFEND % (zombie.name, defending_kittens, dmg_recv))
            
            # Deal Damage
            self.player.updateHealth(-dmg_recv)
            zombie.updateHealth(-dmg_dealt)
            for letter in self.player.healthBar() + " | " + zombie.healthBar() + "\n":
                time.sleep(0.02)
                print(letter, end="", flush=True)
            
            time.sleep(1)
            self.specialCatStuff(zombie, True)
            
            if self.player.health <= 0:
                in_combat = False
                self.gameOver()
            if zombie.health <= 0:
                print(END_COMBAT % zombie.name)
                in_combat = False
                self.player.xp[0] += 1
                self.player.startLevelUp()
                for cat in self.player.kennel:
                    cat.xp[0] += 1
                for scats in self.player.special_kennel:
                    scats.xp[0] += 1
            
        dead_kittens = []
        for i in range(defending_kittens):
            poor_luck = random.random()
            chance = self.kitten_death_chance - self.player.getKittenCourageBonus()
            if poor_luck < chance:
                dead_kittens.append(self._killAKitten())
        
        if dead_kittens:
            time.sleep(1)
            print("    Oh no... oh I'm so sorry. There's been an accident.")
            for cat in dead_kittens:
                time.sleep(1)
                print("    " + cat + " was killed.")
                self.player.defending_kittens -= len(dead_kittens)
    
    def _killAKitten(self):
        
        dead_cat = self.player.kennel.pop(
                random.randint(0, len(self.player.kennel)-1))
        return dead_cat.name
    
    def gameOver(self):
        
        print(GAME_OVER)
        level = self.player.level * 10
        kats = len(self.player) * 2
        items = len(self.player.inventory) * 3
        exp = self.player.xp[0]
        
        score = level + kats + items + exp
        
        print("You scored: " + str(score))
        
        sys.exit()
    
    def _venture(self):
        
        print("You move further into the darkness...")
        time.sleep(2)
        chance = random.random()
        # Check if an item, kitten, or enemy was found
        if chance < self.find_item_chance:
            self.acquireItem()
        elif chance < self.find_kitten_chance + self.player.insanityChanceBonus():
            self._findKitten()
        else:
            self._findZombie()
        
    def assignKittens(self, response):
        
        if response[0] + response[1] > len(self.player):
            print("You don't have that many.")
            return
        self.player.defending_kittens = int(response[1])
        self.player.attacking_kittens = int(response[0])
        print(CAT_HERDING_CONFIRM % (
                self.player.attacking_kittens,
                self.player.defending_kittens,
                len(self.player) - int(response[0]) - int(response[1])))
    
    def _pokeCats(self):    
        
        if self.player.kittenCount() or len(self.player.special_kennel):
            for cat in self.player.kennel:
                cat.displayInfo()
            print("You have %s kittens" % len(self.player))
            if self.player.special_kennel:
                print("Here's something special for you to look at")
                print("(Note: special cats can't be herded)")
                for scat in self.player.special_kennel:
                    scat.displayInfo()
            response = input(CAT_HERDING).split()
            if response and len(response) == 2:
                for i in response:
                    if not i.isdigit():
                        print("Let's just move on.")
                        return
                self.assignKittens(list(map(int, response)))
            else:
                print(INVALID)
        else:
            print("You've rescued no kittens...")
            
    def _showPlayerStats(self):
        
        items = "\n".join(["%s x%s" % (k,v) for k,v in self.player.checkInventory().items()])
        print(SHOW_STATS_STRING % (self.player.health,
                                   self.player.level,
                                   self.player.experienceBar(),
                                   self.player.updateCourage(), 
                                   self.player.updateInsanity(),
                                   self.player._weapon,
                                   self.player.kittenCount(),
                                   items if items else "Nothing",))
    
    def detailed_info(self):
        
        print(DETAILED_INFO_TEXT % (self.player.updateInsanity(),
                                    self.player.getBonusDamageFromInsanity(),
                                    self.player.updateCourage(),
                                    self.player.getKittenCourageBonus() * 100,
                                    ))
    
    def _useItem(self):
        
        items = sorted(self.player.checkInventory().items())
        if items:
            print("Here's what you've got.")
        else:
            print("You haven't collected anything yet.")
            return None, None # Don't even know...
        for x,k in enumerate(items):
            print(str(int(x)+1) + ")", k[0], "x" + str(k[1]))
        choice = input(":")
        if choice and choice.isdigit() and int(choice) <= len(items):
            # This just seems bad... this could be better.
            index = int(choice) - 1
            chosen_item = items[index][0]
            item = None
            for x,i in enumerate(self.player.inventory):
                if i.name == chosen_item:
                    item = self.player.inventory.pop(x)
                    break
            if item:
                #TODO: This should become a "getItemAbility"
                healing = item.getHealing()
                new_health = self.player.updateHealth(healing)
                print("You have been healed for %s. You now have %s health." % (
                        healing, new_health))
            else:
                print(INVALID)
        else:
            print(INVALID)
    
    def run(self):
        
        self.player.intro()
        self._setDifficulty()
        while self.running:
            print()
            self.beginningOfTurnPrompt()
            choice = input("\n:")
            if choice.isdigit() and (int(choice)-1 in range(len(self._turn_choices))):
                index = int(choice) -1
                key_list = sorted(self._turn_choices.keys())
                chosen_key = key_list[index]
                method = self._turn_choices.get(chosen_key)
                method()
    

if __name__ == "__main__":
    if eval(platform.python_version) < 3.4:
        print("Herding cats through the apocalypse requires at least python 3.4")
        sys.exit()
    Game().run()
