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
import logging
import file_manager


SHOW_STATS_STRING = """
Your current health is %s
%s
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
kittens in need of rescuing (find kitten:%s%%, find item:%s%%). You are more 
apt to flailing uncontrollably during combat which proves to be quite 
effective against zombies (+%s bonus dmg).

Your courage (%s) is your fortitude. It's what's keeping you pushing forward
and enables you to stand strong when you're toe to toe with the flesh eating
undead. Without it you'd surely die. Only the brave are willing to risk their
lives for their kittens (%s%% kitten protection)
"""

CAT_HERDING = """
Would you like to attempt to herd your cats? If so, type in 
the number you'd prefer to attack followed by the number to defend you. 
(eg '4 8'). Otherwise, press <ENTER> to skip.\n:
"""

CAT_HERDING_CONFIRM = """
Ok, so that's %s attacking, and %s defending. You've got %s kittens left.
"""

FREAKY_BOSS_TEXT = """
The zombie falls to the ground. 
You think it's over... 
You hear gurgling and moaning behind you...
The zombie rises to its feet ...
This fight isn't finished.
""".splitlines()

GAME_WIN = """
HOLY HELL... You just beat the end of the world...
Like seriously. You're invincible. You can now repopulate the world...
uh...

With cats?


........


.....


Nevermind, you totaly still lose. 
"""


