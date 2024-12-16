import pygame
from pygame.math import Vector2
import math


class Car:
    def __init__(self, position, image_path, max_speed, acceleration, deceleration, turn_speed, scale):
        self.position = Vector2(position)  # Current position of the car
        self.max_speed = max_speed  # Max speed of the car
        self.acceleration = acceleration  # Rate of acceleration
        self.deceleration = deceleration  # Rate of slowing down
        self.turn_speed = turn_speed  # Speed at which the car can turn
        self.speed = 0  # Current velocity of the car
        self.angle = 90  # Initial facing direction set to point upwards (90°)

        # Load and scale the car image
        self.original_surface = pygame.image.load(image_path).convert_alpha()
        scaled_size = (int(self.original_surface.get_width() / scale), int(self.original_surface.get_height() / scale))
        self.surface = pygame.transform.smoothscale(self.original_surface, scaled_size)

    def handle_input(self, keys):
        """Handle forward, backward, and turning input."""
        # Handle forward/backward acceleration
        if keys[pygame.K_UP]:  # Accelerate forward
            self.speed = min(self.speed + self.acceleration, self.max_speed)
        elif keys[pygame.K_DOWN]:  # Accelerate backward
            self.speed = max(self.speed - self.deceleration, -self.max_speed / 2)
        else:
            # Gradually decelerate if no key is pressed
            if self.speed > 0:
                self.speed = max(self.speed - self.deceleration, 0)
            elif self.speed < 0:
                self.speed = min(self.speed + self.deceleration, 0)

        # Handle turning left/right
        if keys[pygame.K_LEFT]:  # Turn left
            self.angle -= self.turn_speed
        if keys[pygame.K_RIGHT]:  # Turn right
            self.angle += self.turn_speed

        # Normalize the angle to ensure it doesn't grow indefinitely
        self.angle %= 360

    def update(self, screen_width, screen_height):
        """Update car's position based on its speed and angle."""
        # Convert angle to radians
        rad_angle = math.radians(self.angle)

        # Calculate the new velocity using trigonometric functions
        velocity_x = math.cos(rad_angle) * self.speed
        velocity_y = math.sin(rad_angle) * self.speed

        # Update the car's position
        self.position.x += velocity_x
        self.position.y += velocity_y

        # Screen wrapping (keep the car within the screen boundaries)
        if self.position.x < 0:
            self.position.x += screen_width
        if self.position.x > screen_width:
            self.position.x -= screen_width
        if self.position.y < 0:
            self.position.y += screen_height
        if self.position.y > screen_height:
            self.position.y -= screen_height

    def draw(self, screen):
        """Draw the car with its correct rotation."""
        # Rotate the surface by the car's angle
        rotated_surface = pygame.transform.rotate(self.surface, -self.angle)
        rotated_rect = rotated_surface.get_rect(center=(self.position.x, self.position.y))
        screen.blit(rotated_surface, rotated_rect.topleft)
