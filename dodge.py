import pygame
import random
import time

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge Jet")

# Load images
jet_img = pygame.image.load("jet.png")
succinct_img = pygame.image.load("succinct.png")
bomb_img = pygame.image.load("bomb.png")
star_img = pygame.image.load("star.png")
heart_img = pygame.image.load("heart.png")
lightning_img = pygame.image.load("lighten.png")
info_icon = pygame.image.load("icon.png")
background_img = pygame.image.load("general background.jpeg")

# Resize images
jet_img = pygame.transform.scale(jet_img, (60, 60))
succinct_img = pygame.transform.scale(succinct_img, (40, 40))
bomb_img = pygame.transform.scale(bomb_img, (50, 50))
star_img = pygame.transform.scale(star_img, (40, 40))
heart_img = pygame.transform.scale(heart_img, (30, 30))
lightning_img = pygame.transform.scale(lightning_img, (40, 40))
info_icon = pygame.transform.scale(info_icon, (40, 40))
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Game variables
jet_x, jet_y = WIDTH // 2, HEIGHT - 80
jet_speed = 5
score = 0
lives = 3
shield_active = False
shield_timer = 0
speed_boost = False
speed_timer = 0
falling_speed = 4  # Base falling speed

# Falling objects
succincts = []
bombs = []
stars = []
lightnings = []

# Function to create objects
def create_object(obj_list, img, width, height):
    obj_list.append([random.randint(0, WIDTH - width), -height])

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.blit(background_img, (0, 0))  # Set background

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move jet
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and jet_x > 0:
        jet_x -= jet_speed
    if keys[pygame.K_RIGHT] and jet_x < WIDTH - 60:
        jet_x += jet_speed

    # Manage shield timer
    if shield_active and time.time() - shield_timer > 10:
        shield_active = False

    # Manage speed boost timer
    if speed_boost and time.time() - speed_timer > 6.5:
        speed_boost = False
        falling_speed = 4

    # Spawn objects
    if random.randint(1, 100) > 98:
        create_object(succincts, succinct_img, 40, 40)
    if random.randint(1, 100) > 90:
        create_object(bombs, bomb_img, 50, 50)
    if random.randint(1, 500) > 495:
        create_object(stars, star_img, 40, 40)
    if random.randint(1, 500) > 498:
        create_object(lightnings, lightning_img, 40, 40)

    # Move and draw objects
    for obj_list, img, effect in [
        (succincts, succinct_img, "score"),
        (bombs, bomb_img, "bomb"),
        (stars, star_img, "shield"),
        (lightnings, lightning_img, "speed")
    ]:
        for obj in obj_list:
            obj[1] += falling_speed
            screen.blit(img, (obj[0], obj[1]))

            # Collision detection
            if jet_x < obj[0] < jet_x + 60 and jet_y < obj[1] < jet_y + 60:
                if effect == "score":
                    score += 10
                elif effect == "bomb" and not shield_active:
                    lives -= 1
                elif effect == "shield":
                    shield_active = True
                    shield_timer = time.time()
                elif effect == "speed":
                    speed_boost = True
                    speed_timer = time.time()
                    falling_speed = 12  # Speed boost makes the game 3x faster

                obj_list.remove(obj)

    # Draw jet
    screen.blit(jet_img, (jet_x, jet_y))

    # Draw shield if active
    if shield_active:
        pygame.draw.circle(screen, (255, 255, 0, 128), (jet_x + 30, jet_y + 30), 40, 2)

    # Display lives
    for i in range(lives):
        screen.blit(heart_img, (10 + i * 35, 10))

    # Display score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (WIDTH - 150, 10))

    # Display info icon
    screen.blit(info_icon, (WIDTH - 50, HEIGHT - 50))

    # Check for game over
    if lives <= 0:
        screen.fill((0, 0, 0))
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(3000)
        running = False

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
