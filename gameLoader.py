import pygame
import os

WIDTH , HEIGHT = 750 , 750
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Space Shooter Game")
#loading the asset images
RED_SPACESHIP= pygame.image.load(os.path.join("assets","pixel_ship_red_small.png"))
GREEN_SPACESHIP= pygame.image.load(os.path.join("assets","pixel_ship_green_small.png"))
BLUE_SPACESHIP= pygame.image.load(os.path.join("assets","pixel_ship_blue_small.png"))
#main player ship
YELLOW_SPACESHIP= pygame.image.load(os.path.join("assets","pixel_ship_yellow.png"))

#lasers
RED_LASER= pygame.image.load(os.path.join("assets","pixel_laser_red.png"))
GREEN_LASER= pygame.image.load(os.path.join("assets","pixel_laser_green.png"))
BLUE_LASER= pygame.image.load(os.path.join("assets","pixel_laser_blue.png"))
YELLOW_LASER= pygame.image.load(os.path.join("assets","pixel_laser_yellow.png"))

#background
BG= pygame.transform.scale(pygame.image.load(os.path.join("assets","background-black.png")),(WIDTH,HEIGHT))