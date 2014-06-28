"""
Handles saving and loading of game states.
"""

import pickle
import os
import subprocess
import time


SAVE_DIR = os.environ["LOCALAPPDATA"] + "\\CCLA"

FIRST_TIME = """
This is your first time running Crazy Cat Lady Apocalypse.
Let's do some setup. I'm being verbose about this because why not?
I'm going to create a directory for you. Mk, now watch.
"""


def saveGame(player):
    """Saves the player game state."""
    
    if not os.access(SAVE_DIR, os.F_OK):
        print(FIRST_TIME)
        os.makedirs(SAVE_DIR)
        time.sleep(6)
        subprocess.Popen(r"explorer /open, %s" % SAVE_DIR)
        time.sleep(1)
        print("And here comes your new save file. Keep this safe. Your cats lives depend on it.")
        time.sleep(5)
    with open(SAVE_DIR + "\\ccla.save", "wb") as f:
        pickle.dump(player, f)
        print("(Game Saved)")

def loadGame():
    
    with open(SAVE_DIR + "\\ccla.save", "rb") as f:
        data = pickle.load(f)
        return data

def deleteSave():
    
    os.remove(SAVE_DIR + "\\ccla.save")


if __name__ == "__main__":
    saveGame("thing")