import pygame
import sys
from pygame.math import Vector2

# Initialize Pygame
pygame.init()

# Screen dimensions (Fullscreen)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Racing Game")

# Colors
WHITE = (255, 255, 255)

# Clock
clock = pygame.time.Clock()
FPS = 60


class Car:
    def __init__(self, position, image_path, max_speed, acceleration, deceleration, turn_speed, scale):
        self.position = Vector2(position)
        self.max_speed = max_speed
        self.acceleration = acceleration
        self.deceleration = deceleration
        self.turn_speed = turn_speed

        self.speed = 0
        self.direction = Vector2(1, 0)  # Initial direction (pointing right)

        # Load and scale car image
        self.original_surface = pygame.image.load(image_path).convert_alpha()
        scaled_size = (int(self.original_surface.get_width() / scale), int(self.original_surface.get_height() / scale))
        self.surface = pygame.transform.smoothscale(self.original_surface, scaled_size)
        self.rect = self.surface.get_rect(center=(self.position.x, self.position.y))

    def handle_input(self, keys):
        # Accelerate and decelerate
        if keys[pygame.K_UP]:
            self.speed = min(self.speed + self.acceleration, self.max_speed)
        elif keys[pygame.K_DOWN]:
            self.speed = max(self.speed - self.deceleration, -self.max_speed / 2)  # Reverse speed is slower
        else:
            # Gradual slowdown when no key is pressed
            if self.speed > 0:
                self.speed = max(self.speed - self.deceleration, 0)
            elif self.speed < 0:
                self.speed = min(self.speed + self.deceleration, 0)

        # Turn the car
        if keys[pygame.K_LEFT]:
            self.direction = self.direction.rotate(-self.turn_speed)
        if keys[pygame.K_RIGHT]:
            self.direction = self.direction.rotate(self.turn_speed)

    def update(self):
        # Update velocity and position
        velocity = self.direction * self.speed
        self.position += velocity

        # Keep the car on the screen
        if self.position.x < 0:
            self.position.x = WIDTH
        elif self.position.x > WIDTH:
            self.position.x = 0

        if self.position.y < 0:
            self.position.y = HEIGHT
        elif self.position.y > HEIGHT:
            self.position.y = 0

    def draw(self, screen):
        # Rotate the car surface based on direction
        angle = self.direction.angle_to(Vector2(1, 0))
        rotated_surface = pygame.transform.rotate(self.surface, -angle)
        self.rect = rotated_surface.get_rect(center=(self.position.x, self.position.y))
        screen.blit(rotated_surface, self.rect.topleft)


# Create a car instance
car = Car(
    position=(WIDTH // 2, HEIGHT // 2),
    image_path="images/Car.png",
    max_speed=5,
    acceleration=0.2,
    deceleration=0.1,
    turn_speed=3,
    scale=7
)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key press handling
    keys = pygame.key.get_pressed()
    car.handle_input(keys)

    # Update car
    car.update()

    # Clear the screen
    screen.fill(WHITE)

    # Draw the car
    car.draw(screen)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
