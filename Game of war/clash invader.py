import pygame
import random
import math
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((800, 600))

#Background Music
mixer.music.load( "background.wav")
mixer.music.play(-1 )

pygame.display.set_caption("Clash Invaders")
icon = pygame.image.load("spaceship.png")
# image of size 32 px download from flaticons
pygame.display.set_icon(icon)
clock=pygame.time.Clock()

background = pygame.image.load("14658088_5509862.jpg")

bulletimg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bullet_xchange = 0
bullet_ychange = 1
bullet_state = "ready"
heart=pygame.image.load("heart.png")
score=0
life=3
font=pygame.font.Font('freesansbold.ttf',50)
textx=10
texty=10
def showscore(x,y):
    score_value=font.render("Score : "+str(score),True,(255,255,255))
    screen.blit(score_value,(x,y))

def showlife(x,y):
    life_value = font.render("Life: " , True, (255, 255, 255))
    screen.blit(life_value,(x,y))
    for j in range(life):
        screen.blit(heart,(x+125 +70*j,y-8))

over_font=pygame.font.Font('freesansbold.ttf',64)
def game_over_text():
    over_text = over_font.render("Game Over", True, (255, 255, 255))
    screen.blit(over_text, (200,250))

over_font2=pygame.font.Font('freesansbold.ttf',50)
def introtext():
    over_text = over_font2.render("Press Space Key to start Game", True, (255, 255, 255))
    screen.blit(over_text, (20, 250))

# ready state means that bullet hasent been fired yet
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))


playerimg = pygame.image.load("spaceship (1).png")
playerX = 370
playerY = 480
player_xchange = 0
def player(x, y):
    screen.blit(playerimg, (x, y))

enemyimg=[]
enemyX=[]
enemyY=[]
enemy_xchange=[]
enemy_ychange=[]
no_of_enemies=6
for j in range(no_of_enemies): #for multiple enemies
    enemyimg.append(pygame.image.load("alien (1).png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(50)
    enemy_xchange.append(0)
    enemy_ychange.append(0.2)


def enemy(x, y,j):
    screen.blit(enemyimg[j], (x, y))


def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 35:
        return True
    else:
        return False

def iscollision2(enemyX, enemyY, playerX, playerY):
    distance = math.sqrt((math.pow(enemyX - playerX, 2)) + (math.pow(enemyY - playerY, 2)))
    if distance < 60:
        return True
    else:
        return False

play=True
running = True
gameover=False
intro=True
while intro:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    introtext()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                intro = False
        if event.type == pygame.QUIT:
            intro = False
            running=False
    pygame.display.update()
a=-1
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    if life <=0:
        game_over_text()
        gameover=True
        running=False
    if play:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_xchange = -0.5
                elif event.key == pygame.K_RIGHT:
                    player_xchange = 0.5
                elif event.key == pygame.K_SPACE:
                    if bullet_state == "ready":  # if multiple spacebars are pressed so again & again x coredinate was changing!
                        bullet_sound=mixer.Sound("laser.wav")
                        bullet_sound.play()
                        bulletX = playerX  # to make sure that bullet moves straight forward after being fired
                        fire_bullet(bulletX, bulletY)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player_xchange = 0
            if event.type == pygame.QUIT:
                running = False
        playerX += player_xchange
        # checking of boundaries
        if playerX < 0:
            playerX = 0
        if playerX >= 736:
            playerX = 736  # 800-64 the size of the image

        for j in range(no_of_enemies):
            #game over
            if enemyY[j]>440:
                enemyY[j]=50
                enemyX[j]=random.randint(0, 735)

            if score !=0 and score %8==0 and a!=score:
                for p in range(no_of_enemies):
                    enemy_ychange[p]+=0.05
                a=max(a,score)

            enemyY[j]+=enemy_ychange[j]


            collision = iscollision(enemyX[j], enemyY[j], bulletX, bulletY)
            if collision:
                bulletY = 480
                bullet_state = "ready"
                score += 1
                collision_sound = mixer.Sound("explosion.wav")
                collision_sound.play()



                enemyX[j] = random.randint(100, 700)
                enemyY [j]= 50



            collision2=iscollision2(enemyX[j], enemyY[j], playerX, playerY)
            if collision2:
                collision_sound = mixer.Sound("explosion2.mp3")
                collision_sound.play()
                life-=1
                enemyX[j] = random.randint(100, 700)
                enemyY[j] = 50
            enemy(enemyX[j], enemyY[j], j)



        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"
        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bullet_ychange
        player(playerX, playerY)
        showscore(textx,texty)
        showlife(350,10)
        pygame.display.update()

while gameover:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameover = False
    game_over_text()
    showscore(textx, texty)
    pygame.display.update()