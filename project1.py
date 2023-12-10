import pygame
import random
import time
import sys

pygame.init()

WIDTH, HEIGHT = 800, 800
FPS = 60
WHITE = (255, 255, 255)
RED = (255, 0, 0)

circle_radius = 50
border_radius = 50
circle_spawn_time = 0.5
click_time_limit = 4
health = 100
points = 0

square_size = 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Klikaj Kółka!")

font = pygame.font.SysFont(None, 36)
input_font = pygame.font.SysFont(None, 48)

clock = pygame.time.Clock()
start_time = time.time()
circles = []


square_x = (WIDTH - square_size) // 2
square_y = (HEIGHT - square_size) // 2


def draw_circle():
    x = random.randint(circle_radius, WIDTH - circle_radius)
    y = random.randint(circle_radius, HEIGHT - circle_radius)
    circle_rect = pygame.draw.circle(screen, RED, (x, y), circle_radius)
    circles.append((circle_rect, time.time()))

def draw_square():
    pygame.draw.rect(screen, WHITE, (square_x, square_y, square_size, square_size), 2)

def draw_stats():
    health_text = font.render(f"Zdrowie: {health}", True, WHITE)
    points_text = font.render(f"Punkty: {points}", True, WHITE)
    screen.blit(health_text, (10, 10))
    screen.blit(points_text, (10, 50))

def save_score(username, points):
    with open("Wyniki.txt", "a") as file:
        file.write(f"{username}: {points}\n")

def draw_input_form():
    input_text = input_font.render("Podaj swoją nazwę użytkownika:", True, WHITE)
    screen.blit(input_text, (WIDTH // 2 - 200, HEIGHT // 2 - 50))

running = True
input_mode = False
username = ""

while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if input_mode:
                if WIDTH // 2 - 200 <= x <= WIDTH // 2 + 200 and HEIGHT // 2 <= y <= HEIGHT // 2 + 50:
                    input_mode = False
                    save_score(username, points)
                    print(f"Twój wynik: {points} punktów")
                    pygame.quit()
                    sys.exit()
            else:
                for circle, spawn_time in circles.copy():
                    circle_rect = circle.inflate(border_radius, border_radius)
                    if circle_rect.collidepoint(x, y) and time.time() - spawn_time <= click_time_limit:
                        points += 1
                        circles.remove((circle, spawn_time))

        elif event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_RIGHT, pygame.K_DOWN]:
                if not input_mode:
                    for circle, spawn_time in circles.copy():
                        if time.time() - spawn_time <= click_time_limit:
                            x, y = pygame.mouse.get_pos()
                            circle_rect = circle.inflate(border_radius, border_radius)
                            if circle_rect.collidepoint(x, y):
                                points += 1
                                circles.remove((circle, spawn_time))

            elif event.key == pygame.K_RETURN:
                if input_mode and username:
                    input_mode = False
                    save_score(username, points)
                    print(f"Twój wynik: {points} punktów")
                    pygame.quit()
                    sys.exit()
            elif event.key == pygame.K_BACKSPACE:
                if input_mode:
                    username = username[:-1]

            elif event.key == pygame.K_ESCAPE:
                if input_mode:
                    input_mode = False
                    username = ""

            elif event.key == pygame.KMOD_SHIFT and event.unicode:  
                pass

            elif event.key < 256:
                if input_mode:
                    username += event.unicode

    current_time = time.time()

    if current_time - start_time > circle_spawn_time and not circles:
        draw_circle()
        start_time = time.time()

    draw_square()

    for circle, spawn_time in circles.copy():
        pygame.draw.circle(screen, RED, circle.center, circle_radius)

    if not input_mode and current_time - start_time > circle_spawn_time:
        health -= 10
        circles = []

    draw_stats()

    if health <= 0:
        if not input_mode:
            input_mode = True
            username = ""

    if input_mode:
        draw_input_form()
        input_surface = input_font.render(username, True, WHITE)
        screen.blit(input_surface, (WIDTH // 2 - 50, HEIGHT // 2 + 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
