'''
Created on Jun 21, 2014

@author: Justin
'''
import unittest
import main
import random
from unittest import mock


class TestGame(unittest.TestCase):

    @mock.patch("builtins.input")
    def testUseItem(self, mInput):

        game = main.Game()
        player = game.player
        item = mock.Mock()
        item.name = "foo"
        item.getHealing.return_value = 1
        player.inventory = [item]
        mInput.return_value = "1"
        game._useItem()
    
    @mock.patch("random.random")
    @mock.patch("player.Player.adoptKitten")
    def test_FindKitten(self, mAdoptKitten, mRandom):
        
        game = main.Game()
        mRandom.return_value = 0.01
        game._findKitten()
        self.assert_(mAdoptKitten.called)
    
    @mock.patch("random.random")
    @mock.patch("builtins.input")
    def test_FindZombie(self, mInput, mRandom):
        
        mRandom.return_value = 0.50
        mInput.return_value = "insane"
        game = main.Game()
        game.player.level = 7
        for i in range(10):
            game._findKitten()
        game.player._courage = 1000
        game.player._insanity = 1000
        game.player.health = 1000 * 2
        game.difficulty = 1.25
        x = random.randint(0, 10)
        y = 10 - x
        game.player.attacking_kittens = x
        game.player.defending_kittens = y
        print(game.player.attacking_kittens, game.player.defending_kittens)
        game._findZombie()
        print(game.player.attacking_kittens, game.player.defending_kittens)
        

if __name__ == "__main__":
    unittest.main()