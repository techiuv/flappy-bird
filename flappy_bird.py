import random
import sys
import pygame
from pygame.locals import * 

# Global Variables for the game
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
GROUNDY = SCREENHEIGHT * 0.8

class FlappyBirdGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        pygame.display.set_caption('Flappy Bird')
        self.clock = pygame.time.Clock()

        # Load game assets
        self.load_assets()

    def load_assets(self):
        #Load all game assets
        self.sprites = {}
        self.sprites['player'] = pygame.image.load('assets/bird.png').convert_alpha()
        self.sprites['background'] = pygame.image.load('assets/background.png').convert()
        self.sprites['pipe'] = (
            pygame.transform.rotate(pygame.image.load('assets/pipe.png').convert_alpha(), 180),
            pygame.image.load('assets/pipe.png').convert_alpha()
        )
        self.sprites['base'] = pygame.image.load('assets/base.png').convert_alpha()
      #  self.sprites['message'] = pygame.image.load('assets/message.png').convert_alpha()

        # Load font for score
        self.font = pygame.font.Font('assets/Roboto-Regular.ttf', 32)

    def welcome_screen(self):
        #Shows welcome images on the screen
        playerx = int(SCREENWIDTH / 5)
        playery = int((SCREENHEIGHT - self.sprites['player'].get_height()) / 2)
       # messagex = int((SCREENWIDTH - self.sprites['message'].get_width()) / 2)
        messagey = int(SCREENHEIGHT * 0.13)
        basex = 0

        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    return  # Start the game

            self.screen.blit(self.sprites['background'], (0, 0))
            self.screen.blit(self.sprites['player'], (playerx, playery))
         #   self.screen.blit(self.sprites['message'], (messagex, messagey))
            self.screen.blit(self.sprites['base'], (basex, GROUNDY))
            pygame.display.update()
            self.clock.tick(FPS)

    def main_game(self):
        score = 0
        playerx = int(SCREENWIDTH / 5)
        playery = int(SCREENWIDTH / 2)
        basex = 0

        # Create 2 pipes for blitting on the screen
        newPipe1 = self.get_random_pipe()
        newPipe2 = self.get_random_pipe()

        # List of upper pipes
        upperPipes = [
            {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
            {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[0]['y']},
        ]
        # List of lower pipes
        lowerPipes = [
            {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
            {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
        ]

        # bird velocity 
        pipeVelX = -4

        playerVelY = -9
        playerMaxVelY = 10
        playerMinVelY = -8
        playerAccY = 1

        playerFlapAccv = -8  # velocity while flapping
        playerFlapped = False  # It is true only when the bird is flapping

        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    if playery > 0:
                        playerVelY = playerFlapAccv
                        playerFlapped = True

            # Check for collision
            if self.is_collide(playerx, playery, upperPipes, lowerPipes):
                return

            # Check for score
            playerMidPos = playerx + self.sprites['player'].get_width() / 2
            for pipe in upperPipes:
                pipeMidPos = pipe['x'] + self.sprites['pipe'][0].get_width() / 2
                if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                    score += 1
                    print(f"Your score is {score}")

            if playerVelY < playerMaxVelY and not playerFlapped:
                playerVelY += playerAccY

            if playerFlapped:
                playerFlapped = False
            playerHeight = self.sprites['player'].get_height()
            playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

            # Move pipes to the left
            for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
                upperPipe['x'] += pipeVelX
                lowerPipe['x'] += pipeVelX

            # Add a new pipe when the first is about to cross the leftmost part of the screen
            if 0 < upperPipes[0]['x'] < 5:
                newpipe = self.get_random_pipe()
                upperPipes.append(newpipe[0])
                lowerPipes.append(newpipe[1])

            # Remove pipes that are out of the screen
            if upperPipes[0]['x'] < -self.sprites['pipe'][0].get_width():
                upperPipes.pop(0)
                lowerPipes.pop(0)

            # Blit the sprites
            self.screen.blit(self.sprites['background'], (0, 0))
            for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
                self.screen.blit(self.sprites['pipe'][0], (upperPipe['x'], upperPipe['y']))
                self.screen.blit(self.sprites['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

            self.screen.blit(self.sprites['base'], (basex, GROUNDY))
            self.screen.blit(self.sprites['player'], (playerx, playery))

            # Render the score
            score_surface = self.font.render(str(score), True, (255, 255, 255))
            score_rect = score_surface.get_rect(center=(SCREENWIDTH / 2, SCREENHEIGHT * 0.12))
            self.screen.blit(score_surface, score_rect)

            pygame.display.update()
            self.clock.tick(FPS)

    def is_collide(self, playerx, playery, upperPipes, lowerPipes):
        #Check for collision
        
        if playery > GROUNDY - 25 or playery < 0:
            return True

        for pipe in upperPipes:
            pipeHeight = self.sprites['pipe'][0].get_height()
            if playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < self.sprites['pipe'][0].get_width():
                return True

        for pipe in lowerPipes:
            if (playery + self.sprites['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < self.sprites['pipe'][0].get_width():
                return True

        return False

    def get_random_pipe(self):
        #Generate positions of pipes (bottom straight and top rotated) for blitting on the screen
        pipeHeight = self.sprites['pipe'][0].get_height()
        offset = SCREENHEIGHT / 3
        y2 = offset + random.randrange(0, int(SCREENHEIGHT - self.sprites['base'].get_height() - 1.2 * offset))
        pipeX = SCREENWIDTH + 10
        y1 = pipeHeight - y2 + offset
        return [
            {'x': pipeX, 'y': -y1},  # upper Pipe
            {'x': pipeX, 'y': y2}  # lower Pipe
        ]

    def run(self):
        #Run the game loop indefinitely
        while True:
            self.welcome_screen()
            self.main_game()

if __name__ == "__main__":
    FlappyBirdGame().run()
