import numpy as np

# Main file for WLClassify execution.
# Stored on server 104.236.65.211 (mean-sandbox)
# This will be broken out into more files as it grows.
# Checked for pep8 compliance with pycodestyle script.

# variable formats:

# let stats array S = [[[]]],
# where s[2][3][4] is player label 2, player stat 3, 4 timestamps back.


class WlClassify:

    def __init__(self, params, hyperParams):
        """
        Generate initial weights for player stats.
        The initial weights are all the same, meaning
        at first glance we weigh each stat equally.
        Since all players are assumed to have the same
        amount of data, we use the player indexed at 0
        to calculate the appropriate weight.
        """

        # store variables
        self.pickEvaluator = params['pickEvaluator']
        self.pickMaker = params['pickMaker']
        self.playerStats = params['playerStats']
        self.hyperParams = hyperParams

        # Indices for playerStats[a][b][c]:
        # a=player number, b=timestamp, c=stat category
        timeCount = len(self.playerStats[0])
        statCount = len(self.playerStats[0][0])
        initialWeight = 1 / (timeCount * statCount)

        # first index is stat id, second index is timestamp id
        self._statWeights = np.full((timeCount, statCount), initialWeight)

    @property
    def hyperParams(self):
        return self._hyperParams

    @hyperParams.setter
    def hyperParams(self, hyperParams):
        requiredParams = ['learnRate', 'perturbs', 'batchSize']
        for required in requiredParams:
            if required not in hyperParams:
                raise Exception('Missing "' + required + '" hyperparameter.')
        self._hyperParams = hyperParams

    def execEval(self, picksA, picksB):
        return self.pickEvaluator(picksA, picksB, self.playerStats)

    def perturbWeight(self):
        # generate a single perturbation of the current statWeights
        learnRate = self.hyperParams['learnRate']
        retWeights = []
        for statCat in self._statWeights:
            curArr = []
            for idx in range(len(statCat)):
                delta = 2 * (np.random.random_sample() - .5) * learnRate
                curArr.append(statCat[idx] + delta)
            retWeights.append(curArr)
        return retWeights

    def calcPickWeights(self, statWeightsIn):
        # given new statWeightsIn, calculate the
        # c_i probability of picking the ith player

        rawPickWeights = []
        finalPickWeights = []  # ith position is probability for ith player
        minPickWeight = 99999999999
        sumOfWeights = 0
        playerIdx = 0
        for player in self.playerStats:
            curRawWeight = 0
            timeIdx = 0
            for timerow in player:
                statIdx = 0
                for statVal in timerow:
                    curRawWeight += statWeightsIn[timeIdx][statIdx] * statVal
                    statIdx += 1
                timeIdx += 1

            rawPickWeights.append(curRawWeight)
            sumOfWeights += curRawWeight
            if curRawWeight < minPickWeight:
                minPickWeight = curRawWeight

        for weightIdx in range(len(rawPickWeights)):
            rawWeight = rawPickWeights[weightIdx]
            finalWeight = (rawWeight + minPickWeight) / \
                (sumOfWeights + len(self.playerStats) * minPickWeight)

            finalPickWeights.append(finalWeight)
        return finalPickWeights

    def evaluatePickWeights(self, pickWeights1, pickWeights2):
        # hyperparams: 'batchSize'
        print(self.hyperparams)
        score = 0

        for i in range(self.hyperparams['batchSize']):
            pick1 = self.pickMaker(pickWeights1)
            pick2 = self.pickMaker(pickWeights2)
            score += self.execEval(pick1, pick2)
        
        return score
    def printStats(self):
        # print player stats; after initialization these
        # will remain constant
        print(self.playerStats)

    def printWeights(self):
        # print current weights applied to player stats
        print(self._statWeights)
