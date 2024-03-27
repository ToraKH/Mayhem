import pygame as pg


# Screen size
SCREEN_X = 1200
SCREEN_Y = 600

BORDER = 50

# Sprite images
SHIP_PLAYER1 = "spaceship_small_red.png"
SHIP_PLAYER2 = "spaceship_small_blue.png"
BACKGROUND = "cave.png"
OBSTACLE = "alien.png"
BULLET = "bullet.png"

# Motion controls
GRAVITY = pg.math.Vector2(0,1.4)
THRUST = 3.0
ROTATION_SPEED = 5.0

# Artillary controls
BULLET_SPEED = 5.0          #How fast the bullets fly
BULLET_COOL_DOWN = 200      #How quick bullet-set fire
BULLET_MAX = 3              #How many bullet per bullet-set

# Gas controls
FUELCOOLDOWN = 1    #Hvor lang tid det skal gå før ny fuel barrel kommer?????
FUELLIMIT = 100       #Størrelsen på tanken
FUELUSE = 50    #amount of fuel used

# Game controls
HEALTH = 250          #Max health
HITPOINT = -10
SCOREPOINT = 10