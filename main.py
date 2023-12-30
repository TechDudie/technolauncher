import pygame

from src.color import AnimatedTheme

from src.scenes.main_menu import get_scene as main_menu_scene
from src.scenes.multiplayer import get_scene as multiplayer_scene

SIZE = (1280, 720)

pygame.init()
pygame.display.set_caption("TechnoClient")
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
delta = 0
position = (0, 0)
clicked = False

pygame.mixer.init()
pygame.mixer.music.load("assets/click.ogg")
pygame.mixer.music.set_volume(0.05)

main_menu = main_menu_scene(screen)
multiplayer = multiplayer_scene(screen)

color = AnimatedTheme()

while True:
    delta = clock.tick(60) / 1000
    color.update(delta)

    screen.fill("#000000")

    main_menu.draw()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()
            clicked = True
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    if main_menu.visible:
        for button in main_menu.buttons.values():
            button.color = color.color()
            area = button.area
            if area[0][0] < position[0] and position[0] < area[1][0] and area[0][1] < position[1] and position[1] < area[1][1] and clicked:
                pygame.mixer.music.play()
                main_menu.callbacks[button.text]()
    
    clicked = False
    
    pygame.display.update()
