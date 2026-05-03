import pygame
import random

FPS = 60
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

TARGET_WIDTH = 50
TARGET_HEIGHT = 50
MESSAGE_DURATION = 500  

def get_safe_color():
    
    for _ in range(100):
        c = (random.randint(60, 220), random.randint(60, 220), random.randint(60, 220))
    
        if not (c[0] > 180 and c[1] < 100) and not (c[2] > 180 and c[1] < 100):
            return c
    
    return (120, 120, 120)

def get_random_pos(surface):
    w, h = surface.get_size()

    limit_x = max(1, w - TARGET_WIDTH)
    limit_y = max(1, h - TARGET_HEIGHT)

    return (random.randint(0, limit_x), random.randint(0, limit_y))

pygame.init() #1
clock = pygame.time.Clock() #2
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE) #3
pygame.display.set_caption('Игра "Тир"') #4
pygame.mouse.set_visible(False)

try:
    SIGHT_IMAGE = pygame.image.load('images/sight.png').convert_alpha()
    SIGHT_IMAGE = pygame.transform.scale(SIGHT_IMAGE, (30, 30))
    APPLE_IMAGE = pygame.image.load('images/apple.png').convert_alpha()
    APPLE_IMAGE = pygame.transform.scale(APPLE_IMAGE, (TARGET_WIDTH, TARGET_HEIGHT))
    pygame.display.set_icon(SIGHT_IMAGE)
except:
    SIGHT_IMAGE = pygame.Surface((30, 30), pygame.SRCALPHA)
    pygame.draw.circle(SIGHT_IMAGE, (0, 255, 0), (15, 15), 15, 2)
    APPLE_IMAGE = pygame.Surface((50, 50))
    APPLE_IMAGE.fill((200, 0, 0))

COLOR = get_safe_color()
flash_color = COLOR

font = pygame.font.SysFont(None, 24) 
message = ""
message_timer = 0
last_click_pos = (0, 0)

target_rect = APPLE_IMAGE.get_rect(topleft=get_random_pos(screen))

hits = 0
misses = 0
current_hits = 0
current_delay = 2000
MOVE_TARGET_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(MOVE_TARGET_EVENT, current_delay)

running = True
while running: #5
    clock.tick(FPS) #6

    mouse_x, mouse_y = pygame.mouse.get_pos()
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get(): #7
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            target_rect.topleft = get_random_pos(screen)    
        elif event.type == MOVE_TARGET_EVENT:
            target_rect.topleft = get_random_pos(screen)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            
            if message and (current_time - message_timer < MESSAGE_DURATION):
                continue

            message_timer = pygame.time.get_ticks()
            last_click_pos = event.pos

            if target_rect.collidepoint(event.pos):

                flash_color = RED
                message = "В точку!"
                hits += 1
                current_hits += 1
                if current_hits % 3 == 0 and current_delay > 400:
                    current_delay -= 200
            else:
                flash_color = BLUE
                message = "Упсс..."
                current_delay += 100
                current_hits = 0
                misses += 1

            target_rect.topleft = get_random_pos(screen)

            pygame.time.set_timer(MOVE_TARGET_EVENT, current_delay + MESSAGE_DURATION)
    
    screen.fill(COLOR) #8
    
    is_flashing = message and (current_time - message_timer < MESSAGE_DURATION)

    if is_flashing:
        pygame.draw.circle(screen, flash_color, last_click_pos, 45)
        msg_surface = font.render(message, True, BLACK)
        text_x = last_click_pos[0] - msg_surface.get_width() // 2
        text_y = last_click_pos[1] - msg_surface.get_height() // 2
        screen.blit(msg_surface, (text_x, text_y))
    else:
        screen.blit(APPLE_IMAGE, target_rect)
        if message != "":
            message = ""

    stats_text = f"Попаданий: {hits} | Промахов: {misses} | Скорость: {current_delay}мс"
    stats_surface = font.render(stats_text, True, BLACK)
    screen.blit(stats_surface, (10, 10))

    sight_rect = SIGHT_IMAGE.get_rect(center=(mouse_x, mouse_y))
    screen.blit(SIGHT_IMAGE, sight_rect)

    pygame.display.flip() #9

pygame.quit() #9