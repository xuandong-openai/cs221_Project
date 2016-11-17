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
    def __init__(self, game=None, previousState=None, currentAgent=0):
        self.enemy_list = pygame.sprite.Group()
        self.missile_list = pygame.sprite.Group()
        self.projectile_list = pygame.sprite.Group()
        if game is not None:
            self.player = deepcopy(game.player)
            self.score = game.score
            for item in game.enemy_list:
                tmp = deepcopy(item)
                tmp.projectile_list = self.projectile_list
                self.enemy_list.add(tmp)

            for item in game.projectile_list:
                tmp = deepcopy(item)
                self.projectile_list.add(tmp)

            for item in game.missile_list:
                tmp = deepcopy(item)
                self.missile_list.add(tmp)
        elif previousState is not None:
            self.player = deepcopy(previousState.player)
            self.score = previousState.score
            for item in previousState.enemy_list:
                tmp = deepcopy(item)
                tmp.projectile_list = self.projectile_list
                self.enemy_list.add(tmp)

            for item in previousState.projectile_list:
                tmp = deepcopy(item)
                self.projectile_list.add(tmp)

            for item in previousState.missile_list:
                tmp = deepcopy(item)
                self.missile_list.add(tmp)
            
        self.currentAgent = currentAgent
        if self.currentAgent == 0:
            for missile in self.missile_list:
                missile.update()
            for projectile in self.projectile_list:
                projectile.update()
        
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
                nextState.score = 0
        else:
            nextState.getFlight(agentIndex).update(action)
            isDead = nextState.checkEnemyDeath(agentIndex)
            nextState.score += SCORE_HIT_ENEMY
            if isDead:
                nextState.removeEnemy(agentIndex)
                nextState.currentAgent -= 1
        return nextState
