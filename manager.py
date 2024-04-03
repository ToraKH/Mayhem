"""
Module name: manager.py
Module Purpose: Creates a game inspired of Mayhem 
Authors:
- Dulmini S. Gamage
- Tora K. Homme
"""


from pygame import mixer
import pygame as pg
import config as cng
import random
import math


#Made the screen a global variable -> so that its easier to recall (+ easier to blit bullets)
screen = pg.display.set_mode((cng.SCREEN_X, cng.SCREEN_Y))

class Object(pg.sprite.Sprite):
    """Represents the visible ovjects in the game"""
    def __init__(self, image):
        """ Initializes Objects''s attributes"""

        super().__init__()
        self.image = image
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.position = pg.math.Vector2(0,0)        # Initialise empty position vector
        self.rect = pg.rect.Rect(self.position.x, self.position.y, self.width, self.height)
    
    def update(self):
        pass


# ============================================================= 
# ============================================================= 


class Obstacle(Object):
    """Represents the alien object in the game"""
    def __init__(self, image):
        """ Initializes Obstacle's attributes"""

        super().__init__(image)
        # Overwrite position to start at the random spot on the screen
        self.position = pg.math.Vector2(random.randint(cng.BORDER, cng.SCREEN_X-cng.BORDER), random.randint(cng.BORDER, cng.SCREEN_Y//2)) 
        self.rect = pg.rect.Rect(self.position.x, self.position.y, self.width, self.height)


# ============================================================= 
# ============================================================= 
        

class FuelSpot(Object):    
    """Represents the fuel cans in the game""" 
    def __init__(self, image, x,y):
        """ Initializes FuelSpot's attributes"""
        super().__init__(image)
        #Overwrite position to start at the bottom of the screen
        self.position = pg.math.Vector2(x, y)
        self.rect = pg.rect.Rect(self.position.x, self.position.y, self.width, self.height)



# ============================================================= 
# ============================================================= 


class SpaceShip(Object):
    """Represents a spaceship object in the game"""
    #---------------------------------------------------
    class Bullets(Object):
        """ Represemts the bullets that space ships shoot"""
        def __init__(self, b_img, position, angle):
            """ Initializes Bullets' attributes"""
            super().__init__(b_img)
            self.angle = angle
            self.position = pg.math.Vector2(position)
            self.rect.center = self.position

            # Calculate the constant velocity vector based on the angle
            angle_rad = math.radians(self.angle)
            direction = pg.math.Vector2(math.cos(angle_rad), -math.sin(angle_rad))
            self.velocity = direction * cng.BULLET_SPEED

        def update(self):
            """ Updates position of the bullet"""
            self.position += self.velocity
            self.rect.center = self.position
            screen.blit(self.image, self.rect)
            self.edge_kill()

        def edge_kill(self):
            """ Terminates the bullet if it steps out-of-bounds"""
            if (self.rect.right < (cng.BORDER//1.5) or self.rect.left > cng.SCREEN_X-(cng.BORDER//1.5)
                 or self.rect.bottom < (cng.BORDER//1.5) or self.rect.top > cng.SCREEN_Y-(cng.BORDER//1.5)):
                self.kill()

    #-----------------------------------------------------    

    def __init__(self, image):
        """ Initializes Spaceship attributes"""
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


#-------------POSITION-CONTROL------------------------

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
        if self.rect.bottom < cng.SCREEN_Y - (cng.BORDER//2-5):
            self.velocity += cng.GRAVITY
        
#--------------ACTION-FUNCTIONS-----------------------

    def edge_kill(self):
        """ Kill ship if crashes into edges"""

        #If ship crashes into the ground
        if self.rect.bottom > (cng.SCREEN_Y - (cng.BORDER//4)):
            print(self.__class__.__name__ + " is tasting the dirt")
            self.health = 0
            self.kill()

        #If ship crashes into the sky
        if self.rect.top < (cng.BORDER//4):
            print(self.__class__.__name__ + " is meeting the Lord")
            self.health = 0
            self.kill()

        #If chrashed into L/R edges
        if self.rect.left < (cng.BORDER//4):
            print(self.__class__.__name__ + " crashed L")
            self.health = 0
            self.kill()
        
        if self.rect.right > cng.SCREEN_X - (cng.BORDER//4):
            print(self.__class__.__name__ + " crashed R")
            self.health = 0
            self.kill()

        #If ship chrashes into the obstacle
        if self.rect.right > cng.SCREEN_X - (cng.BORDER//4):
            print(self.__class__.__name__ + " crashed R")
            self.health = 0
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
        """ Updates score and health when ship is hit by bullet"""
        self.health += cng.HITPOINT
        other.score += cng.SCOREPOINT



    def draw(self):
        """ Overwrites pygames draw function to rotate the image of the sprite"""
        rotated_image = pg.transform.rotate(self.image, self.angle-90)          #Rotate image by calculated angle 
        rotated_rect = rotated_image.get_rect(center=self.rect.center)          #Rotate sprite's rectangle by same angle
        
        screen.blit(rotated_image, rotated_rect)

    

# ============================================================= 
# =============================================================     
    
    

#RED SPACESHIP    
class Player1(SpaceShip): 
    """Represents Player 1's spaceship"""

    def __init__(self, image):
        """ Initializes Player1's attributes"""
        super().__init__(image)
        # Overwrite position to start at the bottom of the screen
        self.position = pg.math.Vector2(random.randint(cng.BORDER,cng.SCREEN_X//2), cng.SCREEN_Y-(cng.BORDER*2.2))
        

    def update(self, b_img, p1_bullets):
        """Update the state of player 1"""
        self.velocity = pg.math.Vector2(0,0) #Reset velocity
        key = pg.key.get_pressed()
        if key[pg.K_a]:
            self.rotate_left()
        if key[pg.K_d]:
            self.rotate_right()
        if key[pg.K_w] and self.fuel >= 0:
            self.thrust()
            self.fuel -= cng.FUELUSE #Uses fuel when thrusts
        else:
            self.gravity()         
        if key[pg.K_LSHIFT]:
            self.shoot(b_img, p1_bullets)
        if self.health <= 0:
            self.kill()
            print("PLAYER1's LAST COSMIC DANCE")

        self.position += self.velocity
        self.rect.topleft = self.position   #Update sprite position

        self.edge_kill()

# ============================================================= 
# ============================================================= 
        

#BLUE SPACESHIP
class Player2(SpaceShip):
    """<Represents Player 2's spaceship"""

    def __init__(self, image):
        """ Initializes Player2's attributes"""
        super().__init__(image)
        # Overwrite position to start at the bottom of the screen
        self.position = pg.math.Vector2(random.randint(cng.SCREEN_X//2, cng.SCREEN_X-cng.BORDER), cng.SCREEN_Y-(cng.BORDER*2.2))

    def update(self, b_img, p2_bullets):
        """Update the state of player 2"""
        self.velocity = pg.math.Vector2(0,0)
        key = pg.key.get_pressed()
        if key[pg.K_LEFT]:
            self.rotate_left()
        if key[pg.K_RIGHT]:
            self.rotate_right()
        if key[pg.K_UP] and self.fuel >= 0:
            self.thrust()
            self.fuel -= cng.FUELUSE #Uses fuel when thrusts
        else: 
            self.gravity()
        if key[pg.K_RCTRL]:
            self.shoot(b_img, p2_bullets)
        if self.health <= 0:
            self.kill()
            print("PLAYER2 BLASTED INTO STARDUST")

        self.position += self.velocity
        self.rect.topleft = self.position

        self.edge_kill()


# ============================================================= 
# ============================================================= 
        

class Manager():
    """Manages the game"""
    def __init__(self):
        pg.init()
        # self.screen = pg.display.set_mode((cng.SCREEN_X, cng.SCREEN_Y))
        self.clock = pg.time.Clock()

        # Load the simulation background and use it
        self.background = pg.image.load(cng.BACKGROUND_IMAGE) 
        self.background = pg.transform.scale(self.background,(cng.SCREEN_X, cng.SCREEN_Y)) 
        self.background.convert()
        self.start_background = pg.image.load(cng.START_BACKGROUND) 
        self.start_background = pg.transform.scale(self.start_background,(cng.SCREEN_X, cng.SCREEN_Y)) 
        self.start_background.convert()
        self.end_background = pg.image.load(cng.END_BACKGROUND) 
        self.end_background = pg.transform.scale(self.end_background,(cng.SCREEN_X, cng.SCREEN_Y)) 
        self.end_background.convert()

        # Load images
        self.player1_img = pg.image.load(cng.SHIP_PLAYER1_IMAGE).convert_alpha() 
        self.player1_img = pg.transform.scale(self.player1_img,(self.player1_img.get_width(), self.player1_img.get_height()))
        self.player2_img = pg.image.load(cng.SHIP_PLAYER2_IMAGE).convert_alpha() 
        self.player2_img = pg.transform.scale(self.player2_img,(self.player2_img.get_width(), self.player2_img.get_height()))
        self.obstacle_img = pg.image.load(cng.OBSTACLE_IMAGE).convert_alpha() 
        self.obstacle_img = pg.transform.scale(self.obstacle_img,(self.obstacle_img.get_width(), self.obstacle_img.get_height()))
        self.bullet_img = pg.image.load(cng.BULLET_IMAGE).convert_alpha() 
        self.bullet_img = pg.transform.scale(self.bullet_img,(self.bullet_img.get_width()/15, self.bullet_img.get_height()/15))
        self.fuel_img = pg.image.load(cng.FUEL_IMAGE).convert_alpha() 
        self.fuel_img = pg.transform.scale(self.fuel_img,(self.fuel_img.get_width(), self.fuel_img.get_height()))
        

        self.game = "starting"     # Game starts on start screen

        
        # Keeps track of player's wins
        self.player1_wins = 0
        self.player2_wins = 0
        self.player1_won = False
        self.player2_won = False
        self.player1_score = 0
        self.player2_score = 0

        # Flags used to make sound only play once
        self.crash_sound_playing_1 = False
        self.crash_sound_playing_2 = False

        
        
        # Scales and converts poof images, and adds them to the poof_images list
        self.poof_images = []
        self.poof_filenames = [cng.I0, cng.I1, cng.I2, cng.I3, cng.I4, cng.I5, cng.I6, cng.I7
        , cng.I8, cng.I9, cng.I10, cng.I11, cng.I12, cng.I13, cng.I14, cng.I15, cng.I16, cng.I17
        , cng.I18, cng.I19, cng.I20, cng.I21, cng.I22, cng.I23, cng.I24, cng.I25, cng.I26, cng.I27
        , cng.I28, cng.I29]

        for filename in self.poof_filenames:
            image = pg.image.load(filename).convert_alpha()
            image = pg.transform.scale(image,(image.get_width(), image.get_height()))
            self.poof_images.append(image)


        self.play_music() 
        self.sprites_init()
        self.poofs_init()
        self.loop()


# ============================================================= 
        
    def poofs_init(self):
        """Initialize the timers and flags for poof images"""

        self.current_image_index1 = -1
        self.timer1 = 0
        self.interval1 = cng.INTERVAL       # Number of milliseconds before shifting poof image
        self.finished_poofing1 = False
        self.player1_wins_incremented = False

                    
        self.current_image_index2 = -1
        self.timer2 = 0
        self.interval2 = cng.INTERVAL       # Number of milliseconds before shifting poof image
        self.finished_poofing2 = False
        self.player2_wins_incremented = False

# ============================================================= 
        
    def loop(self):
        """Main loop for manager. Checks the event for exit strategy, and
           updates all the objects""" 
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()

            #--------------START-SCREEN---------------------------
                    
            # Startscreen
            if self.game == "starting":
                screen.blit(self.start_background, (0,0))
                pg.display.update() 

                # Start simulation when space button is pressed
                key = pg.key.get_pressed()
                if key[pg.K_SPACE]:
                    pg.time.delay(500) #Delay game screen to make transition smooth
                    self.game = "on"
            
            #--------------GAME-SCREEN----------------------------
                    
            # The game starts
            if self.game == "on":

                # If player 1 is dead, start poof animation
                if len(self.player1_group) == 0 and self.finished_poofing1 == False:
                    self.play_crash_sound_p1()
                    self.timer1 += self.clock.get_time()    # Update timer
                    if self.current_image_index1 < len(self.poof_images) -1:    # Make sure not to exceed maximum index
                        if self.timer1 >= self.interval1:   # Checks if it is time to change poof image                    
                            self.current_image_index1 += 1
                            self.timer1 = 0                 # Resets timer for next image
                    if self.current_image_index1 == len(self.poof_images) -1:   # End animating if at the last image
                        self.finished_poofing1 = True
                    
                    # If player 1 is dead, but 2 is alive, player 2 wins this round
                    if len(self.player2_group) != 0 and self.player2_wins_incremented == False:
                        self.player2_wins += 1
                        self.player1.score -= 2*cng.SCOREPOINT    # Player 1 looses score if they die
                        self.player2_won = True
                        self.player2_wins_incremented = True
                
                #-----------------------------------------------------
                        
                # If player 2 is dead, start poof animation
                if len(self.player2_group) == 0 and self.finished_poofing2 == False:
                    self.play_crash_sound_p2()
                    self.timer2 += self.clock.get_time()    # Update timer
                    if self.current_image_index2 < len(self.poof_images) -1:     # Make sure not to exceed maximum index
                        if self.timer2 >= self.interval2:   # Checks if it is time to change poof image
                            self.current_image_index2 += 1
                            self.timer2 = 0                 # Resets timer for next image
                    if self.current_image_index2 == len(self.poof_images) -1:   # End animating if at the last image
                        self.finished_poofing2 = True
                    
                    # If player 2 is dead, but 1 is alive, player 1 wins this round
                    if len(self.player1_group) != 0 and self.player1_wins_incremented == False:
                        self.player1_wins += 1
                        self.player2.score -= 2*cng.SCOREPOINT    # Player 2 looses score if they die
                        self.player1_won = True
                        self.player1_wins_incremented = True
                        
                #-----------------------------------------------------

                # Start end screen when one of the players are dead and poof animation is done
                if len(self.player1_group) == 0 or len(self.player2_group) == 0: 
                    if self.finished_poofing1 or self.finished_poofing2:
                        pg.time.delay(300) # Delay end screen to make transition smooth
                        
                        # Scores each round are added to a total score
                        self.player1_score += self.player1.score
                        self.player2_score += self.player2.score
                        self.game = "ending"

                self.update()
                self.clock.tick(60)  # Frames per second


            #----------------END-SCREEN---------------------------
                
            if self.game == "ending":
                self.end_screen()

                # Restart game
                key = pg.key.get_pressed()
                if key[pg.K_SPACE]:
                    pg.time.delay(800) #Delay start to make transition smooth

                    # Need to reset the sprites so a new, fresh game can start
                    self.player1_won = False
                    self.player2_won = False
                    self.player1_wins_incremented = False
                    self.player2_wins_incremented = False
                    self.crash_sound_playing_1 = False
                    self.crash_sound_playing_2 = False
                    self.sprites_init()
                    self.poofs_init()
                    self.game = "on"


# ============================================================= 
                    
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

        self.obstacle_group = pg.sprite.Group()
        self.obstacle_group.add(Obstacle(self.obstacle_img))

        self.fuel_group = pg.sprite.Group()
        self.fuel_group.add(FuelSpot(self.fuel_img, cng.SCREEN_X/4, cng.SCREEN_Y-cng.BORDER*1.42))
        self.fuel_group.add(FuelSpot(self.fuel_img, cng.SCREEN_X*3/4, cng.SCREEN_Y-cng.BORDER*1.42))

# ============================================================= 
        
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

        self.obstacle_group.draw(screen)
        self.obstacle_group.update()

        self.fuel_group.draw(screen)
        self.fuel_group.update()


        #--------------POOF-IMAGES----------------------------

        # Draws current poof image
        if len(self.player1_group) == 0:
            self.curr_poof_img1 = self.poof_images[self.current_image_index1]
            poof_x1 = self.player1.rect.x-(self.curr_poof_img1.get_width()*0.35)
            poof_y1 = self.player1.rect.y-(self.curr_poof_img1.get_height()*0.35)
            screen.blit(self.curr_poof_img1, (poof_x1, poof_y1))
        
        if len(self.player2_group) == 0:
            self.curr_poof_img2 = self.poof_images[self.current_image_index2]
            poof_x2 = self.player2.rect.x-(self.curr_poof_img2.get_width()*0.35)
            poof_y2 = self.player2.rect.y-(self.curr_poof_img2.get_height()*0.35)
            screen.blit(self.poof_images[self.current_image_index2], (poof_x2, poof_y2))
        
        #--------------COLLISIONS-----------------------------
            
        # Check for Collisions
        if pg.sprite.groupcollide(self.player1_group, self.player2_group, False, False):
            self.player1.health += cng.HITPOINT/10 
            self.player2.health += cng.HITPOINT/10
            print("CRASH COURSE DELIGHT")
        
        if pg.sprite.groupcollide(self.player1_group, self.p2_bullet_group, False, True):
            self.player1.got_shot(self.player2)

            print("Player1 HP:", self.player1.health, "\t Player2 HP:", self.player2.health)
            print("Player1 SCORE:", self.player1.score, "\t Player2 SCORE:", self.player2.score)
            
        
        if pg.sprite.groupcollide(self.player2_group, self.p1_bullet_group, False, True):
            self.player2.got_shot(self.player1)

            print("Player1 HP:", self.player1.health, "\t Player2 HP:", self.player2.health)
            print("Player1 SCORE:", self.player1.score, "\t Player2 SCORE:", self.player2.score)


        if pg.sprite.groupcollide(self.obstacle_group, self.player1_group, False, True):
            print("ALIEN DINNER: PLAYER1's ON THE MENU!")
        if pg.sprite.groupcollide(self.obstacle_group, self.player2_group, False, True):
            print("ALIEN PLAYGROUND: PLAYER2 MEETS DOOM!")
        
        #If the ships touch the fuel can, they get refueled
        if pg.sprite.groupcollide(self.player1_group, self.fuel_group, False, False):
            if self.player1.fuel < cng.FUELLIMIT:
                self.player1.fuel += cng.FUELUSE
            print("PLAYER1 REFUELED, READY FOR LIFTOFF!")
        if pg.sprite.groupcollide(self.player2_group, self.fuel_group, False, False):
            if self.player2.fuel < cng.FUELLIMIT:
                self.player2.fuel += cng.FUELUSE
            print("PLAYER2 FUELLED UP, SKYWARD BOUND!")


        self.text()
        pg.display.flip()

# ============================================================= 

    def end_screen(self):
        """ Creates the end screen"""

        # Create the background and create the fonts
        screen.blit(self.end_background, (0,0))  
        font1 = pg.font.SysFont('arial', 50)
        
        
        # Create the text in the correct font
        playerONE = font1.render('PLAYER 1', True, (255, 255, 255))
        scoreONE = font1.render('SCORE: ' +str(self.player1_score), True, (100, 100, 100))
        healthONE = font1.render('HEALTH: '+ str(self.player1.health), True, (100, 100, 100))

        playerTWO = font1.render('PLAYER 2', True, (255, 255, 255))
        scoreTWO = font1.render('SCORE: ' + str(self.player2_score), True, (100, 100, 100))
        healthTWO = font1.render('HEALTH: '+ str(self.player2.health), True, (100, 100, 100))

        playerONEwon = font1.render('PLAYER 1 REIGNS SUPREME!', True, (255, 255, 255))
        playerTWOwon = font1.render('PLAYER 2 DOMINATES THE SKIES!', True, (255, 255, 255))

        winner_score1 = font1.render('WINS: ' + str(self.player1_wins), True, (100, 100, 100))
        winner_score2 = font1.render('WINS: ' + str(self.player2_wins), True, (100, 100, 100))


        # Print the text
        screen.blit(playerONE, (45, cng.SCREEN_Y/3 + playerONE.get_height()))
        screen.blit(scoreONE, (45, cng.SCREEN_Y/3 + 2*scoreONE.get_height()))
        screen.blit(healthONE, (45, cng.SCREEN_Y/3 + 3*healthONE.get_height()))

        screen.blit(playerTWO, (cng.SCREEN_X-playerTWO.get_width()-45, cng.SCREEN_Y/3 + playerTWO.get_height()))
        screen.blit(scoreTWO, (cng.SCREEN_X-scoreTWO.get_width()-45, cng.SCREEN_Y/3 + 2*scoreTWO.get_height()))
        screen.blit(healthTWO, (cng.SCREEN_X-healthTWO.get_width()-45, cng.SCREEN_Y/3 + 3*healthTWO.get_height()))

        #-----------------------------------------------------

        #Print winner
        if self.player1_won:
            screen.blit(playerONEwon, (cng.SCREEN_X/2-playerONEwon.get_width()/2, cng.SCREEN_Y/3 + 0.5*playerONEwon.get_height()))
        if self.player2_won:
            screen.blit(playerTWOwon, (cng.SCREEN_X/2-playerTWOwon.get_width()/2, cng.SCREEN_Y/3 +  0.5*playerTWOwon.get_height()))

        screen.blit(winner_score1, (45, cng.SCREEN_Y/3 + 4*winner_score1.get_height()))
        screen.blit(winner_score2, (cng.SCREEN_X-winner_score2.get_width()-45, cng.SCREEN_Y/3 + 4*winner_score2.get_height()))

        pg.display.update()        

# ============================================================= 
        
    def text(self):
        """Prints text on screen"""
        font = pg.font.SysFont('arial', 20)

        player1_txt = font.render('PLAYER 1', True, (255, 255, 255))    
        score_player1 = font.render('SCORE: ' + str(self.player1.score), True, (255, 255, 255))
        fuel_player1 = font.render('FUEL: ' + str(self.player1.fuel), True, (255, 255, 255))
        health_player1 = font.render('HEALTH: '+ str(self.player1.health), True, (255, 255, 255))

        player2_txt = font.render('PLAYER 2', True, (255, 255, 255))
        score_player2 = font.render('SCORE: ' + (str(self.player2.score)), True, (255, 255, 255))
        fuel_player2 = font.render('FUEL: ' + str(self.player2.fuel), True, (255, 255, 255))
        health_player2 = font.render('HEALTH: '+ str(self.player2.health), True, (255, 255, 255))

        winner_score1 = font.render('WINS: ' + str(self.player1_wins), True, (255, 255, 255))
        winner_score2 = font.render('WINS: ' + str(self.player2_wins), True, (255, 255, 255))

        screen.blit(player1_txt, (15, cng.SCREEN_Y - 5*player1_txt.get_height()))
        screen.blit(score_player1, (15, cng.SCREEN_Y - 2*score_player1.get_height()))
        screen.blit(fuel_player1, (15, cng.SCREEN_Y - 3*fuel_player1.get_height()))
        screen.blit(health_player1, (15, cng.SCREEN_Y - 4*health_player1.get_height()))
        screen.blit(winner_score1, (15, cng.SCREEN_Y - winner_score1.get_height()))
                    
        screen.blit(player2_txt, (cng.SCREEN_X - player2_txt.get_width()-15, cng.SCREEN_Y - 5*player2_txt.get_height()))
        screen.blit(score_player2, (cng.SCREEN_X - score_player2.get_width()-15, cng.SCREEN_Y - 2*score_player2.get_height()))
        screen.blit(fuel_player2, (cng.SCREEN_X - fuel_player2.get_width()-15, cng.SCREEN_Y - 3*fuel_player2.get_height()))
        screen.blit(health_player2, (cng.SCREEN_X - health_player2.get_width()-15, cng.SCREEN_Y - 4*health_player2.get_height()))
        screen.blit(winner_score2, (cng.SCREEN_X - winner_score2.get_width()-15, cng.SCREEN_Y - winner_score2.get_height()))


# ============================================================= 
    
    def play_music(self):
        """Plays the music"""
        mixer.init()
        mixer.music.load((cng.MUSIC))
        mixer.music.set_volume(cng.VOLUME)
        mixer.music.play(0, 0, 0)
        pg.mixer.music.rewind() # Loops the music


        
    def play_crash_sound_p1(self):
        """Plays the crash sound when player 1 dies"""
        if not self.crash_sound_playing_1:
            crash_sound_1 = mixer.Sound(cng.CRASH_SOUND)
            crash_sound_1.set_volume(cng.VOLUME)
            crash_sound_1.play(0, 0, 0)
            self.crash_sound_playing_1 = True


            
    def play_crash_sound_p2(self):
        """Plays the crash sound when player 2 dies"""
        if not self.crash_sound_playing_2:
            crash_sound_2 = mixer.Sound(cng.CRASH_SOUND)
            crash_sound_2.set_volume(cng.VOLUME)
            crash_sound_2.play(0, 0, 0)
            self.crash_sound_playing_2 = True



if __name__ == "__main__":
    
    Manager()
    
