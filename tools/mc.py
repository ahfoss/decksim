import numpy as np
import game
# Tools for gathering statistics for a single deck simulated
# many times.

def monteCarloRun(numLand: int, spellList: dict, numTurns: int, numMCRuns: int):
    landsArray = np.ones((numMCRuns, numTurns))
    spellCostArray = np.ones((numMCRuns, numTurns))
    for i in range(numMCRuns):
        ith_deck = game.Deck(numLand, game.SpellCards(spellList))
        ith_game = game.Game(ith_deck)
        for j in range(numTurns):
            ith_game.nextTurn()
        landsArray[i,:] = ith_game.landsPlayedList
        spellCostArray[i,:] = ith_game.spellCostPlayedList
    return(landsArray, spellCostArray)

def MCRunStats(larr, sarr, q):
    results = {}
    results["meanLand"] = larr.mean(axis=0)
    results["MCErrLand"] = larr.std(axis=0, ddof = 1) / np.sqrt(larr.shape[0])
    results["meanSpells"] = sarr.mean(axis=0)
    results["MCErrSpells"] = sarr.std(axis=0, ddof = 1) / np.sqrt(sarr.shape[0])
    results["quantSpells"] = np.quantile(sarr, q = q, axis=0)
    return(results)

if __name__ == "__main__":
    turns = 5
    cheapDeck = {1:20, 2:20}
    moderateDeck = {1:10, 2:10, 3:10, 4:5, 5:5}
    landArr1,spellArr1 = monteCarloRun(20, cheapDeck, turns, numMCRuns = 20000)
    landArr2,spellArr2 = monteCarloRun(20, moderateDeck, turns, numMCRuns = 20000)
    ml1 = MCRunStats(landArr1, spellArr1, q = 0.1)
    ml2 = MCRunStats(landArr2, spellArr2, q = 0.1)
    print("ml1['MCErrSpells']")
    print(ml1['MCErrSpells'])
    print("ml1['meanSpells']")
    print(ml1['meanSpells'])
    print("ml2['meanSpells']")
    print(ml2['meanSpells'])
