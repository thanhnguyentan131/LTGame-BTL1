import pygame, sys, time, random
from pygame.locals import *

def score_board(score):
    # Update player's score
    score_string = pygame.font.Font(None, 50)
    score_text = score_string.render("Score: " + str(score), True, BLACK)
    score_text_pos = score_text.get_rect()
    score_text_pos.centerx = DISPLAYSURF.get_rect().centerx
    score_text_pos.centery = wn_magin_top
    DISPLAYSURF.blit(score_text, score_text_pos)

def miss_board(miss):
    # Update player's miss
    score_string = pygame.font.Font(None, 50)
    score_text = score_string.render("Miss: " + str(miss), True, BLACK)
    score_text_pos = score_text.get_rect()
    score_text_pos.centerx = wn_width * 1/5
    score_text_pos.centery = wn_magin_top
    DISPLAYSURF.blit(score_text, score_text_pos)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = hammer_img
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()

class Target(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.is_hit = False
        self.target_img = []
        self.target_img.append(pygame.image.load("images/zombie_1.png"))
        self.target_img.append(pygame.image.load("images/zombie_2.png"))
        self.target_img.append(pygame.image.load("images/zombie_3.png"))
        self.target_img.append(pygame.image.load("images/zombie_4.png"))
        self.target_img.append(pygame.image.load("images/zombie_5.png"))
        self.target_img.append(pygame.image.load("images/zombie_6.png"))
        self.current_sprite = 0
        self.image = self.target_img[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(2*self.rect.width, wn_width - 2*self.rect.width)
        self.rect.y = random.randint(self.rect.height, wn_height - 2*self.rect.height)

    def hitting(self):
        self.is_hit = True

    def update(self):
        if (self.is_hit == True):
            self.current_sprite += 0.2
            if(self.current_sprite >= len(self.target_img)):
                self.current_sprite = 5
                self.is_hit = False
            self.image = self.target_img[int(self.current_sprite)]

        # Boudary checking. 
        # Left and Right
        if(self.rect.right < 0 or self.rect.left > wn_width):
            self.rect.x = random.randint(2*self.rect.width, wn_width - 2*self.rect.width)
            self.rect.y = random.randint(self.rect.height, wn_height - 2*self.rect.height)

    

# Initiate game
pygame.init()

# Define some colors
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)

# Clock
clock = pygame.time.Clock()

# Game windown
wn_magin_top = 20
wn_width = 800
wn_height = 600
DISPLAYSURF = pygame.display.set_mode((wn_width, wn_height))
pygame.display.set_caption('Whack A Zombie')

# images and sounds
bg_img = pygame.image.load("images/floor.png")
bg_img = pygame.transform.scale(bg_img, (wn_width, wn_height))

# 6 aimation of zombie
# target_img = []
# target_img.append(pygame.image.load("images/zombie_1.png"))
# target_img.append(pygame.image.load("images/zombie_2.png"))
# target_img.append(pygame.image.load("images/zombie_3.png"))
# target_img.append(pygame.image.load("images/zombie_4.png"))
# target_img.append(pygame.image.load("images/zombie_5.png"))
# target_img.append(pygame.image.load("images/zombie_6.png"))

hammer_img = pygame.image.load("images/hammer.png")
hammer_img = pygame.transform.scale(hammer_img,(wn_width/10, wn_height/10))
pygame.mouse.set_visible(False)
fire_sound = pygame.mixer.Sound("sounds/fire.wav")

# Game loop
def game_loop():

    # Score
    score = 0

    # Miss
    miss = 0

    # Timer
    

    # Player
    player = Player()
    player_group = pygame.sprite.Group()
    player_group.add(player)

    # Target
    target_group = pygame.sprite.Group()
    new_target = Target()
    target_group.add(new_target)

    

    # Time control
    FPS = 60
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                hits = pygame.sprite.spritecollide(player, target_group, True)

                # for hit in hits:
                if(hits):
                    fire_sound.play()
                    score += 1
                    score_board(score)
                else:
                    miss += 1
                    miss_board(miss)



                # Hit or Miss always add new target
                new_target = Target()
                target_group.add(new_target)
        # Blit bg
        
        DISPLAYSURF.blit(bg_img,(0,0))

        target_group.update()
        target_group.draw(DISPLAYSURF)

        player_group.update()
        player_group.draw(DISPLAYSURF)

        score_board(score)
        miss_board(miss)
        pygame.display.flip()
        clock.tick(FPS)

game_loop()

# Game quit
pygame.quit()
sys.exit()