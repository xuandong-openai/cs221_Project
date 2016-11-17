#!/usr/bin/env python
from vars import *
import random, agent
from game import GameState
from fileLoader import *
from pygame.locals import *
from agent import Directions

images = None
sounds = None
state = None


class Explosion(object):
    def __init__(self):
        self.explosion_list = []
        self.images = (images["explosion01"], images["explosion02"], images["explosion03"],
                       images["explosion04"], images["explosion05"], images["explosion06"],
                       images["explosion07"], images["explosion08"], images["explosion09"],
                       images["explosion10"], images["explosion11"], images["explosion12"],
                       images["explosion13"], images["explosion14"], images["explosion15"])
    
    def add(self, pos):
        self.explosion_list.append([pos, 0])  # the second argument is for the frame number;
        sounds["explosion"].play()
    
    def draw(self, screen):
        if len(self.explosion_list) > 0:
            for item in self.explosion_list:
                screen.blit(self.images[item[1]], item[0])
                if len(self.images) > item[1] + 1:
                    item[1] += 1
                else:
                    self.explosion_list.remove(item)


class Enemy(pygame.sprite.Sprite):
    shootFreezetime = 30
    tick = shootFreezetime  # time before enemy shoots missiles
    projectile_image = None
    
    def __init__(self, img, projectile_list, tick_delay):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        # self.mask = pygame.mask.from_surface(self.image)
        self.rect.topleft = (random.randint(0, 640), -50)
        if self.rect.x < 105:
            self.speed_x = random.randint(0, 5)
        elif self.rect.x < 210:
            self.speed_x = random.randint(-1, 5)
        elif self.rect.x < 315:
            self.speed_x = random.randint(-3, 3)
        elif self.rect.x < 420:
            self.speed_x = random.randint(-5, -1)
        else:
            self.speed_x = random.randint(-5, 0)
        self.projectile_list = projectile_list
        self.speed_y = random.randint(3, 7)
        self.tick_delay = tick_delay
        self.sprayNum = 3  # number of spray projectiles
        self.sprayDiff = 4
    
    def update(self, action=None):
        if action is None:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
        else:
            if action == Directions.UP:
                if self.rect.top <= 0:
                    self.rect.top = 0
                else:
                    self.rect.top -= self.speed_y
            elif action == Directions.DOWN:
                if self.rect.top >= SCREEN_HEIGHT - self.rect.height:
                    self.rect.top = SCREEN_HEIGHT - self.rect.height
                else:
                    self.rect.top += self.speed_y
            elif action == Directions.LEFT:
                if self.rect.left <= 0:
                    self.rect.left = 0
                else:
                    self.rect.left -= self.speed_x
            elif action == Directions.RIGHT:
                if self.rect.left >= SCREEN_WIDTH - self.rect.width:
                    self.rect.left = SCREEN_WIDTH - self.rect.width
                else:
                    self.rect.left += self.speed_x
        self.updateProjectiles()
    
    # enemy can shoot multiple missiles
    def updateProjectiles(self):
        if self.tick == 0:
            projectiles = [None] * self.sprayNum
            for i in range(self.sprayNum):
                projectiles[i] = Projectile(self.rect.center, self.projectile_image)
            myx = self.speed_x
            diff = 0
            for i in range(self.sprayNum):
                if i % 2 == 0:
                    projectiles[i].speed_x = myx - diff
                else:
                    projectiles[i].speed_x = myx + diff
                self.projectile_list.add(projectiles[i])
                diff -= self.sprayDiff
            self.tick = self.tick_delay
        else:
            self.tick -= 1


