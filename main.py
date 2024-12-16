import pygame
import sys
from Player import Car  # Import the Car class

# Initialize Pygame
pygame.init()

# Screen dimensions (Fullscreen)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("SIUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU")

# Clock
clock = pygame.time.Clock()
FPS = 60

# Load the track image (background) and scale it to skærmstørrelsen
try:
    track_image = pygame.image.load("images/Track.png").convert()
    track_surface = pygame.transform.scale(track_image, (WIDTH, HEIGHT))  # Skaler til skærmens størrelse
except pygame.error as e:
    print(f"Error loading track image: {e}")
    sys.exit()

# Create a car instance
car = Car(position=(WIDTH // 2, HEIGHT // 2),image_path= "images/Car.png",max_speed=5,acceleration=0.2,deceleration=0.1,turn_speed=3,scale=7,)

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
    car.update(WIDTH, HEIGHT)

    # Draw the track (background) - nu skaleret til skærmstørrelsen
    screen.blit(track_surface, (0, 0))

    # Draw the car
    car.draw(screen)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
