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
    def __init__(self, rect, isPlayer=False):
        self.x = rect.x
        self.y = rect.y
        self.width = rect.width
        self.height = rect.height
        self.rect = rect
        self.speed_x = 0
        self.speed_y = 0
        self.isPlayer = isPlayer
        self.getSpeed()
        
    def getSpeed(self):
        if self.x < 105:
            self.speed_x = random.randint(0, 5)
        elif self.x < 210:
            self.speed_x = random.randint(-1, 5)
        elif self.x < 315:
            self.speed_x = random.randint(-3, 3)
        elif self.x < 420:
            self.speed_x = random.randint(-5, -1)
        else:
            self.speed_x = random.randint(-5, 0)
        
        if self.isPlayer:
            self.speed_x = PLAYER_SPEED
            self.speed_y = PLAYER_SPEED
    
    def getDistance(self, item2):
        dis = sqrt((self.x - item2.x) ** 2 + (self.y - item2.y) ** 2)
        return dis
    
    def checkCollide(self, item2):
        dist = self.getDistance(item2)
        return self.getDistance(item2) < 20
    
    def updateProjectile(self):
        self.x += self.speed_x
        self.y += self.speed_y
        
    def updateFlight(self, action):
        if action is None:
            self.x += self.speed_x
            self.y += self.speed_y
        else:
            if action == Directions.UP:
                if self.y <= 0:
                    self.y = 0
                else:
                    self.y -= self.speed_y
            elif action == Directions.DOWN:
                if self.y >= SCREEN_HEIGHT - self.height:
                    self.y = SCREEN_HEIGHT - self.height
                else:
                    self.y += self.speed_y
            elif action == Directions.LEFT:
                if self.x <= 0:
                    self.x = 0
                else:
                    self.x -= self.speed_x
            elif action == Directions.RIGHT:
                if self.x >= SCREEN_WIDTH - self.width:
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
            self.enemy_list.append(Item(enemy.rect))
        for proj in state.projectile_list:
            self.projectile_list.append(Item(proj.rect))
        for missile in state.missile_list:
            self.missile_list.append(Item(missile.rect))
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
        return self.enemy_list[agentIndex-1]
    
    def getLegalActions(self, agentIndex):
        res = [Directions.STOP]
        flight = self.getFlight(agentIndex)
        currentPosition = (flight.x, flight.y)
        flightHeight = flight.height
        flightWidth = flight.width
        if currentPosition[0] > 0:
            res.append(Directions.UP)
        if currentPosition[0] < SCREEN_HEIGHT - flightHeight:
            res.append(Directions.DOWN)
        if currentPosition[1] > 0:
            res.append(Directions.LEFT)
        if currentPosition[1] < SCREEN_WIDTH - flightWidth:
            res.append(Directions.RIGHT)
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
    
    def checkEnemyDeath(self, agentIndex):
        enemy = self.getFlight(agentIndex)
        for missile in self.missile_list:
            return enemy.checkCollide(missile)

    
    def removeEnemy(self, agentIndex):
        self.enemy_list.pop(agentIndex-1)
    
    def removeMissile(self, missileIndex):
        self.missile_list.pop(missileIndex)
    
    def getNextAgentIndex(self):
        return (self.currentAgent + 1) % self.getNumAgents()
    
    def getLevel(self):
        if self.getScore() >= 100:
            return 3
        elif self.getScore() >= 50:
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
        nextState = GameState(previousState=self, currentAgent=self.getNextAgentIndex())
        if agentIndex == 0:
            player = nextState.getPlayer()
            
            for projectile in self.projectile_list:
                projectile.updateProjectile()
            
            player.updateFlight(action)
            if nextState.isLose():
                nextState.score = 0
        else:
            enemy = nextState.getFlight(agentIndex)
            enemy.updateFlight(action)
            # isDead = nextState.checkEnemyDeath(agentIndex)
            nextState.score += ENEMY_HIT_SCORE
            # if isDead:
            #     nextState.removeEnemy(agentIndex)
            #     nextState.currentAgent -= 1
        return nextState
