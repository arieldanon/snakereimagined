# Snake Reimagined

Snake Reimagined is a Python mini-game that shows the classic snake game with new immersive elements that adds power-ups, colorful snake changes, and obstacles to avoid! 

## Installation

Use the package for [pygame](https://www.pygame.org/wiki/GettingStarted) to install PyGame and get started.

```bash
python3 -m pip install -U pygame --user

```

## Usage

```python
# Example file showing a basic pygame "game loop"
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()


```

## Contributing
Game contribution ideas are welcome! Please let me know what you'd like!
