import wlOneStatDemoDefs as wlOne
import unittest


class TestWL(unittest.TestCase):

    def setUp(self):
        hyperParams = {
            'learnRate': .1,
            'perturbs': 10,  # number of perturbations per iteration
            'batchSize': 10  # number of runs per perturbation
        }
        self._wlOneLoc = wlOne.WlOneStat(hyperParams)  # initialize

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

        # some of all weights must be 1 (to 3 decimal places in case of rounding errors.)
        self.assertEqual(round(sumOfWeights * 1000) / 1000, 1)

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


unittest.main()
