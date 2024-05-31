import pygame
import numpy as np
from datetime import datetime

import Stopwatch
import Tracking


class GUI:
    def __init__(self, scaling):
        """
        Constructor function for GUI class
        """
        self.SCALING = scaling
        self.WIDTH = 1400 / self.SCALING
        self.HEIGHT = 2 * self.WIDTH / 3
        self.SCREEN = None

        self.stopwatch = Stopwatch.Stopwatch()
        self.tracking = Tracking.Tracking()

        self.stopwatch_is_enabled = True
        self.tracking_is_enabled = True

        self.menu = False

        pygame.font.init()
        self.MAIN_FONT = 'freesansbold.ttf'
        self.FONTS = {
            "radar_font": pygame.font.Font(self.MAIN_FONT, int(30 / self.SCALING)),
            "time_font": pygame.font.Font(self.MAIN_FONT, int(30 / self.SCALING)),
            "stopwatch_font": pygame.font.Font(self.MAIN_FONT, int(30 / self.SCALING)),
            "menu_font": pygame.font.Font(self.MAIN_FONT, int(100 / self.SCALING)),
            "menu_item_font": pygame.font.Font(self.MAIN_FONT, int(50 / self.SCALING)),
            "gain_slider_font": pygame.font.Font(self.MAIN_FONT, int(30 / self.SCALING))
        }

        self.COLORS = {
            "black": (8, 9, 10),
            "green": (50, 205, 50),
            "red": (240, 84, 79),
            "white": (255, 250, 255)
        }

        # Buttons
        self.reset_button = None
        self.start_stop_button = None
        self.menu_button = None
        self.back_button = None
        self.tracking_button = None
        self.stopwatch_button = None
        self.gain_slider = None

        self.gain_slider_x = 0
        self.gain = None
        self.dragging = None

        # Pictograms
        self.pictograms = {
            "menu_image": pygame.image.load("images/menu_white.PNG"),
            "back_image": pygame.image.load("images/back_arrow_white.png")
        }

        # Radar properties
        self.radar_properties = {
            "radius": 500 / self.SCALING,
            "circle_center_x": int(self.WIDTH / 2),
            "circle_center_y": int(4 * self.HEIGHT / 5),
        }
        self.radar_properties["circle_center"] = (self.radar_properties["circle_center_x"], self.radar_properties["circle_center_y"])



    def init_window(self):
        """
        Function for initializing the screen
        :return: Nothing
        """
        pygame.init()
        self.SCREEN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Hornet tracker")

    def make_radar_circles(self):
        """
        Draw radar circles on the GUI.
        """
        for i in range(5):
            radius_outer_circle = self.radar_properties["radius"] - i * (100 / self.SCALING) + 8.4 / self.SCALING
            pygame.draw.circle(self.SCREEN, self.COLORS['green'], self.radar_properties["circle_center"],
                               radius_outer_circle)
            pygame.draw.circle(self.SCREEN, self.COLORS['black'], self.radar_properties["circle_center"],
                               radius_outer_circle - 16.8 / self.SCALING)

            text_surface = self.FONTS['radar_font'].render(f"{500 - i * 100}m", True, self.COLORS['white'])
            text_rect = text_surface.get_rect()
            text_rect.center = (self.radar_properties["circle_center"][0] + 49 / self.SCALING,
                                self.radar_properties["circle_center"][1] - radius_outer_circle - 14 / self.SCALING)
            self.SCREEN.blit(text_surface, text_rect)

        pygame.draw.circle(self.SCREEN, self.COLORS['green'], self.radar_properties["circle_center"], 10 / self.SCALING)

    def make_radar_lines(self):
        """
        Draw radar lines on the GUI.
        """
        for i in range(8):
            angle_rad = np.radians(45 * i)
            end_point_x = self.radar_properties["circle_center"][0] + np.sin(angle_rad) * self.radar_properties["radius"]
            end_point_y = self.radar_properties["circle_center"][1] + np.cos(angle_rad) * self.radar_properties["radius"]
            pygame.draw.line(self.SCREEN, self.COLORS['green'], self.radar_properties["circle_center"], (int(end_point_x), int(end_point_y)), width=int(8.4 / self.SCALING))

    def make_tracker(self):
        """
        Draw the tracker on the radar.
        """
        tracker_x_pos, tracker_y_pos = self.tracking.make_coordinates(self.SCALING)
        tracker_center = (int(tracker_x_pos + self.radar_properties["circle_center_x"]), int(tracker_y_pos + self.radar_properties["circle_center_y"]))
        tracker_radius = 25 / self.SCALING
        pygame.draw.circle(self.SCREEN, self.COLORS['red'], tracker_center, tracker_radius)


    def make_time_block(self, stopwatch):
        """
        Function for making the time block at the right top of the screen
        :param stopwatch: true, then stopwatch is enabled
        :return: Nothing
        """
        rectangle_x = self.WIDTH - 390 / self.SCALING
        rectangle_y = 30 / self.SCALING

        # Add the current time to the screen
        current_time = datetime.now().strftime('%H:%M')
        text_time_surface = self.FONTS.get('time_font').render(f"Local time: {current_time}", True,
                                                               self.COLORS.get('white'))
        text_time_rect = text_time_surface.get_rect()
        text_time_rect.topleft = (rectangle_x + 45 / self.SCALING, rectangle_y + 40 / self.SCALING)

        # Add to the screen
        if not self.menu:
            self.SCREEN.blit(text_time_surface, text_time_rect)

        # Add the outline and the stopwatch function when the stopwatch is enabled
        if stopwatch:
            self.make_stopwatch(rectangle_x, rectangle_y)

    def make_stopwatch(self, rectangle_x, rectangle_y):
        """
        Method to call if the stopwatch feature is turned on
        :return: Nothing
        """

        # Rectangle outline
        rect = pygame.Rect(rectangle_x, rectangle_y, 370 / self.SCALING, 260 / self.SCALING)

        # Stopwatch time
        stopwatch_time_str = str(self.stopwatch.get_elapsed_time()).split('.')[0]
        stopwatch_text_surface = self.FONTS.get('stopwatch_font').render(f"Stopwatch: {stopwatch_time_str}",
                                                                         True, self.COLORS.get('white'))
        stopwatch_text_rect = stopwatch_text_surface.get_rect()
        stopwatch_text_rect.topleft = (rectangle_x + 45 / self.SCALING, rectangle_y + 100 / self.SCALING)

        # Stopwatch buttons
        reset_text = self.FONTS.get('stopwatch_font').render("Reset", True, self.COLORS.get('white'))

        # Change the start stop button text dynamically
        start_stop_button_text = "Start"
        start_stop_color = self.COLORS.get('green')
        if self.stopwatch.is_running:
            start_stop_button_text = "Stop"
            start_stop_color = self.COLORS.get('red')

        start_stop_text = self.FONTS.get('stopwatch_font').render(f"{start_stop_button_text}", True,
                                                                  self.COLORS.get('white'))

        reset_rect = reset_text.get_rect()
        reset_rect.center = (rectangle_x + (45 + 60) / self.SCALING, rectangle_y + 200 / self.SCALING)
        start_stop_rect = start_stop_text.get_rect()
        start_stop_rect.center = (rectangle_x + (45 + 230) / self.SCALING, rectangle_y + 200 / self.SCALING)

        # Make outlines for the buttons
        x_pos_reset = reset_rect[0] - 35 / self.SCALING
        y_pos_reset = reset_rect[1] - 21 / self.SCALING
        x_pos_start_stop = start_stop_rect[0] - 42 / self.SCALING
        y_pos_start_stop = start_stop_rect[1] - 21 / self.SCALING

        self.reset_button = (x_pos_reset, y_pos_reset,
                             160 / self.SCALING, 75 / self.SCALING)
        self.start_stop_button = (x_pos_start_stop, y_pos_start_stop,
                                  160 / self.SCALING, 75 / self.SCALING)

        if not self.menu:
            # Add to the screen
            # Draw the outline rectangle
            pygame.draw.rect(self.SCREEN, self.COLORS.get('white'), rect, width=3, border_radius=30)

            # Draw the stopwatch text
            self.SCREEN.blit(stopwatch_text_surface, stopwatch_text_rect)

            # Fill the inside
            pygame.draw.rect(self.SCREEN, start_stop_color, self.start_stop_button, border_radius=20)

            # Draw the outlines
            pygame.draw.rect(self.SCREEN, self.COLORS.get('white'), self.reset_button, width=3, border_radius=20)
            pygame.draw.rect(self.SCREEN, self.COLORS.get('white'), self.start_stop_button, width=3, border_radius=20)

            # Draw the button text
            self.SCREEN.blit(reset_text, reset_rect)
            self.SCREEN.blit(start_stop_text, start_stop_rect)

    def make_menu_button(self):
        """
        Function to add the menu icon to the screen
        :return: Nothing
        """
        menu_image_scaled = pygame.transform.scale(self.pictograms["menu_image"], (55, 50))
        menu_rect = menu_image_scaled.get_rect(topleft=(48 / self.SCALING, 30 / self.SCALING))
        self.menu_button = menu_rect

        if not self.menu:
            self.SCREEN.blit(menu_image_scaled, menu_rect)

    def make_menu(self):
        """
        Function to make the menu
        :return: Nothing
        """
        rectangle_x = 260 / self.SCALING
        rectangle_y = 250 / self.SCALING

        text_menu_surface = self.FONTS.get('menu_font').render("Menu", True,
                                                               self.COLORS.get('white'))
        text_menu_rect = text_menu_surface.get_rect()
        text_menu_rect.center = (self.WIDTH / 2, 180 / self.SCALING)

        # Make rectangle
        rect = pygame.Rect(rectangle_x, rectangle_y, 875 / self.SCALING, 600 / self.SCALING)

        # Add text
        # Tracking
        text_tracking_surface = self.FONTS.get('menu_item_font').render("Tracking", True,
                                                                        self.COLORS.get('white'))
        text_tracking_rect = text_tracking_surface.get_rect()
        text_tracking_rect.topleft = (rectangle_x + 50 / self.SCALING, rectangle_y + 50 / self.SCALING)

        # Stopwatch
        text_stopwatch_surface = self.FONTS.get('menu_item_font').render("Enable\nstopwatch", True,
                                                                         self.COLORS.get('white'))
        text_stopwatch_rect = text_stopwatch_surface.get_rect()
        text_stopwatch_rect.topleft = (rectangle_x + 50 / self.SCALING, rectangle_y + 200 / self.SCALING)

        # Gain text
        text_gain_surface = self.FONTS.get('menu_item_font').render("Dongle gain", True,
                                                                    self.COLORS.get('white'))
        text_gain_rect = text_gain_surface.get_rect()
        text_gain_rect.topleft = (rectangle_x + 50 / self.SCALING, rectangle_y + 400 / self.SCALING)

        # Gain left bound
        text_gain_left_surface = self.FONTS.get('gain_slider_font').render("0 dB", True,
                                                                           self.COLORS.get('white'))
        text_gain_left_rect = text_gain_left_surface.get_rect()
        text_gain_left_rect.topleft = (rectangle_x + 380 / self.SCALING, rectangle_y + 350 / self.SCALING)

        # Gain right bound
        text_gain_right_surface = self.FONTS.get('gain_slider_font').render("49.6 dB", True,
                                                                            self.COLORS.get('white'))
        text_gain_right_rect = text_gain_right_surface.get_rect()
        text_gain_right_rect.topleft = (rectangle_x + 675 / self.SCALING, rectangle_y + 350 / self.SCALING)

        # Gain value
        text_gain_value_surface = self.FONTS.get('gain_slider_font').render(f"{self.gain} dB", True,
                                                                            self.COLORS.get('white'))
        text_gain_value_rect = text_gain_value_surface.get_rect()
        text_gain_value_rect.topleft = (rectangle_x + 525 / self.SCALING, rectangle_y + 450 / self.SCALING)

        # Make the menu sliders
        self.make_menu_item_slider(rectangle_x, rectangle_y)

        if self.menu:
            # Add to the screen
            pygame.draw.rect(self.SCREEN, self.COLORS.get('white'), rect, width=3, border_radius=30)

            self.SCREEN.blit(text_menu_surface, text_menu_rect)
            self.SCREEN.blit(text_tracking_surface, text_tracking_rect)
            self.SCREEN.blit(text_stopwatch_surface, text_stopwatch_rect)
            self.SCREEN.blit(text_gain_surface, text_gain_rect)
            self.SCREEN.blit(text_gain_left_surface, text_gain_left_rect)
            self.SCREEN.blit(text_gain_right_surface, text_gain_right_rect)
            self.SCREEN.blit(text_gain_value_surface, text_gain_value_rect)

    def make_menu_item_slider(self, rectangle_x, rectangle_y):
        """
        Function for making the menu sliders
        :param rectangle_x: x position of the border
        :param rectangle_y: y position of the border
        :return: Nothing
        """

        # TODO: Divide into multiple functions

        rect_tracking = pygame.Rect(rectangle_x + 670 / self.SCALING, rectangle_y + 50 / self.SCALING,
                                    120 / self.SCALING, 45 / self.SCALING)

        self.tracking_button = rect_tracking

        rect_stopwatch = pygame.Rect(rectangle_x + 670 / self.SCALING, rectangle_y + 200 / self.SCALING,
                                     120 / self.SCALING, 45 / self.SCALING)

        self.stopwatch_button = rect_stopwatch

        tracking_dot_x_pos = 371 / self.SCALING
        tracking_dot_color = self.COLORS.get('red')
        if self.tracking_is_enabled:
            tracking_dot_x_pos = 420 / self.SCALING
            tracking_dot_color = self.COLORS.get('green')

        rect_tracking_dot = pygame.Rect(tracking_dot_x_pos + 575 / self.SCALING,
                                        rectangle_y + 57 / self.SCALING, 40 / self.SCALING, 32 / self.SCALING)

        stopwatch_dot_x_pos = 371 / self.SCALING
        stopwatch_dot_color = self.COLORS.get('red')
        if self.stopwatch_is_enabled:
            stopwatch_dot_x_pos = 420 / self.SCALING
            stopwatch_dot_color = self.COLORS.get('green')

        rect_stopwatch_dot = pygame.Rect(stopwatch_dot_x_pos + 575 / self.SCALING, rectangle_y + 207 / self.SCALING,
                                         40 / self.SCALING, 32 / self.SCALING)

        self.make_gain_slider(rectangle_x, rectangle_y)

        if self.menu:
            pygame.draw.rect(self.SCREEN, self.COLORS.get('white'), rect_tracking, width=3, border_radius=20)
            pygame.draw.rect(self.SCREEN, self.COLORS.get('white'), rect_stopwatch, width=3, border_radius=20)
            pygame.draw.rect(self.SCREEN, tracking_dot_color, rect_tracking_dot, border_radius=20)
            pygame.draw.rect(self.SCREEN, stopwatch_dot_color, rect_stopwatch_dot, border_radius=20)

    def make_gain_slider(self, rectangle_x, rectangle_y):
        """
        Make the gain slider
        :param rectangle_x: x position of the menu rectangle
        :param rectangle_y: y position of the menu rectangle
        :return: Nothing
        """

        slider_x = rectangle_x + 370 / self.SCALING
        slider_y = rectangle_y + 400 / self.SCALING

        slider_width = 420 / self.SCALING
        dot_width = 40 / self.SCALING

        rect_gain = pygame.Rect(slider_x, slider_y, slider_width, 45 / self.SCALING)

        # self.gain_slider_x = slider_x

        if self.gain_slider_x < slider_x:
            self.gain_slider_x = slider_x

        if self.gain_slider_x > slider_x + 261.42857142857144:
            self.gain_slider_x = slider_x + 261.42857142857144

        rect_gain_dot = pygame.Rect(self.gain_slider_x + 7 / self.SCALING,
                                    slider_y + 7 / self.SCALING, dot_width, 32 / self.SCALING)

        self.gain_slider = rect_gain_dot

        self.calculate_gain(slider_x, slider_width, dot_width)

        if self.menu:
            pygame.draw.rect(self.SCREEN, self.COLORS.get('white'), rect_gain, width=3, border_radius=20)
            pygame.draw.rect(self.SCREEN, self.COLORS.get('white'), rect_gain_dot, border_radius=20)

    def calculate_gain(self, slider_x, slider_width, dot_width):
        """
        Calculate the gain value
        :param slider_x: The x position of the slider rectangle
        :param slider_width: The width of the slider rectangle
        :param dot_width: The width of the slider dot
        :return: Nothing
        """
        gain_values = [0.0, 0.9, 1.4, 2.7, 3.7, 7.7, 8.7, 12.5, 14.4, 15.7, 16.6, 19.7, 20.7, 22.9, 25.4, 28.0, 29.7,
                       32.8, 33.8, 36.4, 37.2, 38.6, 40.2, 42.1, 43.4, 43.9, 44.5, 48.0, 49.6]

        min_value_gain = min(gain_values)
        max_value_gain = max(gain_values)

        normalized_gain_values = [(value - min_value_gain) / (max_value_gain - min_value_gain) *
                                  (slider_width - 14 / self.SCALING - dot_width) for value in gain_values]

        slider_value = (self.gain_slider_x - slider_x) / (slider_width - 14 / self.SCALING - dot_width) * \
                       (max_value_gain - min_value_gain) + min_value_gain

        self.gain = min(gain_values, key=lambda x: abs(x - slider_value))

    def make_back_button(self):
        """
        Make the back button
        :return: Nothing
        """
        back_image_scaled = pygame.transform.scale(self.pictograms["back_image"], (60, 50))
        back_rect = back_image_scaled.get_rect(topleft=(48 / self.SCALING, 30 / self.SCALING))
        self.back_button = back_rect

        if self.menu:
            self.SCREEN.blit(back_image_scaled, back_rect)

    def check_stopwatch_buttons(self, mouse_pos):
        """
        Check is the stopwatch buttons are clicked
        :param mouse_pos: position of the mouse
        :return: Nothing
        """
        # Make the hit boxes for the stop watch buttons
        reset_box = pygame.Rect(self.reset_button)
        start_stop_box = pygame.Rect(self.start_stop_button)

        if reset_box.collidepoint(mouse_pos):
            self.stopwatch.reset()
        elif start_stop_box.collidepoint(mouse_pos):
            self.stopwatch.start_stop()

    def check_buttons(self, mouse_pos):
        """
        Function for checking if a button is clicked
        :param mouse_pos: position of the mouse
        :return: Nothing
        """

        if self.menu:
            if self.back_button.collidepoint(mouse_pos):
                self.menu = False

            if self.tracking_button.collidepoint(mouse_pos) and self.tracking_is_enabled:
                self.tracking_is_enabled = False

            elif self.tracking_button.collidepoint(mouse_pos) and not self.tracking_is_enabled:
                self.tracking_is_enabled = True

            if self.stopwatch_button.collidepoint(mouse_pos) and self.stopwatch_is_enabled:
                self.stopwatch_is_enabled = False

            elif self.stopwatch_button.collidepoint(mouse_pos) and not self.stopwatch_is_enabled:
                self.stopwatch_is_enabled = True

        elif not self.menu:
            if self.menu_button.collidepoint(mouse_pos):
                self.menu = True

            if self.stopwatch_is_enabled:
                self.check_stopwatch_buttons(mouse_pos)

    def check_gain_slider(self, event):
        """
        Check if the slider is adjusted
        :param event: Event in the event list
        :return: Noting
        """
        if self.menu:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.gain_slider.collidepoint(event.pos):
                    self.dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging:
                    mouse_x, _ = event.pos
                    self.gain_slider_x = mouse_x

    def handle_events(self):
        """
        Event handler
        :return: Nothing
        """
        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.check_buttons(mouse_pos)

            self.check_gain_slider(event)
        return True

    def draw_track_screen(self):
        """
        Draw the tracking screen
        :return: Nothing
        """
        # Make radar
        self.make_radar_circles()
        self.make_radar_lines()

        if self.tracking_is_enabled:
            self.make_tracker()

        # Make menu button
        self.make_menu_button()
        self.make_back_button()

        # Show or not show the stopwatch
        if self.stopwatch_is_enabled:
            self.make_time_block(True)
        elif not self.stopwatch_is_enabled:
            self.make_time_block(False)

    def draw_menu_screen(self):
        """
        Draw the menu screen
        :return: Nothing
        """
        self.make_menu()
        self.make_back_button()

    def draw_dynamic(self):
        """
        Function for dynamically drawing the items on the screen
        :return: Nothing
        """
        self.make_menu_button()
        self.make_back_button()
        self.make_time_block(self.stopwatch)
        self.make_menu()

        self.SCREEN.fill(self.COLORS.get('black'))

        if self.menu:
            self.SCREEN.fill(self.COLORS.get('black'))

            # print("menu show")
            self.draw_menu_screen()

        if not self.menu:
            self.SCREEN.fill(self.COLORS.get('black'))

            # print("tracking show")
            self.draw_track_screen()
