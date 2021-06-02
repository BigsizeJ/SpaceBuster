#import module
import pygame
import random
import math


#init pygame
pygame.init()

#screen
screen = pygame.display.set_mode((800, 600))

#setup app detail
pygame.display.set_caption("Space Buster")

#main background
background = pygame.image.load("background.png")

#player img and variable
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0

#bullet img and variable
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

#enemy img and variable
enemyImg = []
enemyX = []
enemyY = []
enemyY_change = []
num_of_enemies = 4
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("rock.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(0)
    enemyY_change.append(4.5)

#distance function
def Collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY,2)))
    if distance < 27:
        return True
    else:
        return False

def PlayerCollision(enemyX, enemyY, playerX, playerY):
    playerdistance = math.sqrt((math.pow(enemyX - playerX, 2)) + (math.pow(enemyY - playerY,2)))
    if playerdistance < 50:
        return True
    else:
        return False

#player function
def player(x, y):
    screen.blit(playerImg, (x, y))

#bullet function
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

#enemy function
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

#score variable and function
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textY = 10
textX = 10

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))

#Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

#mainfunction
running = True

while running:

    #init background display
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        #pressing key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerX_change = 2
            if event.key == pygame.K_LEFT:
                playerX_change = -2
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0

    #player setup
    player(playerX, playerY)
    playerX += playerX_change
    if playerX >= 736:
        playerX = 736
    elif playerX <= 0:
        playerX = 0

    #bullet setup
    if bulletY <= -10:
        bulletY = 480
        bullet_state = "ready"
    
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    #enemy setup and collision
    for i in range(num_of_enemies):
        
        enemyY[i] += enemyY_change[i]

        collision_for_player = PlayerCollision(enemyX[i], enemyY[i], playerX, playerY)
        if collision_for_player:
            for j in range(num_of_enemies):
                enemyY_change[i] = 0
                playerX_change = 0
            game_over_text()
            break

        if enemyY[i] >= 650:
            enemyX[i] = 0
            enemyY[i] = 0
            enemyX[i] = random.randint(0, 736)

        collision = Collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 5
            enemyX[i] = 5000
        enemy(enemyX[i], enemyY[i], i)


    #show score
    show_score(textX, textY)
    



    #update
    pygame.display.update()