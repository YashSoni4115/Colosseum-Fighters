"""Asset loading helpers (images, sounds, fonts)."""

from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import pygame

from settings import ASSETS_DIR

@dataclass(frozen=True)
class SoundAssets:
    sword: pygame.mixer.Sound
    shield: pygame.mixer.Sound
    jump: pygame.mixer.Sound
    winner: pygame.mixer.Sound

@dataclass(frozen=True)
class ImageAssets:
    bg: pygame.Surface
    bg_controls: pygame.Surface
    arrow: pygame.Surface

@dataclass(frozen=True)
class FontAssets:
    count: pygame.font.Font

def _p(*parts: str) -> Path:
    return ASSETS_DIR.joinpath(*parts)

def init_audio() -> None:
    # Mixer must be initialized before loading sounds.
    pygame.mixer.init()

def play_background_music() -> None:
    music_path = _p("Colosseum Fighters Assets", "Sound Effects", "Background Sound.wav")
    pygame.mixer.music.load(str(music_path))
    pygame.mixer.music.set_volume(0.15)
    pygame.mixer.music.play(-1, 0.0, 5000)

def load_sounds() -> SoundAssets:
    sword = pygame.mixer.Sound(str(_p("Colosseum Fighters Assets", "Sound Effects", "Sword Sound.mp3")))
    sword.set_volume(0.25)

    shield = pygame.mixer.Sound(str(_p("Colosseum Fighters Assets", "Sound Effects", "Shield Sound.mp3")))
    shield.set_volume(0.10)

    jump = pygame.mixer.Sound(str(_p("Colosseum Fighters Assets", "Sound Effects", "Jump Sound.mp3")))
    jump.set_volume(0.05)

    winner = pygame.mixer.Sound(str(_p("Colosseum Fighters Assets", "Sound Effects", "Winner Sound.mp3")))
    winner.set_volume(0.25)

    return SoundAssets(sword=sword, shield=shield, jump=jump, winner=winner)

def load_images() -> ImageAssets:
    bg = pygame.image.load(str(_p("Colosseum Fighters Assets", "Colosseum Background.png")))
    bg_controls = pygame.image.load(str(_p("Colosseum Fighters Assets", "Coloseum Background With Controls.png"))).convert_alpha()
    arrow = pygame.image.load(str(_p("Colosseum Fighters Assets", "Arrow.png"))).convert_alpha()
    return ImageAssets(bg=bg, bg_controls=bg_controls, arrow=arrow)

def load_fonts() -> FontAssets:
    font_path = _p("Colosseum Fighters Assets", "turok.ttf")
    count = pygame.font.Font(str(font_path), 80)
    return FontAssets(count=count)

def load_player1_sprites() -> list[list[pygame.Surface]]:
    base = ("Colosseum Fighters Assets", "Player 1 Sprites")
    kicking = [
        pygame.image.load(str(_p(*base, f"Kick {i}.png"))).convert_alpha()
        for i in [2,3,4,5,5,5,6,7,8]
    ]
    rested = [pygame.image.load(str(_p(*base, "Idle.png"))).convert_alpha()]
    shield = [
        pygame.image.load(str(_p(*base, f"Shield {i}.png"))).convert_alpha()
        for i in [2,3,4,5,6,6,6,6,6,6,7,8,9,10]
    ]
    bow = [
        pygame.image.load(str(_p(*base, f"Bow {i}.png"))).convert_alpha()
        for i in [2,3,4,5,6,7,8,9,9,9,10,11,12,13,14,15,16]
    ]
    stun = [
        pygame.image.load(str(_p(*base, "Stunned 2.png"))).convert_alpha(),
        pygame.image.load(str(_p(*base, "Stunned 3.png"))).convert_alpha(),
    ]
    sword = [
        pygame.image.load(str(_p(*base, f"Sword {i}.png"))).convert_alpha()
        for i in [2,3,4,5,6,7,8]
    ]
    death = [
        pygame.image.load(str(_p(*base, f"Death {i}.png"))).convert_alpha()
        for i in [2,3,4,5,6]
    ]
    return [rested, kicking, shield, bow, stun, sword, death]

def load_player2_sprites() -> list[list[pygame.Surface]]:
    base = ("Colosseum Fighters Assets", "Player 2 Sprites")
    kicking = [
        pygame.image.load(str(_p(*base, f"Kick {i}.png"))).convert_alpha()
        for i in [2,3,4,5,5,5,6,7,8]
    ]
    rested = [pygame.image.load(str(_p(*base, "Idle.png"))).convert_alpha()]
    shield = [
        pygame.image.load(str(_p(*base, f"Shield {i}.png"))).convert_alpha()
        for i in [2,3,4,5,6,6,6,6,6,6,7,8,9,10]
    ]
    bow = [
        pygame.image.load(str(_p(*base, f"Bow {i}.png"))).convert_alpha()
        for i in [2,3,4,5,6,7,8,9,9,9,10,11,12,13,14,15,16]
    ]
    stun = [
        pygame.image.load(str(_p(*base, "Stunned 2.png"))).convert_alpha(),
        pygame.image.load(str(_p(*base, "Stunned 3.png"))).convert_alpha(),
    ]
    sword = [
        pygame.image.load(str(_p(*base, f"Sword {i}.png"))).convert_alpha()
        for i in [2,3,4,5,6,7,8]
    ]
    death = [
        pygame.image.load(str(_p(*base, f"Death {i}.png"))).convert_alpha()
        for i in [2,3,4,5,6]
    ]
    return [rested, kicking, shield, bow, stun, sword, death]
