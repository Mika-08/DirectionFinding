import pygame
import numpy as np


class GUI:
    SCALING = 1.4
    WIDTH = 1400 / SCALING
    HEIGHT = 2 * WIDTH / 3
    screen = None

    pygame.font.init()
    MAIN_FONT = 'freesansbold.ttf'
    FONTS = {
        "radar_font": pygame.font.Font(MAIN_FONT, int(30 / SCALING)),
        "time_font": pygame.font.Font(MAIN_FONT, int(30 / SCALING)),
        "stopwatch_font": pygame.font.Font(MAIN_FONT, int(30 / SCALING)),
        "menu_font": pygame.font.Font(MAIN_FONT, int(100 / SCALING)),
        "menu_item_font": pygame.font.Font(MAIN_FONT, int(50 / SCALING))
    }

    COLORS = {
        "black": (8, 9, 10),
        "green": (50, 205, 50),
        "red": (240, 84, 79),
        "white": (255, 250, 255)
    }

    # Radar properties
    radar_radius = 500 / SCALING
    radar_circle_center_x = int(WIDTH / 2)
    radar_circle_center_y = int(4 * HEIGHT / 5)
    radar_circle_center = (radar_circle_center_x, radar_circle_center_y)

    def init_window(self):
        """
        Function for initializing the screen
        :return: None
        """
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Hornet tracker")

    def make_outline(self, object_to_be_displayed, location_x, location_y):
        mask = pygame.mask.from_surface(object_to_be_displayed)
        mask_surface = mask.to_surface()
        mask_surface.set_colorkey(self.COLORS.get('green'))
        self.screen.blit(mask_surface, location_x - 1, location_y)
        self.screen.blit(mask_surface, location_x + 1, location_y)
        self.screen.blit(mask_surface, location_x, location_y - 1)
        self.screen.blit(mask_surface, location_x, location_y + 1)

    def make_radar_circles(self):
        """
        Function for making the circles of the radar interface using two circles, one inner and one outer
        :return: None
        """
        for i in range(5):
            # Draw the circles
            radius_outer_circle = self.radar_radius - i * (100 / self.SCALING) + 6 # 6 to correct for the lines width
            pygame.draw.circle(self.screen, self.COLORS.get('green'), self.radar_circle_center, radius_outer_circle)
            pygame.draw.circle(self.screen, self.COLORS.get('black'), self.radar_circle_center, radius_outer_circle
                               - 12)  # 12 to get a green outline of 12

            # Draw the text on the circles
            text_surface = self.FONTS.get('radar_font').render(f"{500 - i * 100}m", True, self.COLORS.get('white'))
            text_rect = text_surface.get_rect()

            # 35 and 10 for spacing the text between the lines
            text_rect.center = (self.radar_circle_center[0] + 35,
                                self.radar_circle_center[1] - radius_outer_circle - 10)
            self.screen.blit(text_surface, text_rect)

        # Draw the middle circle
        pygame.draw.circle(self.screen, self.COLORS.get('green'), self.radar_circle_center, 10 / self.SCALING)

    def make_radar_lines(self):
        """
        Function for making the radar lines every 45 degrees
        :return: None
        """
        for i in range(8):
            angle_rad = np.radians(45 * i)  # Convert degrees to radians
            end_point_x = self.radar_circle_center[0] + np.sin(angle_rad) * self.radar_radius
            end_point_y = self.radar_circle_center[1] + np.cos(angle_rad) * self.radar_radius
            pygame.draw.line(self.screen, self.COLORS.get('green'), self.radar_circle_center,
                             (int(end_point_x), int(end_point_y)), width=6)

    def draw(self):
        """
        Function for drawing all the components at the right place
        :return: None
        """
        # Background radar circle
        self.make_radar_circles()
        self.make_radar_lines()

