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
        # self.pickEvaluator = params['pickEvaluator'] #dont need these...
        # self.pickMaker = params['pickMaker']
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
        requiredParams = ['learnRate', 'perturbs', 'batchSize', 'iterations']
        for required in requiredParams:
            if required not in hyperParams:
                raise Exception('Missing "' + required + '" hyperparameter.')
        self._hyperParams = hyperParams

    def pickMaker(self, pickWeights):
        raise NotImplementedError('This needs to be overwritten')
    def pickEvaluator(self, picksA, picksB, playerStats):
        raise NotImplementedError('This needs to be overwritten')
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
                newWeight = max(statCat[idx] + delta, 0) # keep weight >= 0
                curArr.append(newWeight)
            retWeights.append(curArr)
        return retWeights

    def calcPickWeights(self, statWeightsIn):
        # given new statWeightsIn, calculate the
        # c_i probability of picking the ith player
        # The weights must always add to 1. This was written to guarantee 
        # this, and is checked in unit test but not checked every time
        # this method is called.
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
        score = 0

        for i in range(self.hyperParams['batchSize']):

            pick1 = self.pickMaker(pickWeights1)
            pick2 = self.pickMaker(pickWeights2)
            score += self.execEval(pick1, pick2)
        return score


    def iterateAlgorithm(self):
        print('stats to evaluate on')
        self.printStats()
        # This method under construction
        for i in range(0, self.hyperParams['iterations']):
            if i % 100 == 0:
                print('cur iteration', i)
                print('cur weights', self._statWeights)
            self.singleIteration()


    def singleIteration(self):
        # This method under construction
        # todo: make sure it takes into account multiple stats
        statWeightsLoc = [] # new stat weights to evaluate
        pickWeightsLoc = [] # new player pick weights to evaluate
        idxMax = self.hyperParams['perturbs']
        for idx in range(0, idxMax):
            # rename these! confusing
            statWeightLoc = self.perturbWeight()
            statWeightsLoc.append(statWeightLoc)
            pickWeightLoc = self.calcPickWeights(statWeightLoc)
            pickWeightsLoc.append(pickWeightLoc)
        
        # print(pickWeights)
        # todo: add error handling here- what if best idx isn't found, what 
        # should maxScore be initialized at 
        # todo: more efficient if A v B isn't repeated with B v A
        maxScore = -999999999
        bestIdx = -1

        for outerIdx in range(0, idxMax):
            
            for innerIdx in range(0, idxMax):
                curScore = 0
                # Score how well outerIdx fares against innerIdx
                # Add this score to the current total
                curScore += self.evaluatePickWeights(pickWeightsLoc[outerIdx], pickWeightsLoc[innerIdx])
                if curScore > maxScore:
                    maxScore = curScore
                    bestIdx = outerIdx

        # print('winner score', maxScore)
        # iteration complete, store winner as new stat weight
        self._statWeights = statWeightsLoc[bestIdx]






        
    def printStats(self):
        # print player stats; after initialization these
        # will remain constant
        print(self.playerStats)

    def printWeights(self):
        # print current weights applied to player stats
        print(self._statWeights)
