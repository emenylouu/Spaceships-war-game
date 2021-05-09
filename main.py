import pygame
import time
import random
import gameLoader
pygame.font.init() 

###########################
###### Laser Class  #######
###########################
class Laser:
    
    def __init__(self, x, y , img):
       
        self.x = x
        self.y = y
        self.img = img
        self.mask= pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, velocity):
        self.y+=velocity

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)

###########################
####### Ship Class ########
###########################

class Ship:
    COOL_DOWN=30
    def __init__(self, x, y, health=100):
   
        self.x = x
        self.y = y
        self.health=health
        self.ship_img= None
        self.laser_img=None
        self.lasers= []
        self.cool_down_counter=0


    def draw(self, window):
        window.blit(self.ship_img,(self.x,self.y))
        for laser in self.lasers:
            laser.draw(window)

##### checks if every laser hits the enemies and vice versa with the player

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(gameLoader.HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                 obj.health -= 10
                 self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter>=self.COOL_DOWN:
            self.cool_down_counter=0
        elif self.cool_down_counter>0:
            self.cool_down_counter+=1


    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x,self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter=1

    
    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

###########################
###### Player Class #######
###########################
   
class Player(Ship):
    
    #EXTENDING THE SHIP PARAMS
    def __init__(self,x,y,health=100 ):
        super().__init__(x,y,health)
        self.ship_img= gameLoader.YELLOW_SPACESHIP
        self.laser_img= gameLoader.YELLOW_LASER
# CREATE A MASK TO DEFINE PIXLE POSITIONS IN AN IMAGE TO PREDICT COLLISION
        self.mask=pygame.mask.from_surface(self.ship_img)
        self.max_health=health

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(gameLoader.HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                       objs.remove(obj)
                       self.lasers.remove(laser) 
 
    def healthbar(self,window):
        pygame.draw.rect(window, (255,0,0), (self.x,self.y+self.ship_img.get_height()+10,self.ship_img.get_width(),10))
        pygame.draw.rect(window, (0,255,0), (self.x,self.y+self.ship_img.get_height()+10,self.ship_img.get_width()*(self.health/self.max_health),10))

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

###########################
####### Enemy Class  ######
###########################

class Enemy(Ship):
    COLOR_MAP= {
    "red": (gameLoader.RED_SPACESHIP, gameLoader.RED_LASER),
    "blue": (gameLoader.BLUE_SPACESHIP, gameLoader.BLUE_LASER),
    "green": (gameLoader.GREEN_SPACESHIP, gameLoader.GREEN_LASER)
    }
    """docstring for EnemyShip"""
    def __init__(self, x,y,color,health=100):
        super().__init__(x,y,health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
    
    def move(self, v):
        self.y += v


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

###########################
###### Main function #####
###########################

def main():
    run = True
    FPS= 60
    clock = pygame.time.Clock()
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans",50)
    lost_font = pygame.font.SysFont("comicsans",60)
    velocity=5
    enemy_velocity=1
    player = Player(300,650)
    enemies=[]
    wave_length=5
    lost = False
    lost_count=0
    laser_velocity=4


    def redraw_window():
        #blit takes one of the images and draws it to the window into the precised location (0.0)
        gameLoader.WIN.blit(gameLoader.BG,(0,0))
        #to add the text to the screen (level and lives) we need to create font that have been already intialized 
        lives_lable= main_font.render(f"lives: {lives} ", 1 , (255,255,255))
        level_lable = main_font.render(f"Level: {level} ", 1 ,(255,255,255))
        gameLoader.WIN.blit(lives_lable,(10,10))
        gameLoader.WIN.blit(level_lable,(gameLoader.WIDTH- level_lable.get_width()-10,0))

        for enemy in enemies:
            enemy.draw(gameLoader.WIN)

        player.draw(gameLoader.WIN)

        if lost:
            lost_lable = lost_font.render("You lost!!",1,(255,255,255))
            gameLoader.WIN.blit(lost_lable,(gameLoader.WIDTH/2 - lost_lable.get_width()/2,350))

        #refreshes the windows everytime we loop into the while loop
        pygame.display.update()



    while  run:
        clock.tick(FPS)
        redraw_window()

######## check for losing conditions and end the game one you lose.        
        if lives <=0 or player.health<=0:
            lost=True
            lost_count+=1

        if lost:
            if lost_count> FPS * 3:
                run = False
            else: 
                continue 


######### spawn enemies from random positions

        if len(enemies)==0:
            level +=1
            wave_length+=5
            for i in range(wave_length):
                enemy=Enemy(random.randrange(50,gameLoader.WIDTH-100),random.randrange(-1500, -100), random.choice(["red","blue","green"]))
                enemies.append(enemy)



######### event that checked every time we run the loop (60 times/sec) we'll loop in all the events in pygame event and do something about it 
        for event in pygame.event.get():
            #Quit bitton is the X on the top right.
            if event.type == pygame.QUIT:
                run = False



######## checks which key you're using and moves the player ACCORDINGLY
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - velocity >0:
           player.x -= velocity
        if keys[pygame.K_RIGHT] and player.x + velocity + player.get_width() < gameLoader.WIDTH:
            player.x += velocity
        if keys[pygame.K_UP] and player.y +velocity > 0:
            player.y -= velocity
        if keys[pygame.K_DOWN] and player.y + velocity + player.get_height() < gameLoader.HEIGHT:
            player.y += velocity
        ### creating the laser
        if keys[pygame.K_SPACE]:
            player.shoot()

######## move enemies with their given velocity
        for enemy in enemies[:]:
            enemy.move(enemy_velocity)
            enemy.move_lasers(laser_velocity,player)

            ### make the enemy shoot laser at the mainplayer
            if random.randrange(0,2*FPS)==1:
                enemy.shoot()
            if collide(enemy,player):
                player.health -=10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > gameLoader.HEIGHT:
                lives-=1
                enemies.remove(enemy)

        player.move_lasers(-laser_velocity, enemies)

       

main()
               