class Game(object):
    
    def __init__(self):
        
        self.running = False
        self.version = "\n\n\t\tCrazy Cat Lady Apocalypse v%s" % 103
        self.difficulty = 1.05
        self.dif_list = ["1: Easy", "2: Normal", "3: Your Grave\n"]
        self.find_kitten_chance = 0.22
        self.find_item_chance = 0.08
        self.find_food_chance = 0.9
        self.kitten_death_chance = 0.3
        
        self._turn_choices = {"1) Venture further into the darkness?": self.venture,
                              "2) Check yourself out in a mirror?": self.showPlayerStats,
                              "3) Use an item?": self.useItem,
                              "4) Poke your cats?": self.pokeCats,
                              "5) How am I doing?": self.detailed_info,
                              "6) Suicide!": self.die,}
    
    def setDifficulty(self):
        
        print("Choose a difficulty")
        while type(self.difficulty) == type([]):
            self.dif_list = ["1: Easy", "2: Normal", "3: Your Grave\n"]
            dif = input("\n".join([d for d in self.dif_list]))
            if dif.isdigit() and int(dif) -1 in range(len(self.dif_list)):
                self.difficulty = self.difficulty[int(dif)-1]
                print("\nDifficulty set to %s" % (self.dif_list[int(dif)-1].split()[-1]))
            else:
                print(INVALID)
            
    def beginningOfTurnPrompt(self):
        
        print
        for k in sorted(self._turn_choices):
            print(k)
    
    def acquireItem(self, forced_chance=None):
        
        item_chance = random.random() if not forced_chance else forced_chance
        # determine whether a weapon or food was found
        if item_chance < self.find_food_chance:
            item = getRandomFood()
            self.player.inventory.append(item)
            print("You found a %s" % item.name)
        else:
            item = generateNextWeapon(self.player.weapon)
            if item:
                print("You found a %s" % item.name)
                print("You toss your %s to the ground in favor of your new %s!" % (
                        self.player.weapon, item))
                self.player.equip(item)
            else:
                self.acquireItem(0)
    
    def findKitten(self):
        
        print("You found a wee kitty! Awwww.")
        chance = random.random()
        if len(special.SPECIAL_CATS) == 0:
            chance = 1
        if chance > 0.16:
            name = names.generateName()
            print("The kitty mews at you and you see a collar with a tag reading: %s" % (
                    name))
            new_kitten = kitten.Kitten(name)
            self.player.adoptKitten(new_kitten)
        else:
            new_kittens = special.spawnSpecialKitty()
            owned_kittens = [i.name for i in self.player.special_kennel]
            for _kitten in new_kittens:
                if _kitten.name not in owned_kittens:
                    print("But this is no ordinary kitten!!! It's %s!" % _kitten.name)
                    self.player.adoptKitten(_kitten, True)
                    return
            self.findKitten()
    
    def specialCatStuff(self, zombie, post=False):
    
        for cat in self.player.special_kennel:
            if cat.post == post and random.random() < cat.activation_chance:
                random.choice(cat.specialMoves)(cat, player=self.player, zombie=zombie)
    
    def WinCheck(self):
        
        if len(self.player.boss_fights) == 1:
            print(GAME_WIN)
            self.gameOver()
        else:
            self.player.boss_fights.pop(0)
    
    def endCombatCheck(self, zombie):
        
        if self.player.health <= 0:
            self.gameOver()
            self.running = False
            return False
        if zombie.health <= 0:
            if zombie.boss and zombie.rounds > 1:
                if self.player.inventory:
                    self.useItem()
                for line in FREAKY_BOSS_TEXT:
                    print(line)
                    time.sleep(1)
                zombie.health = zombie.m_health
                zombie.rounds -= 1
                zombie.specialMove(self.player)
                return True
            print(END_COMBAT % zombie.name)
            self.player.xp[0] += 1
            for cat in self.player.kennel:
                cat.xp[0] += 1
            for scats in self.player.special_kennel:
                scats.xp[0] += 1
            if zombie.boss:
                self.WinCheck()
                self.player.setMaxHealth()
                self.player.xp[0] = int(self.player.xp[1]/2)
                for i in range(int(self.player.level/5) + 1):
                    self.acquireItem()
            return False
        else:
            return True
    
    def findZombie(self, roll):
        
        if roll == 1.0: # Basically, player rolled a 100
            print("Woah! Where'd this thing come from!?")
            time.sleep(1)
            zombie = enemy.Boss(self.player.level, self.difficulty)
        elif self.player.level % 5 == 0 and self.player.level in self.player.boss_fights:
            zombie = enemy.Boss(self.player.level, self.difficulty)
            print("\nThere's something peculiar about this one...\n")
            time.sleep(1.5)
        else:
            zombie = enemy.Zombie(self.player.level, self.difficulty)
        print("Aaannd now you're being attacked by a %s" % zombie.name)
        in_combat = True
        cats_vulnerable = 0
        while in_combat:
            time.sleep(2)
            self.specialCatStuff(zombie, False)

            choice = input("\nENTER to attack, or 1 to use an item.\n:")
            if choice:
                if choice == "1":
                    self.useItem()
            dmg_dealt, attacking_kittens = self.player.getDamage()
            dmg_recv, defending_kittens = zombie.getDamage(self.player)
            if defending_kittens > cats_vulnerable:
                cats_vulnerable += defending_kittens - cats_vulnerable
            print(COMBAT_ATTACK % (self.player.weapon, attacking_kittens,
                                   zombie.name, dmg_dealt))
            
            if "burning" in zombie.debuffs:
                print("%s is on fire! It burns for %s damage!" % (
                        zombie.name, zombie.burning_damage))
                zombie.updateHealth(-zombie.burning_damage)
            if "restrained" in zombie.debuffs:
                print(ZOMBIE_RESTRAINED)
                zombie.debuffs.discard("restrained")
            else:
                print(COMBAT_DEFEND % (zombie.name, defending_kittens, dmg_recv))
            
            # Deal Damage
            self.player.updateHealth(-dmg_recv)
            zombie.updateHealth(-dmg_dealt)
            print(self.player.healthBar()) 
            print(zombie.healthBar())

            self.specialCatStuff(zombie, True)
            in_combat = self.endCombatCheck(zombie)
        time.sleep(1)
        self.deadKittenCheck(cats_vulnerable)
        self.player.startLevelUp(rewards=[self.findKitten, self.acquireItem])
        time.sleep(1)

    def deadKittenCheck(self, cats_vulnerable):
        
        dead_kittens = []
        for i in range(cats_vulnerable):
            poor_luck = random.random()
            chance = self.kitten_death_chance - self.player.getKittenCourageBonus()
            if poor_luck < chance:
                dead_kittens.append(self.killAKitten())
        
        if dead_kittens:
            time.sleep(1)
            print("    Oh no... oh I'm so sorry. There's been an accident.")
            for cat, level in dead_kittens:
                time.sleep(1)
                print("    " + cat + " was killed.", "[lvl %s]" % level, "\n")
                
                self.player.defending_kittens -= len(dead_kittens)

    def killAKitten(self):
        
        dead_cat = self.player.kennel.pop(
                random.randint(0, len(self.player.kennel)-1))
        return dead_cat.name, dead_cat.level
    
    def venture(self):
        
        print("You move further into the darkness...")
        time.sleep(2)
        chance = random.random()
        percent = int(chance * 100)
        print("%% roll = %s" % percent)
        time.sleep(.75)
        if percent <= 1:
            print("Hey hey! Today's you'r lucky day!")
            self.acquireItem(1.0)
        # Check if an item, kitten, or enemy was found
        if chance < self.find_item_chance + self.player.insanityChanceBonus()/2:
            self.acquireItem()
        elif chance < self.find_kitten_chance + self.player.insanityChanceBonus():
            self.findKitten()
        else:
            self.findZombie(round(chance, 2))
        
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
    
    def pokeCats(self):    
        
        if self.player.kittenCount() or len(self.player.special_kennel):
            for cat in self.player.kennel:
                cat.displayInfo()
            print("You have %s kittens" % len(self.player))
            print("Current configuration:",
                  "    Attacking: %s" % self.player.attacking_kittens,
                  "    Defending: %s" % self.player.defending_kittens,
                  "    Idle: %s" % (
                    len(self.player.kennel) - self.player.attacking_kittens - self.player.defending_kittens),
                  sep="\n")
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
            
    def showPlayerStats(self):
        
        items = "\n".join(["%s x%s" % (k,v) for k,v in self.player.checkInventory().items()])
        print(SHOW_STATS_STRING % (self.player.health,
                                   "".join(self.player.healthBar().split()[1:]),
                                   self.player.level,
                                   self.player.experienceBar(),
                                   self.player.updateCourage(), 
                                   self.player.updateInsanity(),
                                   self.player.weapon,
                                   self.player.kittenCount(),
                                   items if items else "Nothing",))
    
    def detailed_info(self):
        
        item_chance = self.find_item_chance + self.player.insanityChanceBonus()/2
        kitten_chance = self.find_kitten_chance + self.player.insanityChanceBonus() - item_chance
        save_kitten_chance = 1 - self.kitten_death_chance + self.player.getKittenCourageBonus()
        print(DETAILED_INFO_TEXT % (self.player.updateInsanity(),
                                    round(kitten_chance * 100, 2),
                                    round(item_chance * 100, 2),
                                    self.player.getBonusDamageFromInsanity(),
                                    self.player.updateCourage(),
                                    round(save_kitten_chance * 100, 2),
                                    ))
    
    def useItem(self):
        
        items = sorted(self.player.checkInventory().items())
        if items:
            print("Here's what you've got.")
        else:
            print("You haven't collected anything yet.")
            return None, None # Don't even know...
        for x,k in enumerate(items):
            print("    ", str(int(x)+1) + ")", k[0], "x" + str(k[1]))
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

    def die(self):

        sure = input("Are you sure you want to end it now?\n:")
        if sure and "y" in sure.lower():
            self.gameOver()

    def gameOver(self):
        
        self.running = False
        if self.player:
            print(GAME_OVER)
            level = self.player.level * 10
            kats = len(self.player) * 2
            items = len(self.player.inventory) * 3
            exp = self.player.xp[0]
            
            score = level + kats + items + exp
            
            print("You scored: " + str(score))
            print (self.version)
        
        file_manager.deleteSave()
        try:
            sys.exit()
        except:
            pass

    def startNewGame(self):
        
        print("Starting a new game...")
        print("Creating player...")
        self.player = player.Player()
        self.player.equip(generateNextWeapon(self.player.weapon))
        file_manager.saveGame(self.player)
        #self.setDifficulty()
        self.player.intro()
        #self.player.difficulty = self.difficulty
        self.findKitten()
        self.running = True

    def tryLoadExistingSave(self):
        
        print("Attempting to load an existing save...")
        try:
            self.player = file_manager.loadGame()
            #self.difficulty = self.player.difficulty
            if self.player:
                self.running = True
            else:
                self.startNewGame()
        except FileNotFoundError:
            logging.exception("DEBUG")
            self.startNewGame()
        except AttributeError:
            logging.exception("DEBUG")
            print("Your game save is incompatible with this new version.",
                  "I realize this sucks, but life goes on... or does it?")
            self.startNewGame()

    def run(self):

        print(self.version)
        print("Press Ctrl + C to quit.")
        self.tryLoadExistingSave()
        
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
            if self.running:
                file_manager.saveGame(self.player)
    

if __name__ == "__main__":
    if (sys.version_info) < (3, 4):
        print("Incorrect version. Python 3.4 or later needed.")
    else:
        try:
            game = Game()
            game.run()
        except KeyboardInterrupt:
            if game.running:
                file_manager.saveGame(game.player)
            print(game.version)
            print("\n\tBye!\n\n")
        except:
            print(game.version)
            logging.exception("Something happened ...")
    input("Press ENTER to quit")

        
