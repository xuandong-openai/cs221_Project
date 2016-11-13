from sky_fighter import Game

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640
ENEMY_SIZE = 80

class GameState:
    def __init__(self, game):
        self.data = game
    
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
    
    def getEnemyImgSize(self):
        return ENEMY_SIZE, ENEMY_SIZE
    
    def getScore(self):
        return self.data.score
    
    def isEnd(self):
        return self.terminate
    
    def getLevel(self):
        return self.data.level
    
    def getEnemyNum(self):
        return len(self.data.enemy_list)
