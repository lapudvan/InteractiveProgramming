import pygame
from pygame.locals import QUIT, KEYDOWN, MOUSEMOTION
from pygame.sprite import spritecollide, groupcollide
import time
import random

class Dory(pygame.sprite.Sprite):
    """Creates Dpry sprite"""
    def __init__(self,picture,left,top,width,height):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.left = left
        self.top = top

class Jellyfish(pygame.sprite.Sprite):
    """Creates pipe sprites"""
    def __init__(self,picture,left,top,width,height):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.left = left
        self.top = top

class ScreenView(object):
    """Shows game"""
    def __init__(self, model, screen):
        self.model = model
        self.screen = screen
    def draw(self):
        screen.blit(model.ocean_image, model.ocean_rect)
        screen.blit(model.dory_image, model.dory_rect)
        screen.blit(model.jellyfish1_image, model.jellyfish1_rect)
        screen.blit(model.jellyfish2_image, model.jellyfish2_rect)
        screen.blit(model.jellyfish3_image, model.jellyfish3_rect)
        screen.blit(model.jellyfish4_image, model.jellyfish4_rect)
        pygame.display.update()

class FindingDoryModel(object):
    """Behind the scenes, what makes the bird and pipes move"""
    def __init__(self,left,top,width,height):
        """ocean"""
        self.image3 = pygame.image.load('ocean.jpg')
        self.ocean_image = pygame.transform.scale(self.image3,(640,480))
        self.ocean_rect = self.ocean_image.get_rect()
        """Dory"""
        self.image1 = pygame.image.load('dory.jpg')
        self.dory_image = pygame.transform.scale(self.image1, (40,40))
        self.dory = Dory(self.dory_image,left,top,width,height)
        self.dory_rect = self.dory_image.get_rect()
        self.dory_rect.x = 100
        self.dory_rect.y = top

        """bottom Jellyfish 1"""
        self.image2 = pygame.image.load('jellyfish.png')
        r_height1 = random.randint(120,200)
        self.jellyfish1_image = pygame.transform.scale(self.image2, (60,r_height1))
        self.jellyfish1 = Jellyfish(self.jellyfish1_image,300,200,50,r_height1)
        self.jellyfish1_rect = self.jellyfish1_image.get_rect()
        self.jellyfish1_rect.x = 160
        self.jellyfish1_rect.y = 480 - r_height1
        """top Jellyfish 2"""
        r_height2 = random.randint(120,310)
        self.jellyfish2_image = pygame.transform.scale(self.image2, (60,r_height2))
        self.jellyfish2 = Jellyfish(self.jellyfish2_image,300,200,50,r_height2)
        self.jellyfish2_rect = self.jellyfish2_image.get_rect()
        self.jellyfish2_rect.x = 320
        self.jellyfish2_rect.y = 0
        """bottom Jellyfish 3"""
        r_height3 = random.randint(120,310)
        self.jellyfish3_image = pygame.transform.scale(self.image2, (60,r_height3))
        self.jellyfish3 = Jellyfish(self.jellyfish3_image,300,200,50,r_height3)
        self.jellyfish3_rect = self.jellyfish1_image.get_rect()
        self.jellyfish3_rect.x = 480
        self.jellyfish3_rect.y = 480 - r_height3
        """top Jellyfish 4"""
        r_height4 = random.randint(120,310)
        self.jellyfish4_image = pygame.transform.scale(self.image2, (60,r_height4))
        self.jellyfish4 = Jellyfish(self.jellyfish4_image,300,200,50,r_height4)
        self.jellyfish4_rect = self.jellyfish4_image.get_rect()
        self.jellyfish4_rect.x = 640
        self.jellyfish4_rect.y = 0

class KeyboardInput(object):
    """ Look for up and down keypresses to
    modify the y position of the bird """
    def __init__(self, model):
        self.model = model
    def handle_event(self, event):
        if event.type != KEYDOWN:
            return
        if event.key == pygame.K_UP:
            self.model.dory_rect.y -= 60
        if event.key == pygame.K_DOWN:
            self.model.dory_rect.y += 60

"""LET'S PLAY"""
if __name__ == '__main__':
    """game setup"""
    pygame.init()
    size = (640, 480)
    screen = pygame.display.set_mode(size)
    model = FindingDoryModel(150,200,30,30)
    view = ScreenView(model, screen)
    controller = KeyboardInput(model)
    pygame.mixer.music.load('keepswimming.mp3')
    pygame.mixer.music.play(-1)
    """run game"""
    running = True
    STATE = 'STATE_INGAME'
    clock = 0
    font = pygame.font.Font(None, 36) # This is a font we use to draw text on the screen (size 36)
    RED = (255, 0, 0)
    while running:
        if STATE == 'STATE_INGAME':    
            jellyfishies = [model.jellyfish1_rect,model.jellyfish2_rect,model.jellyfish3_rect,model.jellyfish4_rect]
            for jellyfish in jellyfishies:
                if model.dory_rect.colliderect(jellyfish):
                    STATE = 'STATE_GAMEOVER'
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                controller.handle_event(event)
            """gravity?"""
            model.dory_rect.y -= 1
            """move jellyfish"""
            model.jellyfish1_rect.x -= 1
            model.jellyfish2_rect.x -= 1
            model.jellyfish3_rect.x -= 1
            model.jellyfish4_rect.x -= 1
            """restart jellyfish"""
            if model.jellyfish1_rect.x <= -60:
                r_height1 = random.randint(120,310)
                model.jellyfish1_image = pygame.transform.scale(model.image2, (60,r_height1))
                model.jellyfish1 = Jellyfish(model.jellyfish1_image,300,200,50,r_height1)
                model.jellyfish1_rect.y = 480 - r_height1
                model.jellyfish1_rect.x = 640
            if model.jellyfish2_rect.x <= -60:
                r_height2 = random.randint(120,310)
                model.jellyfish2_image = pygame.transform.scale(model.image2, (60,r_height2))
                model.jellyfish2 = Jellyfish(model.jellyfish2_image,300,200,50,r_height2)
                model.jellyfish2_rect.y = 0
                model.jellyfish2_rect.x = 640
            if model.jellyfish3_rect.x <= -60:
                r_height3 = random.randint(120,310)
                model.jellyfish3_image = pygame.transform.scale(model.image2, (60,r_height3))
                model.jellyfish3 = Jellyfish(model.jellyfish3_image,300,200,50,r_height3)
                model.jellyfish3_rect.y = 480 - r_height3
                model.jellyfish3_rect.x = 640
            if model.jellyfish4_rect.x <= -60:
                r_height4 = random.randint(120,310)
                model.jellyfish4_image = pygame.transform.scale(model.image2, (60,r_height4))
                model.jellyfish4 = Jellyfish(model.jellyfish4_image,300,200,50,r_height4)
                model.jellyfish4_rect.y = 0
                model.jellyfish4_rect.x = 640
            clock += .007
            view.draw()

        if STATE == 'STATE_GAMEOVER':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                controller.handle_event(event)
            text = font.render("Game Over Score: " + str(clock), True, RED)
            text_rect = text.get_rect()
            text_x = 320 - text_rect.width / 2
            text_y = 240 - text_rect.height / 2
            screen.blit(text, [text_x, text_y])
            pygame.display.update()

        time.sleep(.001)