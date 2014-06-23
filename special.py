"""
Handles the specialty cats
"""

from kitten import Kitten
import random


MEDICAT_HEALING = ["slapped a bandage on your face",
                   "cast a healing spell (???)",
                   "administered a tetanus shot",
                   "threw a healing poultice at you",
                   "kissed your booboo",
                   "patted you on the head... there there...",
                   "licked your wounds",
                   "dried your tears",
                   "sanitized your wounds with rubbing alcohol",
                   "stitched you up",
                   "sang you a soothing song",
                   "invoked the way of the swan",
                   "performed a voodoo ritual",
                   ]


NINJA_CAT_HDING_PLACES = [
                          "some rubble",
                          "a bush",
                          "a large sock",
                          "under a boulder",
                          "the bag",
                          "nowhere",
                          "somewhere",
                          "apparently everywhere",
                          "over your shoulder",
                          "out of the zombie",
                          "a hot air balloon",
                          "a Japanese kamakazi airplane",
                          "a mud puddle",
                          "your pocket",
                          "behind a small tree",
                          "behind a toothpick",
                          "your shadow"
                          ]

SPASTIC_CAT_STUFF = ["darts in and out, tripping the %s.",
                     "hacks a furball at the %s.",
                     "leaps on the face of the %s.",
                     "circles the %s rapidly, setting it off balance.",
                     "gets stepped on by the %s, causing it to fall.",
                     "pins the arms of the %s behind its back!",
                     "executes the Vulcan Nerve Pinch on the %s.",
                     "puts the %s in a sleeper hold.",
                     "exclaims, 'You shall not paaaaasss!' and stiff-arms the %s!."
                     ]

FIRECAT_AWESOMENESS = ["dawns dark shades, flicking a match at the %s.",
                       "breathes a cone of flame at the %s!",
                       "lobs a molotov cocktail at the %s.",
                       "hurls a fireball at the %s.",
                       "conjures hellfire and brimstone upon thy %s!",
                       "lights a fart in the %s's general direction. Hmm... smells of elderberries",
                       "doesn't watch the %s explode into flames.",
                       "reinvents greek fire, dowsing the %s in it.",
                       "offers the %s an incendiary grenade but doesn't offer the pin.",
                       "says, '%s go boom!'"
                       ]


# Method to bind to SpecialCat
def mediCatSpecial(self, player=None, zombie=None):
    
    player.updateHealth(self.level)
    print("Medicat just %s for %s healing" % (
            random.choice(MEDICAT_HEALING), self.level))


def ninjaCatSpecial(self, player=None, zombie=None):
    
    dmg = int(round(self.level * (self.level/2) + 5.5))
    zombie.updateHealth(-dmg)
    print("Ninjacat jumps out from %s dealing %s damage to %s!" % (
            random.choice(NINJA_CAT_HDING_PLACES), dmg, zombie.name))

def spasticCatSpecial(self, player=None, zombie=None):
    
    self.activation_chance = 0.1 + self.level/50
    zombie.debuffs.add("restrained")
    print(self.name, random.choice(SPASTIC_CAT_STUFF) % zombie.name)

def fireCatSpecial(self, player=None, zombie=None):
    
    if "burning" not in zombie.debuffs:
        print(self.name, random.choice(FIRECAT_AWESOMENESS) % zombie.name)
        zombie.debuffs.add("burning")
        zombie.name = "flaming " + zombie.name
        zombie.burning_damage = self.level


def spawnSpecialKitty():
    
    index = random.randint(0, len(SPECIAL_CATS)-1)
    cat_args = SPECIAL_CATS.pop(index)
    new_cat = SpecialCat(**cat_args)
    return new_cat


SPECIAL_CATS = [
                {"name": "Medicat",
                 "unbound_method": mediCatSpecial,
                 "activation_chance": 0.5,
                 "post": True},
                {"name": "Ninjacat",
                 "unbound_method": ninjaCatSpecial,
                 "activation_chance": 0.10,
                 "post": False},
                {"name": "Spasticat",
                 "unbound_method": spasticCatSpecial,
                 "activation_chance": 0.1,
                 "post": False},
                {"name": "Firecat",
                 "unbound_method": fireCatSpecial,
                 "activation_chance": 0.5,
                 "post": False},
                ]


class SpecialCat(Kitten):
    
    def __init__(self, name=None, unbound_method=None, activation_chance=0.0,
                 post = True):
        super().__init__(self)
        self.name = name
        self.specialMove = unbound_method
        self.activation_chance = activation_chance
        self.post = post
        
