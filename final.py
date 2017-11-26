import pygame, random, sys ,os,time
from pygame.locals import *


# Height and Width of Screen
WINDOWWIDTH = 800
WINDOWHEIGHT = 600

# Colours
TEXTCOLOR = (255, 255, 0)
BACKGROUNDCOLOR = (0, 0, 0)

FPS = 40
OBSTACLEMINSPEED = 6
OBSTACLEMAXSPEED = 8
ADDNEWOBSTACLERATE = 18
PLAYERMOVERATE = 5
count=3

def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return

def playerHasHitobstacle(playerRect, obstacles):
    for b in obstacles:
        if playerRect.colliderect(b['rect']):
            return True
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# set up pygame, the window, and the mouse cursor
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Galactic Warrior')



#fonts
font = pygame.font.SysFont(None, 30)


# Images
playerImage = pygame.image.load('image/ship.png')
playerRect = playerImage.get_rect()
meteor = pygame.image.load('image/meteor.png')
planet1 = pygame.image.load('image/planet1.png')
planet2= pygame.image.load('image/planet2.png')
satellite = pygame.image.load('image/satellite.png')
alien = pygame.image.load('image/alien.png')
bg = pygame.image.load('image/bg.jpg')
logo = pygame.image.load('image/logo.png')
start = pygame.image.load('image/start.png')
sample = [meteor,planet1,planet2,satellite,alien,meteor]


#sounds
pygame.mixer.init()
music_file = 'soundtrack.mp3'
pygame.mixer.music.load(music_file)
pygame.mixer.music.play(-1)

windowSurface.blit(bg,(-250,-200))
windowSurface.blit(logo,(190,100))
windowSurface.blit(start,(105,400))
pygame.display.update()
waitForPlayerToPressKey()

zero=0

# Initial Top Score
if not os.path.exists("save.dat"):
    f=open("save.dat",'w')
    f.write(zero)
    f.close()   
v=open("save.dat",'r')
topScore = int(v.readline())
v.close()

# Game Loop-------------
while (count>0):

    # start of the game
    obstacles = []
    score = 0
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    obstacleAddCounter = 0

    while True:
        windowSurface.blit(bg,(-250,-200))
        score +=1
        for event in pygame.event.get():
            
            if event.type == QUIT:
                terminate()

            # Key events when pressed
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT:
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP:
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN:
                    moveUp = False
                    moveDown = True

            # Key events when key lifted up
            if event.type == KEYUP:
                if event.key == K_ESCAPE:   
                        terminate()
                if event.key == K_LEFT:
                    moveLeft = False
                if event.key == K_RIGHT:
                    moveRight = False
                if event.key == K_UP:
                    moveUp = False
                if event.key == K_DOWN:
                    moveDown = False
        
        # Add new obstacles    
        obstacleAddCounter +=1
        if obstacleAddCounter == ADDNEWOBSTACLERATE:
            obstacleAddCounter = 0
            obstacleSize =70 
            newobstacle = {'rect': pygame.Rect(random.randint(10, 790), 0 - obstacleSize, 25, 25),
                        'speed': random.randint(OBSTACLEMINSPEED, OBSTACLEMAXSPEED),
                        'surface':pygame.transform.scale(random.choice(sample), (60, 60)),
                        }
            obstacles.append(newobstacle)

        # Move the player around.
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)


        for b in obstacles:
            b['rect'].move_ip(0,b['speed'])

        for b in obstacles:
            if b['rect'].top > WINDOWHEIGHT:
                obstacles.remove(b)  



        # Score
        drawText('Score: %s' % (score), font, windowSurface, 0, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface,0, 20)
        drawText('Rest Life: %s' % (count), font, windowSurface,0, 40)
        windowSurface.blit(playerImage, playerRect)
        for b in obstacles:
            windowSurface.blit(b['surface'], b['rect'])
        
        pygame.display.update()

        #Check if obstuction is hit by the player
        if playerHasHitobstacle(playerRect, obstacles):
            if score > topScore:
                g=open("save.dat",'w')
                g.write(str(score))
                g.close()
                topScore = score
            break
        mainClock.tick(FPS)

        # Difficulty Levels
        if(score == 500):
            ADDNEWOBSTACLERATE = 15
        elif(score == 1000):
            ADDNEWOBSTACLERATE = 12
        elif(score == 1500):
            ADDNEWOBSTACLERATE = 9
        elif(score == 2000):
            ADDNEWOBSTACLERATE = 6



    # Game Over Screen    
    count=count-1
    time.sleep(1)
    if (count==0):
        windowSurface.fill(BACKGROUNDCOLOR)
        img = pygame.image.load('image/game over.jpg')
        windowSurface.blit(img, (0,0))
        pygame.display.update()
        time.sleep(2)
        waitForPlayerToPressKey()
        count=3
        ADDNEWOBSTACLERATE = 18
