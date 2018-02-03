import wlMain as wl
import numpy as np


class WlOneStat(wl.WlClassify):
    # first index is stat id, second index is timestamp id

    def __init__(self, hyperParams):
        self.players = self.makePlayers(10)
        self.playerStats = self.generateStats()
        params = {
            'pickEvaluator': self.evaluatePicks,
            'playerStats': self.playerStats,
            'pickMaker': self.pickMaker}
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

    def evaluatePicks(self, picksA, picksB, playerStats):
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
        return True
