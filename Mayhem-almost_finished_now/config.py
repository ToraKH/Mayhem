# Screen size
SCREEN_X = 1200
SCREEN_Y = 600
BORDER = 50

# Sprite images [retrieved from opengameart.org]
SHIP_PLAYER1_IMAGE = "images/spaceship_small_red.png" #Retrieved from  https://opengameart.org/content/pixel-spaceship
SHIP_PLAYER2_IMAGE = "images/spaceship_small_blue.png"   #Retrieved from  https://opengameart.org/content/pixel-spaceship 
BACKGROUND_IMAGE = "images/cave.png"


START_BACKGROUND = "images/cosmic_cavern.png"
END_BACKGROUND = "images/cosm_cav_restart.png"


OBSTACLE_IMAGE = "images/alien.png"  #Retrieved from https://www.vecteezy.com/png/19017599-an-8-bit-retro-styled-pixel-art-illustration-of-a-goblin 
BULLET_IMAGE = "images/bullet.png"
FUEL_IMAGE = "images/fuel_can.png"
POOF_IMAGE = "images/Poof.png" #Retrieved from https://opengameart.org/content/poof-effect-spritesheet 

# Motion controls
GRAVITY = 1.4
THRUST = 3.0
ROTATION_SPEED = 5.0

# Artillary controls
BULLET_SPEED = 5.0          #How fast the bullets fly
BULLET_COOL_DOWN = 200      #How quick bullets fire
BULLET_MAX = 3              #How many bullet per bullet-set

# Gas controls 
FUELLIMIT = 1000    # Size of fuel tank
FUELUSE = 1         # Amount of fuel used
REFUEL_RATE = 100   # Amount of fuel the ship gets when refueling

#Control number of obstacles
OBSTACLES = 2

# Game controls
HEALTH = 500          #Health at the beginning
HITPOINT = -10
SCOREPOINT = 10


# Music controls
"""MÅ VELGE EN AV DE, ELLER EN ANNEN"""
MUSIC = "sound/space1.mp3" # Music by Dmitrii Kolesnikov from Pixabay: https://pixabay.com/music/ambient-space-158081/ 
VOLUME = 0.25

CRASH_SOUND = "sound/epic_swoosh.mp3" #Sound Effect by floraphonic from Pixabay: https://pixabay.com/sound-effects/epic-swoosh-boom-1-183996/


# Poof images from https://opengameart.org/content/poof-effect-spritesheet
I0 = "poof_images/tile000.png"
I1 = "poof_images/tile001.png"
I2 = "poof_images/tile002.png"
I3 = "poof_images/tile003.png"
I4 = "poof_images/tile004.png"
I5 = "poof_images/tile005.png"
I6 = "poof_images/tile006.png"
I7 = "poof_images/tile007.png"
I8 = "poof_images/tile008.png"
I9 = "poof_images/tile009.png"
I10 = "poof_images/tile010.png"
I11 = "poof_images/tile011.png"
I12 = "poof_images/tile012.png"
I13 = "poof_images/tile013.png"
I14 = "poof_images/tile014.png"
I15 = "poof_images/tile015.png"
I16 = "poof_images/tile016.png"
I17 = "poof_images/tile017.png"
I18 = "poof_images/tile018.png"
I19 = "poof_images/tile019.png"
I20 = "poof_images/tile020.png"
I21 = "poof_images/tile021.png"
I22 = "poof_images/tile022.png"
I23 = "poof_images/tile023.png"
I24 = "poof_images/tile024.png"
I25 = "poof_images/tile025.png"
I26 = "poof_images/tile026.png"
I27 = "poof_images/tile027.png"
I28 = "poof_images/tile028.png"
I29 = "poof_images/tile029.png"

#0.07 seconds between shifting poof images
INTERVAL = 70