import wlOneStatDemoDefs as wlOne

hyperParams = {
    'learnRate': .1,
    'perturbs': 10,  # number of perturbations per iteration
    'batchSize': 10  # number of runs per perturbation
}
wlOneLoc = wlOne.WlOneStat(hyperParams)  # initialize

# wlOneLoc.printStats()
# wlOneLoc.printWeights()

playersA = [0, 1, 2]
playersB = [7, 8, 9]

# print(wlOneLoc.execEval(playersA, playersB))
print(wlOneLoc.hyperParams)
