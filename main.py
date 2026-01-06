"""Colosseum Fighters (refactored).

How to run:
1) Put your asset folder under: ./assets/Colosseum Fighters Assets/...
   or update ASSETS_DIR in settings.py
2) pip install pygame
3) python main.py
"""

from __future__ import annotations
import pygame

from settings import (
    WIDTH, HEIGHT, FPS, CAPTION,
    PLAYER_1_START_X, PLAYER_1_START_Y,
    PLAYER_2_START_X, PLAYER_2_START_Y,
    BLACK
)
from assets import (
    init_audio, play_background_music,
    load_sounds, load_images, load_fonts,
    load_player1_sprites, load_player2_sprites
)
from entities import Fighter
from ui import draw_bg, draw_text, draw_health_bar

def main() -> None:
    pygame.init()
    init_audio()

    # Screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(CAPTION)
    clock = pygame.time.Clock()

    # Assets
    play_background_music()
    sounds = load_sounds()
    images = load_images()
    fonts = load_fonts()

    # Sprites
    p1_sprites = load_player1_sprites()
    p2_sprites = load_player2_sprites()

    # Offsets (same as original)
    offset = [80, 60]

    # Instances
    player1 = Fighter(1, PLAYER_1_START_X, PLAYER_1_START_Y, p1_sprites, False, offset, images.arrow)
    player2 = Fighter(2, PLAYER_2_START_X, PLAYER_2_START_Y, p2_sprites, True, offset, images.arrow)

    arrows = []

    # Intro + background swap logic
    current_bg = images.bg_controls
    intro_count = 3
    bg_change_timer = 7
    last_tick = pygame.time.get_ticks()

    gameover = False
    winner = 0

    running = True
    while running:
        clock.tick(FPS)

        # Background
        draw_bg(screen, current_bg)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Move arrows, remove used/offscreen
        for a in list(arrows):
            if a.x > WIDTH or a.x < 0 or a.arrow_used:
                arrows.remove(a)
            else:
                a.x = a.x + a.vel
                a.update_and_draw(screen, a.target, sounds.shield)

        # Health bars
        draw_health_bar(screen, player1.health, 20, 20)
        draw_health_bar(screen, player2.health, 704, 20)

        if not gameover:
            if intro_count <= 0:
                # Movement first
                player1.move(player2, sounds.jump)
                player2.move(player1, sounds.jump)

                # Attacks after movement (keeps code easier to reason about)
                player1.handle_attacks(player2)
                player2.handle_attacks(player1)
            else:
                draw_text(screen, str(intro_count), fonts.count, BLACK, int(WIDTH / 2), int(HEIGHT / 3))
                if (pygame.time.get_ticks() - last_tick) >= 1000:
                    intro_count -= 1
                    last_tick = pygame.time.get_ticks()

        # Swap background after timer
        if bg_change_timer <= 0:
            current_bg = images.bg
        else:
            if (pygame.time.get_ticks() - last_tick) >= 1000:
                bg_change_timer -= 1
                last_tick = pygame.time.get_ticks()

        # Updates, check bow fire frame
        if player1.update(player2, sounds.sword):
            arrows.append(player1.spawn_arrow(player2))
        if player2.update(player1, sounds.sword):
            arrows.append(player2.spawn_arrow(player1))

        # Draw fighters
        player1.draw(screen)
        player2.draw(screen)

        # Winner
        if (not player1.alive) and (not gameover):
            winner = 2
            gameover = True
            sounds.winner.play()
            current_bg = images.bg
        if (not player2.alive) and (not gameover):
            winner = 1
            gameover = True
            sounds.winner.play()
            current_bg = images.bg

        if winner == 2:
            draw_text(screen, "PLAYER 2 WINS", fonts.count, BLACK, int(WIDTH / 3 - 50), int(HEIGHT / 3))
        elif winner == 1:
            draw_text(screen, "PLAYER 1 WINS", fonts.count, BLACK, int(WIDTH / 3 - 50), int(HEIGHT / 3))

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