class Missile(pygame.sprite.Sprite):
    def __init__(self, pos, img, speed_x=0, speed_y=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("files/missile.png").convert_alpha()
        images["missile"] = pygame.transform.scale(self.image, (MISSILE_SIZE_W, MISSILE_SIZE_H))
        # self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.speed_x = speed_x
        self.speed_y = speed_y
    
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y


class Projectile(Missile):
    def __init__(self, pos, img):
        Missile.__init__(self, pos, img)
        self.image = pygame.image.load("files/projectile.png").convert()
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (PROJECTILE_SIZE, PROJECTILE_SIZE))
        # self.mask = pygame.mask.from_surface(self.image)
        self.speed_y = 8


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("files/fighter.png").convert()
        self.image = pygame.transform.scale(self.image, (PLAYER_SIZE, PLAYER_SIZE))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.bottomright = [SCREEN_WIDTH / 2 - PLAYER_SIZE / 2, SCREEN_HEIGHT]  # born at the bottom of screen
        # self.mask = pygame.mask.from_surface(self.image)
        self.speed = PLAYER_SPEED
    
    def update(self, direction):
        # self.rect.center = pygame.mouse.get_pos()
        # using keyboard to move
        key_pressed = pygame.key.get_pressed()
        # update direction according to key_pressed
        if key_pressed is not None:
            if key_pressed[K_UP]:
                direction = Directions.UP
            elif key_pressed[K_DOWN]:
                direction = Directions.DOWN
            elif key_pressed[K_LEFT]:
                direction = Directions.LEFT
            elif key_pressed[K_RIGHT]:
                direction = Directions.RIGHT
        
        if direction == Directions.UP:
            if self.rect.top <= 0:
                self.rect.top = 0
            else:
                self.rect.top -= self.speed
        if direction == Directions.DOWN:
            if self.rect.top >= SCREEN_HEIGHT - self.rect.height:
                self.rect.top = SCREEN_HEIGHT - self.rect.height
            else:
                self.rect.top += self.speed
        if direction == Directions.LEFT:
            if self.rect.left <= 0:
                self.rect.left = 0
            else:
                self.rect.left -= self.speed
        if direction == Directions.RIGHT:
            if self.rect.left >= SCREEN_WIDTH - self.rect.width:
                self.rect.left = SCREEN_WIDTH - self.rect.width
            else:
                self.rect.left += self.speed


