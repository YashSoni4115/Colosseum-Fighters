#Colosseum Fighters
#January 17, 2023
#A fighting game with an ancient Rome theme such that gladiators are fighting each other with a cheering croud
#Yash Soni

#import all neccessary packages
import pygame
from pygame.locals import *
from pygame import mixer

mixer.init()
pygame.init()

#playing background music
pygame.mixer.music.load(
    r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Sound Effects/Background Sound.wav")
pygame.mixer.music.set_volume(0.15)
pygame.mixer.music.play(-1, 0.0, 5000)

#creating sound effects for different events that happen in game
sword_fx = pygame.mixer.Sound(
    r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Sound Effects/Sword Sound.mp3")
sword_fx.set_volume(0.25)
shield_fx = pygame.mixer.Sound(
    r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Sound Effects/Shield Sound.mp3")
shield_fx.set_volume(0.1)
jump_fx = pygame.mixer.Sound(
    r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Sound Effects/Jump Sound.mp3")
jump_fx.set_volume(0.05)
winner_fx = pygame.mixer.Sound(
    r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Sound Effects/Winner Sound.mp3")
winner_fx.set_volume(0.25)

#specifying properties of characters
playerW = 100
playerH = 175
width = 1224
height = 544
speed = 10
health = 100
player_1_x = 200
player_1_y = 325
player_2_x = 900
player_2_y = player_1_y
groundHeight = player_1_y + playerH
arrows = []

#creating the colours I will use
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)


#class for arrow that will be fired
class arrow:

    def __init__(self, x, y, direction, target, image):
        self.x = x
        self.y = y
        self.image = image
        self.vel = 15
        self.direction = direction
        self.arrow_used = False
        self.target = target
        #making it so that the arrow faces the right direction
        if direction:
            self.vel = -self.vel

    #method to draw the newly updated coordinates of an arrow
    def draw(self, target):
        attacking_rect = pygame.Rect(self.x, self.y, 98, 17)
        img = pygame.transform.flip(self.image, self.direction, False)
        screen.blit(img, (self.x, self.y))
        if self.arrow_used == False:
            #checking if the arrow hit the opponent and whether or not they had a shield up
            if attacking_rect.colliderect(target.rect):
                self.arrow_used = True
                if target.shield == False:
                    target.health -= 1
                else:
                    #playin sound if hits the opponents shield
                    shield_fx.play()


#class for the characters that will fight
class fighters:

    def __init__(self, player, x, y, sprites, animation_steps, flipped, data,
                 arrow):
        self.player = player
        self.flip = flipped
        self.offset = data[0]
        self.sprites = sprites
        self.rect = pygame.Rect((x, y, playerW, playerH))
        self.animation_steps = animation_steps
        self.action = 0
        self.frame_index = 0
        self.image = self.sprites[self.action][self.frame_index]
        self.vel_y = 0
        self.jump = False
        self.attacking = False
        self.idle = True
        self.attack_type = 0
        self.health = health
        self.sprites = sprites
        self.update_time = pygame.time.get_ticks()
        self.attack_cooldown = 0
        self.attack_time = 0
        self.arrow = arrow
        self.alive = True
        self.shield = False

    #method to draw the character at an updated location
    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(
            img, (self.rect.x - self.offset[0], self.rect.y - self.offset[1]))

    #method where movement takes place
    def move(self, target):
        dx = 0
        dy = 0
        gravity = 2
        self.attack_type = 0
        self.target = target

        key = pygame.key.get_pressed()
        if self.attacking == False and self.alive == True:
            if self.player == 1:  #player 1 controls
                if key[pygame.K_a]:  #move left
                    dx = -speed
                if key[pygame.K_d]:  #move right
                    dx = speed
                if key[pygame.K_w] and self.jump == False:  #jumping
                    jump_fx.play()
                    self.vel_y = -30
                    self.jump = True
                if key[pygame.K_e] or key[pygame.K_f] or key[
                        pygame.K_s] or key[
                            pygame.K_q]:  #check if there was an attack
                    if key[pygame.K_e]:
                        self.attack_type = 1
                    if key[pygame.K_f]:
                        self.attack_type = 2
                    if key[pygame.K_s]:
                        self.attack_type = 3
                    if key[pygame.K_q]:
                        self.attack_type = 4
                    self.attack(target)
            if self.player == 2:  #player 2 controls
                if key[pygame.K_LEFT]:
                    dx = -speed
                if key[pygame.K_RIGHT]:
                    dx = speed
                if key[pygame.K_UP] and self.jump == False:
                    jump_fx.play()
                    self.vel_y = -30
                    self.jump = True
                if key[pygame.K_j] or key[pygame.K_k] or key[
                        pygame.K_l] or key[pygame.K_h]:
                    if key[pygame.K_j]:
                        self.attack_type = 1
                    if key[pygame.K_k]:
                        self.attack_type = 2
                    if key[pygame.K_l]:
                        self.attack_type = 3
                    if key[pygame.K_h]:
                        self.attack_type = 4
                    self.attack(target)

        self.vel_y += gravity
        dy += self.vel_y  #creating gravity

        #setting bounding boxes of the screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > width:
            dx = width - self.rect.right
        if self.rect.bottom + dy > groundHeight:
            self.y_vel = 0
            self.jump = False
            dy = groundHeight - self.rect.bottom

        #make the character oriented in the right direction
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        #set attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        #moving the x and y coordinates
        self.rect.x += dx
        self.rect.y += dy

    #class to update the character's animation
    def update(self, target):
        if self.health <= 0:  #death animation
            self.health = 0
            self.alive = False
            self.update_action(6)
        elif self.attacking == True:
            if self.attack_type == 1:  #sword attack
                sword_fx.play()
                self.update_action(5)
            elif self.attack_type == 2:  #kick attack
                self.update_action(1)
            elif self.attack_type == 3:
                self.update_action(3)  #bow attack
            elif self.attack_type == 4:
                self.update_action(2)  #shield
        else:
            self.update_action(0)  #idle pose
        animation_cooldown = 50
        self.image = self.sprites[self.action][self.frame_index]
        if self.image == self.sprites[3][
                7]:  #shooting an arrow if at the right frame for bow animation
            self.bow(target)
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.sprites[self.action]):
            if self.alive == False:  #checking if the player is alive so that if it isn't then it stays dead
                self.frame_index = len(self.sprites[self.action]) - 1
            else:
                self.frame_index = 0
                if self.action == 1 or self.action == 5 or self.action == 3 or self.action == 2:
                    self.attacking = False
                    self.attack_cooldown = 50
                    self.shield = False

    def bow(
        self, target
    ):  #creates a new instance of an arrow and adds it to a list of arrows
        new = arrow(self.rect.centerx - (2 * self.rect.width * self.flip),
                    self.rect.y + (playerH / 2), self.flip, target, self.arrow)
        arrows.append(new)
        new.draw(target)

    def attack(self, target):
        if self.attack_cooldown == 0:  #check if attack colldown is finished
            self.attacking = True
            if self.attack_type == 1:  #sword attack
                attacking_rect = pygame.Rect(
                    self.rect.centerx - (2 * self.rect.width * self.flip),
                    self.rect.y, 1.5 * self.rect.width, self.rect.height)
                if attacking_rect.colliderect(
                        target.rect) and target.shield == False:
                    target.health -= 10  #checking if the sword hit the oppenent
                if target.shield == True:
                    shield_fx.play()  #playing sound effecte if hit the shield
            if self.attack_type == 2:
                attacking_rect = pygame.Rect(
                    self.rect.centerx - (2 * self.rect.width * self.flip),
                    self.rect.y, 1.5 * self.rect.width, self.rect.height)
                if attacking_rect.colliderect(
                        target.rect):  #checking if kicked opponent
                    target.health -= 5
                if target.shield == True:
                    shield_fx.play()  #playing sound effect if hits shield
            if self.attack_type == 4:
                self.shield = True  #making player shielded

    def update_action(
            self,
            new_action):  #method to check which slide of an animation to show
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


#creating screen
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption('Colosseum Fighters')
clock = pygame.time.Clock()
FPS = 60

#loading in sprites for every kind of action
player_1_kicking = [
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Kick 2.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Kick 3.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Kick 4.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Kick 5.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Kick 5.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Kick 5.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Kick 6.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Kick 7.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Kick 8.png"
                      ).convert_alpha()
]
player_1_rested = [
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Idle.png").
    convert_alpha()
]
player_1_shield = [
    pygame.image.load(
        r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Shield 2.png"
    ).convert_alpha(),
    pygame.image.load(
        r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Shield 3.png"
    ).convert_alpha(),
    pygame.image.load(
        r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Shield 4.png"
    ).convert_alpha(),
    pygame.image.load(
        r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Shield 5.png"
    ).convert_alpha(),
    pygame.image.load(
        r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Shield 6.png"
    ).convert_alpha(),
    pygame.image.load(
        r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Shield 6.png").
    convert_alpha(),
    pygame.image.load(
        r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Shield 6.png").
    convert_alpha(),
    pygame.image.load(
        r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Shield 6.png"
    ).convert_alpha(),
    pygame.image.load(
        r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Shield 6.png"
    ).convert_alpha(),
    pygame.image.load(
        r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Shield 6.png"
    ).convert_alpha(),
    pygame.image.load(
        r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Shield 7.png"
    ).convert_alpha(),
    pygame.image.load(
        r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Shield 8.png"
    ).convert_alpha(),
    pygame.image.load(
        r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Shield 9.png"
    ).convert_alpha(),
    pygame.image.load(
        r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Shield 10.png"
    ).convert_alpha()
]
player_1_bow = [
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Bow 2.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Bow 3.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Bow 4.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Bow 5.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Bow 6.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Bow 7.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Bow 8.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Bow 9.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Bow 9.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Bow 9.png").
    convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Bow 10.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Bow 11.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Bow 12.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Bow 13.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Bow 14.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Bow 15.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Bow 16.png"
                      ).convert_alpha()
]
player_1_stun = [
    pygame.image.load(
        r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Stunned 2.png").
    convert_alpha(),
    pygame.image.load(
        r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Stunned 3.png").
    convert_alpha()
]
player_1_sword = [
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Sword 2.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Sword 3.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Sword 4.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Sword 5.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Sword 6.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Sword 7.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Sword 8.png"
                      ).convert_alpha()
]
player_1_death = [
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Death 2.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Death 3.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Death 4.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Death 5.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 1 Sprites/Death 6.png"
                      ).convert_alpha()
]
#putting sprites in a list
player_1_sprites = [
    player_1_rested, player_1_kicking, player_1_shield, player_1_bow,
    player_1_stun, player_1_sword, player_1_death
]
player_1_sprites_steps = [
    len(player_1_rested),
    len(player_1_kicking),
    len(player_1_shield),
    len(player_1_bow),
    len(player_1_stun),
    len(player_1_sword)
]

#player 2 sprites
player_2_kicking = [
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Kick 2.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Kick 3.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Kick 4.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Kick 5.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Kick 5.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Kick 5.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Kick 6.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Kick 7.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Kick 8.png"
                      ).convert_alpha()
]
player_2_rested = [
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Idle.png").
    convert_alpha()
]
player_2_shield = [
    pygame.image.load(
        r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Shield 2.png"
    ).convert_alpha(),
    pygame.image.load(
        r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Shield 3.png"
    ).convert_alpha(),
    pygame.image.load(
        r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Shield 4.png"
    ).convert_alpha(),
    pygame.image.load(
        r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Shield 5.png"
    ).convert_alpha(),
    pygame.image.load(
        r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Shield 6.png"
    ).convert_alpha(),
    pygame.image.load(
        r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Shield 6.png").
    convert_alpha(),
    pygame.image.load(
        r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Shield 6.png").
    convert_alpha(),
    pygame.image.load(
        r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Shield 6.png"
    ).convert_alpha(),
    pygame.image.load(
        r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Shield 6.png"
    ).convert_alpha(),
    pygame.image.load(
        r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Shield 6.png"
    ).convert_alpha(),
    pygame.image.load(
        r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Shield 7.png"
    ).convert_alpha(),
    pygame.image.load(
        r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Shield 8.png"
    ).convert_alpha(),
    pygame.image.load(
        r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Shield 9.png"
    ).convert_alpha(),
    pygame.image.load(
        r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Shield 10.png"
    ).convert_alpha()
]
player_2_bow = [
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Bow 2.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Bow 3.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Bow 4.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Bow 5.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Bow 6.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Bow 7.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Bow 8.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Bow 9.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Bow 9.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Bow 9.png").
    convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Bow 10.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Bow 11.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Bow 12.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Bow 13.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Bow 14.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Bow 15.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Bow 16.png"
                      ).convert_alpha()
]
player_2_stun = [
    pygame.image.load(
        r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Stunned 2.png").
    convert_alpha(),
    pygame.image.load(
        r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Stunned 3.png").
    convert_alpha()
]
player_2_sword = [
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Sword 2.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Sword 3.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Sword 4.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Sword 5.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Sword 6.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Sword 7.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Sword 8.png"
                      ).convert_alpha()
]
player_2_death = [
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Death 2.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Death 3.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Death 4.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Death 5.png"
                      ).convert_alpha(),
    pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Player 2 Sprites/Death 6.png"
                      ).convert_alpha()
]
player_2_sprites = [
    player_2_rested, player_2_kicking, player_2_shield, player_2_bow,
    player_2_stun, player_2_sword, player_2_death
]
player_2_sprites_steps = [
    len(player_2_rested),
    len(player_2_kicking),
    len(player_2_shield),
    len(player_2_bow),
    len(player_2_stun),
    len(player_2_sword)
]

#loading in two types of bg images, one with controls and one without the controls shown
bg = pygame.image.load(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Colosseum Background.png")
bg_controls = pygame.image.load(
    r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Coloseum Background With Controls.png"
).convert_alpha()

#image for the arrow
arrow_img = pygame.image.load(
    r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/Arrow.png").convert_alpha()

#font that is used
count_font = pygame.font.Font(r"/Users/user/Downloads/ColosseumFighters/Colosseum Fighters Assets/turok.ttf", 80)

#making a variable that stores the current bg that will be shown
current_bg = bg_controls


#method to draw text onto screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


#method to draw current background onto screen
def drawBG():
    bg_img = pygame.transform.scale(current_bg, [width, height])
    screen.blit(bg_img, (0, 0))


player_offset = [80, 60]
player_data = [player_offset]


#method which draws health bar on the top
def drawHealthBar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, BLACK, (x - 5, y - 5, 510, 40))
    pygame.draw.rect(screen, RED, (x, y, 500, 30))
    pygame.draw.rect(screen, GREEN, (x, y, 500 * ratio, 30))


drawBG()

#varibles needed for counting in the introduction and changing the background
intro_count = 3
bg_change_timer = 7
last_count_update = pygame.time.get_ticks()

gameover = False

#creating instances of the fighters
player1 = fighters(1, player_1_x, player_1_y, player_1_sprites,
                   player_1_sprites_steps, False, player_data, arrow_img)
player2 = fighters(2, player_2_x, player_2_y, player_2_sprites,
                   player_2_sprites_steps, True, player_data, arrow_img)

winner = 0

#main game loop
running = True
while running:

    clock.tick(FPS)

    #draw background
    drawBG()

    #check if user quits
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #moving arrows and deletes arrows thet have gone off the screen or have hit the opposing player
    for a in arrows:
        if a.x > width or a.x < 0 or a.arrow_used:
            arrows.pop(arrows.index(a))
        else:
            a.x = a.x + a.vel
            a.draw(a.target)

    #drawing health bar for both players
    drawHealthBar(player1.health, 20, 20)
    drawHealthBar(player2.health, 704, 20)

    #creating the intro counter and only allowing players to move after its done or when the game is still playing
    if gameover == False:
        if intro_count <= 0:
            player1.move(player2)
            player2.move(player1)
        else:
            draw_text(str(intro_count), count_font, BLACK, width / 2,
                      height / 3)
            if (pygame.time.get_ticks() - last_count_update) >= 1000:
                intro_count -= 1
                last_count_update = pygame.time.get_ticks()

    #changing the background after the timer is done
    if bg_change_timer <= 0:
        current_bg = bg
    else:
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            bg_change_timer -= 1
            last_count_update = pygame.time.get_ticks()

    #calling update method for both players
    player1.update(player2)
    player2.update(player1)

    #drawing both players onto the screen
    player1.draw(screen)
    player2.draw(screen)

    #playing sound when game finishes
    if player1.alive == False and gameover == False:
        winner = 2
        gameover = True
        winner_fx.play()
        current_bg = bg
    if player2.alive == False and gameover == False:
        winner = 1
        gameover = True
        winner_fx.play()
        current_bg = bg

    #printing who won the game
    if winner == 2:
        draw_text("PLAYER 2 WINS", count_font, BLACK, width / 3 - 50,
                  height / 3)
    if winner == 1:
        draw_text("PLAYER 1 WINS", count_font, BLACK, width / 3 - 50,
                  height / 3)

    pygame.display.update()

pygame.quit