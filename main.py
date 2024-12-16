import pygame
import sys
from pygame.math import Vector2

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Car attributes
CAR_WIDTH, CAR_HEIGHT = 50, 30
car_pos = Vector2(WIDTH // 2, HEIGHT // 2)
car_velocity = Vector2(0, 0)
car_direction = Vector2(1, 0)  # Initial direction (pointing right)
car_speed = 0
max_speed = 5
acceleration = 0.2
deceleration = 0.1
turn_speed = 3

# Car surface (for rotation)
car_surface = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
car_surface.fill(RED)
car_rect = car_surface.get_rect(center=(car_pos.x, car_pos.y))

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key press handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        car_speed = min(car_speed + acceleration, max_speed)
    elif keys[pygame.K_DOWN]:
        car_speed = max(car_speed - deceleration, -max_speed / 2)  # Reverse speed is slower
    else:
        # Gradual slowdown when no key is pressed
        if car_speed > 0:
            car_speed = max(car_speed - deceleration, 0)
        elif car_speed < 0:
            car_speed = min(car_speed + deceleration, 0)

    if keys[pygame.K_LEFT]:
        car_direction = car_direction.rotate(-turn_speed)
    if keys[pygame.K_RIGHT]:
        car_direction = car_direction.rotate(turn_speed)

    # Update car velocity and position
    car_velocity = car_direction * car_speed
    car_pos += car_velocity

    # Keep the car on the screen
    if car_pos.x < 0:
        car_pos.x = WIDTH
    elif car_pos.x > WIDTH:
        car_pos.x = 0

    if car_pos.y < 0:
        car_pos.y = HEIGHT
    elif car_pos.y > HEIGHT:
        car_pos.y = 0

    # Clear the screen
    screen.fill(WHITE)

    # Rotate car surface based on direction
    angle = car_direction.angle_to(Vector2(1, 0))
    rotated_car = pygame.transform.rotate(car_surface, -angle)
    car_rect = rotated_car.get_rect(center=(car_pos.x, car_pos.y))

    # Draw the car
    screen.blit(rotated_car, car_rect.topleft)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
