import pygame
import random
import numpy as np
import sounddevice as sd
import time
pygame.init()
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")
background_image_path = r'C:\Users\Vimal Kumar\Downloads\flappybirdbg.png'
background_image = pygame.image.load(background_image_path)
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
pipe_top_image_path = r'C:\Users\Vimal Kumar\Downloads\toppipe.png'
pipe_bottom_image_path = r'C:\Users\Vimal Kumar\Downloads\bottompipe.png'
pipe_top_image = pygame.image.load(pipe_top_image_path)
pipe_bottom_image = pygame.image.load(pipe_bottom_image_path)
NEW_PIPE_WIDTH = 40 
PIPE_HEIGHT = pipe_top_image.get_height()
pipe_top_image = pygame.transform.scale(pipe_top_image, (NEW_PIPE_WIDTH, PIPE_HEIGHT))
pipe_bottom_image = pygame.transform.scale(pipe_bottom_image, (NEW_PIPE_WIDTH, PIPE_HEIGHT))
bird_image_path = r'C:\Users\Vimal Kumar\Downloads\flappybird.png'
bird_image = pygame.image.load(bird_image_path)
BIRD_SIZE = 15  # Adjust based on your image size
bird_image = pygame.transform.scale(bird_image, (BIRD_SIZE, BIRD_SIZE))
GRAVITY = 0.5
FLAP_STRENGTH = -10
PIPE_GAP = 400 
PIPE_SPEED = 3
THRESHOLD = 4  
FLAP_DELAY = 0.3  

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.rect = pygame.Rect(self.x, self.y, BIRD_SIZE, BIRD_SIZE)
        self.last_flap_time = time.time()
    def flap(self):
        current_time = time.time()
        if current_time - self.last_flap_time > FLAP_DELAY:
            self.velocity = FLAP_STRENGTH
            self.last_flap_time = current_time
    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        if self.y < 0:
            self.y = 0
            self.velocity = 0
        self.rect.y = self.y
        if self.y >= SCREEN_HEIGHT - BIRD_SIZE:
            self.y = SCREEN_HEIGHT - BIRD_SIZE
            self.velocity = 0
    def draw(self, screen):
        screen.blit(bird_image, (self.x, self.y))
class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)  # Randomize the height
        self.rect_top = pygame.Rect(self.x, 0, NEW_PIPE_WIDTH, self.height)
        self.rect_bottom = pygame.Rect(self.x, self.height + PIPE_GAP, NEW_PIPE_WIDTH, SCREEN_HEIGHT - self.height - PIPE_GAP)
        self.image_top = pygame.transform.scale(pipe_top_image, (NEW_PIPE_WIDTH, self.height))
        self.image_bottom = pygame.transform.scale(pipe_bottom_image, (NEW_PIPE_WIDTH, SCREEN_HEIGHT - self.height - PIPE_GAP))
    def update(self):
        self.x -= PIPE_SPEED
        self.rect_top.x = self.x
        self.rect_bottom.x = self.x
    def draw(self, screen):
        screen.blit(self.image_top, self.rect_top.topleft)
        screen.blit(self.image_bottom, self.rect_bottom.topleft)
def check_collision(bird, pipes):
    for pipe in pipes:
        if bird.rect.colliderect(pipe.rect_top) or bird.rect.colliderect(pipe.rect_bottom):
            return True
    if bird.y <= 0 or bird.y >= SCREEN_HEIGHT - BIRD_SIZE:
        return True
    return False
def draw_button(screen, text, x, y, width, height, font, color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    button_text = font.render(text, True, BLACK)
    text_rect = button_text.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(button_text, text_rect)
def main():
    global THRESHOLD
    clock = pygame.time.Clock()
    bird = Bird()
    pipes = [Pipe()]
    score = 0
    running = True
    game_started = False
    font = pygame.font.SysFont(None, 36)
    def audio_callback(indata, frames, time, status):
        volume = np.linalg.norm(indata)
        if volume > THRESHOLD:
            bird.flap()
    stream = sd.InputStream(callback=audio_callback)

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button.collidepoint(mouse_pos):
                    game_started = True
                    stream.start()
                if plus_button.collidepoint(mouse_pos):
                    THRESHOLD += 1
                if minus_button.collidepoint(mouse_pos):
                    THRESHOLD -= 1
        screen.blit(background_image, (0, 0))
        if game_started:
            bird.update()
            for pipe in pipes:
                pipe.update()
                if pipe.x + NEW_PIPE_WIDTH < 0:
                    pipes.remove(pipe)
                    pipes.append(Pipe())
                    score += 1
            if check_collision(bird, pipes):
                running = False
            bird.draw(screen)
            for pipe in pipes:
                pipe.draw(screen)
            text = font.render(f"Score: {score}", True, BLACK)
            screen.blit(text, (10, 10))
        else:
            start_button = pygame.Rect(150, 250, 100, 50)
            draw_button(screen, "Start", start_button.x, start_button.y, start_button.width, start_button.height, font, RED)
            plus_button = pygame.Rect(300, 100, 50, 50)
            minus_button = pygame.Rect(50, 100, 50, 50)
            draw_button(screen, "+", plus_button.x, plus_button.y, plus_button.width, plus_button.height, font, WHITE)
            draw_button(screen, "-", minus_button.x, minus_button.y, minus_button.width, minus_button.height, font, WHITE)
            threshold_text = font.render(f"Threshold: {THRESHOLD}", True, BLACK)
            screen.blit(threshold_text, (150, 100))
        pygame.display.flip()
    stream.stop()
    pygame.quit()
if __name__ == "__main__":
    main()