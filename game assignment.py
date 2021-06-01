import pygame
import random
import math
from pygame import mixer

pygame.init()



# Create the screen
screen = pygame.display.set_mode((800, 600))

# Create background
background = pygame.image.load('background.png')

# background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# title and icon
pygame.display.set_caption("MONSTER SHOOTER")
icon = pygame.image.load("monster.png")
pygame.display.set_icon(icon)

# Adding player
playerImg = pygame.image.load('shooter.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# adding enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 10

for i in range(num_of_enemies):
    for j in range(1,4):
        enemyImg.append(pygame.image.load('monster.png'))
        enemyX.append(random.randint(0,735))
        enemyY.append(random.randint(50, 150))
    # increase the speed based upon your needs
    enemyX_change.append(1)
    enemyY_change.append(40)

bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1

# ready state - you can't see bullet on screen
# fire state - bullet moving currently

bullet_state = "ready"
# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10


# Game over text
over_font = pygame.font.Font('freesansbold.ttf', 68)

# Game loop
running = True



def show_score(x, y):
    score = font.render("Score : " + str(score_value) + " Highscore" + str(highscore), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))

    if distance < 27:
        return True
    else:
        return False


while running:
    screen.fill((58, 0, 28))
    screen.blit(background, (0, 0))


    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                playerX_change = -1

            if event.key == pygame.K_RIGHT:
                playerX_change = 1

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    # Get the current x coordinate of the player
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT :
                playerX_change = 0



    playerX += playerX_change


    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

        # Creating boundaries
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
        # Enemy movement
    for i in range(num_of_enemies):
        # Game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            with open("highscore.txt","w") as f:
                f.write(str(highscore))
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.5
            enemyY[i] += enemyY_change[i]
        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            # Reset the bullet
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)
        with open("highscore.txt", "r") as f:
            highscore = f.read()
        if score_value > int(highscore):
            highscore = score_value
        # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)

    pygame.display.update()