class Game(object):
    display_help_screen = False
    display_credits_screen = False
    texture_increment = -SCREEN_HEIGHT
    tick = GAME_FPS  # 60 fps = 1 second
    tick_delay = 35
    level = 1
    running = False
    menu_choice = 0
    score_text = None
    level_text = None
    
    def __init__(self):
        self.player = Player()
        self.player_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.missile_list = pygame.sprite.Group()
        self.projectile_list = pygame.sprite.Group()
        self.player_list.add(self.player)
        # ---------------------------------------------------------------
        self.font = pygame.font.Font("FreeSansBold.ttf", 20)  # text font...
        self.menu_font = pygame.font.Font("FreeSansBold.ttf", 28)  # Menu font...
        self.menu_text = []
        # -----------Menu Texts------------------------------------------
        txt = self.menu_font.render("START", True, (255, 0, 0))
        self.menu_text.append(txt)
        txt = self.menu_font.render("HELP", True, (255, 0, 0))
        self.menu_text.append(txt)
        txt = self.menu_font.render("CREDITS", True, (255, 0, 0))
        self.menu_text.append(txt)
        txt = self.menu_font.render("EXIT", True, (255, 0, 0))
        self.menu_text.append(txt)
        # ---------------------------------------------------------------
        self.explosion = Explosion()
        self.level1Score = 500
        self.level2Score = 1000
        self.level1EnemyFreq = 25
        self.level2EnemyFreq = 15
        self.agent = agent.MinimaxAgent()
        # self.agent = agent.AlphaBetaAgent()
    
    def scroll_menu_up(self):
        if self.menu_choice > 0:
            self.menu_choice -= 1
    
    def scroll_menu_down(self):
        if self.menu_choice + 1 < len(self.menu_text):
            self.menu_choice += 1
    
    def start_game(self):
        self.running = True
        sounds["plane"].play(-1)  # Start the plane sound;
        self.terminate_count_down = 100
        self.terminate = False
        self.score = 0
        if len(self.enemy_list) > 0:
            self.enemy_list.empty()
        if len(self.missile_list) > 0:
            self.missile_list.empty()
        if len(self.projectile_list) > 0:
            self.projectile_list.empty()
        self.tick_delay = GAME_FPS  # enemy frequency
        self.level = 1
        self.score_text = self.font.render("Score: 0", True, (255, 255, 255))
        self.level_text = self.font.render("Level: 1", True, (255, 255, 255))
    
    def run_game(self):
        if self.terminate_count_down != 0:
            state = GameState(game=self, currentAgent=0)
            direction = self.agent.getAction(state)
            self.player.update(direction)
        self.enemy_list.update()
        self.missile_list.update()
        self.projectile_list.update()
        self.score += SCORE_STAY_ONE_FRAME
        
        # clear out of bound missiles
        for missile in self.missile_list:
            if missile.rect.x < 0 or missile.rect.x > SCREEN_WIDTH:
                self.missile_list.remove(missile)
            elif missile.rect.y < - MISSILE_SIZE or missile.rect.y > SCREEN_HEIGHT:
                self.missile_list.remove(missile)
        
        # clear out of bound projectiles
        for projectile in self.projectile_list:
            if projectile.rect.x < 0 or projectile.rect.x > SCREEN_WIDTH:
                self.projectile_list.remove(projectile)
            elif projectile.rect.y < - PROJECTILE_SIZE or projectile.rect.y > SCREEN_HEIGHT:
                self.projectile_list.remove(projectile)
        
        # clear out of bound enemies
        for enemy in self.enemy_list:
            if enemy.rect.x < -ENEMY_SIZE or enemy.rect.x > SCREEN_WIDTH:
                self.enemy_list.remove(enemy)
            elif enemy.rect.y < -ENEMY_SIZE or enemy.rect.y > SCREEN_HEIGHT:
                self.enemy_list.remove(enemy)
        
        # clear hit enemies
        for enemy in self.enemy_list:
            hit_list = pygame.sprite.spritecollide(enemy, self.missile_list, True)
            if len(hit_list) > 0:
                self.explosion.add((enemy.rect.x + 20, enemy.rect.y + 20))
                self.enemy_list.remove(enemy)
                self.score += SCORE_HIT_ENEMY
                if self.level == 1:
                    if self.score == self.level1Score:
                        self.level += 1
                        self.tick_delay = self.level1EnemyFreq
                        self.level_text = self.font.render("Level: " + str(self.level), True, (255, 255, 255))
                elif self.level == 2:
                    if self.score == self.level2Score:
                        self.level += 1
                        self.tick_delay = self.level2EnemyFreq
                        self.level_text = self.font.render("Level: " + str(self.level), True, (255, 255, 255))
        
        # hit_list = pygame.sprite.spritecollide(self.player, self.enemy_list, False, pygame.sprite.collide_mask)
        hit_list = pygame.sprite.spritecollide(self.player, self.enemy_list, False)
        if len(hit_list) > 0 and not self.terminate:
            self.terminate = True
            self.explosion.add(self.player.rect.topleft)
            sounds["plane"].stop()
            for enemy in hit_list:
                self.explosion.add(enemy.rect.topleft)
                self.enemy_list.remove(enemy)
        
        # hit_list = pygame.sprite.spritecollide(self.player, self.projectile_list, False, pygame.sprite.collide_mask)
        hit_list = pygame.sprite.spritecollide(self.player, self.projectile_list, False)
        if len(hit_list) > 0 and not self.terminate:
            self.terminate = True
            self.explosion.add(self.player.rect.topleft)
            sounds["plane"].stop()
            for projectile in hit_list:
                self.projectile_list.remove(projectile)
        
        if self.tick == 0:
            enemy = Enemy(random.choice((images["enemy1"], images["enemy2"], images["enemy3"])), self.projectile_list,
                          self.tick_delay)
            enemy.projectile_image = images["projectile"]
            if len(self.enemy_list) <= 1:
                self.enemy_list.add(enemy)
            self.tick = self.tick_delay
        else:
            self.tick -= 1
        
        if self.texture_increment == 0:
            self.texture_increment = -SCREEN_HEIGHT
        else:
            self.texture_increment += 1
        
        if self.terminate:
            self.score = -10000
            if self.terminate_count_down == 0:
                self.running = False
            else:
                self.terminate_count_down -= 1
        self.score_text = self.font.render("Score: " + str(self.score), True, (255, 255, 255))
    
    def display_frame(self, screen):
        if self.running:
            # screen.blit(images["ocean"],(0,self.texture_increment))
            screen.blit(images["background"], (0, 0))
            
            self.missile_list.draw(screen)
            self.projectile_list.draw(screen)
            self.enemy_list.draw(screen)
            if not self.terminate:
                self.player_list.draw(screen)
            screen.blit(self.score_text, (75, 20))
            screen.blit(self.level_text, (285, 20))
            self.explosion.draw(screen)
            if self.terminate_count_down <= 90:
                # screen.blit(images["gameOver"],(100,145))
                screen.blit(images["gameover"], (0, 0))
        elif self.display_credits_screen:
            screen.blit(images["introImage"], (0, 0))
            screen.blit(images["creditsImage"], (80, 100))
        elif self.display_help_screen:
            screen.blit(images["introImage"], (0, 0))
            screen.blit(images["helpImage"], (70, 50))
        else:
            screen.blit(images["introImage"], (0, 0))
            increment = 100
            for text in self.menu_text:
                screen.blit(text, (135, increment))
                increment += 50
            pygame.draw.rect(screen, (0, 0, 255), [125, 90 + self.menu_choice * 50, 160, 45], 3)
    
    def shoot(self):
        missile = Missile(self.player.rect.center, images["missile"], speed_y=-MISSILE_SPEED)
        self.missile_list.add(missile)


