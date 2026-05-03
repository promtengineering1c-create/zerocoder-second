import pygame
import random

def create_target():
    x = random.randint(0, SCREEN_WIDTH - TARGET_WIDTH)
    y = random.randint(0, SCREEN_HEIGHT - TARGET_HEIGHT)
    
    return x, y

pygame.init() #1

FPS = 60
clock = pygame.time.Clock() #2

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE) #3
pygame.display.set_caption('Игра "Тир"') #4

SIGHT_IMAGE = pygame.image.load('images/sight.png')
pygame.display.set_icon(SIGHT_IMAGE)

font = pygame.font.SysFont(None, 24) 
COLOR = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

APPLE_IMAGE = pygame.image.load('images/apple.png').convert_alpha()
TARGET_WIDTH = 50
TARGET_HEIGHT = 50

targer_x, targer_y = create_target()


runngin = True
while runngin:
    pass

pygame.quit()