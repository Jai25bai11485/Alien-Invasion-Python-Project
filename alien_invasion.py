import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard

class Alien_Invasion:
    """Overall Class to manage game assests and behaviour"""

    def __init__(self):
        """Intialize game, and create game resources"""

        pygame.init()

        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        
        #Create an instance to store game statistics
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullet = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()
        self.sb = Scoreboard(self)

        self.game_active = False

        #Make play button
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Start main loop for game"""
        while True:
            self._check_events()
            
            if self.game_active:
                self.ship.update()
                self._update_aliens()
                self._update_bullets()

            self._update_screen()
            self.clock.tick(60)
            

            
    def _check_events(self):
        """Respond to keyboard and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:  #in pygame each key press is registered as KEYDOWN event.
                self._check_keydown_events(event)
                 
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos= pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player hits play."""

        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked  and not self.game_active:
            self.settings.initialize_dynamic_settings()
            self._start_game()
 

    def _start_game(self):
         #Reset the game statistics
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ship()
            self.game_active = True

            #get rid of any remaining bullets and aliens.
            self.bullet.empty()
            self.aliens.empty()

            #Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            #Hide the mouse cursor.
            pygame.mouse.set_visible(False)



    def _check_keydown_events(self, event):
        """Respond to keypress."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p:
            self._start_game()


    def _check_keyup_events(self, event):
        """Respond to key release."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _create_fleet(self):
        """Create the fleet of aliens."""
        #Create an alien and keep adding aliens until there is no space left
    
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
           

        current_x, current_y = alien_width, alien_height  #current position of the placed alien
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width): # we subtracted this to have some margin left-over
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            #Finished a row, reset the x, and increment the y value
            current_x = alien_width
            current_y += 4 * alien_height 
        #What this is loop is doing is: whenever is there space for atleast 2 aliens, add an alien
        #Then repeat this until the specifies condition relating to y-pos i.e. rows are achieved

    def _create_alien(self, x_position, y_position):
        new_alien = Alien(self)         #strange obeservation: when I use new_alien = alien only 1 alien appears on screen 
                                        #but when i use new_alien = Alien(self) the code works correctly
                                        #this is because it refers to the same alien and keeps updating its position until the condition is satisfied.
        new_alien.x = x_position 
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _update_aliens(self):
        """Update all the aliens of the fleet."""
        self.aliens.update()
        self._check_fleet_edges()

        #Look for ship-alien collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        #Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()


    def _ship_hit(self):
        """Resopnd to ship being hit by an alien"""
        #Decrement ships left.
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ship()

            #Get rid of any remaining bullets or aliens
            self.bullet.empty()
            self.aliens.empty()

            #Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            #Pause
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                #Treat this same as the ship got hit
                self._ship_hit()
                break

    def _update_bullets(self):
        """Update the position of bullets and get rid of old bullets."""
        #Update bullet positions
        self.bullet.update()
        
        self._check_bullet_alien_collisions()
        

        if not self.aliens:
            #Destroy existing bullets and create new fleet
            self.bullet.empty()
            self._create_fleet()
            self.settings.increase_speed()

            #Increase level
            self.stats.level += 1
            self.sb.prep_level()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions"""
        #Check for bullet collision with aliens, if collision exists get rid of the alien
        collisions = pygame.sprite.groupcollide(
            self.bullet, self.aliens, True, True  #The 2 true arguemets tell pygame to delete both the bullet and the alien that have collided
            )

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()


        #Get rid of bullets that have disappeared.
        for bullet in self.bullet.copy():
            if bullet.rect.bottom <= 0:
                self.bullet.remove(bullet)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change directions."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1 #We want the y pos of each alien to change but we want the 
                                            #fleet direction to change only once, so the dirction change is outside the for-loop
        

    def _update_screen(self):
        """Update images on the screen and flip to new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullet.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        #Draw scoreboard
        self.sb.show_score()

        #Draw the button if the game is inactive
        if not self.game_active:
            self.play_button.draw_button()
    
        #Flip to new screen
        pygame.display.flip()

    def _fire_bullet(self):
        """Create a new bullet and add it to bullets group"""
        if len(self.bullet) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullet.add(new_bullet)

if __name__ == '__main__':
    #Make a game instance, and run the game:
    ai = Alien_Invasion()

    ai.run_game()
