import pygame
from vars import *
from copy import deepcopy


class Directions:
    UP = 'Up'
    DOWN = 'Down'
    STOP = 'Stop'
    LEFT = 'Left'
    RIGHT = 'Right'


class GameState(object):
    enemy_list = pygame.sprite.Group()
    missile_list = pygame.sprite.Group()
    projectile_list = pygame.sprite.Group()
    
    def __init__(self, game=None, previousState=None, currentAgent=0):
        if game is not None:
            self.player = game.player
            # self.deepCopy(self.enemy_list, game.enemy_list)
            # self.deepCopy(self.missile_list, game.missile_list)
            # self.deepCopy(self.projectile_list, game.projectile_list)
            # self.enemy_list = deepcopy(game.enemy_list)
            # self.missile_list = deepcopy(game.missile_list)
            # self.projectile_list = deepcopy(game.projectile_list)
            self.enemy_list = game.enemy_list.copy()
            self.missile_list = game.missile_list.copy()
            self.projectile_list = game.projectile_list.copy()
            self.score = game.score
        elif previousState is not None:
            self.player = previousState.player
            self.enemy_list = previousState.enemy_list.copy()
            self.missile_list = previousState.missile_list.copy()
            self.projectile_list = previousState.projectile_list.copy()
            # self.deepCopy(self.enemy_list, previousState.enemy_list)
            # self.deepCopy(self.missile_list, previousState.missile_list)
            # self.deepCopy(self.projectile_list, previousState.projectile_list)
            # self.enemy_list = deepcopy(previousState.enemy_list)
            # self.missile_list = deepcopy(previousState.missile_list)
            # self.projectile_list = deepcopy(previousState.projectile_list)
            self.score = previousState.score
            
        self.currentAgent = currentAgent
        # if self.currentAgent == 0:
        #     for missile in self.missile_list:
        #         missile.update()
        #     for projectile in self.projectile_list:
        #         projectile.update()
        
    def deepCopy(self, target, list):
        # target = pygame.sprite.Group()
        for item in list:
            target.add(deepcopy(item))
            
    def getProjPositions(self):
        res = []
        for projectile in self.projectile_list:
            res.append((projectile.rect.x, projectile.rect.y))
        return res
            
    def getPlayerPosition(self):
        return self.player.rect.x, self.player.rect.y
    
    def getEnemyPositions(self):
        res = []
        for enemy in self.enemy_list:
            res.append((enemy.rect.x, enemy.rect.y))
        return res
    
    def getFlight(self, agentIndex):
        if agentIndex == 0:
            return self.player
        index = 1
        for enemy in self.enemy_list:
            if agentIndex == index:
                return enemy
            else:
                index += 1
        return None
    
    def getLegalActions(self, agentIndex):
        res = [Directions.STOP]
        flight = self.getFlight(agentIndex)
        currentPosition = (flight.rect.top, flight.rect.left)
        flightHeight = flight.rect.height
        flightWidth = flight.rect.width
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
        # hitList = pygame.sprite.spritecollide(self.getPlayer(), self.getEnemies(), False, pygame.sprite.collide_mask)
        hitList = pygame.sprite.spritecollide(self.getPlayer(), self.getEnemies(), False)
        if len(hitList) > 0:
            return True
        # hitList = pygame.sprite.spritecollide(self.getPlayer(), self.getProjectiles(), False, pygame.sprite.collide_mask)
        hitList = pygame.sprite.spritecollide(self.getPlayer(), self.getProjectiles(), False)
        if len(hitList) > 0:
            return True
        return False
    
    def checkEnemyDeath(self, agentIndex):
        # hitList = pygame.sprite.spritecollide(self.getFlight(agentIndex), self.missile_list, True, pygame.sprite.collide_mask)
        hitList = pygame.sprite.spritecollide(self.getFlight(agentIndex), self.missile_list, True)
        return True if len(hitList) > 0 else False
    
    def removeEnemy(self, agentIndex):
        for enemy, index in self.enemy_list:
            if agentIndex == index + 1:
                self.enemy_list.remove(enemy)
    
    def removeMissile(self, missileIndex):
        for missile, index in self.missile_list:
            if missileIndex == index + 1:
                self.missile_list.remove(missile)
    
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
        # if self.isWin() or self.isLose():
        #     raise Exception('Can\'t generate a successor of a terminal state.')
        
        nextState = GameState(previousState=self, currentAgent=self.getNextAgentIndex())
        if agentIndex == 0:
            nextState.getPlayer().update(action)
            if nextState.isLose():
                nextState.score = -10000
        # else:
        #     nextState.getFlight(agentIndex).update(action)
        #     isDead = nextState.checkEnemyDeath(agentIndex)
        #     nextState.score += ENEMY_HIT_SCORE
        #     if isDead:
        #         nextState.removeEnemy(agentIndex)
        #         nextState.currentAgent -= 1
        return nextState
