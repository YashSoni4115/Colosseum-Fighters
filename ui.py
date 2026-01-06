"""Drawing utilities (background, text, health bars)."""

from __future__ import annotations
import pygame

from settings import WIDTH, HEIGHT, BLACK, RED, GREEN

def draw_text(screen: pygame.Surface, text: str, font: pygame.font.Font, text_col: tuple[int,int,int], x: int, y: int) -> None:
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_bg(screen: pygame.Surface, bg: pygame.Surface) -> None:
    bg_img = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    screen.blit(bg_img, (0, 0))

def draw_health_bar(screen: pygame.Surface, health: int, x: int, y: int) -> None:
    ratio = health / 100
    pygame.draw.rect(screen, BLACK, (x - 5, y - 5, 510, 40))
    pygame.draw.rect(screen, RED, (x, y, 500, 30))
    pygame.draw.rect(screen, GREEN, (x, y, 500 * ratio, 30))
