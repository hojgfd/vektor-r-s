import pygame
import sys
from Player import Car

# Initialize Pygame og mixer for epic gamer music
pygame.init()
pygame.mixer.init()

# Load the epic music
pygame.mixer.music.load('music.mp3')  # Replace with your music file path
pygame.mixer.music.play(-1)  # Loop

# Fuld skærm
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("3D Vector Race Simulation")

# Clock
clock = pygame.time.Clock()
FPS = 60

# Loader baggrunden og scaler til fuld skærm
try:
    track_image = pygame.image.load("images/Track.png").convert()
    track_surface = pygame.transform.scale(track_image, (WIDTH, HEIGHT))
except pygame.error as e:
    print(f"Error loading track image: {e}")
    sys.exit()

# Laver My Queen
car = Car(position=(WIDTH // 2, HEIGHT // 2), image_path="images/Car.png",
          max_speed=5, acceleration=0.2, deceleration=0.1, turn_speed=3, scale=7)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key press handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:  # Add jump functionality
        car.jump()

    car.handle_input(keys)

    # Update car
    car.update(WIDTH, HEIGHT, track_surface)

    # Tegn baggrund
    screen.blit(track_surface, (0, 0))

    # Tegn bil
    car.draw(screen)

    # Update  display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# SES
pygame.quit()
sys.exit()
