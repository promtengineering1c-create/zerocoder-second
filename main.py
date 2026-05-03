import pygame
import random

FPS = 60
COLOR = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
BLACK = (0, 0, 0)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TARGET_WIDTH = 50
TARGET_HEIGHT = 50
MESSAGE_DURATION = 500  

def create_target():
    x = random.randint(0, SCREEN_WIDTH - TARGET_WIDTH)
    y = random.randint(0, SCREEN_HEIGHT - TARGET_HEIGHT)
    
    return x, y

pygame.init() #1

clock = pygame.time.Clock() #2

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE) #3
pygame.mouse.set_visible(False)

SIGHT_IMAGE = pygame.image.load('images/sight.png').convert_alpha()
SIGHT_IMAGE = pygame.transform.scale(SIGHT_IMAGE, (TARGET_WIDTH - 20, TARGET_HEIGHT - 20))
APPLE_IMAGE = pygame.image.load('images/apple.png').convert_alpha()
APPLE_IMAGE = pygame.transform.scale(APPLE_IMAGE, (TARGET_WIDTH, TARGET_HEIGHT))

pygame.display.set_caption('Игра "Тир"') #4

pygame.display.set_icon(SIGHT_IMAGE)

font = pygame.font.SysFont(None, 24) 
message = ""
message_timer = 0
last_click_pos = (0, 0)

target_x, target_y = create_target()

hits = 0
misses = 0
current_hits = 0
current_delay = 2000
MOVE_TARGET_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(MOVE_TARGET_EVENT, current_delay)


runngin = True
while runngin: #5
    clock.tick(FPS) #6

    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get(): #7
        if event.type == pygame.QUIT:
            runngin = False
        elif event.type == MOVE_TARGET_EVENT:
            target_x, target_y = create_target()    
        elif event.type == pygame.MOUSEBUTTONDOWN:
            
            message_timer = pygame.time.get_ticks()
            last_click_pos = event.pos

            if target_rect.collidepoint(event.pos):
                message = "В точку!"
                hits += 1
                current_hits += 1
                if current_hits % 3 == 0 and current_delay > 400:
                    current_delay -= 200
            else:
                message = "Упсс..."
                current_delay += 100
                current_hits = 0
            pygame.time.set_timer(MOVE_TARGET_EVENT, current_delay)
            target_x, target_y = create_target()
    
    screen.fill(COLOR) #8

    if message and pygame.time.get_ticks() - message_timer < MESSAGE_DURATION:
        msg_surface = font.render(message, True, BLACK)
        screen.blit(msg_surface, (last_click_pos[0] + 15, last_click_pos[1] + 15))

    stats_text = f"Попаданий: {hits} | Промахов: {misses} | Скорость: {current_delay}мс"
    stats_surface = font.render(stats_text, True, (0, 0, 0))
    screen.blit(stats_surface, (10, 10))

    target_rect = APPLE_IMAGE.get_rect(topleft=(target_x, target_y))
    screen.blit(APPLE_IMAGE, target_rect)

    sight_rect = SIGHT_IMAGE.get_rect(center=(mouse_x, mouse_y))
    screen.blit(SIGHT_IMAGE, sight_rect)

    pygame.display.flip() #9

pygame.quit() #9