from game import Directions
import random
from vars import *


def scoreEvaluationFunction(currentGameState):
    enemyPos = currentGameState.getEnemyPositions()
    projPos = currentGameState.getProjPositions()
    pos = currentGameState.getPlayerPosition()
    enemyPosDiff = [abs(enemy[0] - pos[0]) + abs(enemy[1] - pos[1]) for enemy in enemyPos]
    projPosDiff = [abs(proj[0] - pos[0]) + abs(proj[1] - pos[1]) for proj in projPos]
    closestEnemy = min(enemyPosDiff) if len(enemyPos) != 0 else SCREEN_HEIGHT
    if closestEnemy > SCREEN_HEIGHT / 4:
        closestEnemy = SCREEN_HEIGHT / 4
    closestProj = min(projPosDiff) if len(projPos) != 0 else SCREEN_HEIGHT
    if closestProj > SCREEN_HEIGHT / 2:
        closestProj = SCREEN_HEIGHT / 2
    threatDistScore = closestEnemy + 20 * closestProj
    
    # punish the score if flying too wide
    distToCenter = abs(pos[0] - SCREEN_WIDTH / 2)
    distToCenterScore = -distToCenter
    
    totalScore = (2 * currentGameState.getScore(), threatDistScore, distToCenterScore)
    # print totalScore
    return sum(totalScore)


class Agent:
    def __init__(self, depth='1'):
        self.index = 0  # player is always agent index 0
        self.evaluationFunction = scoreEvaluationFunction
        self.depth = int(depth)


class MinimaxAgent(Agent):
    def getAction(self, gameState):
        def recurse(state, index, depth):
            print "depth %d, index %d" % (depth, index)
            # check if it's the terminal state
            if state.isWin() or state.isLose() or len(state.getLegalActions(index)) == 0 or depth == 0:
                return self.evaluationFunction(state), Directions.STOP
            
            nextIndex = (index + 1) % state.getNumAgents()
            nextDepth = depth - 1 if nextIndex == state.getNumAgents() - 1 else depth
            # compute the recursion
            legalActions = state.getLegalActions(index)
            # if Directions.STOP in legalActions and len(legalActions) > 1:
            #     legalActions.remove(Directions.STOP)
            choices = []
            for legalAction in legalActions:
                choices.append((recurse(state.generateSuccessor(index, legalAction), nextIndex, nextDepth)[0], legalAction))
            
            # return max value if it's agent otherwise min if it's opponent
            chosenValue = max(choices) if index == 0 else min(choices)
            indices = [i for i in range(len(choices)) if choices[i][0] == chosenValue[0]]
            chosenIndex = random.choice(indices)  # Pick randomly among max
            action = legalActions[chosenIndex]
            if len(indices) > 1:
                action = Directions.STOP
            return chosenValue, action
            
            # return max(choices) if index == 0 else min(choices)
        
        value, action = recurse(gameState, self.index, self.depth)
        return action


class AlphaBetaAgent(Agent):
    def getAction(self, gameState):
        def recurse(state, index, depth, lowerBound, upperBound):
            print "depth %d, index %d" % (depth, index)
            # check if it's the terminal state
            if state.isWin() or state.isLose() or len(state.getLegalActions(index)) == 0 or depth == 0:
                return self.evaluationFunction(state), Directions.STOP
            
            nextIndex = (index + 1) % state.getNumAgents()
            nextDepth = depth - 1 if nextIndex == state.getNumAgents() - 1 else depth
            
            legalActions = state.getLegalActions(index)
            # if Directions.STOP in legalActions and len(legalActions) > 1:
            #     legalActions.remove(Directions.STOP)
            choices = []
            for legalAction in legalActions:
                # compute the recursion
                value, action = recurse(state.generateSuccessor(index, legalAction), nextIndex, nextDepth, lowerBound, upperBound)
                choices.append((value, legalAction))
                # update the local lower and upper bound
                if index == 0:
                    lowerBound = max(value, lowerBound)
                else:
                    upperBound = min(value, upperBound)
                # prune a node if its interval doesn't have non-trivial overlap with every ancestor
                if lowerBound > upperBound:
                    break
            # return max value if it's agent otherwise min if it's opponent
            chosenValue = max(choices) if index == 0 else min(choices)
            indices = [i for i in range(len(choices)) if choices[i][0] == chosenValue[0]]
            chosenIndex = random.choice(indices)  # Pick randomly among max
            action = legalActions[chosenIndex]
            if len(indices) > 1:
                action = Directions.STOP
            return chosenValue, action
            # return max(choices) if index == 0 else min(choices)
        
        value, action = recurse(gameState, self.index, self.depth, -INF, INF)
        return action
