import pygame

pygame.init()
font = pygame.font.Font('freesansbold.ttf', 24)


class Position:
    def __init__(self, x=0, y=0, text=""):
        self.x = x
        self.y = y
        self.text = text

    def point(self):
        return (self.x, self.y)

    def display(self, screen, color):
        text = font.render(self.text, True, color)
        text_rect = text.get_rect()
        if self.y > 540:
            text_rect.center = (self.x, self.y + 30)
        else:
            text_rect.center = (self.x, self.y - 35)
        screen.blit(text, text_rect)
        pygame.draw.circle(screen, color, (self.x, self.y), 10)
