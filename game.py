import pygame
import time
import math
from util import scale_image
from util import blit_rotate_center

GRASS = scale_image(pygame.image.load("imgs/grass.jpg"),3)
RED_CAR = scale_image(pygame.image.load("imgs/redcar.png"),0.2)
BLUE_CAR = scale_image(pygame.image.load("imgs/bluecar.png"),0.3)
BROWN_CAR = scale_image(pygame.image.load("imgs/browncar.png"),0.3)


TRACK = scale_image(pygame.image.load("imgs/trak.png"),1.2)
TRACK_BORDER = scale_image(pygame.image.load("imgs/tra.png"),1.2)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)
FINISH = pygame.image.load("imgs/Finish.png",)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Racing Game!!')
  
FPS = 60
class AbstractCar:
    def __init__(self,max_val,rotational_val):
        self.img = self.IMG
        self.max_val = max_val
        self.vel = 0
        self.rotational_val = rotational_val
        self.angle = 90
        self.x,self.y = self.START_POS
        self.acceleration = 0.1
        
    def rotate(self,left = False,right = False):
        if left:
            self.angle += self.rotational_val
        elif right:
            self.angle -= self.rotational_val
            
    def draw(self,win):
        blit_rotate_center(win,self.img,(self.x,self.y), self.angle)
        
    def move_forward(self):
        self.vel = min(self.vel + self.acceleration,self.max_val)
        self.move()
        
    def move_backward(self):
        self.vel = max(self.vel - self.acceleration,-self.max_val/2)
        self.move()
    
    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel
        
        self.y -= vertical
        self.x -= horizontal
        
    def collide(self,mask,x=10,y=10):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x-x),int(self.y-y))
        poi = mask.overlap(car_mask,offset)
        return poi
        
class PlayerCar(AbstractCar):
    IMG = RED_CAR
    START_POS = (200,45)   
    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration,0)
        self.move()
    
    def bounce(self):
        self.vel -= self.vel
        self.move()
            
        
def draw(win,images, player_car):
    for img,pos in images:
        win.blit(img,pos)
    player_car.draw(win)
    pygame.display.update()
    
    
def move_player(player_car):
    keys = pygame.key.get_pressed()
    moved = False
    
    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    if keys[pygame.K_d]:
        player_car.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True
        player_car.move_forward()
    if keys[pygame.K_s]:
        moved = True
        player_car.move_backward()
    
    
    if not moved:
        player_car.reduce_speed()

run = True
clock = pygame.time.Clock()
images = [(GRASS,(0,0)),(TRACK,(0,0))]
player_car = PlayerCar(4, 4)

while run:
    clock.tick(FPS)
    
    draw(WIN, images,player_car)

    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
    move_player(player_car)
    
    if player_car.collide(TRACK_BORDER_MASK) != None:
        print("collide")
        player_car.bounce()
         
pygame.quit()