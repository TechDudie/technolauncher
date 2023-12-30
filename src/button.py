import pygame

class Button:
    def __init__(self, screen: pygame.Surface, text, location, size, color="#3366ee", radius=8):
        self.screen = screen

        self.text = text
        self.color = color
        self.font = pygame.font.Font("assets/minecraft.otf", 24)
        self.render = self.font.render(self.text, True, "#ffffff")
        self.render_size = (self.render.get_width(), self.render.get_height())

        self.location = location
        self.size = size
        self.radius = radius

        self.rectangle = pygame.Rect(location[0] - size[0] // 2, location[1] - size[1] // 2, size[0], size[1])
        self.text_area = pygame.Rect(location[0] - self.render_size[0] // 2, location[1] - self.render_size[1] // 2, self.render_size[0], self.render_size[1])
        self.area = ((location[0] - size[0] // 2, location[1] - size[1] // 2), (location[0] + size[0] // 2, location[1] + size[1] // 2))
    
    def draw(self):
        self.rectangle_render = pygame.draw.rect(self.screen, self.color, self.rectangle, 0, self.radius)
        self.screen.blit(self.render, self.text_area)