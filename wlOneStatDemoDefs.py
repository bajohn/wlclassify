import wlMain as wl
import numpy as np


class WlOneStat(wl.WlClassify):
    # first index is stat id, second index is timestamp id

    def __init__(self, hyperParams):
        self.players = self.makePlayers(10)
        self.playerStats = self.generateStats()
        # todo: delete these params, should overwrite instead of pass
        params = {
            'playerStats': self.playerStats
        }
        super().__init__(params, hyperParams)

    def generateStats(self):
        """
        generate() creates player statistics for player array "players"
        based on normal distributions defined below
        """
        playerStatsOut = []
        for player in self.players:
            arrayToAppend = []
            playerAvg = 10 * (player + 1)  # mean to center normal distr about
            variance = 2  # variance for normal distribution
            yearsBack = 0
            while yearsBack < 3:
                # todo: add yearsBack to this calculation to make the algorithm have 
                # some data to play with 
                statToAppend = np.random.normal(playerAvg, variance)
                if statToAppend > 0:
                    yearsBack += 1
                    arrayToAppend.append([statToAppend])
            playerStatsOut.append(arrayToAppend)
        return playerStatsOut

    def makePlayers(self, numberOfPlayers):
        """
        generate array of player labels in an array,
        [0,1,2,...,numberOfPlayers]
        """
        returnArr = []
        for player in range(numberOfPlayers):
            returnArr.append(player)
        return returnArr

    def pickEvaluator(self, picksA, picksB, playerStats):
        """
        for the competition in this demo, two
        picks of players compete against each other.
        sum the most recent stat
        value for each player in each pick; the highest sum wins
        """
        picksAVal = 0
        picksBVal = 0
        if(len(picksA) != len(picksB)):
            raise Exception('picks to evaluate must be same length')
        for a in picksA:
            picksAVal += playerStats[a][0][0]  # add most recent stat value
        for b in picksB:
            picksBVal += playerStats[b][0][0]

        if picksAVal == picksBVal:
            return 0  # tie
        elif picksAVal > picksBVal:
            return 1  # pick A beats pick B
        elif picksAVal < picksBVal:
            return -1  # pick B beats pick A

    def pickMaker(self, playerWeights):
        """
        For the competition in this demo, simply pick any 3 players. 
        Assume playerWeights is an array where each entry is the weight
        to place on the nth player, like [.01, .02, .07] (must sum to 1)
        """
        boundaryArr = [] # takes form [.01, .03, 1.0] for use with RNG on [0,1)
        lastBoundary = 0
        for entry in playerWeights:
            newBoundary = lastBoundary + entry
            boundaryArr.append(newBoundary)
            lastBoundary = newBoundary
        
        playerArr = []
        thisPick = 99
        while len(playerArr) < 3: # this game assumes 3 player picks.
            randNum = np.random.random_sample()
            for playerIdx in range(len(boundaryArr)):
                if playerIdx == 0 and randNum <  boundaryArr[playerIdx]:
                    thisPick = playerIdx
                    break
                elif randNum < boundaryArr[playerIdx] and randNum > boundaryArr[playerIdx-1]:
                    thisPick = playerIdx
                    break
                
            # cannot repeat a pick:
            if thisPick not in playerArr:
                playerArr.append(thisPick)
        playerArr.sort()
        return playerArr
