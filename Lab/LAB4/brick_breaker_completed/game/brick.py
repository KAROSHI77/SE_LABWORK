import pygame

class Brick:
    def __init__(self, x, y, width, height, row):
        self.rect = pygame.Rect(x, y, width, height)
        self.row = row
        self.alive = True

    def draw(self, screen):
        if not self.alive:
            return
        colors = [
            (240, 90, 90),
            (245, 155, 70),
            (240, 210, 70),
            (100, 200, 120),
            (90, 160, 240),
            (170, 110, 220),
        ]
        color = colors[self.row % len(colors)]
        pygame.draw.rect(screen, color, self.rect, border_radius=4)
        pygame.draw.rect(screen, (35, 35, 45), self.rect, 1, border_radius=4)
