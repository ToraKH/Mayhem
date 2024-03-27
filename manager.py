import pygame as pg
import config as cng
import random
import math

#Made the screen a global variable -> so that its easier to recall (+ easier to blit bullets)
screen = pg.display.set_mode((cng.SCREEN_X, cng.SCREEN_Y))

class Object(pg.sprite.Sprite):
    # Your implementation goes here
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.position = pg.math.Vector2(0,0)        # Initialise empty position vector
        self.rect = pg.rect.Rect(self.position.x, self.position.y, self.width, self.height)
    
    def update(self):
        pass


class Obstacle(Object):
    def __init__(self):
        super().__init__(Manager().obstacle_img)


class FuelSpot(Object):     #NEEDS A SPRITE
    def __init__(self):
        super().__init__()


    def refuel_ships(self):
        """If the ships lands on the platform, they get refueled"""
        if pg.sprite.groupcollide(Manager().player2_group, Manager().fuel_group):
            Player2().fuel = cng.FUELLIMIT
        if pg.sprite.groupcollide(Manager().player1_group, Manager().fuel_group):
            Player1().fuel = cng.FUELLIMIT



class SpaceShip(Object):
    #---------------------------------------------------
    class Bullets(Object):
        def __init__(self, b_img, position, angle):
            super().__init__(b_img)
            self.angle = angle
            self.position = pg.math.Vector2(position)
            self.rect.center = self.position

            # Calculate the constant velocity vector based on the angle
            angle_rad = math.radians(self.angle)
            direction = pg.math.Vector2(math.cos(angle_rad), -math.sin(angle_rad))
            self.velocity = direction * cng.BULLET_SPEED

        def update(self):
            """updates position of the bullet"""
            self.position += self.velocity
            self.rect.center = self.position
            screen.blit(self.image, self.rect)
            self.edge_kill()

        def edge_kill(self):
            """terminates the bullet if it steps out-of-bounds"""
            if (self.rect.right < (cng.BORDER//1.5) or self.rect.left > cng.SCREEN_X-(cng.BORDER//1.5)
                 or self.rect.bottom < (cng.BORDER//1.5) or self.rect.top > cng.SCREEN_Y-(cng.BORDER//1.5)):
                self.kill()

    #-----------------------------------------------------    

    def __init__(self, image):
        super().__init__(image)
        self.fuel = cng.FUELLIMIT
        self.score = 0
        self.health = cng.HEALTH   
        self.velocity = pg.math.Vector2(0,0)
        self.angle = 90     #So the spaceship faces upwards
        self.rotated_rect = None

        self.max_bullets = cng.BULLET_MAX
        self.shoot_cooldown = cng.BULLET_COOL_DOWN
        self.bullet_count = 0
        self.last_shot_time = 0

# =============================================================

## POSITION CONTROL
        

    def rotate_right(self):
        ''' Rotates the ship to the right'''
        self.angle -= cng.ROTATION_SPEED
        

    def rotate_left(self):
        ''' Rotates the ship to the left'''
        self.angle += cng.ROTATION_SPEED
        

    def thrust(self):
        ''' The ship moves forward'''
        angl_rad = math.radians(self.angle)
        direction = pg.math.Vector2(math.cos(angl_rad), -math.sin(angl_rad))
        
        self.velocity +=  direction * cng.THRUST

    
    def gravity(self):
        ''' Gravitational force to drag the ship downwards'''
        if self.rect.bottom < cng.SCREEN_Y - (cng.BORDER//2):
            self.velocity += cng.GRAVITY
        
# ============================================================= 
# ============================================================= 

## ACTION FUNCTIONS
    def edge_kill(self):
        """New crash function to kill ship if crashes into edges"""

        #If ship crashes into the ground
        if self.rect.bottom > (cng.SCREEN_Y - (cng.BORDER//4)):
            print(self.__class__.__name__ + " is tasting the dirt")
            self.kill()

        #If ship crashes into the sky
        if self.rect.top < (cng.BORDER//4):
            print(self.__class__.__name__ + " is meeting the Lord")
            self.kill()

        #If chrashed into L/R edges
        if self.rect.left < (cng.BORDER//4):
            print(self.__class__.__name__ + " crashed L")
            self.kicng.ll()
        
        if self.rect.right > cng.SCREEN_X - (cng.BORDER//4):
            print(self.__class__.__name__ + " crashed R")
            self.kill()

    def shoot(self, b_img, bullets):
        ''' The ship shoots bullets'''
        current_time = pg.time.get_ticks()
        # Reset bullet count if cooldown has passed
        if (current_time - self.last_shot_time) > self.shoot_cooldown:
            self.bullet_count = 0

        # Shoot if there are less than max_bullets bullets already shot
        if self.bullet_count < self.max_bullets:
            bullet = SpaceShip.Bullets(b_img, self.rect.center, self.angle)
            bullets.add(bullet)
            self.bullet_count += 1
            self.last_shot_time = current_time


    def got_shot(self, other): 
        """Checks whether ship got hit by bullet"""
        self.health += cng.HITPOINT
        other.score += cng.SCOREPOINT

        if self.health <=0:
            print("PLAYER HAS BEEN DESTROYED")
            self.kill()


    def draw(self):
        """ overwrites pygames draw function to rotate the image of the sprite"""
        rotated_image = pg.transform.rotate(self.image, self.angle-90)          #Rotate image by calculated angle 
        rotated_rect = rotated_image.get_rect(center=self.rect.center)  #Rotate sprite's rectangle by same angle
        #pg.draw.rect(screen, (255, 0, 0), self.rect, 2)
        
        screen.blit(rotated_image, rotated_rect)

    
# ============================================================= 
# =============================================================     
    
## FUNCTIONS NOT USED
    def fuel_use(self):
        """Decreases the amount of fuel as the time goes"""
        self.fuel -= cng.FUELUSE
        return self.fuel
    

    def crash(self):
        """Checks whether ship has crashed into obstacles"""
        pass

    def update_score(self, scorepoints):
        """Updates the score"""
        # #hvis crasher, så går score ned [ie -10]
        # #hvis man treffer motstander går score opp [ie +10]
        # #hvis motstander dør av skuddet, går score masse opp [ie +50?]
        # self.score += scorepoints
        # return self.score
        pass


    def update_health(self, healthpoints):
        """Updates health"""
        # self.health += healthpoints
        # if self.health < 0:
        #     self.kill()
        # #hvis man crasher går health ned
        # #hvis man blir skutt går health ned
        # #hvis man har null health så dør man
        # return self.health
        pass


    def update_health_and_score(self):
        # #If crashed in walls or obstacles, then kill
        # if self.crash:
        #     self.kill()
        
        # # If they crash in each other, they loose points and health
        # if self.crash_eachother():
        #     self.update_health(random.randint(1, 8)*cng.HITPOINT)
        #     self.update_score(-3*cng.SCOREPOINT)

        # if self.got_shot(self):
        #     self.update_health(2.5*cng.HITPOINT)
        #     self.update_score(-4*cng.SCOREPOINT)
        pass

       
        
# ============================================================= 
    

#RED SPACESHIP    
class Player1(SpaceShip):

    def __init__(self, image):
        super().__init__(image)
        # Overwrite position to start at the bottom of the screen
        self.position = pg.math.Vector2(random.randint(cng.BORDER,cng.SCREEN_X//2), cng.SCREEN_Y-(cng.BORDER*2.2))
        

    def update(self, b_img, p1_bullets):
        self.velocity = pg.math.Vector2(0,0) #Reset velocity
        key = pg.key.get_pressed()
        if key[pg.K_a]:
            self.rotate_left()
        if key[pg.K_d]:
            self.rotate_right()
        if key[pg.K_w]:
            self.thrust()
        else:
            self.gravity()
        if key[pg.K_LSHIFT]:
            self.shoot(b_img, p1_bullets)

        self.position += self.velocity
        self.rect.topleft = self.position   #Update sprite position

        self.edge_kill()


#BLUE SPACESHIP
class Player2(SpaceShip):

    def __init__(self, image):
        super().__init__(image)
        # Overwrite position to start at the bottom of the screen
        self.position = pg.math.Vector2(random.randint(cng.SCREEN_X//2, cng.SCREEN_X-cng.BORDER), cng.SCREEN_Y-(cng.BORDER*2.2))

    def update(self, b_img, p2_bullets):
        self.velocity = pg.math.Vector2(0,0)
        key = pg.key.get_pressed()
        if key[pg.K_LEFT]:
            self.rotate_left()
        if key[pg.K_RIGHT]:
            self.rotate_right()
        if key[pg.K_UP]:
            self.thrust()
        else: 
            self.gravity()
        if key[pg.K_RSHIFT]:
            self.shoot(b_img, p2_bullets)


        self.position += self.velocity
        self.rect.topleft = self.position

        self.edge_kill()



class Manager():
    def __init__(self):
        pg.init()
        # self.screen = pg.display.set_mode((cng.SCREEN_X, cng.SCREEN_Y))
        self.clock = pg.time.Clock()

        # Load the simulation background and use it
        self.background = pg.image.load(cng.BACKGROUND) 
        self.background = pg.transform.scale(self.background,(cng.SCREEN_X, cng.SCREEN_Y)) 
        self.background.convert()

        # Load images
        self.player1_img = pg.image.load(cng.SHIP_PLAYER1).convert_alpha() 
        self.player1_img = pg.transform.scale(self.player1_img,(self.player1_img.get_width(), self.player1_img.get_height()))
        
        self.player2_img = pg.image.load(cng.SHIP_PLAYER2).convert_alpha() 
        self.player2_img = pg.transform.scale(self.player2_img,(self.player2_img.get_width(), self.player2_img.get_height()))
        
        self.obstacle_img = pg.image.load(cng.OBSTACLE).convert_alpha() 
        self.obstacle_img = pg.transform.scale(self.obstacle_img,(self.obstacle_img.get_width(), self.obstacle_img.get_height()))
        
        self.bullet_img = pg.image.load(cng.BULLET).convert_alpha() 
        self.bullet_img = pg.transform.scale(self.bullet_img,(self.bullet_img.get_width()/15, self.bullet_img.get_height()/15))
        
        
        self.sprites_init()
        self.loop()


    def loop(self):
        """Main loop for manager. Checks the event for exit strategy, and
           updates all the objects""" 
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()

            self.update()

            self.clock.tick(60)  # Frames per second


    def sprites_init(self):
        """Initializes objects, and groups them"""
        self.player1 = Player1(self.player1_img)
        self.player1_group = pg.sprite.Group()
        self.player1_group.add(self.player1)

        self.player2 = Player2(self.player2_img)
        self.player2_group = pg.sprite.Group()
        self.player2_group.add(self.player2)

        self.p1_bullet_group = pg.sprite.Group()
        self.p2_bullet_group = pg.sprite.Group()


        """
        self.obstacle = Obstacle()
        self.obstacle_group = pg.sprite.Group()
        self.obstacle_group.add(self.obstacle)

        """


    def update(self):
        """Updates all objects through sprite's group update"""
        screen.blit(self.background, (0,0))

        for player in self.player1_group:
            player.draw()

        for player in self.player2_group:
            player.draw()


        #Update Group
        self.player1_group.update(self.bullet_img, self.p1_bullet_group)
        self.player2_group.update(self.bullet_img, self.p2_bullet_group)
        
        if self.p1_bullet_group is not None:
            for bullet in self.p1_bullet_group:
                bullet.update()
                
        if self.p2_bullet_group is not None:
            for bullet in self.p2_bullet_group:
                bullet.update()

        #self.obstacle_group.draw(screen)
        #self.obstacle_group.update()


        # Check for Collisions
        if pg.sprite.groupcollide(self.player1_group, self.player2_group, True, True):
            print("CRASH COURSE DELIGHT")
        
        if pg.sprite.groupcollide(self.player1_group, self.p2_bullet_group, False, True):
            self.player1.got_shot(self.player2)

            print("Player1 HP:", self.player1.health, "\t Player2 HP:", self.player2.health)
            print("Player1 SCORE:", self.player1.score, "\t Player2 SCORE:", self.player2.score)
            
        
        if pg.sprite.groupcollide(self.player2_group, self.p1_bullet_group, False, True):
            self.player2.got_shot(self.player1)

            print("Player1 HP:", self.player1.health, "\t Player2 HP:", self.player2.health)
            print("Player1 SCORE:", self.player1.score, "\t Player2 SCORE:", self.player2.score)


        pg.display.flip()



    '''def text(self):
        """Prints text on screen"""
        font = pg.font.SysFont('arial', 20)
        player1_txt = font.render('PLAYER 1', True, (255, 255, 255))
        score_player1 = font.render('SCORE: ' + str(self.player1.score), True, (255, 255, 255))
        fuel_player1 = font.render('FUEL: ' + str(self.player1.fuel), True, (255, 255, 255))

        player2_txt = font.render('PLAYER 2', True, (255, 255, 255))
        score_player2 = font.render('SCORE: ' + str(self.player2.score), True, (255, 255, 255))
        fuel_player2 = font.render('FUEL: ' + str(self.player2.fuel), True, (255, 255, 255))

        self.screen.blit(player1_txt, (cng.SCREEN_X - player1_txt.get_width(), cng.SCREEN_Y - 2*player1_txt.get_height()))
        self.screen.blit(score_player1, (cng.SCREEN_X - score_player1.get_width(), cng.SCREEN_Y - 3*score_player1.get_height()))
        self.screen.blit(fuel_player1, (cng.SCREEN_X - fuel_player1.get_width(), cng.SCREEN_Y - 4*fuel_player1.get_height()))
        self.screen.blit(player2_txt, (cng.SCREEN_X - player2_txt.get_width(), cng.SCREEN_Y - 5*player2_txt.get_height()))
        self.screen.blit(score_player2, (cng.SCREEN_X - score_player2.get_width(), cng.SCREEN_Y - 6*score_player2.get_height()))
        self.screen.blit(fuel_player2, (cng.SCREEN_X - fuel_player2.get_width(), cng.SCREEN_Y - 7*fuel_player2.get_height()))
    '''

if __name__ == "__main__":
    Manager()
