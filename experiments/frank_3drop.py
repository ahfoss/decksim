import sys
sys.path.append("../tools/")

import mc

goldLand = 25
turns = 3
goldDeck = {1:17, 2:13, 3:5}
goldLand, goldSpell = mc.monteCarloRun(goldLand, goldDeck, turns + 3, numMCRuns = 100)

print("goldSpell")
print(goldSpell)
