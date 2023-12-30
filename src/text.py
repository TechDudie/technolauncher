import pygame

class Text:
    def __init__(self, screen: pygame.Surface, text, location, color="#ffffff", font="assets/minecraft.otf", size=24):
        self.screen = screen

        self.text = text
        self.color = color
        self.font = pygame.font.Font(font, size)
        self.render = self.font.render(self.text, True, "#ffffff")

        self.location = location

        self.rectangle = self.render.get_rect()
        self.rectangle.center = location
    
    def draw(self):
        self.screen.blit(self.render, self.rectangle)