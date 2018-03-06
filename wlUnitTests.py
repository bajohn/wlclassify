import wlOneStatDemoDefs as wlOne
import numpy as np
import unittest


class TestWL(unittest.TestCase):

    def setUp(self):
        hyperParams = {
            'learnRate': .1,
            'perturbs': 10,  # number of perturbations per iteration
            'batchSize': 100  # number of runs per perturbation
        }
        self._wlOneLoc = wlOne.WlOneStat(hyperParams)  # initialize
        print('Setting up test.')
        # wlOneLoc.printStats()
        # wlOneLoc.printWeights()

        #
        # print(wlOneLoc.printWeights())
        # print(wlOneLoc.perturbWeight())

    def testCalcPickWeights(self):
        result = self._wlOneLoc.calcPickWeights(self._wlOneLoc.perturbWeight())
        sumOfWeights = 0
        for weight in result:
            sumOfWeights += weight

        # Sum of all weights must 
        # be 1 (to 3 decimal places in case of rounding errors.)
        self.assertAlmostEqual(sumOfWeights, 1, places=5)

    def testPlayerPickEval(self):
        # Checking that the evaluation of player A vs player B in the
        # onestatdemo contest works.
        # Player B should beat player A
        playersA = [0, 1, 2]
        playersB = [7, 8, 9]
        contest1 = self._wlOneLoc.execEval(playersA, playersB)
        contest2 = self._wlOneLoc.execEval(playersB, playersA)
        contest3 = self._wlOneLoc.execEval(playersA, playersA)
        # Negative 1 indicates second entry beat first entry
        self.assertEqual(contest1, -1)
        # Positive 1 indicates second entry beat first entry
        self.assertEqual(contest2, 1)
        # 0 indicates tie, such as an entry competing against itself.
        self.assertEqual(contest3, 0)


    def testPickMaker(self):
        # Just check that 3 players are returned for now, and each is 
        # an integer on [0,9]
        # A more rigorous test would be to run a large number of times
        # and check the statistical distribution
        playerWeights =  [.01, 0, .09, .2, .1, .05, .05, .1, .1, .3] 
        pick = self._wlOneLoc.pickMaker(playerWeights)
        self.assertEqual(len(pick), 3)
        for player in pick:
            self.assertTrue(player in range(len(playerWeights)))
        
    def testEvaluatePickWeights(self):
        # playerWeights1 are superior weights to playerWeights3
        # playerWeights2 are random.
        # Therefore we assert over batchSize of 100 that,
        # performance-wise, playerWeights1 > playerWeights2 > playerWeights3
        playerWeights1 = [0,0,0,0,0,0,0,.3,.3,.4]
        playerWeights2 = [.1,.1,.1,.1,.1,.1,.1,.1,.1,.1]
        playerWeights3 = [.3,.3,.4,0,0,0,0,0,0,0]

        result12 = self._wlOneLoc.evaluatePickWeights(playerWeights1, playerWeights2)
        result13 = self._wlOneLoc.evaluatePickWeights(playerWeights1, playerWeights3)
        result23 = self._wlOneLoc.evaluatePickWeights(playerWeights2, playerWeights3)

        # assert symmetry 
        result21 = self._wlOneLoc.evaluatePickWeights(playerWeights2, playerWeights1)
        result31 = self._wlOneLoc.evaluatePickWeights(playerWeights3, playerWeights1)
        result32 = self._wlOneLoc.evaluatePickWeights(playerWeights3, playerWeights2)
        print(result12, result13, result23, result21, result31, result32)
        self.assertTrue(result21 < 0)
        self.assertTrue(result31 <= result32)
        self.assertTrue(result32 < 0 )
        self.assertTrue(result12 > 0)
        self.assertTrue(result12 >= result23)
        self.assertTrue(result23 > 0 )
        
unittest.main()
