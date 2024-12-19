import pygame

class Button:
    def __init__(self, x, y, width, height, text="Button", text_size=36, text_font=None, sprite_path=None, text_color=[0, 0, 0],  color=[200, 200, 200], highlighted_color=[110, 110, 110], duration=1.0):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.default_color = color  
        self.h_color = highlighted_color 
        self.text_color = text_color
        self.color = color 
        self.is_animating = False 
        self.animation_start_time = 0  
        self.duration = duration  
        self.text_size = text_size
        self.text_font = text_font
        self.sprite = None
        if sprite_path:
            self.sprite = pygame.image.load(sprite_path).convert_alpha()
            self.sprite = pygame.transform.scale(self.sprite, (width, height))
        self.sprite_mask = True

    def draw(self, screen):
        if self.sprite:
            if self.sprite_mask:
                colored_sprite = self.apply_color_mask(self.sprite, self.color)
                screen.blit(colored_sprite, self.rect.topleft)
            else:
                screen.blit(self.sprite, self.rect.topleft)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        text_surf = pygame.font.Font(self.text_font, self.text_size).render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.is_animating = True
                self.animation_start_time = pygame.time.get_ticks()
                return True
        return False

    def update(self):
        if self.is_animating:
            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - self.animation_start_time) / 1000 
            t = elapsed_time / (self.duration / 2)

            if t <= 1.0:
                self.color = self.lerp_color(self.default_color, self.h_color, t)
            elif t <= 2.0:
                self.color = self.lerp_color(self.h_color, self.default_color, t - 1.0)
            else:
                self.color = self.default_color
                self.is_animating = False

    @staticmethod
    def lerp_color(start, end, t):
        """Линейная интерполяция между двумя цветами"""
        return (
            int(start[0] + (end[0] - start[0]) * t),
            int(start[1] + (end[1] - start[1]) * t),
            int(start[2] + (end[2] - start[2]) * t)
        )

    @staticmethod
    def apply_color_mask(sprite, color):
        """Применение цветовой маски к спрайту"""
        colored_sprite = sprite.copy()
        colored_surface = pygame.Surface(sprite.get_size(), pygame.SRCALPHA)
        colored_surface.fill((*color, 255))  # Цвет маски
        colored_sprite.blit(colored_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        return colored_sprite
