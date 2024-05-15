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



#Initialise screen display as a global variable
screen = pg.display.set_mode((cng.SCREEN_X, cng.SCREEN_Y))

class Object(pg.sprite.Sprite):
    """Represents the visible ovjects in the game"""
    def __init__(self, image):
        """ Initializes Objects''s attributes"""

        super().__init__()
        #Store corresponsing images and dimensions of the spite
        self.image = image                          
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        #Initialise empty position vector
        self.position = pg.math.Vector2(0,0)
        #Create rectangle around sprite based on its position
        self.rect = pg.rect.Rect(self.position.x, self.position.y, self.width, self.height)



# ============================================================= 
# ============================================================= 

class Obstacle(Object):
    """Represents the alien object in the game"""
    def __init__(self, image):
        """ Initializes Obstacle's attributes"""
        super().__init__(image)
        # Overwrite position to start at the random spot on the screen
        self.position = pg.math.Vector2(random.randint(cng.BORDER, cng.SCREEN_X-cng.BORDER), random.randint(cng.BORDER, cng.SCREEN_Y//2)) 
        #Update rectangle's position
        self.rect = pg.rect.Rect(self.position.x, self.position.y, self.width, self.height)
        self.speed_x = random.uniform(0.3, 1) #få tilfeldig tall mellom 0 og 1


    
    def update(self):
        """Make obstacle move fram og tilbake på skjermen"""
        self.position.x += self.speed_x #flytter seg en pixel bortover
        self.rect.x = self.position.x #det nye rektangelet sitt x  må opdateres til fiskens nye posisjon x
        
        # Sjekk om objektet har nådd kanten av skjermen og endre retning
        if self.position.x < 0 - self.image.get_width():  # Hvis objektet er utenfor venstre kant
            self.position.x = cng.SCREEN_X  # Flytt objektet til høyre kant
        elif self.position.x > cng.SCREEN_X:  # Hvis objektet er utenfor høyre kant
            self.position.x = 0 - self.image.get_width()  # Flytt objektet til venstre kant

# ============================================================= 
# =============================================================        

class FuelSpot(Object):    
    """Represents the fuel cans in the game""" 
    def __init__(self, image, x,y):
        """ Initializes FuelSpot's attributes"""
        super().__init__(image)
        #Overwrite position to start at the bottom of the screen
        self.position = pg.math.Vector2(x, y)
        #Update rectangle's position
        self.rect = pg.rect.Rect(self.position.x, self.position.y, self.width, self.height)


# ============================================================= 
# ============================================================= 


class SpaceShip(Object):
    """Represents a spaceship object in the game"""
    #---------------------------------------------------
    #Define nested class to be used by every Spaceship
    class Bullet(Object):
        """ Represents the bullets that space ships shoot"""
        def __init__(self, b_img, position, angle):
            """ Initializes Bullet' attributes"""
            super().__init__(b_img)
            #Overwrite position and rectangle based on given variables
            self.position = pg.math.Vector2(position)
            self.rect.center = self.position
            #Store angle for bullet's trajectory
            self.angle = angle

            ## Calculate the constant velocity vector based on its angle
            #Covert angle from degrees to radians
            angle_rad = math.radians(self.angle)
            #Use bullet's angle to create a directional vector
            direction = pg.math.Vector2(math.cos(angle_rad), -math.sin(angle_rad))
            #Adjust magnitude of final velocity vector based on bullet's assigned speed
            self.velocity = direction * cng.BULLET_SPEED


        def edge_kill(self):
            """ Terminates the bullet if it steps out-of-bounds"""
            #Kill bullet if either side of its rectange touches screen-border
            if (self.rect.right < 0 or self.rect.left > cng.SCREEN_X
                or self.rect.bottom < 0 or self.rect.top > cng.SCREEN_Y):
                self.kill()


        def update(self):
            """ Updates position of the bullet"""
            #Update position and rectange based on velocity
            self.position += self.velocity
            self.rect.center = self.position

            #Check if bullet has gone out-of-bounds
            self.edge_kill()
            
            #Draw bullet directly to the screen
            screen.blit(self.image, self.rect)

    #-----------------------------------------------------    
    #Proceed with methods related to the Spaceship Class
    def __init__(self, image):
        """ Initializes Spaceship attributes"""
        super().__init__(image)
        #Initialise game stats based on value from configuration-file
        self.fuel = cng.FUELLIMIT
        self.score = 0
        self.health = cng.HEALTH
        #Initialise zero velocity vector 
        self.velocity = pg.math.Vector2(0,0)

        #Initialise angle so that the spaceship faces upwards
        self.angle = 90

        #Initialise empty bullet counter & timer
        self.bullet_count = 0
        self.last_shot_time = 0


#-------------POSITION-CONTROL------------------------

    def rotate_right(self):
        """ Rotates the ship to the right"""
        #Decrease sprite's angle to turn right
        self.angle -= cng.ROTATION_SPEED
        

    def rotate_left(self):
        """ Rotates the ship to the left"""
        #Increase sprite's angle to turn left
        self.angle += cng.ROTATION_SPEED
        

    def thrust(self):
        """ The ship moves forward"""
        # Calculate the constant velocity vector based on its angle
        angl_rad = math.radians(self.angle)
        direction = pg.math.Vector2(math.cos(angl_rad), -math.sin(angl_rad))
        #Adjust magnitude of final velocity based on spaceship's thrust power
        self.velocity +=  direction * cng.THRUST

        #Update fuel usage
        self.fuel -= cng.FUELUSE

    
    def gravity(self):
        """ Gravitational force to drag the ship downwards"""
        #Applies a downwards gavitational force if spaceship is above ground
        if self.rect.bottom < cng.SCREEN_Y-2:
            self.velocity.y += cng.GRAVITY

#--------------SOUND-EFFECTS--------------------------
    
    def shoot_sound(self):
        sound = mixer.Sound((cng.SHOOT_SOUND))
        #Adjust volume
        sound.set_volume(cng.SHOOT_VOLUME)
        #Play music from the beginning
        sound.play(0, 0, 0)    

#--------------ACTION-FUNCTIONS-----------------------

    def edge_kill(self):
        """ Kill ship if it crashes into edges"""

        #If ship crashes into the ground
        if self.rect.bottom > cng.SCREEN_Y:
            self.health = 0
            self.kill()

        #If ship crashes into the sky
        if self.rect.top < 0:
            self.health = 0
            self.kill()

        #If chrashed into left/right edges
        if self.rect.left < 0:
            self.health = 0
            self.kill()
        
        if self.rect.right > cng.SCREEN_X:
            self.health = 0
            self.kill()          


    def shoot(self, b_img, bullets):
        """ The ship shoots bullets"""
        #Get the 'time'
        current_time = pg.time.get_ticks()
        # Reset bullet count if cooldown has passed
        if (current_time - self.last_shot_time) > cng.BULLET_COOL_DOWN:
            self.bullet_count = 0
            self.shoot_sound()

        # Shoot if there are less than max_bullets bullets already shot
        if self.bullet_count < cng.BULLET_MAX:
            #Create another bullet
            bullet = SpaceShip.Bullet(b_img, self.rect.center, self.angle)
            bullets.add(bullet)
            self.bullet_count += 1
            #Update timer
            self.last_shot_time = current_time

        

    def got_shot(self, other): 
        """ Updates score and health when ship is hit by bullet"""
        #Decreases health of shot spaceship
        self.health += cng.HITPOINT
        #Increases score of shooter
        other.score += cng.SCOREPOINT


    def draw(self):
        """ Overwrites pygames draw function to rotate the image of the sprite"""
        #Rotate image by calculated angle 
        rotated_image = pg.transform.rotate(self.image, self.angle-90)
        #Rotate sprite's rectangle by same angle
        rotated_rect = rotated_image.get_rect(center=self.rect.center)
        
        #Draw updated sprite to screen
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
        self.position = pg.math.Vector2(random.randint(cng.BORDER+10,cng.SCREEN_X//2), cng.SCREEN_Y-(cng.BORDER*2.2))
        

    def update(self, b_img, p1_bullets):
        """Update the state of player 1"""

        #Reset velocity vector
        self.velocity = pg.math.Vector2(0,0)
        
        #Register pressed keys + complete correspond method
        key = pg.key.get_pressed()
        if key[pg.K_a]:
            self.rotate_left()
        if key[pg.K_d]:
            self.rotate_right()       
        if key[pg.K_LSHIFT]:
            self.shoot(b_img, p1_bullets)
        if key[pg.K_w] and self.fuel >= 0:
            self.thrust()
        else:
            #Will only apply gravity if spaceship is not in motion
            self.gravity()  

        #Update position based on current velocity
        self.position += self.velocity
        #Update rectangle
        self.rect.topleft = self.position

        #Check if spaceship has gone out-of-bounds
        self.edge_kill()

        #Check whether spaceship is dead
        if self.health <= 0:
            #Ensures that HP is not displayed as as a negative
            self.health = 0
            self.kill()

# ============================================================= 
# ============================================================= 
      

#BLUE SPACESHIP
class Player2(SpaceShip):
    """Represents Player 2's spaceship"""

    def __init__(self, image):
        """ Initializes Player2's attributes"""
        super().__init__(image)
        # Overwrite position to start at the bottom of the screen
        self.position = pg.math.Vector2(random.randint(cng.SCREEN_X//2, cng.SCREEN_X-cng.BORDER-10), cng.SCREEN_Y-(cng.BORDER*2.2))

    def update(self, b_img, p2_bullets):
        """Update the state of player 2"""
        #Reset velocity vector
        self.velocity = pg.math.Vector2(0,0)

        #Register pressed keys + complete correspond method
        key = pg.key.get_pressed()
        if key[pg.K_LEFT]:
            self.rotate_left()
        if key[pg.K_RIGHT]:
            self.rotate_right()
        if key[pg.K_RCTRL]:
            self.shoot(b_img, p2_bullets)
        if key[pg.K_UP] and self.fuel >= 0:
            self.thrust()
        else: 
            #Only apply gravity if spaceship is not in motion
            self.gravity()

        #Update position based on current velocity
        self.position += self.velocity
        #Update rectangle
        self.rect.topleft = self.position

        #Check if spaceship has gone out-of-bounds
        self.edge_kill()

        #Check whether spaceship is dead
        if self.health <= 0:
            #Ensures that HP is not displayed as as a negative
            self.health = 0
            self.kill()


# ============================================================= 
# ============================================================= 
class Button:
    def __init__(self, img, pos_x, pos_y):
        self.img = img
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = img.get_width()
        self.height = img.get_height()
        self.rect = pg.rect.Rect(self.pos_x, self.pos_y, self.width, self.height)
    
    def show(self,):
        """ Show buttons on screen"""
        screen.blit(self.img, (self.pos_x, self.pos_y))
    
    
    def check_for_event(self):
        """Checks whether player has interacted"""      
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                if self.pos_x <= mouse_pos[0] <= self.pos_x+self.width and self.pos_y <= mouse_pos[1] <= self.pos_y+self.height:
                    print("PRESSED ON BUTTON")
                    return True
                else:
                    return False
      
# ============================================================= 
# ============================================================= 

class Manager():
    """Manages the game"""
    def __init__(self):
        #Start pygame
        pg.init()
        #Initialise clock for frame-rate
        self.clock = pg.time.Clock()

        #Start game status
        self.game = "starting"

        #Initialise player total scores
        self.p1_total_score = 0
        self.p2_total_score = 0

        #Initialise player total wins
        self.p1_total_wins = 0
        self.p2_total_wins = 0

        #Boolean to control which player gets scores
        self.player1_won = False
        self.player2_won = False

        #Ensured that only one victory is counted for
        self.player1_wins_incremented = False
        self.player2_wins_incremented = False

        self.arena_list = []
        self.ships_list1 = []
        self.ships_list2 = []
        
        #Collect images for game
        self.load_images()


        #Assign the first images
        self.background = None 
        self.player1_img = None
        self.player2_img = None
        self.flagg = False
        self.obstacle_img = None


        #Start background music
        self.play_music() 
        #Create sprite groups
        # self.sprites_init()
        #Create timers + flags for poof images
        self.poofs_init()
        #Run simulation loop
        self.loop()

    
    def load_images(self):
        """Loads the images"""
        #Load and scale simulation background
        self.start_bg = pg.image.load(cng.START) 
        self.start_bg = pg.transform.scale(self.start_bg,(cng.SCREEN_X, cng.SCREEN_Y)) 
        self.start_bg.convert()
        self.end_bg = pg.image.load(cng.END) 
        self.end_bg = pg.transform.scale(self.end_bg,(cng.SCREEN_X, cng.SCREEN_Y)) 
        self.end_bg.convert()
        self.custom_bg = pg.image.load(cng.CUSTOMIZER) 
        self.custom_bg = pg.transform.scale(self.custom_bg,(cng.SCREEN_X, cng.SCREEN_Y)) 
        self.custom_bg.convert()


        # Arena backgrounds
        self.arena1_bg = pg.image.load(cng.ARENA1) 
        self.arena1_bg = pg.transform.scale(self.arena1_bg,(cng.SCREEN_X, cng.SCREEN_Y)) 
        self.arena1_bg.convert()
        self.arena2_bg = pg.image.load(cng.ARENA2) 
        self.arena2_bg = pg.transform.scale(self.arena2_bg,(cng.SCREEN_X, cng.SCREEN_Y)) 
        self.arena2_bg.convert()
        self.arena3_bg = pg.image.load(cng.ARENA3) 
        self.arena3_bg = pg.transform.scale(self.arena3_bg,(cng.SCREEN_X, cng.SCREEN_Y)) 
        self.arena3_bg.convert()


        # Load arena background photos
        self.arena1_pic = pg.image.load(cng.ARENA_IMG1).convert_alpha()  
        self.arena1_pic = pg.transform.scale(self.arena1_pic,(self.arena1_pic.get_width()/12, self.arena1_pic.get_height()/12)) 
        self.arena_list.append(self.arena1_pic)
        self.arena2_pic= pg.image.load(cng.ARENA_IMG2).convert_alpha()  
        self.arena2_pic= pg.transform.scale(self.arena2_pic,(self.arena2_pic.get_width()/12, self.arena2_pic.get_height()/12)) 
        self.arena_list.append(self.arena2_pic)
        self.arena3_pic = pg.image.load(cng.ARENA_IMG3).convert_alpha()  
        self.arena3_pic = pg.transform.scale(self.arena3_pic,(self.arena3_pic.get_width()/12, self.arena3_pic.get_height()/12)) 
        self.arena_list.append(self.arena3_pic)


        # Load and scale buttons
        self.start_but_img = pg.image.load(cng.START_BUTTON).convert_alpha() 
        self.start_but_img = pg.transform.scale(self.start_but_img,(self.start_but_img.get_width()*cng.BUTTON_SIZE, self.start_but_img.get_height()*cng.BUTTON_SIZE))
        self.restart_but_img = pg.image.load(cng.RESTART_BUTTON).convert_alpha() 
        self.restart_but_img = pg.transform.scale(self.restart_but_img,(self.restart_but_img.get_width()*cng.BUTTON_SIZE, self.restart_but_img.get_height()*cng.BUTTON_SIZE))
        self.confirm_but_img = pg.image.load(cng.CONFIRM_BUTTON).convert_alpha() 
        self.confirm_but_img = pg.transform.scale(self.confirm_but_img,(self.confirm_but_img.get_width()*cng.BUTTON_SIZE, self.confirm_but_img.get_height()*cng.BUTTON_SIZE))
        self.choose_ship1_but_img = pg.image.load(cng.CHOOSE_SHIP1).convert_alpha() 
        self.choose_ship1_but_img = pg.transform.scale(self.choose_ship1_but_img,(self.choose_ship1_but_img.get_width()*cng.BUTTON_SIZE, self.choose_ship1_but_img.get_height()*cng.BUTTON_SIZE))
        self.choose_ship2_but_img = pg.image.load(cng.CHOOSE_SHIP2).convert_alpha() 
        self.choose_ship2_but_img = pg.transform.scale(self.choose_ship2_but_img,(self.choose_ship2_but_img.get_width()*cng.BUTTON_SIZE, self.choose_ship2_but_img.get_height()*cng.BUTTON_SIZE))
        self.choose_arena_but_img = pg.image.load(cng.CHOOSE_ARENA).convert_alpha() 
        self.choose_arena_but_img = pg.transform.scale(self.choose_arena_but_img,(self.choose_arena_but_img.get_width()*cng.BUTTON_SIZE, self.choose_arena_but_img.get_height()*cng.BUTTON_SIZE))
        self.r_arr_but_img = pg.image.load(cng.RIGHT_ARROW).convert_alpha() 
        self.r_arr_but_img = pg.transform.scale(self.r_arr_but_img,(self.r_arr_but_img.get_width()*cng.BUTTON_SIZE, self.r_arr_but_img.get_height()*cng.BUTTON_SIZE))
        self.l_arr_but_img = pg.image.load(cng.LEFT_ARROW).convert_alpha() 
        self.l_arr_but_img = pg.transform.scale(self.l_arr_but_img,(self.l_arr_but_img.get_width()*cng.BUTTON_SIZE, self.l_arr_but_img.get_height()*cng.BUTTON_SIZE))
        self.goto_start_but_img = pg.image.load(cng.GOTO_START).convert_alpha()
        self.goto_start_but_img = pg.transform.scale(self.goto_start_but_img,(self.goto_start_but_img.get_width()*cng.BUTTON_SIZE, self.goto_start_but_img.get_height()*cng.BUTTON_SIZE))
        self.credit_but_img = pg.image.load(cng.CREDIT).convert_alpha()
        self.credit_but_img = pg.transform.scale(self.credit_but_img,(self.credit_but_img.get_width()*cng.BUTTON_SIZE, self.credit_but_img.get_height()*cng.BUTTON_SIZE))
        
        # Load and scale sprite images
        self.ship1_img1 = pg.image.load(cng.SHIP_GRØNN).convert_alpha() 
        self.ship1_img1 = pg.transform.scale(self.ship1_img1,(self.ship1_img1.get_width(), self.ship1_img1.get_height()))
        self.ships_list1.append(self.ship1_img1)
        self.ship1_img2 = pg.image.load(cng.SHIP_SVART).convert_alpha() 
        self.ship1_img2 = pg.transform.scale(self.ship1_img2,(self.ship1_img2.get_width(), self.ship1_img2.get_height()))
        self.ships_list1.append(self.ship1_img2)
        self.ship1_img3 = pg.image.load(cng.SHIP_LYS_BLÅ).convert_alpha() 
        self.ship1_img3 = pg.transform.scale(self.ship1_img3,(self.ship1_img3.get_width(), self.ship1_img3.get_height()))
        self.ships_list1.append(self.ship1_img3)        
        self.ship1_img4 = pg.image.load(cng.SHIP_MØRK_BLÅ).convert_alpha() 
        self.ship1_img4 = pg.transform.scale(self.ship1_img4,(self.ship1_img4.get_width(), self.ship1_img4.get_height()))
        self.ships_list1.append(self.ship1_img4)
        self.ship1_img5 = pg.image.load(cng.SHIP_MØRK_GRØNN).convert_alpha() 
        self.ship1_img5 = pg.transform.scale(self.ship1_img5,(self.ship1_img5.get_width(), self.ship1_img5.get_height()))
        self.ships_list1.append(self.ship1_img5)
        self.ship1_img6 = pg.image.load(cng.SHIP_MULTI_CAVE).convert_alpha() 
        self.ship1_img6 = pg.transform.scale(self.ship1_img6,(self.ship1_img6.get_width(), self.ship1_img6.get_height()))
        self.ships_list1.append(self.ship1_img6)
        self.ship1_img7 = pg.image.load(cng.SHIP_MULTI_SPACE).convert_alpha() 
        self.ship1_img7 = pg.transform.scale(self.ship1_img7,(self.ship1_img7.get_width(), self.ship1_img7.get_height()))
        self.ships_list1.append(self.ship1_img7)


        self.ship2_img1 = pg.image.load(cng.SHIP_GUL).convert_alpha() 
        self.ship2_img1 = pg.transform.scale(self.ship2_img1,(self.ship2_img1.get_width(), self.ship2_img1.get_height()))
        self.ships_list2.append(self.ship2_img1)
        self.ship2_img2 = pg.image.load(cng.SHIP_ORANSJ).convert_alpha() 
        self.ship2_img2 = pg.transform.scale(self.ship2_img2,(self.ship2_img2.get_width(), self.ship2_img2.get_height()))
        self.ships_list2.append(self.ship2_img2)             
        self.ship2_img3 = pg.image.load(cng.SHIP_MULTI_LAVA).convert_alpha() 
        self.ship2_img3 = pg.transform.scale(self.ship2_img3,(self.ship2_img3.get_width(), self.ship2_img3.get_height()))
        self.ships_list2.append(self.ship2_img3)        
        self.ship2_img4 = pg.image.load(cng.SHIP_RØD).convert_alpha() 
        self.ship2_img4 = pg.transform.scale(self.ship2_img4,(self.ship2_img4.get_width(), self.ship2_img4.get_height()))
        self.ships_list2.append(self.ship2_img4)       
        self.ship2_img5 = pg.image.load(cng.SHIP_ROSA).convert_alpha() 
        self.ship2_img5 = pg.transform.scale(self.ship2_img5,(self.ship2_img5.get_width(), self.ship2_img5.get_height()))
        self.ships_list2.append(self.ship2_img5)        
        self.ship2_img6 = pg.image.load(cng.SHIP_LILLA).convert_alpha() 
        self.ship2_img6 = pg.transform.scale(self.ship2_img6,(self.ship2_img6.get_width(), self.ship2_img6.get_height()))
        self.ships_list2.append(self.ship2_img6)
        self.ship2_img7 = pg.image.load(cng.SHIP_MULTI_GUL).convert_alpha() 
        self.ship2_img7 = pg.transform.scale(self.ship2_img7,(self.ship2_img7.get_width(), self.ship2_img7.get_height()))
        self.ships_list2.append(self.ship2_img7)
       

        self.frames_obs_1 = pg.image.load(cng.OBSTACLE_ARENA1).convert_alpha()
        self.frames_obs_1 = pg.transform.scale(self.frames_obs_1,(self.frames_obs_1.get_width()*2, self.frames_obs_1.get_height()*2))
        self.frames_obs_2 = pg.image.load(cng.OBSTACLE_ARENA2).convert_alpha()
        self.frames_obs_2 = pg.transform.scale(self.frames_obs_2,(self.frames_obs_2.get_width()*1.5, self.frames_obs_2.get_height()*1.5))
        self.frames_obs_3 = pg.image.load(cng.OBSTACLE_ARENA3).convert_alpha()
        self.frames_obs_3 = pg.transform.scale(self.frames_obs_3,(self.frames_obs_3.get_width()/4, self.frames_obs_3.get_height()/4))

        
        self.bullet_img = pg.image.load(cng.BULLET_IMAGE).convert_alpha() 
        self.bullet_img = pg.transform.scale(self.bullet_img,(self.bullet_img.get_width()/15, self.bullet_img.get_height()/15))
        self.fuel_img = pg.image.load(cng.FUEL_IMAGE).convert_alpha() 
        self.fuel_img = pg.transform.scale(self.fuel_img,(self.fuel_img.get_width(), self.fuel_img.get_height()))

        #List of the poof images (in order)
        self.poof_filenames = [cng.I0, cng.I1, cng.I2, cng.I3, cng.I4, cng.I5, cng.I6, cng.I7
        , cng.I8, cng.I9, cng.I10, cng.I11, cng.I12, cng.I13, cng.I14, cng.I15, cng.I16, cng.I17
        , cng.I18, cng.I19, cng.I20, cng.I21, cng.I22, cng.I23, cng.I24, cng.I25, cng.I26, cng.I27
        , cng.I28, cng.I29]

        #Empty list for the scaled images
        self.poof_images = []

        #Load and convert each poof image accordinly
        for filename in self.poof_filenames:
            #Convert image to an alpha channel for rendering
            image = pg.image.load(filename).convert_alpha()
            #Add scaled images into the list
            self.poof_images.append(image)


# ============================================================= 
                    
    def sprites_init(self):
        """Initializes objects, and groups them"""
        #Create Players and fill in Player-groups
        self.player1 = Player1(self.player1_img)
        self.player1_group = pg.sprite.Group()
        self.player1_group.add(self.player1)

        self.player2 = Player2(self.player2_img)
        self.player2_group = pg.sprite.Group()
        self.player2_group.add(self.player2)


        #Create group for players bullets
        self.p1_bullet_group = pg.sprite.Group()
        self.p2_bullet_group = pg.sprite.Group()

        #Create group for obstacles and fill in group
        self.obstacle_group = pg.sprite.Group()
        for _ in range(cng.OBSTACLES):
            self.obstacle_group.add(Obstacle(self.obstacle_img))

        #Create fuel-group and fill in group
        self.fuel_group = pg.sprite.Group()
        self.fuel_group.add(FuelSpot(self.fuel_img, cng.SCREEN_X/4, cng.SCREEN_Y-3-self.fuel_img.get_height()))
        self.fuel_group.add(FuelSpot(self.fuel_img, cng.SCREEN_X*3/4, cng.SCREEN_Y-3-self.fuel_img.get_height()))
        

# ============================================================= 
        
    def poofs_init(self):
        """Initialize the timers and flags for poof images"""
        #Index-variables to blit images in order
        self.current_image_index1 = -1
        self.current_image_index2 = -1
        
        #Timers to space out animation
        self.timer1 = 0
        self.timer2 = 0
        
        #Number of milliseconds before shifting poof-image
        self.interval1 = cng.INTERVAL
        self.interval2 = cng.INTERVAL
        
        #Flags for when to stop animating
        self.finished_poofing1 = False
        self.finished_poofing2 = False

        # Flags used to make sound only play once
        self.crash_sound_playing_1 = False
        self.crash_sound_playing_2 = False


# ============================================================= 
        
    def loop(self):
        """Main loop for manager. Checks the event for exit strategy, and
           updates all the objects""" 
        #Infitite loop to keep simulation running
        while True:
            #Process events
            for event in pg.event.get():
                #Quits simulation if window gets closed
                if event.type == pg.QUIT:
                    exit()
            # key = pg.key.get_pressed()
            # if key[pg.K_HOME]:
            #     self.game = "choose_customisation"
                
            #--------------START-SCREEN--------------------------
                    
            # Startscreen
            if self.game == "starting":
                #Draw starting screen
                self.start_screen()

            #--------------GAME-SCREEN---------------------------
                    
            #Let the games begin...
            if self.game == "on":
                screen.blit(self.background, (0,0))  
                
                #Updates sprites
                self.update_sprites()
                self.game_screen()
                #Maintains 60 frames per second
                self.clock.tick(60)

            #--------------CUSTOMIZE-SCREEN-----------------------
            if self.game == "choose_customisation":
                #print("PRØVER Å CUSTOMISERE her")
                self.choose_custom_screen()

            if self.game == "choose_ship1":
                self.choose_ship1()
                
                
            
            if self.game == "choose_ship2":
                self.choose_ship2()
                
                
            
            if self.game == "choose_arena":
                self.choose_arena()
            #----------------END-SCREEN----------------------------
            #Game Over...
            if self.game == "ending":
                #Call method to open end screen
                self.end_screen()

            if self.game == "credits":
                self.show_credit()


                    

# ============================================================= 
        
    def update_sprites(self):
        """Updates all objects through sprite's group update"""

        #Draw players to screen
        for player in self.player1_group:
            player.draw()

        for player in self.player2_group:
            player.draw()


        #Update Groups
        self.obstacle_group.draw(screen)
        self.obstacle_group.update()

        self.fuel_group.draw(screen)
        self.fuel_group.update()
        
        self.player1_group.update(self.bullet_img, self.p1_bullet_group)
        self.player2_group.update(self.bullet_img, self.p2_bullet_group)
        
        #Update bullets only if they have been shot
        if self.p1_bullet_group is not None:
            for bullet in self.p1_bullet_group:
                bullet.update()
                
        if self.p2_bullet_group is not None:
            for bullet in self.p2_bullet_group:
                bullet.update()

        #--------------POOF-IMAGES----------------------------

        # Draw poof images if player is no longer in group (aka dead)
        if len(self.player1_group) == 0:
            #Collect poof-images list
            self.curr_poof_img1 = self.poof_images[self.current_image_index1]
            #Get dead player's position
            poof_x1 = self.player1.rect.x-(self.curr_poof_img1.get_width()*0.35)
            poof_y1 = self.player1.rect.y-(self.curr_poof_img1.get_height()*0.35)
            #Draw images at player's position
            screen.blit(self.curr_poof_img1, (poof_x1, poof_y1))
        
        if len(self.player2_group) == 0:
            #Collect poof-images list
            self.curr_poof_img2 = self.poof_images[self.current_image_index2]
            #Get dead player's position
            poof_x2 = self.player2.rect.x-(self.curr_poof_img2.get_width()*0.35)
            poof_y2 = self.player2.rect.y-(self.curr_poof_img2.get_height()*0.35)
            #Draw images at player's position
            screen.blit(self.curr_poof_img2, (poof_x2, poof_y2))
        
        #--------------COLLISIONS-----------------------------
            
        # Check for Collisions between players
        if pg.sprite.groupcollide(self.player1_group, self.player2_group, False, False):
            self.player1.health += cng.HITPOINT/10 
            self.player2.health += cng.HITPOINT/10
        
        #Check for collision between player and bullet
        if pg.sprite.groupcollide(self.player1_group, self.p2_bullet_group, False, True):
            self.player1.got_shot(self.player2)
        if pg.sprite.groupcollide(self.player2_group, self.p1_bullet_group, False, True):
            self.player2.got_shot(self.player1)

        #Check for collusion between player and obstacle
        pg.sprite.groupcollide(self.obstacle_group, self.player1_group, False, True)
        pg.sprite.groupcollide(self.obstacle_group, self.player2_group, False, True)
        
        #If players touch the fuel-can, fuel-stat goes up
        if pg.sprite.groupcollide(self.player1_group, self.fuel_group, False, False):
            if self.player1.fuel < cng.FUELLIMIT:
                self.player1.fuel += cng.FUELUSE
        if pg.sprite.groupcollide(self.player2_group, self.fuel_group, False, False):
            if self.player2.fuel < cng.FUELLIMIT:
                self.player2.fuel += cng.FUELUSE

        #Print on-screen game-stats
        self.text()
        pg.display.flip()

# ============================================================= 

    def end_screen(self):
        """ Creates the end screen"""

        #Create the background and create the fonts
        screen.blit(self.end_bg, (0,0))  
        font1 = pg.font.SysFont('arial', 50)
        
        
        #Create text in the correct font
        playerONE = font1.render('PLAYER 1', True, (255, 255, 255))
        scoreONE = font1.render('SCORE: ' +str(self.p1_total_score), True, (255, 255, 255))
        healthONE = font1.render('HEALTH: '+ str(self.player1.health), True, (255, 255, 255))

        playerTWO = font1.render('PLAYER 2', True, (255, 255, 255))
        scoreTWO = font1.render('SCORE: ' + str(self.p2_total_score), True, (255, 255, 255))
        healthTWO = font1.render('HEALTH: '+ str(self.player2.health), True, (255, 255, 255))

        playerONEwon = font1.render('PLAYER 1 REIGNS SUPREME!', True, (255, 255, 255))
        playerTWOwon = font1.render('PLAYER 2 DOMINATES THE SKIES!', True, (255, 255, 255))

        winner_score1 = font1.render('WINS: ' + str(self.p1_total_wins), True, (255, 255, 255))
        winner_score2 = font1.render('WINS: ' + str(self.p2_total_wins), True, (255, 255, 255))


        #Print text at correct place of the screen
        screen.blit(playerONE, (45, cng.SCREEN_Y/3 + playerONE.get_height()))
        screen.blit(scoreONE, (45, cng.SCREEN_Y/3 + 2*scoreONE.get_height()))
        screen.blit(healthONE, (45, cng.SCREEN_Y/3 + 3*healthONE.get_height()))

        screen.blit(playerTWO, (cng.SCREEN_X-playerTWO.get_width()-45, cng.SCREEN_Y/3 + playerTWO.get_height()))
        screen.blit(scoreTWO, (cng.SCREEN_X-scoreTWO.get_width()-45, cng.SCREEN_Y/3 + 2*scoreTWO.get_height()))
        screen.blit(healthTWO, (cng.SCREEN_X-healthTWO.get_width()-45, cng.SCREEN_Y/3 + 3*healthTWO.get_height()))

        #-----------------------------------------------------

        #Print winner
        if self.player1_won:
            screen.blit(playerONEwon, ((cng.SCREEN_X-playerONEwon.get_width())/2, cng.SCREEN_Y/3 + 0.5*playerONEwon.get_height()))
        if self.player2_won:
            screen.blit(playerTWOwon, ((cng.SCREEN_X-playerTWOwon.get_width())/2, cng.SCREEN_Y/3 +  0.5*playerTWOwon.get_height()))

        screen.blit(winner_score1, (45, cng.SCREEN_Y/3 + 4*winner_score1.get_height()))
        screen.blit(winner_score2, (cng.SCREEN_X-winner_score2.get_width()-45, cng.SCREEN_Y/3 + 4*winner_score2.get_height()))

      
        key = pg.key.get_pressed()


        restart_button = Button(self.restart_but_img, (cng.SCREEN_X-self.restart_but_img.get_width())/2,  3*self.restart_but_img.get_height())
        goto_start_button = Button(self.goto_start_but_img, (cng.SCREEN_X-self.goto_start_but_img.get_width())/2,  4*self.goto_start_but_img.get_height())   
        credit_button = Button(self.credit_but_img, (cng.SCREEN_X-self.credit_but_img.get_width())/2, 5*self.credit_but_img.get_height())
        restart_button.show()
        event = restart_button.check_for_event()

        # Start game if pressed on start button
        if event == True or key[pg.K_SPACE]:
            pg.time.delay(150)
            self.game = "on"    #start game
            self.player1_won = False
            self.player2_won = False
            self.player1_wins_incremented = False
            self.player2_wins_incremented = False
            self.crash_sound_playing_1 = False
            self.crash_sound_playing_2 = False
            self.sprites_init()
            self.poofs_init()

        goto_start_button.show()
        goto_start = goto_start_button.check_for_event()
        
        if goto_start == True or key[pg.K_g]:
            pg.time.delay(150)
            self.game = "choose_customisation"    #goto start
            #Reset sprite and game status for a new, fresh game
            self.player1_won = False
            self.player2_won = False
            self.player1_wins_incremented = False
            self.player2_wins_incremented = False
            self.crash_sound_playing_1 = False
            self.crash_sound_playing_2 = False
            self.sprites_init()
            self.poofs_init()
        
        credit_button.show()
        credit_button_press = credit_button.check_for_event()
        if credit_button_press == True or key[pg.K_ESCAPE]:
            pg.time.delay(150)
            self.game = "credits"


        
        pg.display.update() 
# ============================================================= 

    def game_screen(self):
        """Show the game screen"""
        #If player 1 is dead -> start poof animation
        if len(self.player1_group) == 0 and self.finished_poofing1 == False:
            self.play_crash_sound_p1()
            #Update timer
            self.timer1 += self.clock.get_time()
            #Check if it's time to change image
            if self.timer1 >= self.interval1:                  
                self.current_image_index1 += 1
                #Reset timer
                self.timer1 = 0
            #End animation if at last image
            if self.current_image_index1 == len(self.poof_images) -1:
                self.finished_poofing1 = True
            
            # If player 1 is dead, but 2 is alive -> player 2 wins this round
            if len(self.player2_group) != 0 and self.player2_wins_incremented == False:
                self.p2_total_wins += 1
                self.player2_won = True
                self.player2_wins_incremented = True
                #Loosing player gets a penalty if they die
                self.player1.score -= 2*cng.SCOREPOINT
        
        #-----------------------------------------------------
                
        # If player 2 is dead -> start poof animation
        if len(self.player2_group) == 0 and self.finished_poofing2 == False:
            self.play_crash_sound_p2()
            #Update timer
            self.timer2 += self.clock.get_time()
            #Check if it's time to change image
            if self.timer2 >= self.interval2:
                self.current_image_index2 += 1
                #Reset timer
                self.timer2 = 0
            #End animation if at last image
            if self.current_image_index2 == len(self.poof_images) -1:
                self.finished_poofing2 = True
            
            # If player 2 is dead, but 1 is alive -> player 1 wins this round
            if len(self.player1_group) != 0 and self.player1_wins_incremented == False:
                self.p1_total_wins += 1 
                self.player1_won = True
                self.player1_wins_incremented = True
                #Loosing player gets a penalty if they die
                self.player2.score -= 2*cng.SCOREPOINT
                
        #-----------------------------------------------------

        # Start end screen when one of the players is dead and poof animation is done
        if self.finished_poofing1 or self.finished_poofing2:
            #Delay end screen for smooth transition
            pg.time.delay(150)
            
            #Update total scores with last game scores
            self.p1_total_score += self.player1.score
            self.p2_total_score += self.player2.score
            
            #Update game status
            self.game = "ending"      
        # pg.display.update()   


# ============================================================= 
    def start_screen(self):
        """ Shows the start screen"""
        screen.blit(self.start_bg, (0,0)) 
        
        key = pg.key.get_pressed()

        start_button = Button(self.start_but_img, (cng.SCREEN_X-self.start_but_img.get_width())/2, cng.SCREEN_Y/3 + 3*self.start_but_img.get_height())
        
        start_button.show()
        event = start_button.check_for_event()

        # Start game if pressed on start button
        if event == True or key[pg.K_SPACE]:
            pg.time.delay(150)
            self.game = "choose_customisation"    #start game

        #-----------------------------------------------------
        
        # Blit text
        font1 = pg.font.SysFont('arial', 21)
        font2 = pg.font.SysFont('arial', 70)
        title = font2.render('COSMIC ADVENTURE', True, (255,255,255))
        created_by = font1.render('A game by Dulmini S. Gamage and Tora K. Homme', True, (255,255,255))
        screen.blit(title, ((cng.SCREEN_X-title.get_width())/2, cng.SCREEN_Y/2+45))
        screen.blit(created_by, ((cng.SCREEN_X-created_by.get_width())/2, cng.SCREEN_Y/2+47+title.get_height()))

        pg.display.update()    

# ============================================================= 

    def customize_pics(self, list, scale):
        """ Show pictures to choose from on screen"""
        print("yup")
        key = pg.key.get_pressed()
        right_arrow_button = Button(self.r_arr_but_img, (cng.SCREEN_X+2*self.r_arr_but_img.get_width())/2, cng.SCREEN_Y/2 + 5*self.r_arr_but_img.get_height())
        left_arrow_button = Button(self.l_arr_but_img, (cng.SCREEN_X-4*self.l_arr_but_img.get_width())/2, cng.SCREEN_Y/2 + 5*self.l_arr_but_img.get_height())
        right_arrow_button.show()
        
        left_arrow_button.show()
       
        run = True
        index = 0
        prev_r_arr_pressed = False  # Holder styr på om høyrepiltasten var nede i forrige iterasjon
        prev_l_arr_pressed = False  # Holder styr på om venstrepiltasten var nede i forrige iterasjon
        
        # Legg til en kort forsinkelse i millisekunder mellom hvert bildebytte
        delay = 200  # 200 ms = 0.2 sekunder

        while run:
            key = pg.key.get_pressed()
            image = list[index]
            if scale:
                scaled_image = pg.transform.scale(image, (image.get_width()*4, image.get_height()*4))
                image = scaled_image
                
            screen.blit(image, ((cng.SCREEN_X-image.get_width())/2, cng.SCREEN_Y/3 + 20))
            button = Button(self.confirm_but_img, (cng.SCREEN_X-self.confirm_but_img.get_width())/2, cng.SCREEN_Y- 1*self.confirm_but_img.get_height()-10)
            button.show()
            button_press = button.check_for_event()
            
            # Sjekk om høyrepiltasten nettopp ble trykket ned og ikke var nede i forrige iterasjon
            if not prev_r_arr_pressed or key[pg.K_a] or key[pg.K_RIGHT]:
                index = (index+1) % len(list)
                pg.time.delay(delay)  # Legg til en forsinkelse før neste bildebytte
            prev_r_arr_pressed = True  # Oppdater forrige tilstand av høyrepiltasten
            
            # Sjekk om venstrepiltasten nettopp ble trykket ned og ikke var nede i forrige iterasjon
            if not prev_l_arr_pressed or key[pg.K_s] or key[pg.K_LEFT]:
                index = (index-1) % len(list)
                pg.time.delay(delay)  # Legg til en forsinkelse før neste bildebytte
            prev_l_arr_pressed = True  # Oppdater forrige tilstand av venstrepiltasten
            
            if button_press == True or key[pg.K_SPACE]:
                pg.time.delay(150)
                run = False
            pg.display.update()
        
        return list[index]

        
    def choose_arena(self):
        """Screen for choosing an arena"""
        # Show text on screen
        screen.blit(self.custom_bg, (0,0)) 
        font = pg.font.SysFont('arial', 50)
        text = font.render('CHOOSE YOUR ARENA', True, (255, 255, 255))
        screen.blit(text, ((cng.SCREEN_X-text.get_width())/2,2* text.get_height()))
        self.background_pic = self.customize_pics(self.arena_list, False)
        if self.background_pic == self.arena1_pic:
            self.background = self.arena1_bg       
            self.obstacle_img = self.frames_obs_1
        if self.background_pic == self.arena2_pic:
            self.background = self.arena2_bg  
            self.obstacle_img = self.frames_obs_2    
        if self.background_pic == self.arena3_pic:
            self.background = self.arena3_bg
            self.obstacle_img = self.frames_obs_3
        self.game = "choose_customisation" 
        pg.display.update()
        

    def choose_ship1(self):
        """Screen for customizing a player"""
        screen.blit(self.custom_bg, (0,0)) 
        font = pg.font.SysFont('arial', 50)
        player = font.render(' CHOOSE AIRSHIP PLAYER 1', True, (255, 255, 255))
        screen.blit(player, ((cng.SCREEN_X-player.get_width())/2, 2*player.get_height()))
        self.player1_img = self.customize_pics(self.ships_list1, True)                              
        self.game = "choose_customisation"
        pg.time.delay(150)

    def choose_ship2(self):
        """Screen for customizing a player"""
        screen.blit(self.custom_bg, (0,0)) 
        font = pg.font.SysFont('arial', 50)
        player = font.render(' CHOOSE AIRSHIP PLAYER 2', True, (255, 255, 255))
        screen.blit(player, ((cng.SCREEN_X-player.get_width())/2, 2*player.get_height()))
        self.player2_img = self.customize_pics(self.ships_list2, True) 
        self.game = "choose_customisation"
        pg.time.delay(150)
 

    def choose_custom_screen(self):
        """Shows screen where one chooses if customize ship or arena"""
        screen.blit(self.custom_bg, (0,0)) 
        key = pg.key.get_pressed()
        
        choose_ship1_button = Button(self.choose_ship1_but_img, (cng.SCREEN_X-self.choose_ship1_but_img.get_width())/2, 3*self.choose_ship1_but_img.get_height())
        choose_ship2_button = Button(self.choose_ship2_but_img, (cng.SCREEN_X-self.choose_ship2_but_img.get_width())/2, 4*self.choose_ship2_but_img.get_height())
        choose_arena_button = Button(self.choose_arena_but_img, (cng.SCREEN_X-self.choose_arena_but_img.get_width())/2, 2*self.choose_arena_but_img.get_height())   
        choose_ship1_button.show()
        chose_ship1 = choose_ship1_button.check_for_event()
        choose_ship2_button.show()
        chose_ship2 = choose_ship2_button.check_for_event()
        choose_arena_button.show()
        chose_arena = choose_arena_button.check_for_event()
        
        start_but = Button(self.start_but_img, (cng.SCREEN_X-self.start_but_img.get_width())/2, self.start_but_img.get_height())
        
        if self.background and self.player1_img and self.player2_img: 
            start_but.show()
            self.flagg = True
        event_start_but = start_but.check_for_event()


        # Start game if pressed on start button
        if self.flagg == True and (event_start_but == True or key[pg.K_SPACE]):
            pg.time.delay(150)
            self.game = "on"    #start game
            self.sprites_init()
            self.flagg = False

        # Choose ships if pressed on choose ship button or S
        if chose_ship1 == True or key[pg.K_2]:
            pg.time.delay(150)
            self.game = "choose_ship1"

        if chose_ship2 == True or key[pg.K_3]:
            pg.time.delay(150)
            self.game = "choose_ship2"

        # Choose area if pressed on choose area button or A
        if chose_arena== True or key[pg.K_1]:
            pg.time.delay(150)
            self.game = "choose_arena"
        pg.display.update()   


# ============================================================= 
    def show_credit(self):
        screen.blit(self.end_bg, (0,0))
        font2 = pg.font.SysFont('arial', 50)
        font1 = pg.font.SysFont('arial', 21)
        
        #-----------------------------------------------------
        
        #Create text in the correct font
        credit_title = font2.render('CREDITS', True, (255, 255, 255))

        creators = font1.render('CREATORS', True, (255, 255, 255))
        game_devs = font1.render('Game developers: Tora K. Homme and Dulmini S. Gamage', True, (255, 255, 255))
        em_sup = font1.render('Emotional support to Tora: Sigurd A. Lorentzen', True, (255, 255, 255))

        images = font1.render('IMAGES', True, (255, 255, 255))
        bats = font1.render('Bats by SilverVoidArt' , True, (255, 255, 255))
        planets = font1.render('Planets by pixilart', True, (255, 255, 255))
        dragons = font1.render('Dragons by embea-icons', True, (255, 255, 255))
        spaceship = font1.render('Spaceships by dsonyy', True, (255, 255, 255))
        spaceship_col = font1.render('Spaceships colored by Tora', True, (255, 255, 255))
        background = font1.render('Backgrounds by upklyak', True, (255, 255, 255))
        poofs = font1.render('Poof images by jellyfizh ', True, (255, 255, 255))
        buttons = font1.render('Buttons by Tora', True, (255, 255, 255))
        bullets = font1.render('Bullets by Tora', True, (255, 255, 255))
        fuel_can = font1.render('Fuel can by Tora', True, (255, 255, 255))
        
        music = font1.render('MUSIC', True, (255, 255, 255))
        song = font1.render('Song by Dimitrii', True, (255, 255, 255))
        crash = font1.render('Crash sound by floraphonic', True, (255, 255, 255))
        shoot = font1.render('Shoot sound by Pixabay', True, (255, 255, 255))
        
        #-----------------------------------------------------

        #Print text at correct place of the screen
        screen.blit(credit_title, ((cng.SCREEN_X-credit_title.get_width())/2, 5))

        screen.blit(creators, ((cng.SCREEN_X-creators.get_width())/2, 3* creators.get_height()))
        screen.blit(game_devs, ((cng.SCREEN_X-game_devs.get_width())/2, 4*game_devs.get_height()))
        screen.blit(em_sup, ((cng.SCREEN_X-em_sup.get_width())/2, 5*em_sup.get_height()))

        screen.blit(images, ((cng.SCREEN_X-images.get_width())/2, 7*images.get_height()))
        screen.blit(bats, ((cng.SCREEN_X-bats.get_width())/2, 8*bats.get_height()))
        screen.blit(planets, ((cng.SCREEN_X-planets.get_width())/2, 9*planets.get_height()))
        screen.blit(dragons, ((cng.SCREEN_X-dragons.get_width())/2, 10*dragons.get_height()))
        screen.blit(spaceship, ((cng.SCREEN_X-spaceship.get_width())/2, 11*spaceship.get_height()))
        screen.blit(spaceship_col, ((cng.SCREEN_X-spaceship_col.get_width())/2, 12*spaceship_col.get_height()))
        screen.blit(background, ((cng.SCREEN_X-background.get_width())/2, 13*background.get_height()))
        screen.blit(poofs, ((cng.SCREEN_X-poofs.get_width())/2, 14*poofs.get_height()))
        screen.blit(buttons, ((cng.SCREEN_X-buttons.get_width())/2, 15*buttons.get_height()))
        screen.blit(bullets, ((cng.SCREEN_X-bullets.get_width())/2, 16*bullets.get_height()))
        screen.blit(fuel_can, ((cng.SCREEN_X-fuel_can.get_width())/2, 17*fuel_can.get_height()))
        
        screen.blit(music, ((cng.SCREEN_X-music.get_width())/2, 19*music.get_height()))
        screen.blit(song, ((cng.SCREEN_X-song.get_width())/2, 20*song.get_height()))
        screen.blit(crash, ((cng.SCREEN_X-crash.get_width())/2, 21*crash.get_height()))
        screen.blit(shoot, ((cng.SCREEN_X-shoot.get_width())/2, 22*shoot.get_height()))

        pg.display.update() 
        pg.time.delay(7000)
        # Exit game if pressed
        exit()



        

# =============================================================   
    def text(self):
        """Prints text on screen"""
        #Register chosen font + its size
        font = pg.font.SysFont('arial', 20)

        #Create text for game-stats
        player1_txt = font.render('PLAYER 1', True, (255, 255, 255))    
        score_player1 = font.render('SCORE: ' + str(self.player1.score), True, (255, 255, 255))
        fuel_player1 = font.render('FUEL: ' + str(self.player1.fuel), True, (255, 255, 255))
        health_player1 = font.render('HEALTH: '+ str(self.player1.health), True, (255, 255, 255))

        player2_txt = font.render('PLAYER 2', True, (255, 255, 255))
        score_player2 = font.render('SCORE: ' + (str(self.player2.score)), True, (255, 255, 255))
        fuel_player2 = font.render('FUEL: ' + str(self.player2.fuel), True, (255, 255, 255))
        health_player2 = font.render('HEALTH: '+ str(self.player2.health), True, (255, 255, 255))

        winner_score1 = font.render('WINS: ' + str(self.p1_total_wins), True, (255, 255, 255))
        winner_score2 = font.render('WINS: ' + str(self.p2_total_wins), True, (255, 255, 255))

        #Draw text to screen at correct place
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
        #Initialise pygame music mixer
        mixer.init()
        #Load chosen music-file
        mixer.music.load((cng.MUSIC))
        #Adjust volume
        mixer.music.set_volume(cng.VOLUME)
        #Play music from the beginning
        mixer.music.play(-1, 0, 0)


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
    #Run game manager
    Manager()
