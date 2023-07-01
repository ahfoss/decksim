from collections import defaultdict, Counter
from random import choices
from itertools import chain, combinations

# Should debug statements about the inner calculations be printed.
DEBUG = False

# Should the narrative of the game be printed.
VERBOSE = False

# A core algorithm required by this simulation.
def powerset(iterable):
    '''
    powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    '''
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

class SpellCards:
    '''
    A class to describe a collection of spell cards.
    '''
    def __init__(self, cmcDict: dict) -> None:
        '''
        cmcDict: A dictionary of format CMC: count.
        '''
        self.cmcDict = defaultdict(int, cmcDict)
    def items(self) -> list:
        return(self.cmcDict.items())
    def getNumCards(self) -> int:
        return(sum(self.cmcDict.values()))
    def getSpellList(self) -> defaultdict:
        return(self.cmcDict)
    def addSpellByCost(self, cost: int) -> None:
        self.cmcDict[cost] += 1
    def removeSpellByCost(self, cost: int) -> None:
        if self.cmcDict[cost] > 0:
            self.cmcDict[cost] -= 1
        else:
            raise Exception("Cannot remove a spell that doesn't exist.")
    def removeSpellList(self, spells: dict):
        for tup in spells.items():
            for i in range(tup[1]):
                self.removeSpellByCost(tup[0])
    def selectMaxCostSpell(self) -> int:
        positiveCosts = [x[0] for x in self.cmcDict.items() if x[1] > 0]
        return(max(positiveCosts))
    def removeMaxCostSpell(self) -> int:
        maxCost = self.selectMaxCostSpell()
        self.removeSpellByCost(maxCost)
        return(maxCost)
    def selectRandomSpell(self) -> int:
        cost = choices(list(self.cmcDict.keys()), weights = self.cmcDict.values())
        return(cost[0])
    def removeRandomSpell(self) -> int:
        cost = self.selectRandomSpell()
        self.removeSpellByCost(cost)
        return(cost)

class Deck:
    '''
    numLand: Integer, number of basic lands in the deck.
    spells: an object of class SpellCards describing cost of spells.
    '''
    def __init__(self, numLand: int, spells: SpellCards) -> None:
        self.numLand = numLand
        self.spells = spells
    def getNumSpells(self) -> int:
        return(self.spells.getNumCards())
    def printDeckSize(self) -> None:
        print("The decksize is %d" % (self.getNumSpells() + self.numLand))
    def print(self) -> None:
        print("Deck: Land = %d, with spell cmc:" % self.numLand, end = '')
        print(dict(self.spells.getSpellList()))

class Hand:
    def __init__(self) -> None:
        self.numLand = 0
        self.spells = SpellCards({})
    def getNumSpells(self) -> None:
        return(self.spells.getNumCards())
    def discardMaxCostSpell(self) -> int:
        maxCost = self.spells.removeMaxCostSpell()
        return(maxCost)
    def playMaxCost(self, numLandInPlay: int) -> dict:
        # Create list of all spell cmcs (with repeats) with cost less than numLandInPlay.
        listOfLists = [[tup[0]] * tup[1] for tup in self.spells.items() if tup[0] <= numLandInPlay]
        spellList = list(chain.from_iterable(listOfLists))
        if DEBUG:
            print("spellList")
            print(spellList)
        # Construct power set of this list.
        thisPowerset = list(set(powerset(spellList)))
        if DEBUG:
            print("thisPowerset")
            print(thisPowerset)
        # For each element of power set, calculate total cmc and number of spells.
        totalCmc = [sum(x) for x in thisPowerset]
        if DEBUG:
            print("totalCmc")
            print(totalCmc)
        numSpells = [len(x) for x in thisPowerset]
        if DEBUG:
            print("numSpells")
            print(numSpells)
        # Choose element with 1) highest cmc less than numLandInPlay, and 2) largest number of spells.
        dataArray = list(zip(thisPowerset, totalCmc, numSpells))
        dataArray = [row for row in dataArray if row[1] <= numLandInPlay]
        sortedArray = sorted(dataArray, key = lambda x: (-x[1], -x[2]))
        if DEBUG:
            print("sortedArray")
            print(sortedArray)
        # Deduct chosen set's values.
        chosenValue = dict(Counter(sortedArray[0][0]))
        self.spells.removeSpellList(chosenValue)
        if DEBUG:
            print("chosenValue")
            print(chosenValue)
        # Return dict describing this chosen set.
        return(chosenValue)

    def draw(self, deck):
        # choose land or spell
        drawType = choices(['L','S'], weights = [deck.numLand, deck.getNumSpells()])[0]
        if drawType == 'L':
            # if land, decrement deck land and add to hand.
            deck.numLand -= 1
            self.numLand += 1
        else:
            # else decrement spells and return a spell cmc.
            cmc = deck.spells.removeRandomSpell()
            self.spells.addSpellByCost(cmc)
        if VERBOSE:
            print("Drew %s" % drawType)
            self.print()
    def print(self) -> None:
        print("Hand: Land = %d, with spell cmc:" % self.numLand, end = '')
        print(dict(self.spells.getSpellList()))

class Game:
    def __init__(self, deck: Deck, initialHandSize: int = 7) -> None:
        self.deck = deck
        self.hand = Hand()
        self.landInPlay = 0
        self.spellCostPlayedList = []
        self.spellsPlayedList = []
        self.landsPlayedList = []
        if VERBOSE:
            print("DRAWING HAND OF %d" % initialHandSize)
        for i in range(initialHandSize):
            self.hand.draw(self.deck)
    def print(self) -> None:
        print("self.landsPlayedList")
        print(self.landsPlayedList)
        print("self.spellCostPlayedList")
        print(self.spellCostPlayedList)
        print("self.spellsPlayedList")
        print(self.spellsPlayedList)
    def nextTurn(self) -> None:
        if VERBOSE:
            print("STARTING TURN %d" % (len(self.landsPlayedList) + 1))
        # draw
        self.hand.draw(self.deck)
        # play land if able.
        if self.hand.numLand > 0:
            self.hand.numLand -= 1
            self.landInPlay += 1
            self.landsPlayedList.append(1)
        else:
            self.landsPlayedList.append(0)
        if VERBOSE:
            print("Played %d land, total %d" % (self.landsPlayedList[-1], self.landInPlay))
        # play as much spell cost as possible
        # - if spells, play max cost
        playedDict = self.hand.playMaxCost(self.landInPlay)
        self.spellsPlayedList.append(len(playedDict))
        self.spellCostPlayedList.append(sum([x[0]*x[1] for x in playedDict.items()]))
        if VERBOSE:
            print("Played %d spells, cmc %d" % (self.spellsPlayedList[-1], self.spellCostPlayedList[-1]))
        # Discard down to 7
        while self.hand.numLand + self.hand.getNumSpells() > 7:
            if VERBOSE:
                print('Discarding a spell due to 8+ cards')
            self.hand.discardMaxCostSpell()

if __name__ == "__main__":
    balancedSpells = SpellCards({1:10, 2:10, 3:8, 4:8, 5:4})
    cheapSpells = SpellCards({1:25, 2:15})
    deck1 = Deck(20, balancedSpells)
    deck1.printDeckSize()
    game1 = Game(deck1)
    game1.deck.print()
    game1.hand.print()
    for _ in range(20):
        game1.nextTurn()
    game1.print()
