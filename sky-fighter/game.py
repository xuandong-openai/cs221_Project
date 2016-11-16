import pygame
from sky_fighter import Game

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640
ENEMY_SIZE = 80


class Directions:
	UP = 'Up'
	DOWN = 'Down'
	LEFT = 'Left'
	RIGHT = 'Right'
	STOP = 'Stop'


class GameState:
	def __init__(self, game):
		self.data = game
		self.getPositions(self)

	def getPositions(self):
		i = 1
		res = {}
		res[0] = (self.data.player.rect.x, self.data.player.rect.y)
		for enemy in self.data.enemy_list:
			pos = (enemy.rect.x, enemy.rect.y)
			res[i] = pos
			i += 1
		for projectile in self.data.projectile_list:
			pos = (projectile.rect.x, projectile.rect.y)
			res[i] = pos
			i += 1
		self.positions = res
		return res

	def getLegalActions(self):
		if self.isWin or self.isLose:
			return []
		currPosition = (self.player.rect.x, self.player.rect.y)
		actions = []
		pass

	def getPlayerPosition(self):
		return self.player.rect.x, self.player.rect.y

	def getPlayer(self):
		return self.data.player

	def getLethal(self):
		return self.data.enemy_list, self.data.projectile_list

	def getEnemyPositions(self):
		res = []
		for enemy in self.data.enemy_list:
			res.append((enemy.rect.x, enemy.rect.y))
		return res

	def getProjPositions(self):
		res = []
		for projectile in self.data.projectile_list:
			res.append((projectile.rect.x, projectile.rect.y))
		return res

	def getMisslPositions(self):
		res = []
		for missile in self.data.missile_list:
			res.append((missile.rect.x, missile.rect.y))
		return res

	def isWin(self):
		return False

	def isLose(self):
		hitList = pygame.sprite.spritecollide(self.getPlayer(), self.getLethal()[0], \
			False, pygame.sprite.collide_mask)
		if len(hitList) > 0:
			return True
		hitList = pygame.sprite.spritecollide(self.getPlayer(), self.getLethal()[1], \
			False, pygame.sprite.collide_mask)
		if len(hitList) > 0:
			return True
		return False

	def getEnemyImgSize(self):
		return ENEMY_SIZE, ENEMY_SIZE

	def isEnd(self):
		return self.terminate

	def getLevel(self):
		if self.getScore() >= 100:
			return 3
		elif self.getScore() >= 50:
			return 2
		else:
			return 1

	def getEnemyNum(self):
		return len(self.data.enemy_list)

	def getNumAgents(self):
		return self.data.enemy_list + 1

	def generateSuccessor(self, index, action):
		nextState = GameState(self)
		game = nextState.data

		for projectile in game.projectile_list:
			projectile.update()

		if index == 0:
			game.player.update(action)
		else:
			movedEnemy = game.enemy_list[index]
			movedEnemy.update(action)

		return GameState(game)