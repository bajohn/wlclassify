import numpy as np

# Main file for WLClassify execution.
# Stored on server 104.236.65.211 (mean-sandbox)
# This will be broken out into more files as it grows.
# Checked for pep8 compliance with pycodestyle script.

# variable formats:

# let stats array S = [[[]]],
# where s[2][3][4] is player label 2, player stat 3, 4 timestamps back.


class WlClassify:

    def __init__(self, playerStats, pickEvaluator, hyperParams):
        """
        Generate initial weights for player stats.
        The initial weights are all the same, meaning
        at first glance we weigh each stat equally.
        Since all players are assumed to have the same
        amount of data, we use the player indexed at 0
        to calculate the appropriate weight.
        """
        playerStats0 = playerStats[0]
        yearCount = len(playerStats[0])
        statCount = len(playerStats[0][0])
        initialWeight = 1 / (yearCount * statCount)

        # store variables
        self.pickEvaluator = pickEvaluator
        self.playerStats = playerStats
        self.hyperParams = hyperParams

        self.__testVar = 3

        # first index is stat id, second index is timestamp id
        self.statWeights = np.full((statCount, yearCount), initialWeight)

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

    def printStats(self):
        # print player stats; after initialization these
        # will remain constant
        print(self.playerStats)

    def printWeights(self):
        # print current weights applied to player stats
        print(self.statWeights)
