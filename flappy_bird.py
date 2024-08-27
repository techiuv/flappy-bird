import pygame
import random
import os

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game settings
GRAVITY = 0.25
FLAP_POWER = -6
PIPE_SPEED = 4
PIPE_GAP = 150

# Load assets 
ASSETS_DIR = 'assets'
bird_img = pygame.image.load(os.path.join(ASSETS_DIR, 'bird.png'))
bg_img = pygame.image.load(os.path.join(ASSETS_DIR, 'background.png'))
pipe_img = pygame.image.load(os.path.join(ASSETS_DIR, 'pipe.png'))
base_img = pygame.image.load(os.path.join(ASSETS_DIR, 'base.png'))
flappy_font = pygame.font.Font(os.path.join(ASSETS_DIR, 'flappy_font.ttf'), 36)

# Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird Advanced')

clock = pygame.time.Clock()

class Bird:
    def __init__(self):
        self.rect = bird_img.get_rect(center=(50, SCREEN_HEIGHT // 2))
        self.movement = 0

    def flap(self):
        self.movement = FLAP_POWER
        
    def update(self):
        self.movement += GRAVITY
        self.rect.centery += self.movement
        screen.blit(bird_img, self.rect)

    def check_collision(self, pipes, base):
        for pipe in pipes:
            if self.rect.colliderect(pipe.rect):
                 
                return False
        if self.rect.bottom >= base.y or self.rect.top <= 0:
            
            return False
        return True

class Pipe:
    def __init__(self, x):
        self.height = random.choice([300, 400, 500])
        self.rect = pipe_img.get_rect(midtop=(x, self.height + PIPE_GAP))
        self.top_rect = pipe_img.get_rect(midbottom=(x, self.height - PIPE_GAP))

    def move(self):
        self.rect.centerx -= PIPE_SPEED
        self.top_rect.centerx -= PIPE_SPEED
        screen.blit(pipe_img, self.rect)
        flip_pipe = pygame.transform.flip(pipe_img, False, True)
        screen.blit(flip_pipe, self.top_rect)

class Base:
    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = base_img.get_width()

    def move(self):
        self.x1 -= PIPE_SPEED
        self.x2 -= PIPE_SPEED
        if self.x1 <= -base_img.get_width():
            self.x1 = self.x2 + base_img.get_width()
        if self.x2 <= -base_img.get_width():
            self.x2 = self.x1 + base_img.get_width()

        screen.blit(base_img, (self.x1, self.y))
        screen.blit(base_img, (self.x2, self.y))

def create_pipe():
    return Pipe(SCREEN_WIDTH)

def display_score(score):
    score_surface = flappy_font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_surface, (SCREEN_WIDTH // 2 - score_surface.get_width() // 2, 50))

def game_over_screen(score, high_score):
    game_over_surface = flappy_font.render('Game Over', True, WHITE)
    score_surface = flappy_font.render(f'Score: {score}', True, WHITE)
    high_score_surface = flappy_font.render(f'High Score: {high_score}', True, WHITE)
    
    screen.blit(game_over_surface, (SCREEN_WIDTH // 2 - game_over_surface.get_width() // 2, 150))
    screen.blit(score_surface, (SCREEN_WIDTH // 2 - score_surface.get_width() // 2, 250))
    screen.blit(high_score_surface, (SCREEN_WIDTH // 2 - high_score_surface.get_width() // 2, 300))
    
    pygame.display.update()
    pygame.time.wait(2000)

def main_game():
    bird = Bird()
    base = Base(SCREEN_HEIGHT - 100)
    pipes = [create_pipe()]
    score = 0
    high_score = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()

        bird.update()

        for pipe in pipes:
            pipe.move()

        base.move()

        # Add new pipe and remove old pipes
        if pipes[-1].rect.centerx < SCREEN_WIDTH // 2:
            pipes.append(create_pipe())
        if pipes[0].rect.centerx < -pipe_img.get_width():
            pipes.pop(0)
            score += 1
            # score_sound.play()  

        if not bird.check_collision(pipes, base):
            if score > high_score:
                high_score = score
            game_over_screen(score, high_score)
            return

        display_score(score)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main_game()
