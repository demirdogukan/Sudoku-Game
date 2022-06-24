import pygame as pg


pg.init()

def draw_text(screen, text, size, color, pos):
    font = pg.font.SysFont("arial", size)
    txt_surface = font.render(text, True, color).convert_alpha()
    txt_rect = txt_surface.get_rect(topleft=pos)
    screen.blit(txt_surface, (txt_rect.x + txt_surface.get_width(), txt_rect.y))
