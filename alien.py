import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Class to represent a single alien in fleet."""

    def __init__(self, ai_game):
        """Initialize the alien and set its starting point."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        #Load alien image
        self.image = pygame.image.load("images/Nave.bmp")
        self.rect = self.image.get_rect()

        #Start with an alien at top left
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #Store alien's exact horzintal position
        self.x = float(self.rect.x)

    def update(self):
        """Make the alien move to the right."""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

    def check_edges(self):
        """Return True if alien is at the edge of screen."""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right ) or (self.rect.left <= 0) 