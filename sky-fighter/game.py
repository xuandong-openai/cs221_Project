import pygame
from vars import *
import random
from math import sqrt


class Directions:
    UP = 'Up'
    DOWN = 'Down'
    STOP = 'Stop'
    LEFT = 'Left'
    RIGHT = 'Right'


class Item(object):
    def __init__(self, rect, speed_x=0, speed_y=0, isPlayer=False):
        self.x = rect.x
        self.y = rect.y
        self.width = rect.width
        self.height = rect.height
        self.rect = rect
        self.isPlayer = isPlayer
        if self.isPlayer:
            self.speed_x = PLAYER_SPEED
            self.speed_y = PLAYER_SPEED
        else:
            self.speed_x = speed_x
            self.speed_y = speed_y
    
    def getDistance(self, item2):
        dis = sqrt((self.x - item2.x) ** 2 + (self.y - item2.y) ** 2)
        return dis
    
    def checkXCollide(self, item2):
        if self.x < item2.x:
            return item2.x - self.x < self.width
        else:
            return self.x - item2.x < item2.width
        
    def checkYCollide(self, item2):
        if self.y < item2.y:
            return item2.y - self.y < self.height
        else:
            return self.y - item2.y < item2.height
    
    def checkCollide(self, item2):
        return self.checkXCollide(item2) and self.checkYCollide(item2)
    
    def updateProjectile(self):
        self.x += self.speed_x
        self.y += self.speed_y
    
    def updateFlight(self, action):
        if action is None:
            self.x += self.speed_x
            self.y += self.speed_y
        else:
            if action == Directions.UP:
                if self.y <= self.speed_y:
                    self.y = 0
                else:
                    self.y -= self.speed_y
            elif action == Directions.DOWN:
                if self.y >= SCREEN_HEIGHT - self.height - self.speed_y:
                    self.y = SCREEN_HEIGHT - self.height
                else:
                    self.y += self.speed_y
            elif action == Directions.LEFT:
                if self.x <= self.speed_x:
                    self.x = 0
                else:
                    self.x -= self.speed_x
            elif action == Directions.RIGHT:
                if self.x >= SCREEN_WIDTH - self.width - self.speed_x:
                    self.x = SCREEN_WIDTH - self.width
                else:
                    self.x += self.speed_x


class GameState(object):
    def __init__(self, game=None, previousState=None, currentAgent=0):
        self.enemy_list = []
        self.missile_list = []
        self.projectile_list = []
        state = None
        if game is not None:
            state = game
        elif previousState is not None:
            state = previousState
        
        self.player = Item(state.player.rect, isPlayer=True)
        for enemy in state.enemy_list:
            self.enemy_list.append(Item(enemy.rect, speed_x=enemy.speed_x, speed_y=enemy.speed_y))
        for projectile in state.projectile_list:
            self.projectile_list.append(Item(projectile.rect, speed_x=projectile.speed_x, speed_y=projectile.speed_y))
        for missile in state.missile_list:
            self.missile_list.append(Item(missile.rect, speed_x=missile.speed_x, speed_y=missile.speed_y))
        self.score = state.score
        self.currentAgent = currentAgent
    
    def getProjPositions(self):
        res = []
        for projectile in self.projectile_list:
            res.append((projectile.x, projectile.y))
        return res
    
    def getPlayerPosition(self):
        return self.player.x, self.player.y
    
    def getEnemyPositions(self):
        res = []
        for enemy in self.enemy_list:
            res.append((enemy.x, enemy.y))
        return res
    
    def getFlight(self, agentIndex):
        if agentIndex == 0:
            return self.player
        return self.enemy_list[agentIndex - 1]
    
    def getLegalActions(self, agentIndex):
        res = [Directions.STOP]
        flight = self.getFlight(agentIndex)
        currentPosition = (flight.x, flight.y)
        flightHeight = flight.height
        flightWidth = flight.width
        if currentPosition[0] > 0:
            res.append(Directions.LEFT)
        if currentPosition[0] < SCREEN_WIDTH - flightWidth:
            res.append(Directions.RIGHT)
        if currentPosition[1] > 0:
            res.append(Directions.UP)
        if currentPosition[1] < SCREEN_HEIGHT - flightHeight:
            res.append(Directions.DOWN)
        return res
    
    def getScore(self):
        return self.score
    
    def getPlayer(self):
        return self.player
    
    def getEnemies(self):
        return self.enemy_list
    
    def getProjectiles(self):
        return self.projectile_list
    
    def isWin(self):
        return False
    
    def isLose(self):
        for enemy in self.enemy_list:
            if enemy.checkCollide(self.player):
                return True
        for projectile in self.projectile_list:
            if projectile.checkCollide(self.player):
                return True
        return False
    
    def getMissileHitList(self, agentIndex):
        enemy = self.getFlight(agentIndex)
        hitList = []
        for missile, index in self.missile_list:
            if enemy.checkCollide(missile):
                hitList.append(index)
        return hitList
    
    def removeEnemy(self, agentIndex):
        self.enemy_list.pop(agentIndex - 1)
    
    def removeMissile(self, missileIndex):
        self.missile_list.pop(missileIndex)
    
    def getNextAgentIndex(self):
        return (self.currentAgent + 1) % self.getNumAgents()
    
    def getLevel(self):
        if self.getScore() >= SCORE_LEVEL_THREE:
            return 3
        elif self.getScore() >= SCORE_LEVEL_TWO:
            return 2
        else:
            return 1
    
    def getNumAgents(self):
        return len(self.enemy_list) + 1
    
    def getNumMissisle(self):
        return len(self.missile_list)
    
    def getNumProjectile(self):
        return len(self.projectile_list)
    
    def generateSuccessor(self, agentIndex, action):
        nextAgentIndex = self.getNextAgentIndex()
        nextState = GameState(previousState=self, currentAgent=nextAgentIndex)
        if agentIndex == 0:
            player = nextState.getPlayer()
            for projectile in self.projectile_list:
                projectile.updateProjectile()
            player.updateFlight(action)
            if nextState.isLose():
                nextState.score = SCORE_LOSE
        else:
            enemy = nextState.getFlight(agentIndex)
            enemy.updateFlight(action)
            hitList = nextState.getMissileHitList(agentIndex)
            if len(hitList) > 0:
                nextState.score += SCORE_HIT_ENEMY
                nextState.removeEnemy(nextAgentIndex)
                nextState.currentAgent = nextAgentIndex % nextState.getNumAgents()
        return nextState
