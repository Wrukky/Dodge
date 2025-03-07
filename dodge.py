import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge Jet")

# Load assets
jet_img = pygame.image.load("jet.png")
succinct_img = pygame.image.load("succinct.png")
bomb_img = pygame.image.load("bomb.png")
star_img = pygame.image.load("star.png")
lightning_img = pygame.image.load("lighten.png")
heart_img = pygame.image.load("heart.png")
info_icon = pygame.image.load("icon.png")
background_img = pygame.image.load("general background.jpeg")

# Resize images
jet_img = pygame.transform.scale(jet_img, (70, 70))
succinct_img = pygame.transform.scale(succinct_img, (120, 120))  # 3x bigger
bomb_img = pygame.transform.scale(bomb_img, (50, 50))
star_img = pygame.transform.scale(star_img, (40, 40))
lightning_img = pygame.transform.scale(lightning_img, (50, 50))
heart_img = pygame.transform.scale(heart_img, (30, 30))
info_icon = pygame.transform.scale(info_icon, (40, 40))
background_img = pygame.image.load("light pink.jpeg")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))


# Font setup
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 50)

# Game variables
jet_x, jet_y = WIDTH // 2, HEIGHT - 80
base_speed = 5  # Base speed of jet
jet_speed = base_speed
lives = 3
score = 0
shield_active = False
shield_timer = 0
speed_boost = False
speed_boost_timer = 0

# Falling objects lists
succincts = []
bombs = []
stars = []
lightnings = []

# Create falling objects
def create_object(obj_list, img, speed):
    x = random.randint(50, WIDTH - 50)
    y = random.randint(-150, -50)
    obj_list.append({"x": x, "y": y, "speed": speed, "img": img})

# Draw game objects
def draw_objects(obj_list):
    for obj in obj_list:
        screen.blit(obj["img"], (obj["x"], obj["y"]))

# Move falling objects (Faster movement)
def move_objects(obj_list, speed_multiplier=1):
    for obj in obj_list:
        obj["y"] += obj["speed"] * speed_multiplier
    return [obj for obj in obj_list if obj["y"] < HEIGHT]

# Collision check (Adjusted for bigger succinct icon)
def check_collision(player_x, player_y, obj_list, obj_width, obj_height):
    for obj in obj_list:
        if player_x < obj["x"] + obj_width and player_x + 70 > obj["x"]:
            if player_y < obj["y"] + obj_height and player_y + 70 > obj["y"]:
                obj_list.remove(obj)
                return True
    return False

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    screen.blit(background_img, (0, 0))

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and jet_x > 0:
        jet_x -= jet_speed
    if keys[pygame.K_RIGHT] and jet_x < WIDTH - 70:
        jet_x += jet_speed

    # Create falling objects
    if random.randint(1, 50) == 1:
        create_object(succincts, succinct_img, 6)  # Faster succinct fall
    if random.randint(1, 25) == 1:  # More bombs now
        create_object(bombs, bomb_img, 7)  # Faster bombs
    if random.randint(1, 300) == 1:
        create_object(stars, star_img, 6)
    if random.randint(1, 400) == 1:
        create_object(lightnings, lightning_img, 7)

    # Move objects (Speed boost affects falling speed too)
    speed_multiplier = 3 if speed_boost else 1
    succincts = move_objects(succincts, speed_multiplier)
    bombs = move_objects(bombs, speed_multiplier)
    stars = move_objects(stars, speed_multiplier)
    lightnings = move_objects(lightnings, speed_multiplier)

    # Check collisions with correct sizes
    if check_collision(jet_x, jet_y, succincts, 120, 120):  # Adjusted for bigger succinct
        score += 1
    if check_collision(jet_x, jet_y, bombs, 50, 50) and not shield_active:
        lives -= 1
        if lives == 0:
            running = False
    if check_collision(jet_x, jet_y, stars, 40, 40):
        shield_active = True
        shield_timer = time.time()
    if check_collision(jet_x, jet_y, lightnings, 50, 50):
        speed_boost = True
        speed_boost_timer = time.time()
        jet_speed = base_speed * 3  # Jet moves 3x faster

    # Shield Timer (10s duration)
    if shield_active and time.time() - shield_timer > 10:
        shield_active = False

    # Speed Boost Timer (6.5s duration)
    if speed_boost and time.time() - speed_boost_timer > 6.5:
        speed_boost = False
        jet_speed = base_speed  # Reset speed

    # Draw player
    screen.blit(jet_img, (jet_x, jet_y))

    # Draw shield
    if shield_active:
        pygame.draw.circle(screen, (255, 255, 0), (jet_x + 35, jet_y + 35), 40, 3)

    # Show "2x Speed" when boosted
    if speed_boost:
        speed_text = font.render("3x Speed!", True, (255, 255, 0))
        screen.blit(speed_text, (jet_x + 20, jet_y - 30))

    # Draw objects
    draw_objects(succincts)
    draw_objects(bombs)
    draw_objects(stars)
    draw_objects(lightnings)

    # Draw score and lives
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    for i in range(lives):
        screen.blit(heart_img, (WIDTH - 110 + (i * 35), 10))

    # Draw info icon
    screen.blit(info_icon, (WIDTH - 50, HEIGHT - 50))

    # Update display
    pygame.display.flip()
    clock.tick(30)

# Game over screen
screen.fill((0, 0, 0))
game_over_text = title_font.render("GAME OVER", True, (255, 0, 0))
final_score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
screen.blit(final_score_text, (WIDTH // 2 - 70, HEIGHT // 2 + 10))
pygame.display.flip()
time.sleep(3)

pygame.quit()
