import wlMain as wl
import numpy as np

def generate(playerStatsIn, players):
    """
    generate() creates player statistics for player array "players"
    and blank input array "playerStatsIn", based on a normal distribution 
    defined below
    """
    for player in players:
        arrayToAppend = []
        playerAvg = 10*(player+1)  # mean to center normal distr about
        variance = 2  # variance for normal distribution
        yearsBack = 0
        while yearsBack < 3:
            statToAppend = np.random.normal(playerAvg, variance)
            if statToAppend > 0:
                yearsBack += 1
                arrayToAppend.append([statToAppend])
        playerStatsIn.append(arrayToAppend)


def makePlayers(numberOfPlayers):
    """
    generate array of player labels in an array, [0,1,2,...,numberOfPlayers]
    """
    returnArr = []
    for player in range(numberOfPlayers):
        returnArr.append(player)
    return returnArr


players = makePlayers(10)
playerStats = []
generate(playerStats, players)
wl.wlClassify(playerStats)
# print(playerStats)