def main():
    pygame.init()
    
    # Set the width and height of the screen [width, height]
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Sky Fighter")
    
    # -------------make the mouse cursor invisible-------------------
    pygame.mouse.set_visible(False)
    
    # -----------------------------------------
    done = False
    # Loop until the user clicks the close button.
    global images
    global sounds
    try:
        images = loadImages()
        sounds = loadSounds()
        # -----------------------------------------------
        game = Game()  # Create the game object
    except pygame.error:
        print pygame.get_error()
        done = True
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    # -------- Main Program Loop ---------------------------------------
    while not done:
        # --- Main event loop
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop
            
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     game.shoot()                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # using spacebar to shoot
                    game.shoot()
                
                elif event.key == pygame.K_RETURN:
                    if not game.running:
                        # ------The user's menu selection----------------
                        if game.menu_choice == 0:
                            game.start_game()
                        elif game.menu_choice == 1:
                            game.display_help_screen = True
                        elif game.menu_choice == 2:
                            game.display_credits_screen = True
                        elif game.menu_choice == 3:
                            done = True
                
                elif event.key == pygame.K_UP:
                    game.scroll_menu_up()
                elif event.key == pygame.K_DOWN:
                    game.scroll_menu_down()
                
                elif event.key == pygame.K_ESCAPE:
                    if game.running:
                        game.running = False
                        sounds["plane"].stop()
                    else:
                        game.display_help_screen = False
                        game.display_credits_screen = False
        
        # --- Game logic should go here
        if game.running:
            game.run_game()
        # First, clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.
        screen.fill((255, 255, 255))
        
        # --- Drawing code should go here
        game.display_frame(screen)
        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
        
        # --- Limit to 30 frames per second
        clock.tick(GAME_FPS)
    
    # Close the window and quit.
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    pygame.quit()


if __name__ == '__main__':
    main()
