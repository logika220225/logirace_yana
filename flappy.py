import pygame
import random
import sys

pygame.init()

WIDTH = 400
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

bird_x = 80
bird_y = HEIGHT // 2
bird_radius = 20
bird_velocity = 0
gravity = 0.5
jump = -8

pipe_width = 70
pipe_gap = 170
pipe_velocity = 4

pipes = []

score = 0

def create_pipe():
    height = random.randint(100, 400)
    top_pipe = pygame.Rect(WIDTH, 0, pipe_width, height)
    bottom_pipe = pygame.Rect(
        WIDTH,
        height + pipe_gap,
        pipe_width,
        HEIGHT - height - pipe_gap
    )
    return top_pipe, bottom_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.x -= pipe_velocity
    return [pipe for pipe in pipes if pipe.x > -pipe_width]

def draw_pipes(pipes):
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, pipe)

def check_collision(pipes):
    bird_rect = pygame.Rect(
        bird_x - bird_radius,
        bird_y - bird_radius,
        bird_radius * 2,
        bird_radius * 2
    )

    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return True

    if bird_y <= 0 or bird_y >= HEIGHT:
        return True

    return False

running = True
frame_count = 0

while running:
    clock.tick(60)
    screen.fill(BLUE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = jump

    bird_velocity += gravity
    bird_y += bird_velocity

    frame_count += 1
    if frame_count % 90 == 0:
        pipes.extend(create_pipe())

    pipes = move_pipes(pipes)

    for pipe in pipes:
        if pipe.x == bird_x:
            score += 0.5

    if check_collision(pipes):
        game_over = font.render("GAME OVER", True, WHITE)
        screen.blit(game_over, (110, 250))
        pygame.display.update()
        pygame.time.delay(2000)
        running = False

    pygame.draw.circle(
        screen,
        YELLOW,
        (bird_x, int(bird_y)),
        bird_radius
    )

    draw_pipes(pipes)

    score_text = font.render(f"Score: {int(score)}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.update()

pygame.quit()
sys.exit()