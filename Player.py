import pygame
from pygame.math import Vector2
import math


class Car:
    def __init__(self, position, image_path, max_speed, acceleration, deceleration, turn_speed, scale):
        self.position = Vector2(position)
        self.max_speed = max_speed
        self.acceleration = acceleration
        self.deceleration = deceleration
        self.turn_speed = turn_speed
        self.speed = 0
        self.angle = 90

        # Z-akse til hop
        self.z = 0  # Nuværende højde
        self.z_velocity = 0  # Vertikal hastighed
        self.gravity = -0.5  # Tyngdekraftens effekt
        self.on_ground = True  # Er bilen på jorden?

        # Indlæs og scale bilens billede
        self.original_surface = pygame.image.load(image_path).convert_alpha()
        scaled_size = (int(self.original_surface.get_width() / scale), int(self.original_surface.get_height() / scale))
        self.surface = pygame.transform.smoothscale(self.original_surface, scaled_size)

    def is_on_invalid_color(self, track_surface):
        # Definer de farver, som bilen ikke må køre på (RGB værdier)
        invalid_colors = [
            (209, 159, 62),
            (168, 231, 83),
            (87, 201, 34),
            (140, 175, 111),
            (189,159,91),
            (144, 94, 113),
            (141, 94, 111),
            (141, 94, 112),
            (145, 92, 109),
            (154, 106, 101),
            (143, 106, 101),
            (143, 93, 110),
            (146, 93, 110),
            (146, 93, 112),
            (145, 93, 108),

        ]

        # Find bilens position i pixel-koordinater
        x = int(self.position.x)
        y = int(self.position.y)

        # Tjek farven på banen ved bilens position
        if 0 <= x < track_surface.get_width() and 0 <= y < track_surface.get_height():
            color = track_surface.get_at((x, y))[:3]
            if color in invalid_colors:
                return True
        return False

    def jump(self):
        if self.on_ground:
            self.z_velocity = 10
            self.on_ground = False


# Håndter acceleration fremad/tilabe
    def handle_input(self, keys):
        if keys[pygame.K_UP]:
            self.speed = min(self.speed + self.acceleration, self.max_speed)
        elif keys[pygame.K_DOWN]:
            self.speed = max(self.speed - self.deceleration, -self.max_speed / 2)
        else:
            # reducere hastigheden, hvis ingen knap trykkes
            if self.speed > 0:
                self.speed = max(self.speed - self.deceleration, 0)
            elif self.speed < 0:
                self.speed = min(self.speed + self.deceleration, 0)

        # Håndter drejning til venstre/højre
        if keys[pygame.K_LEFT]:
            self.angle -= self.turn_speed
        if keys[pygame.K_RIGHT]:
            self.angle += self.turn_speed


    def update(self, screen_width, screen_height, track_surface):
        # Konverter vinkel til radianer
        rad_angle = math.radians(self.angle)

        # Beregn den nye hastighed ved hjælp af trigonometriske funktioner
        velocity_x = math.cos(rad_angle) * self.speed
        velocity_y = math.sin(rad_angle) * self.speed

        # Opdater bilens position midlertidigt
        new_position = Vector2(self.position.x + velocity_x, self.position.y + velocity_y)

        # Opdater Z-aksen for hop
        if not self.on_ground:
            self.z_velocity += self.gravity # Anvend tyngdekraft
            self.z += self.z_velocity # Opdater højde
            if self.z <= 0: # Tjek om bilen lander
                self.z = 0
                self.z_velocity = 0
                self.on_ground = True

        # Tjek for ugyldige farver, men kun hvis bilen er på jorden
        if self.on_ground:
            self.position = new_position  # Midlertidig opdatering for at tjekke farve
            if self.is_on_invalid_color(track_surface):
                self.speed = 0  # Stop bilen, hvis den rammer en ugyldig farve
            else:
                self.position = new_position  # Endelig opdatering, hvis alt er OK
        else:
            self.position = new_position  # Fortsæt uanset farven, hvis bilen er i luften

        # Screen wrapping (keep the car within the screen boundaries)
        if self.position.x < 0:
            self.position.x = screen_width  # Kommer fra højre
        if self.position.x > screen_width:
            self.position.x = 0  # Kommer fra venstre
        if self.position.y < 0:
            self.position.y = screen_height  # Kommer fra bunden
        if self.position.y > screen_height:
            self.position.y = 0  # Kommer fra toppen

    def draw(self, screen):
        # Rotate the surface by the car's angle
        rotated_surface = pygame.transform.rotate(self.surface, -self.angle)

        # Simulate 3D effect by adjusting the Y-position based on Z-height
        adjusted_position = (self.position.x, self.position.y - self.z)

        rotated_rect = rotated_surface.get_rect(center=adjusted_position)
        screen.blit(rotated_surface, rotated_rect.topleft)
