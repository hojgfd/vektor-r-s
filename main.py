import pygame
import math

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vector Racing Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Clock for controlling the frame rate
clock = pygame.time.Clock()
FPS = 60

# Car settings
car_pos = [WIDTH // 2, HEIGHT // 2]
car_angle = 0  # Angle in degrees
car_speed = 0
max_speed = 5
acceleration = 0.1
deceleration = 0.05
turn_speed = 5

# Track (simple rectangle for now)
track = pygame.Rect(100, 100, WIDTH - 200, HEIGHT - 200)

def draw_car(position, angle):
    """Draw the car as a simple rectangle."""
    car_width, car_height = 40, 20
    x, y = position

    # Calculate car corners based on angle
    rad = math.radians(angle)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)

    points = [
        (x + cos_a * car_width / 2 - sin_a * car_height / 2, y + sin_a * car_width / 2 + cos_a * car_height / 2),
        (x - cos_a * car_width / 2 - sin_a * car_height / 2, y - sin_a * car_width / 2 + cos_a * car_height / 2),
        (x - cos_a * car_width / 2 + sin_a * car_height / 2, y - sin_a * car_width / 2 - cos_a * car_height / 2),
        (x + cos_a * car_width / 2 + sin_a * car_height / 2, y + sin_a * car_width / 2 - cos_a * car_height / 2),
    ]

    pygame.draw.polygon(screen, RED, points)

running = True
while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        car_speed = min(car_speed + acceleration, max_speed)
    if keys[pygame.K_DOWN]:
        car_speed = max(car_speed - acceleration, -max_speed / 2)
    if keys[pygame.K_LEFT]:
        car_angle += turn_speed if car_speed != 0 else 0
    if keys[pygame.K_RIGHT]:
        car_angle -= turn_speed if car_speed != 0 else 0

    # Apply deceleration when no input
    if not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
        if car_speed > 0:
            car_speed = max(car_speed - deceleration, 0)
        elif car_speed < 0:
            car_speed = min(car_speed + deceleration, 0)

    # Update car position
    rad_angle = math.radians(car_angle)
    car_pos[0] += car_speed * math.cos(rad_angle)
    car_pos[1] -= car_speed * math.sin(rad_angle)

    # Draw track
    pygame.draw.rect(screen, BLACK, track, 5)

    # Draw car
    draw_car(car_pos, car_angle)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()
