from game import Directions
import random
from vars import *
import math


def scoreEvaluationFunction(currentGameState):
    enemyPos = currentGameState.getEnemyPositions()
    projPos = currentGameState.getProjPositions()
    pos = currentGameState.getPlayerPosition()
    
    def getSquaredDistance(pos1, pos2):
        return (pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2

    enemyPosDiff = [getSquaredDistance(pos, enemy) for enemy in enemyPos if enemy[1] < pos[1] + PLAYER_SIZE]
    projPosDiff = [getSquaredDistance(pos, proj) for proj in projPos if proj[1] < pos[1] + PLAYER_SIZE]

    # calculate the number of threats in a range centered at player's position
    radius = 256
    closestEnemy = 0
    for diff in enemyPosDiff:
        if diff < (2 * radius)**2:            
            closestEnemy += radius**2 / diff
    closestProj = 0
    for diff in projPosDiff:
        if diff < (2 * radius)**2:
            closestProj += radius**2 / diff

    threatDistScore = -10 * closestEnemy - 100 * closestProj

    # if len(projPosDiff) > 0:
    #     print math.sqrt(min(projPosDiff))

    # punish the score if flying too wide
    distToCenterScore = -abs(pos[0] - (SCREEN_WIDTH - PLAYER_SIZE) / 2)**2 / 32 - abs(int(0.85 * SCREEN_HEIGHT) - pos[1]) / 64

    # current game score
    gameScore = 2 * currentGameState.getScore()

    # cross aaaaaaaaaaaaaaaa got dammit!!!
    bypassScore = -1000 *(len(projPosDiff) + len(enemyPosDiff))

    # horizontal distances to enemies
    horizontalDist = [abs(pos[0] - enemy[0]) for enemy in enemyPos if enemy[1] < pos[1] + PLAYER_SIZE]
    if len(horizontalDist) == 0:
        horizontalScore = SCREEN_WIDTH
    else:
        horizontalScore = sum(horizontalDist) / 4

    totalScore = (gameScore, threatDistScore, distToCenterScore, horizontalScore)
    #print totalScore, sum(totalScore)
    return sum(totalScore)


class Agent:
    def __init__(self, depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = scoreEvaluationFunction
        self.depth = int(depth)


class MinimaxAgent(Agent):
    def getAction(self, gameState):
        def recurse(state, index, depth):
            # print gameState.getNumProjectile()
            # check if it's the terminal state
            if state.isWin() or state.isLose() or len(state.getLegalActions(index)) == 0 or depth == 0:
                return self.evaluationFunction(state), Directions.STOP
            
            nextIndex = 0 if index == state.getNumAgents() - 1 else index + 1
            nextDepth = depth - 1 if nextIndex == state.getNumAgents() - 1 else depth
            # compute the recursion
            legalActions = state.getLegalActions(index)
            if Directions.STOP in legalActions and len(legalActions) > 1:
                legalActions.remove(Directions.STOP)
            choices = []
            for legalAction in legalActions:
                choices.append((recurse(state.generateSuccessor(index, legalAction), nextIndex, nextDepth)[0], legalAction))
            # return max value if it's agent otherwise min if it's opponent
            
            chosenValue = max(choices) if index == 0 else min(choices)
            indices = [i for i in range(len(choices)) if choices[i][0] == chosenValue[0]]
            # print choices
            # print chosenValue
            # print indices
            chosenIndex = random.choice(indices)  # Pick randomly among max
            
            return chosenValue, legalActions[chosenIndex]
        
        # return max(choices) if index == 0 else min(choices)
        
        value, action = recurse(gameState, self.index, self.depth)
        return action