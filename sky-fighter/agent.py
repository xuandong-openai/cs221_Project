from game import Directions
import random
from vars import *
import math
from collections import Counter


def scoreEvaluationFunction(currentGameState):
    pos = currentGameState.getPlayerPosition()
    enemies = currentGameState.getEnemies()
    enemyPos = currentGameState.getEnemyPositions()
    projPos = currentGameState.getProjPositions()

    def getSquaredDistance(pos1, pos2):
        return (pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2

    enemyPosDiff = [getSquaredDistance(pos, enemy) for enemy in enemyPos if enemy[1] < pos[1] + PLAYER_SIZE]
    projPosDiff = [getSquaredDistance(pos, proj) for proj in projPos if proj[1] < pos[1] + PLAYER_SIZE]

    # calculate the number of threats in a range centered at player's position
    closestEnemyWeight, closestProjWeight = -50, -100
    radius = 256
    closestEnemy = 0
    for diff in enemyPosDiff:
        if diff < (2 * radius) ** 2:
            closestEnemy += radius ** 2 / diff
    closestProj = 0
    for diff in projPosDiff:
        if diff < (2 * radius) ** 2:
            closestProj += radius ** 2 / diff
    closestEnemyScore = closestEnemyWeight * closestEnemy
    closestProjScore = closestProjWeight * closestProj

    # punish the score if flying too wide
    xDeviationWeight, yDeviationWeight = -1.0 / 25, -1.0 / 50
    xDeviation = abs(pos[0] - (SCREEN_WIDTH - PLAYER_SIZE) / 2) ** 2
    yDeviation = abs(int(0.85 * SCREEN_HEIGHT) - pos[1])
    distToCenterScore = int(xDeviationWeight * xDeviation) + int(yDeviationWeight * yDeviation)

    # current game score
    gameScoreWeight = 1
    game = currentGameState.getScore()
    gameScore = gameScoreWeight * game

    # horizontal distances to enemies
    horizontalDistWeight = 1.0 / 4
    horizontalDist = [abs(pos[0] - enemy[0]) for enemy in enemyPos if enemy[1] < pos[1] + PLAYER_SIZE]
    if len(horizontalDist) == 0:
        horizontalDist = [4 * SCREEN_WIDTH]
    horizontalScore = int(horizontalDistWeight * sum(horizontalDist))

    totalScore = [gameScore, closestEnemyScore, closestProjScore, distToCenterScore, horizontalScore]
    return sum(totalScore)


def getFeatureVector(currentGameState):
    enemyPos = currentGameState.getEnemyPositions()
    projPos = currentGameState.getProjPositions()
    pos = currentGameState.getPlayerPosition()
    # weight = currentGameState.learner.getWeight()

    def getSquaredDistance(pos1, pos2):
        return (pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2

    enemyPosDiff = [getSquaredDistance(pos, enemy) for enemy in enemyPos if enemy[1] < pos[1] + PLAYER_SIZE]
    projPosDiff = [getSquaredDistance(pos, proj) for proj in projPos if proj[1] < pos[1] + PLAYER_SIZE]

    features = {}
    # calculate the number of threats in a range centered at player's position
    features['radius'] = 256
    features['closestEnemy'] = 0
    for diff in enemyPosDiff:
        if diff < (2 * features['radius']) ** 2:
            features['closestEnemy'] += features['radius'] ** 2 / diff
    features['closestProj'] = 0
    for diff in projPosDiff:
        if diff < (2 * features['radius']) ** 2:
            features['closestProj'] += features['radius'] ** 2 / diff

    # punish the score if flying too wide
    features['xDeviation'] = abs(pos[0] - (SCREEN_WIDTH - PLAYER_SIZE) / 2) ** 2
    features['yDeviation'] = abs(int(0.85 * SCREEN_HEIGHT) - pos[1])

    # current game score
    features['game'] = currentGameState.getScore()

    # horizontal distances to enemies
    horizontalDist = [abs(pos[0] - enemy[0]) for enemy in enemyPos if enemy[1] < pos[1] + PLAYER_SIZE]
    if len(horizontalDist) == 0:
        horizontalDist = [4 * SCREEN_WIDTH]
    features['horizontalDist'] = sum(horizontalDist)

    return Counter(features)


def ultimateEvaluationFunction(currentGameState):
    enemies = currentGameState.getEnemies()
    projs = currentGameState.getProjectiles()
    player = currentGameState.getPlayerPosition()
    gameScore = currentGameState.getScore()

    enemyScore = 0
    epDiff = (PLAYER_SIZE + ENEMY_WIDTH) / 2, (PLAYER_SIZE + ENEMY_HEIGHT) / 2
    for enemy in enemies:
    	ePos = enemy.x, enemy.y
    	if ePos[1] >= player[1]:
    		continue
    	v = enemy.speed_x, enemy.speed_y
    	threshold = (SCREEN_HEIGHT - ePos[1]) / v[1]
    	if v[0] != 0:
    		thresholdX = (SCREEN_WIDTH - ePos[0]) / v[0] if v[0] > 0 else ePos[0] / -v[0]
    		threshold = min(threshold, thresholdX)    	
    	for t in range(threshold):
    		newePos = ePos[0] + v[0] * t, ePos[1] + v[1] * t
    		if abs(newePos[0] - player[0]) <= epDiff[0] and abs(newePos[1] - player[1]) <= epDiff[1]:
    			enemyScore -= 200
    			break

    projScore = 0
    ppDiff = (PLAYER_SIZE + PROJECTILE_SIZE) / 2, (PLAYER_SIZE + PROJECTILE_SIZE) / 2
    for proj in projs:
    	pPos = proj.x, proj.y
    	if pPos[1] >= player[1]:
    		continue
    	v = proj.speed_x, proj.speed_y
    	threshold = (SCREEN_HEIGHT - pPos[1]) / v[1]
    	if v[0] != 0:
    		thresholdX = (SCREEN_WIDTH - pPos[0]) / v[0] if v[0] > 0 else pPos[0] / -v[0]
    		threshold = min(threshold, thresholdX)
    	for t in range(threshold):
    		newpPos = pPos[0] + v[0] * t, pPos[1] + v[1] * t
    		if abs(newpPos[0] - player[0]) <= ppDiff[0] and abs(newpPos[1] - player[1]) <= ppDiff[1]:
    			projScore -= 200
    			break

    totalScore = [gameScore, enemyScore, projScore]
    return sum(totalScore)


def shootScoreEvaluationFunction(currentGameState):
    enemyPos = currentGameState.getEnemyPositions()
    pos = currentGameState.getPlayerPosition()
    missilePos = currentGameState.getMissilePositions()
    enemies = currentGameState.getEnemies()
    numMissile = len(missilePos)
    numEnemy = len(enemyPos)

    def checkEMCollide(pos1, pos2):
        # pos1 is enemy, pos2 is missile
        if pos1[0] <= pos2[0]:
            xCollide = pos2[0] - pos1[0] < ENEMY_WIDTH
        else:
            xCollide = pos1[0] - pos2[0] < MISSILE_WIDTH
        if pos1[1] <= pos2[1]:
            yCollide = pos2[1] - pos1[1] < ENEMY_HEIGHT
        else:
            yCollide = pos1[1] - pos2[1] < MISSILE_HEIGHT
        return xCollide and yCollide

    missileScore = -10000
    offset = (PLAYER_SIZE - MISSILE_WIDTH) / 2, (PLAYER_SIZE - MISSILE_HEIGHT) / 2
    if numMissile >= 1 or pos[1] < 0.8 * SCREEN_HEIGHT:
    	missileScore = -10000
    else:
    	# mx, my = pos[0] + offset[0] + MISSILE_WIDTH / 2, pos[1] + offset[1] + MISSILE_HEIGHT / 2
    	# for enemy in enemies:
	    # 	x, y = enemy.x + ENEMY_WIDTH / 2, enemy.y + ENEMY_HEIGHT / 2
	    # 	if y >= my:
	    # 		continue
	    #     vx, vy = enemy.speed_x, enemy.speed_y
	    #     for t in range(1, my / MISSILE_SPEED):
	    #         newEnemyPos = x + vx * t, y + vy * t
	    #         newMislePos = mx, my - MISSILE_SPEED * t
	    #         checkX = abs(newEnemyPos[0] - newMislePos[0]) < (ENEMY_WIDTH + MISSILE_WIDTH) / 2
	    #         checkY = abs(newEnemyPos[1] - newMislePos[1]) < (ENEMY_HEIGHT + MISSILE_HEIGHT) / 2
	    #         if checkX and checkY:
	    #             missileScore = 2000
	    #             break
	    rx = (ENEMY_WIDTH + MISSILE_WIDTH) / 2
	    mx, my = pos[0] + offset[0] + MISSILE_WIDTH / 2, pos[1] + offset[1] + MISSILE_HEIGHT / 2
	    for enemy in enemies:
	    	x, y = enemy.x + ENEMY_WIDTH / 2, enemy.y + ENEMY_HEIGHT / 2
	    	if abs(x - mx) < rx and y >= 0 and y < my:
	    		missileScore = 1000
	    		break

    # current game score
    gameScore = currentGameState.getScore()

    totalScore = [gameScore, missileScore]
    return sum(totalScore)


class Agent:
    def __init__(self, depth=1):
        self.index = 0
        self.depth = depth
        self.evaluationFunction = scoreEvaluationFunction
        self.shootEvaluationFunction = shootScoreEvaluationFunction
        self.ultimateEvaluationFunction = ultimateEvaluationFunction
        self.depth = int(depth)


class MinimaxAgent(Agent):
    def getAction(self, gameState):
        def recurse(state, index, depth):
            # check if it's the terminal state
            if state.isWin() or state.isLose():
                return state.getScore(), Directions.STOP
            if len(state.getLegalActions(index)) == 0 or depth == 0:
                return self.evaluationFunction(state), Directions.STOP

            nextIndex = (index + 1) % state.getNumAgents()
            nextDepth = depth - 1 if nextIndex == state.getNumAgents() - 1 else depth

            legalActions = state.getLegalActions(index)
            choices = []
            for legalAction in legalActions:
                choices.append(
                    (recurse(state.generateSuccessor(index, legalAction), nextIndex, nextDepth)[0], legalAction))
                # return max value if it's agent otherwise min if it's opponent
            chosenValue = max(choices) if index == 0 else min(choices)
            indices = [i for i in range(len(choices)) if choices[i][0] == chosenValue[0]]
            chosenIndex = random.choice(indices)  # Pick randomly among max
            action = legalActions[chosenIndex]
            return chosenValue[0], action

        value, action = recurse(gameState, self.index, self.depth)
        return action


class AlphaBetaAgent(Agent):
    def getAction(self, gameState):
        def recurse(state, index, depth, lowerBound, upperBound):
            # check if it's the terminal state
            if state.isWin() or state.isLose():
                return state.getScore(), Directions.STOP
            if len(state.getLegalActions(index)) == 0 or depth == 0:
                return self.evaluationFunction(state), Directions.STOP

            nextIndex = (index + 1) % state.getNumAgents()
            nextDepth = depth - 1 if nextIndex == (self.index - 1) % state.getNumAgents() else depth

            legalActions = state.getLegalActions(index)
            choices = []
            for legalAction in legalActions:
            	if legalAction == Directions.SHOOT:
            		value = self.shootEvaluationFunction(state)
            	else:
                	value, _ = recurse(state.generateSuccessor(index, legalAction), nextIndex, nextDepth, lowerBound, upperBound)
                choices.append((value, legalAction))
                if index == 0:
                    lowerBound = max(value, lowerBound)
                else:
                    upperBound = min(value, upperBound)
                if lowerBound > upperBound:
                    break
            # return max value if it's agent otherwise min if it's opponent
            chosenValue = max(choices) if index == 0 else min(choices)
            indices = [i for i in range(len(choices)) if choices[i][0] == chosenValue[0]]
            chosenIndex = random.choice(indices)  # Pick randomly among max
            action = legalActions[chosenIndex]
            print choices
            return chosenValue[0], action

        value, action = recurse(gameState, self.index, self.depth, -INF, INF)
        return action


class ExpectimaxAgent(Agent):
    def getAction(self, gameState):
        def recurse(state, index, depth):
            # check if it's the terminal state
            if state.isWin() or state.isLose():
                return state.getScore(), Directions.STOP
            if len(state.getLegalActions(index)) == 0 or depth == 0:
                return self.evaluationFunction(state), Directions.STOP
                # return self.ultimateEvaluationFunction(state), Directions.STOP

            nextIndex = (index + 1) % state.getNumAgents()
            nextDepth = depth - 1 if nextIndex == state.getNumAgents() - 1 else depth
            # compute the recursion
            values = []
            choices = []
            legalActions = state.getLegalActions(index)
            for legalAction in legalActions:
            	if legalAction == Directions.SHOOT:
            		value = self.shootEvaluationFunction(state)
            	else:
                	value = recurse(state.generateSuccessor(index, legalAction), nextIndex, nextDepth)[0]
                choices.append((value, legalAction))
                values.append(value)
            maxValue = max(choices)[0]
            newChoices = [choice for choice in choices if choice[0] == maxValue]
            mean = sum(values) / len(values)
            return (mean, random.choice(legalActions)) if index != 0 else (maxValue, random.choice(newChoices)[1])

        value, action = recurse(gameState, self.index, self.depth)
        return action
