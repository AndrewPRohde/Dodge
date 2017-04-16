import pygame, random, sys
from pygame.locals import *

WINDOWWIDTH = 600
WINDOWHEIGHT = 600
TEXTCOLOR = (0, 0, 0)
BACKGROUNDCOLOR = (255, 255, 255)
FPS = 60
ENEMYMINSIZE = 10
ENEMYMAXSIZE = 40
ENEMYMINSPEED = 1
ENEMYMAXSPEED = 8
ADDNEWENEMYRATE = 6
PLAYERMOVERATE = 5

def terminate():
    pygame.quit()
    sys.exit()
    
def waitForPlayerInteraction():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    # Escape key quits game
                    terminate()
                return
            
def playerHasHitEnemy(playerRECT, enemies):
    for e in enemies:
        if playerRect.colliderect(e['rect']):
            return True
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
    
# create pygame, the window, and the cursor
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Dodge')
pygame.mouse.set_visible(False)

# set up font
font = pygame.font.SysFont(None, 48)

# set up sound
gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('background.mid')

# set up graphics
playerImage = pygame.image.load('player.png')
playerRect = playerImage.get_rect()
enemyImage = pygame.image.load('enemy.png')

# show start screen
windowSurface.fill(BACKGROUNDCOLOR)
drawText('Dodge', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText('Press any key to start', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerInteraction()

topScore = 0
while True:
    # Set up game start
    enemies = []
    score = 0
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    enemyAddCounter = 0
    pygame.mixer.music.play(-1, 0.0)
    
    while True:
    # the game loop plays while game is active
        score += 1
    
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            
            if event.type == KEYDOWN:
                if event.key == ord('z'):
                    reverseCheat = True
                if event.key == ord('x'):
                    slowCheat = True
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True
                
            if event.type == KEYUP:
                if event.key == ord('z'):
                    reverseCheat = False
                    score = 0
                if event.key == ord('x'):
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                    terminate()
                    
                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False
                
            if event.type == MOUSEMOTION:
                # Move the player to where the mouse is
                playerRect.move_ip(event.pos[0] - playerRect.centerx, event.pos[1] - playerRect.centery)
            
        # spawn enemies at top
        if not reverseCheat and not slowCheat:
            enemyAddCounter += 1
        if enemyAddCounter == ADDNEWENEMYRATE:
            enemyAddCounter = 0
            enemySize = random.randint(ENEMYMINSIZE, ENEMYMAXSIZE)
            newEnemy = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH-enemySize), 0 - enemySize, enemySize, enemySize), 'speed': random.randint(ENEMYMINSPEED, ENEMYMAXSPEED), 'surface': pygame.transform.scale(enemyImage, (enemySize, enemySize)), }
            enemies.append(newEnemy)
        
        # player movement
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)
        
        # mouse player movement
        pygame.mouse.set_pos(playerRect.centerx, playerRect.centery)
        
        # move enemies
        for e in enemies:
            if not reverseCheat and not slowCheat:
                e['rect'].move_ip(0, e['speed'])
            elif reverseCheat:
                e['rect'].move_ip(0, -5)
            elif slowCheat:
                e['rect'].move_ip(0, 1)
            
        # remove enemies from bottom
        for e in enemies[:]:
            if e['rect'].top > WINDOWHEIGHT:
                enemies.remove(e)
            
        # Draw gameboard
        windowSurface.fill(BACKGROUNDCOLOR)
    
        # Draw scores
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('High Score: %s' % (topScore), font, windowSurface, 10, 40)
    
        # Draw player icon
        windowSurface.blit(playerImage, playerRect)
    
        # Draw Enemies
        for e in enemies:
            windowSurface.blit(e['surface'], e['rect'])
    
        pygame.display.update()
    
        # Check for player collision
        if playerHasHitEnemy(playerRect, enemies):
            if score > topScore:
                topScore = score
            break
        mainClock.tick(FPS)
    
    # Display Game over screen
    pygame.mixer.music.stop()
    gameOverSound.play()
    
    drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    drawText('Press any key to restart', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerInteraction()
    
    gameOverSound.stop()
            
        
        
        
        
        
        
        
        