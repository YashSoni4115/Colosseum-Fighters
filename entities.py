"""Game entities: Arrow and Fighter."""

from __future__ import annotations
import pygame

from settings import (
    WIDTH, GROUND_HEIGHT, PLAYER_W, PLAYER_H, SPEED, STARTING_HEALTH
)

class Arrow:
    def __init__(self, x: int, y: int, direction: bool, target: "Fighter", image: pygame.Surface):
        self.x = x
        self.y = y
        self.image = image
        self.vel = 15
        self.direction = direction  # True means flip left
        self.arrow_used = False
        self.target = target

        # Make it so that the arrow faces the right direction
        if direction:
            self.vel = -self.vel

    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, 98, 17)

    def update_and_draw(self, screen: pygame.Surface, target: "Fighter", shield_fx: pygame.mixer.Sound) -> None:
        img = pygame.transform.flip(self.image, self.direction, False)
        screen.blit(img, (self.x, self.y))

        if not self.arrow_used and self.rect().colliderect(target.rect):
            self.arrow_used = True
            if not target.shield:
                target.health -= 1
            else:
                shield_fx.play()


class Fighter:
    def __init__(
        self,
        player: int,
        x: int,
        y: int,
        sprites: list[list[pygame.Surface]],
        flipped: bool,
        offset: list[int],
        arrow_image: pygame.Surface,
    ):
        self.player = player
        self.flip = flipped
        self.offset = offset
        self.sprites = sprites

        self.rect = pygame.Rect((x, y, PLAYER_W, PLAYER_H))
        self.action = 0
        self.frame_index = 0
        self.image = self.sprites[self.action][self.frame_index]

        self.vel_y = 0
        self.jump = False

        self.attacking = False
        self.attack_type = 0
        self.health = STARTING_HEALTH

        self.update_time = pygame.time.get_ticks()
        self.attack_cooldown = 0

        self.arrow_image = arrow_image
        self.alive = True
        self.shield = False

    def draw(self, surface: pygame.Surface) -> None:
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.rect.x - self.offset[0], self.rect.y - self.offset[1]))

    def move(self, target: "Fighter", jump_fx: pygame.mixer.Sound) -> None:
        dx = 0
        dy = 0
        gravity = 2
        self.attack_type = 0

        key = pygame.key.get_pressed()

        if (not self.attacking) and self.alive:
            if self.player == 1:
                if key[pygame.K_a]:
                    dx = -SPEED
                if key[pygame.K_d]:
                    dx = SPEED
                if key[pygame.K_w] and (not self.jump):
                    jump_fx.play()
                    self.vel_y = -30
                    self.jump = True
            else:
                if key[pygame.K_LEFT]:
                    dx = -SPEED
                if key[pygame.K_RIGHT]:
                    dx = SPEED
                if key[pygame.K_UP] and (not self.jump):
                    jump_fx.play()
                    self.vel_y = -30
                    self.jump = True

        # Gravity
        self.vel_y += gravity
        dy += self.vel_y

        # Screen bounds
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > WIDTH:
            dx = WIDTH - self.rect.right
        if self.rect.bottom + dy > GROUND_HEIGHT:
            self.vel_y = 0
            self.jump = False
            dy = GROUND_HEIGHT - self.rect.bottom

        # Face target
        self.flip = not (target.rect.centerx > self.rect.centerx)

        # Cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Apply movement
        self.rect.x += dx
        self.rect.y += dy

    def handle_attacks(self, target: "Fighter") -> None:
        key = pygame.key.get_pressed()
        if self.attacking or (not self.alive):
            return

        if self.player == 1:
            if key[pygame.K_e] or key[pygame.K_f] or key[pygame.K_s] or key[pygame.K_q]:
                if key[pygame.K_e]:
                    self.attack_type = 1
                elif key[pygame.K_f]:
                    self.attack_type = 2
                elif key[pygame.K_s]:
                    self.attack_type = 3
                elif key[pygame.K_q]:
                    self.attack_type = 4
                self.attack(target)
        else:
            if key[pygame.K_j] or key[pygame.K_k] or key[pygame.K_l] or key[pygame.K_h]:
                if key[pygame.K_j]:
                    self.attack_type = 1
                elif key[pygame.K_k]:
                    self.attack_type = 2
                elif key[pygame.K_l]:
                    self.attack_type = 3
                elif key[pygame.K_h]:
                    self.attack_type = 4
                self.attack(target)

    def update(self, target: "Fighter", sword_fx: pygame.mixer.Sound) -> bool:
        """Returns True if an arrow should be spawned on this frame."""
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6)
        elif self.attacking:
            if self.attack_type == 1:
                sword_fx.play()
                self.update_action(5)
            elif self.attack_type == 2:
                self.update_action(1)
            elif self.attack_type == 3:
                self.update_action(3)
            elif self.attack_type == 4:
                self.update_action(2)
        else:
            self.update_action(0)

        animation_cooldown = 50
        self.image = self.sprites[self.action][self.frame_index]

        # In the original code, the bow fires on a specific frame
        bow_fire = (self.image == self.sprites[3][7]) if len(self.sprites) > 3 and len(self.sprites[3]) > 7 else False

        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        if self.frame_index >= len(self.sprites[self.action]):
            if not self.alive:
                self.frame_index = len(self.sprites[self.action]) - 1
            else:
                self.frame_index = 0
                if self.action in (1, 5, 3, 2):
                    self.attacking = False
                    self.attack_cooldown = 50
                    self.shield = False

        return bow_fire

    def spawn_arrow(self, target: "Fighter") -> Arrow:
        return Arrow(
            self.rect.centerx - int(2 * self.rect.width * self.flip),
            int(self.rect.y + (PLAYER_H / 2)),
            self.flip,
            target,
            self.arrow_image,
        )

    def attack(self, target: "Fighter") -> None:
        if self.attack_cooldown != 0:
            return

        self.attacking = True

        # Sword and kick share a hitbox style in the original
        if self.attack_type in (1, 2):
            attacking_rect = pygame.Rect(
                self.rect.centerx - (2 * self.rect.width * self.flip),
                self.rect.y,
                int(1.5 * self.rect.width),
                self.rect.height,
            )
            if attacking_rect.colliderect(target.rect):
                if self.attack_type == 1 and (not target.shield):
                    target.health -= 10
                elif self.attack_type == 2:
                    target.health -= 5

        if self.attack_type == 4:
            self.shield = True

    def update_action(self, new_action: int) -> None:
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
