import pygame

class Button:
    def __init__(self, x, y, w, h, image, font, text):
        self.x = x
        self.screen = pygame.display.get_surface()
        self.y = y
        self.w = w
        self.h = h
        self.image = pygame.transform.scale(image, (w, h))
        self.font = font.render(text, 1, (247,151,41))
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self):
        self.screen.blit(self.image, self.rect)
        x,y = self.x - self.font.get_width()/2 + self.w/2, self.y
        self.screen.blit(self.font, (x,y+35))

    def click(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True
        return False