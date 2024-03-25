# Author: Sivert Steinholt
# Date: February 12, 2024
# Description: This Python file demonstrates a simple manager class for pygame.

import pygame
import config as cng
import random

class Object(pygame.sprite.Sprite):
    # Your implementation goes here
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.position = pygame.math.Vector2(random.randint(0,cng.SCREEN_X-cng.BORDER),random.randint(0,cng.SCREEN_Y-cng.BORDER) )
        self.rect = pygame.rect.Rect(self.position.x, self.position.y, self.width, self.height)


    
    def update(self):
        pass


class Obstacle(Object):
    def __init__(self):
        super().__init__(Manager().obstacle_img)




class Bullets(Object):
    
    def __init__(self):
        super().__init__(Manager().bullet_img)

    def update(self):
        pass


class FuelSpot(Object):
    def __init__(self):
        super().__init__()


    def refuel_ships(self):
        """If the ships lands on the platform, they get refueled"""
        if pygame.sprite.groupcollide(Manager().player2_group, Manager().fuel_group):
            Player2().fuel = cng.FUELLIMIT
        if pygame.sprite.groupcollide(Manager().player1_group, Manager().fuel_group):
            Player1().fuel = cng.FUELLIMIT
        




class SpaceShip(Object):
    
    def __init__(self, image):
        super().__init__(image)
        self.fuel = cng.FUELLIMIT
        self.score = 0
        self.health = cng.HEALTH   
        self.velocity = pygame.math.Vector2()

    def rotate_right(self):
        ''' Rotates the ship to the right'''
        pass

        

    def rotate_left(self):
        ''' Rotates the ship to the left'''
        pass


  
    def thrust(self):
        ''' The ship moves forward'''
        pass

    def shoot(self):
        ''' The ship shoots bullets'''
        pass
        
    
    def update_score(self, scorepoints):
        """Updates the score"""
        #hvis crasher, så går score ned
        #hvis man treffer motstander går score opp
        #hvis motstander dør av skuddet, går score masse opp
        self.score += scorepoints
        return self.score
        

    def crash(self):
        """Checks whether ship has crashed in walls or obstacles"""

        #Return true if ship crashed in the walls
        if self.rect.x > cng.SCREEN_X - cng.BORDER or self.rect.x < 0 + cng.BORDER:
            return True
        if self.rect.y > cng.SCREEN_Y - cng.BORDER or self.rect.y < 0 + cng.BORDER:
            return True
        
        #Return true if ships collided with 
        if pygame.sprite.groupcollide(Manager().player1_group, Manager().obstacle_group):
            return True
        if pygame.sprite.groupcollide(Manager().player2_group, Manager().obstacle_group):
            return True
        
    
    def crash_eachother():
        """Checks if ships have crashed in eachother"""
        if pygame.sprite.groupcollide(Manager().player1_group, Manager().player2_group):
            return True

        


    def got_shot(self): 
        """Checks whether ship got hit by bullet"""
        if pygame.sprite.groupcollide(self, Manager().bullet_group):
            return True
        


    def update_health(self, healthpoints):
        """Updates health"""
        self.health += healthpoints
        if self.health < 0:
            self.kill()
        #hvis man crasher går health ned
        #hvis man blir skutt går health ned
        #hvis man har null health så dør man
        return self.health

    def gravity(self):

        pass


    def update_health_and_score(self):

        #If crashed in walls or obstacles, then kill
        if self.crash:
            self.kill()
            
        
        # If they crash in each other, they loose points and health
        if self.crash_eachother():
            self.update_health(random.randint(1, 8)*cng.HITPOINT)
            self.update_score(-3*cng.SCOREPOINT)


        if self.got_shot(self):
            self.update_health(2.5*cng.HITPOINT)
            self.update_score(-4*cng.SCOREPOINT)
        


    def fuel_use(self):
        """Decreases the amount of fuel as the time goes"""
        self.fuel -= cng.FUELUSE
        return self.fuel
    
    

    
class Player1(SpaceShip):

    def __init__(self, image):
        super().__init__(image)
        self.score = 1

    def update(self):
        key = pygame.key.get_pressed()
        if key == pygame.K_a:
            self.rotate_left()
        if key == pygame.K_d:
            self.rotate_right()
        if key == pygame.K_w:
            self.thrust()
        if key == pygame.K_CAPSLOCK:
            self.shoot()


class Player2(SpaceShip):

    def __init__(self, image):
        super().__init__(image)
        self.score = 2

    def update(self):
        key = pygame.key.get_pressed()
        if key == pygame.K_LEFT:
            self.velocity.x -= cng.MOVEMENT
            #self.rotate_left()
        if key == pygame.K_RIGHT:
            self.velocity.x += cng.MOVEMENT 
            #self.rotate_right()
        if key == pygame.K_UP:
            self.thrust()
        if key == pygame.K_LCTRL:
            self.shoot()
        

class Manager():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((cng.SCREEN_X, cng.SCREEN_Y))
        self.clock = pygame.time.Clock()

        # Load the simulation background and use it
        self.background = pygame.image.load(cng.BACKGROUND) 
        self.background = pygame.transform.scale(self.background,(cng.SCREEN_X, cng.SCREEN_Y)) 
        self.background.convert()

        # Load images
        self.player1_img = pygame.image.load(cng.SHIP_PLAYER1).convert_alpha() 
        self.player1_img = pygame.transform.scale(self.player1_img,(self.player1_img.get_width(), self.player1_img.get_height()))
        
        self.player2_img = pygame.image.load(cng.SHIP_PLAYER2).convert_alpha() 
        self.player2_img = pygame.transform.scale(self.player2_img,(self.player2_img.get_width(), self.player2_img.get_height()))
        
        self.obstacle_img = pygame.image.load(cng.OBSTACLE).convert_alpha() 
        self.obstacle_img = pygame.transform.scale(self.obstacle_img,(self.obstacle_img.get_width(), self.obstacle_img.get_height()))
        
        self.bullet_img = pygame.image.load(cng.BULLET).convert_alpha() 
        self.bullet_img = pygame.transform.scale(self.bullet_img,(self.bullet_img.get_width(), self.bullet_img.get_height()))
        
        
        self.sprites_init()
        self.loop()


    def loop(self):
        """Main loop for manager. Checks the event for exit strategy, and
           updates all the objects""" 
        while True:
            self.event()
            self.update()


    def sprites_init(self):
        """Initializes objects, and groups them"""
        self.player1 = Player1(self.player1_img)
        self.player1_group = pygame.sprite.Group()
        self.player1_group.add(self.player1)

        self.player2 = Player2(self.player2_img)
        self.player2_group = pygame.sprite.Group()
        self.player2_group.add(self.player2)
        """
        self.obstacle = Obstacle()
        self.obstacle_group = pygame.sprite.Group()
        self.obstacle_group.add(self.obstacle)

        self.bullet = Bullets()
        self.bullet_group = pygame.sprite.Group()
        self.bullet_group.add(self.bullet)

        """


    def event(self):
        """Pygame event"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        self.clock.tick(60)  # Frames per second


    def update(self):
        """Updates all objects through sprite's group update"""
        self.screen.blit(self.background, (0,0))
        self.player1_group.draw(self.screen)
        self.player1_group.update()

        self.player2_group.draw(self.screen)
        self.player2_group.update()

        #self.obstacle_group.draw(self.screen)
        #self.obstacle_group.update()



        
        pygame.display.update()

    '''def text(self):
        """Prints text on screen"""
        font = pygame.font.SysFont('arial', 20)
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