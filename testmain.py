'''
Created on Jun 21, 2014

@author: Justin
'''
import unittest
import main
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
        
        mRandom.return_value = 0.01
        mInput.return_value = "insane"
        game = main.Game()
        game.difficulty = 1.25
        game._findKitten()
        game._findZombie()
        

if __name__ == "__main__":
    unittest.main()