import pygame 
from pygame.locals import *
import os
import random

pygame.init()

SCREEN_WIDTH = 864
SCREEN_HEIGHT = 936

WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("FLAPPY BIRD")

#font
FONT = pygame.font.SysFont( 'Bauhaus 93', 75)
WHITE = [255, 255, 255]

#LOAD IMAGES
BG = pygame.image.load(os.path.join('Assets_FB', 'bg.png'))
GROUND = pygame.image.load(os.path.join('Assets_FB', 'ground.png'))

# DRAW WINDOW
def draw_window(bird_group, pipe_group, collision, start, game_over):
    WIN.blit(BG, (0,0)) #background
    
    bird_group.draw(WIN) # drawing everything from the bird group
    pipe_group.draw(WIN) # draw all pipes
    
    if start == True :
        bird_group.update(collision)
    if start == True and game_over == False:
        pipe_group.update()
        
# DRAW POINTS       
def draw_score(points):
    score = FONT.render(str(points), 1, WHITE)   
    WIN.blit(score,(SCREEN_WIDTH//2,50))     

# MAIN
def main():
    FPS = 60
    clock = pygame.time.Clock()
    
    ground_scroll = 0
    scroll_speed = 4
    
    pipe_gap = 150
    pipe_freq = 1500 #millisecond
    last_pipe = pygame.time.get_ticks() - pipe_freq
    
    jump = True
    
    points = 0
    passed = False
    
    start = False
    game_over = False
    collision = False

     
    class Bird(pygame.sprite.Sprite):
        def __init__(self, x, y): #initiate the class
            pygame.sprite.Sprite.__init__(self) #initiate the sprite attributes and methods for class bird
            self.images = [] #list of images
            self.index = 0 #starting image
            self.counter = 0 #speed of the animation
            for num in range(1,4):
                img = pygame.image.load(os.path.join('Assets_FB', f'bird{num}.png')) #adding different flap images to images list; which will later be used in crating animation
                self.images.append(img)
            
                    
            self.image = self.images[self.index]
            self.rect = self.image.get_rect() # gets rect with dimensions of the image
            self.rect.center = [x,y] # centre start position of the bird
            self.vel = 0
            self.tap = False # prevents holding down the spacebar: check JUMP
             
        def update(self, collision):
            
            #gravity
            self.vel += 0.5 #acceleration; 
            if self.vel > 7:
                self.vel = 7 # to stop vel from increasing forever
            if self.rect.bottom < 768: #ground is at 768
                self.rect.y += self.vel
            
                
            #flapping animation
            if collision == False:
                self.counter += 1
                cooldown = 5
                if self.counter >= cooldown:
                    self.counter = 0
                    self.index += 1
                    if self.index >= len(self.images):
                        self.index = 0
                    self.image = self.images[self.index]
                    
                self.image = pygame.transform.rotate(self.images[self.index], -3*self.vel)
                
    class Pipe(pygame.sprite.Sprite):
        def __init__(self, x, y, position):
            pygame.sprite.Sprite.__init__(self) # to inherit sprite  functions from sprite class
            self.image =  pygame.image.load(os.path.join('Assets_FB', 'pipe.png'))   
            self.rect = self.image.get_rect()
    
            if position == 1:
                self.image = pygame.transform.flip(pygame.image.load(os.path.join('Assets_FB', 'pipe.png')), False, True) # flip it along y axis; not x axis
                self.rect.bottomleft = [x,y]
            else:
                self.rect.topleft = [x,y] 
                
        def update(self):
            self.rect.x -= scroll_speed
            if self.rect.right <= 0: # to test and witness killing, kill before 0
                self.kill()
            
                      
    #object creation         
    bird_group = pygame.sprite.Group()
    flappy = Bird(100, SCREEN_HEIGHT//2 )
    bird_group.add(flappy)
    
    pipe_group = pygame.sprite.Group()
    
    
    # main loop
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and jump == True:
                    if start == False:
                        start = True   
                    flappy.vel -= 10
                    if flappy.vel < -10:
                        flappy.vel = -10            
        
        draw_window(bird_group, pipe_group, collision, start, game_over)
        
        draw_score(points)
        
        #Collision
        if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top <= 0:
            collision = True
            game_over = True
            flappy.image = pygame.transform.rotate(flappy.images[1], -90) 
            jump = False
            
        #Point_counter
        if len(pipe_group) > 0:
            if flappy.rect.left > pipe_group.sprites()[0].rect.left\
                and flappy.rect.right < pipe_group.sprites()[0].rect.right and passed == False:
                passed = True  
                
            if flappy.rect.left > pipe_group.sprites()[0].rect.right and passed == True:
                passed = False
                #print("passed"+ str(points))
                points += 1
            
        #stops flapping and displays bird face down 
        if flappy.rect.bottom >= 770 :
            game_over = True
            flappy.image = pygame.transform.rotate(flappy.images[1], -90) 
            
     
            
        WIN.blit(GROUND, (ground_scroll, 768))
        
        if start == True and game_over == False:
            
            #pipe timer and creation
            time_now = pygame.time.get_ticks()  
            if time_now - last_pipe >= pipe_freq:
                last_pipe = time_now
                pipe_height = random.randint(200, 600)
                btm_pipe = Pipe(SCREEN_WIDTH, pipe_height + pipe_gap//2, -1 )
                top_pipe = Pipe(SCREEN_WIDTH, pipe_height - pipe_gap//2, 1 )
                pipe_group.add(btm_pipe) 
                pipe_group.add(top_pipe) 
                
            #ground scroll    
            ground_scroll -= scroll_speed
            if abs(ground_scroll) > 35:
                ground_scroll = 0
                
        pygame.display.update()
        
        
        
    main()    
        
        
if __name__ == "__main__": 
    main()
