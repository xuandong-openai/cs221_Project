#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from collections import Counter

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640
ENEMY_SIZE = 80
MISSILE_SIZE_H = 40
MISSILE_SIZE_W = 20
PROJECTILE_SIZE = 20


def loadImages():
    images = Counter()
    
    images["explosion01"] = pygame.image.load("files/explosion01.png").convert_alpha()
    images["explosion02"] = pygame.image.load("files/explosion02.png").convert_alpha()
    images["explosion03"] = pygame.image.load("files/explosion03.png").convert_alpha()
    images["explosion04"] = pygame.image.load("files/explosion04.png").convert_alpha()
    images["explosion05"] = pygame.image.load("files/explosion05.png").convert_alpha()
    images["explosion06"] = pygame.image.load("files/explosion06.png").convert_alpha()
    images["explosion07"] = pygame.image.load("files/explosion07.png").convert_alpha()
    images["explosion08"] = pygame.image.load("files/explosion08.png").convert_alpha()
    images["explosion09"] = pygame.image.load("files/explosion09.png").convert_alpha()
    images["explosion10"] = pygame.image.load("files/explosion10.png").convert_alpha()
    images["explosion11"] = pygame.image.load("files/explosion11.png").convert_alpha()
    images["explosion12"] = pygame.image.load("files/explosion12.png").convert_alpha()
    images["explosion13"] = pygame.image.load("files/explosion13.png").convert_alpha()
    images["explosion14"] = pygame.image.load("files/explosion14.png").convert_alpha()
    images["explosion15"] = pygame.image.load("files/explosion15.png").convert_alpha()
    images["enemy1"] = pygame.image.load("files/enemy_1.png").convert_alpha()
    images["enemy1"] = pygame.transform.scale(images["enemy1"], (ENEMY_SIZE, ENEMY_SIZE))
    images["enemy2"] = pygame.image.load("files/enemy_2.png").convert_alpha()
    images["enemy2"] = pygame.transform.scale(images["enemy2"], (ENEMY_SIZE, ENEMY_SIZE))
    images["enemy3"] = pygame.image.load("files/enemy_3.png").convert_alpha()
    images["enemy3"] = pygame.transform.scale(images["enemy3"], (ENEMY_SIZE, ENEMY_SIZE))
    #images["ocean"] = pygame.image.load("files/ocean_texture.png").convert()
    images["background"] = pygame.image.load("files/background.png").convert()
    images["background"] = pygame.transform.scale(images["background"], (SCREEN_WIDTH, SCREEN_HEIGHT))
    images["missile"] = pygame.image.load("files/missile.png").convert_alpha()
    images["missile"] = pygame.transform.scale(images["missile"], (MISSILE_SIZE_W, MISSILE_SIZE_H))
    images["projectile"] = pygame.image.load("files/projectile.png").convert()
    images["projectile"].set_colorkey((0,0,0))
    images["projectile"] = pygame.transform.scale(images["projectile"], (PROJECTILE_SIZE, PROJECTILE_SIZE))
    #images["gameOver"] = pygame.image.load("files/game_over.png").convert()
    images["gameover"] = pygame.image.load("files/gameover.png").convert()
    images["gameover"] = pygame.transform.scale(images["gameover"], (SCREEN_WIDTH, SCREEN_HEIGHT))
    #images["gameOver"].set_colorkey((0,0,0))
    images["helpImage"] = pygame.image.load("files/help_image.png").convert_alpha()
    images["creditsImage"] = pygame.image.load("files/credits_image.png").convert_alpha()
    #images["introImage"] = pygame.image.load("files/intro_image.png").convert_alpha()

    images["introImage"] = pygame.image.load("files/umbrella.png").convert_alpha()
    images["introImage"] = pygame.transform.scale(images["introImage"], (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    return images


def loadSounds():
    sounds = Counter()
    sounds["explosion"] = pygame.mixer.Sound("files/explosion.ogg")
    sounds["plane"] = pygame.mixer.Sound("files/plane.ogg")
    return sounds
