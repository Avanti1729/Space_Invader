import pygame
import random
import math
#todo ; add command line parameters to change the speed

pygame.init()
# setting screen size
screen = pygame.display.set_mode((800, 600))
# setting background image
background = pygame.image.load('background.png')

# setting caption of the game as Space Invaders
pygame.display.set_caption("Space Invaders")

# setting and displaying the icon of the game on the title bar
icon = pygame.image.load('rocket.png')
pygame.display.set_icon(icon)

# creating and setting up Player variable
playerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0

# creating a list of enemy variable
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

# setting the path of enemies (6 of them) and making them appear on the screen at random coordinates in for loop
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 759))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.2)
    enemyY_change.append(40)

# creating and setting up Bullet variable
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 0.5
bullet_state = "ready"

# creating variable for the value of score and adding font
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

over_font = pygame.font.Font('freesansbold.ttf', 64)

# creating the function to show the score value on the background screen
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

# creating the function to show GAME OVER on screen after the player and enemy have collided
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

# creating a function to draw the image of player on the screen
def player(x, y):
    screen.blit(playerImg, (x, y))

# creating a function to draw the images of multiple enemies of the screen and re-spawning them
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

# creating a function to draw the images of the bullet and to set its mode in motion
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

# creating a function to check if the bullet and enemy are colliding
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


running = True
# starting of while loop to run the program
while running:
    # setting up RGB value for screen
    screen.fill((0, 0, 0))
    # displaying background image on the window
    screen.blit(background, (0, 0))
    # starting of for loop to check if the user has pressed a keystroke
    for event in pygame.event.get():
        # to check if the user has pressed the cross button to quit the game
        if event.type == pygame.QUIT:
            running = False
        # condition to check if the user has pressed the right or left arrow
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
    # end of for loop
    # to change the value of player if the user has pressed the left or right arrow
    playerX += playerX_change

    # An if , elif condition to make the player stay in bounds
    if playerX <= 0:
        playerX = 0
    elif playerX >= 732:
        playerX = 732

    # starting of another for loop to continuously change the coordinates of the enemies
    for i in range(num_of_enemies):
        # if enemy gets close to the player then end the game and break out from the WHILE loop
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 760:
            enemyX_change[i] = -0.2
            enemyY[i] += enemyY_change[i]
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        # if collision occurs then the value of score increases and the bullet is back to its original "ready" state
        if collision:
            score_value += 1
            bulletY = 480
            bullet_state = "ready"
            enemyX[i] = random.randint(0, 759)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)
    # end of for loop
    # if statement to make the bullet go back to the original position after going out of boundary
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    # if statement which will decrease the Y coordinates of the bullet in order to make it move
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # calling all the functions created
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
