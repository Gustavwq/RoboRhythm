import pygame
import pygame_gui
import time

import pygame_gui.ui_manager
# inicialização do pygame
pygame.init()
pygame.display.set_caption("RoboRhythm")
icon = pygame.image.load('76011.png')
original_logo = pygame.image.load('logo.jpeg')
original_keybinds = pygame.image.load('keybinds.png')
lar_tel = 800
alt_tel = 600
logo = pygame.transform.scale(original_logo,(600, 600))
keybinds = pygame.transform.scale(original_keybinds,(200,150))
pygame.display.set_icon(icon)

#gamestates
#---------------#
MAINMENU = 1
PLAYING = 2
#PAUSED = 3
#---------------#
#levels
LEVELONE = 4
LEVELTWO = 5
LEVELTHREE = 6
#---------------#
lar_snake = 40
alt_snake = 40
x_snake = lar_tel/2 - lar_snake/2
y_snake = alt_tel/2 - alt_snake/2
screen = pygame.display.set_mode((lar_tel, alt_tel))
manager = pygame_gui.UIManager((lar_tel, alt_tel))
#mainbuttons
start_game = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((x_snake+10, y_snake+70), (200, 50)),
    text='Start Game',
    manager=manager
)
# criar a tela
# loop principal do jogo
running = True

gamestate = MAINMENU
while running:
    # percorrendo os eventos

    for event in pygame.event.get():
        manager.process_events(event)
        #print("type", event)
                
        if event.type == pygame_gui.UI_BUTTON_PRESSED and gamestate == MAINMENU:
            if event.ui_element == start_game:
                print("User has started playing the game!")
                show_image = False
                gamestate = PLAYING

        if event.type == pygame.KEYDOWN and gamestate == PLAYING:
            if event.key == pygame.K_LEFT:
                print("User inputted the selected key:","KEY:",event.key, "LEFT KEY")
                x_snake = x_snake - 20
            if event.key == pygame.K_RIGHT:
                print("User inputted the selected key:","KEY:",event.key, "RIGHT KEY")
                x_snake = x_snake + 20
            if event.key == pygame.K_UP:
                print("User inputted the selected key:","KEY:",event.key, "UP KEY")
                y_snake = y_snake - 10
            if event.key == pygame.K_DOWN:
                print("User inputted the selected key:","KEY:",event.key,"DOWN KEY")
                y_snake = y_snake + 10

        # verificando se o evento é do tipo QUIT
        if event.type == pygame.QUIT:
            running = False
    screen.fill([52,36,65])
    if gamestate == PLAYING:
        plr = pygame.draw.rect(screen, (51, 204, 51), [(x_snake, y_snake), (lar_snake, alt_snake)])
        pygame.draw.rect(screen, (201, 204, 51), [(lar_tel/2 - lar_snake/2-390,alt_tel/2 - alt_snake/2+40), (lar_snake+775, alt_snake)])
    if gamestate == MAINMENU:
        screen.blit(logo, (100, -50))
        screen.blit(keybinds, (0, 450))
        manager.update(1/60)
        manager.draw_ui(screen)
    pygame.display.flip()