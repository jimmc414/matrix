import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("Matrix Digital Rain - Advanced")

# Colors (shades of green)
greens = [
    (0, 255, 70),    # Bright Green
    (0, 230, 60),
    (0, 200, 50),
    (0, 170, 40),
    (0, 140, 30),
    (0, 110, 20),
    (0, 80, 10),     # Darker Green
]

black = (0, 0, 0)

# Font setup
font_size = 15
font = pygame.font.SysFont("consolas", font_size, bold=True)

# Character set: Latin, numbers, katakana, and symbols
chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789ァアィイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン0123456789!@#$%^&*()-_=+<>?/|\\[]{};:'\",.`~"

# Number of columns based on screen width and font size
columns = width // font_size

# Stream class to manage individual streams
class Stream:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = random.randint(5, 15)
        self.length = random.randint(10, 30)  # Length of the stream
        self.chars = [random.choice(chars) for _ in range(self.length)]
        self.last_update = pygame.time.get_ticks()

    def draw(self, surface):
        for i in range(len(self.chars)):
            # Calculate position
            pos_y = self.y - i * font_size
            if pos_y < 0:
                continue

            # Determine brightness based on the character's position in the stream
            brightness_index = min(i, len(greens) - 1)
            color = greens[brightness_index]

            # Render the character
            char_surface = font.render(self.chars[i], True, color)
            surface.blit(char_surface, (self.x, pos_y))

    def update(self, height):
        self.y += self.speed
        # Replace characters to simulate dynamic streams
        if random.random() > 0.975:
            self.chars.insert(0, random.choice(chars))
            self.chars.pop()

        # Reset stream if it goes beyond the screen
        if self.y - self.length * font_size > height:
            self.reset(height)

    def reset(self, height):
        self.y = random.randint(-1000, 0)
        self.speed = random.randint(5, 15)
        self.length = random.randint(10, 30)
        self.chars = [random.choice(chars) for _ in range(self.length)]

# Create streams
streams = []
for i in range(columns):
    x = i * font_size
    y = random.randint(-1000, 0)
    streams.append(Stream(x, y))

# Frame rate
clock = pygame.time.Clock()
fps = 30

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            width, height = event.size
            screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            columns = width // font_size
            # Reset streams to adapt to new window size
            streams = []
            for i in range(columns):
                x = i * font_size
                y = random.randint(-1000, 0)
                streams.append(Stream(x, y))

    # Create a semi-transparent overlay for fading effect
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 25))  # Last value is alpha (transparency)
    screen.blit(overlay, (0, 0))

    # Update and draw each stream
    for stream in streams:
        stream.draw(screen)
        stream.update(height)

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(fps)

# Quit pygame
pygame.quit()
sys.exit()
