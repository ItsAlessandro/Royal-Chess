import pygame

class Textbox:
    def __init__(self, x, y, w, h, font, placeholder):
        self.x = x
        self.screen = pygame.display.get_surface()
        self.y = y
        self.w = w
        self.h = h
        self.font = font
        self.rect = pygame.Rect(x, y, w, h)
        self.text = placeholder
        self.placeholder = placeholder
        self.active = False
    
    def draw(self):
        pygame.draw.rect(self.screen, (103, 58,183), self.rect)
        if self.active:
            pygame.draw.rect(self.screen, (247,151,41), self.rect, 5)
        else:
            pygame.draw.rect(self.screen, (0,0,0), self.rect, 5)

        text_surface = self.font.render(self.text, 1, (239,201,119))
        self.screen.blit(text_surface, (self.x +5, self.y +10))
    
    def click(self):
        self.active = self.rect.collidepoint(pygame.mouse.get_pos())
        if self.text == self.placeholder or self.text.endswith('error'): self.text = ''

    def write(self, event):
        if self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif len(self.text) < 20:
                self.text += event.unicode