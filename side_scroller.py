import pygame
import random

pygame.init()
screen_width = 500
screen_height =450
win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Side Scroller")
background_x = 0
background_x2 = screen_width

#loading images
background = pygame.image.load("images\\background.png")
character = [pygame.image.load("images\\chickR%s.png" % frame) for frame in range(1, 6)]
character_slide = [pygame.image.load("images\\chick_slide%s.png"%frame) for frame in range (1,8)]
#try try git hub

#loading music
'''
bgm = pygame.mixer.music.load("music\\bgm.mp3") 
pygame.mixer.music.set_volume(0.5)
'''
bgm = pygame.mixer.Sound("music\\bgm.wav")
bgm.set_volume(0.5)
slide_sound = pygame.mixer.Sound("music\\slide.wav")
jump_sound = pygame.mixer.Sound("music\\jump.wav")
crash_sound = pygame.mixer.Sound("music\\crash.wav")
laugh_sound = pygame.mixer.Sound("music\\laugh.wav")


class hitboxes:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def update(self,x ,y):
        self.x = x
        self.y = y

class spikes:
    image = pygame.image.load("images\\spike.png")

    def __init__(self,x, y, velocity):
        self.x = x
        self.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.hitbox = hitboxes(self.x + 9, self.y +20 , self.width - 27 , self.height - 20)
        self.velocity = velocity

    def redraw(self, win):
        self.x -= self.velocity
        self.hitbox.x = self.x + 9
        win.blit(self.image, (self.x, self.y))
        #pygame.draw.rect(win, (255, 0, 0), (self.hitbox.x, self.hitbox.y, self.hitbox.width, self.hitbox.height), 2)

class rocks:
    image = pygame.image.load("images\\rock.png")
    def __init__(self, x, y, velocity):
        self.x = x
        self.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.velocity = velocity
        self.hitbox = hitboxes(self.x, self.y + 40, self.width - 10, self.height - 40)

    def redraw(self, win):
        self.x -= self.velocity
        win.blit(self.image, (self.x, self.y))
        self.hitbox.x = self.x
        self.hitbox.y = self.y + 40
        #pygame.draw.rect(win,(255,0,0), (self.hitbox.x, self.hitbox.y, self.hitbox.width, self.hitbox.height), 2)

class bees:
    image = [pygame.image.load("images\\bee%s.png"%frame)for frame in range(1,5)]
    flyCount = 0
    def __init__(self, x, y, velocity):
        self.x = x
        self.y = y
        self.width = self.image[0].get_width()
        self.height = self.image[0].get_height()
        self.velocity = velocity
        self.hitbox = hitboxes(self.x + 10, self.y + 10, self.width - 15, self.height-10)

    def redraw(self, win):
        self.x -= self.velocity
        self.flyCount += 1
        win.blit(self.image[self.flyCount%4], (self.x, self.y))
        self.hitbox.x = self.x + 10
        self.hitbox.y = self.y + 10
        #pygame.draw.rect(win, (255, 0, 0), (self.hitbox.x, self.hitbox.y, self.hitbox.width, self.hitbox.height), 2)

class buttons:
    def __init__(self, x, y,width, height, colour):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.colour = colour

    def redraw(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(win, (0,0,0), (self.x, self.y, self.width, self.height), 2)

    def isOver(self, mouse_x, mouse_y):
        if (self.x < mouse_x < self.x + self.width) and (self.y < mouse_y < self.y + self.height):
            return True
        else :
            return False

#jumping function
def jump():
    global jumpCount, initjumpCount, character_y, isJump, play_jumpSound
    if not play_jumpSound:
        play_jumpSound = True
        jump_sound.play()
    if jumpCount >= -initjumpCount:
        character_y -= jumpCount
        jumpCount -= 1
    else:
        isJump = False
        play_jumpSound = False
        jumpCount = initjumpCount

#sliding function
def slide():
    global slideCount, character_hitbox, play_slideSound
    if not play_slideSound:
        slide_sound.play()
        play_slideSound = True
    character_hitbox.y = character_y + 40
    #print("character_hitbox.y : ", character_hitbox.y)
    character_hitbox.height = character[0].get_height()-40
    #print("character_hitbox.height : ", character_hitbox.height)
    win.blit(character_slide[slideCount],(character_x, character_y))
    if slideCount < 6:
        slideCount += 1

#draw the startscreem
def startscreen():
    run = True
    win.blit(background, (background_x, 0))
    font = pygame.font.SysFont("tahoma", 20, bold=True)
    pressstart_text = font.render("Press to Start", True, [123, 140, 149])
    win.blit(pressstart_text, ((screen_width - pressstart_text.get_width())//2, 120))
    start_text = font.render("Start", True, (255, 255, 255))
    start_button = buttons(200, 200, 100, 30, [123, 140, 149])
    credit_text = font.render("Credit", True, (255, 255, 255))
    credit_button = buttons(200, 250, 100, 30, [123, 140, 149])
    while run:
        start_button.redraw(win)
        win.blit(start_text, (start_button.x + (start_button.width - start_text.get_width())//2,
                             start_button.y + (start_button.height - start_text.get_height())//2))
        credit_button.redraw(win)
        win.blit(credit_text, (credit_button.x + (credit_button.width - credit_text.get_width())//2,
                             credit_button.y + (credit_button.height - credit_text.get_height())//2))
        pygame.display.update()
        for event in pygame.event.get():
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if start_button.isOver(mouse_x, mouse_y):
                start_button.colour = [150, 170, 180]
                if pygame.mouse.get_pressed()[0]:
                    run = False
            else:
                start_button.colour = [123, 140, 149]

            if credit_button.isOver(mouse_x, mouse_y):
                credit_button.colour = [150, 170, 180]
                if pygame.mouse.get_pressed()[0]:
                    creditscreen()
            else:
                credit_button.colour = [123, 140, 149]
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                exit()

#draw the endscreen
def endscreen():
    global speed, clock, highestScore
    '''
    pygame.mixer.music.stop()
    '''
    bgm.stop()
    crash_sound.play()
    laugh_sound.play()
    run = True
    font = pygame.font.SysFont("tahoma", 20, bold=True)
    lose_text = font.render("You Lose !", True, [123, 140, 149])
    win.blit(lose_text, ((screen_width - lose_text.get_width())//2,120))
    highestScore_text = font.render("Highest Score : "+str(highestScore), True, [123, 140, 149])
    win.blit(highestScore_text, ((screen_width - highestScore_text.get_width())//2, 160))
    restart_button = buttons(200, 200, 100, 30, [123, 140, 149])
    restart_text = font.render("Restart", True, (255, 255, 255))
    exit_button = buttons(200, 250, 100, 30, [123, 140, 149])
    exit_text = font.render("Exit", True, (255, 255, 255))

    while run:
        exit_button.redraw(win)
        restart_button.redraw(win)
        win.blit(exit_text, (exit_button.x + (exit_button.width - exit_text.get_width())//2,
                             exit_button.y + (exit_button.height - exit_text.get_height())//2))
        win.blit(restart_text, (restart_button.x + (restart_button.width - restart_text.get_width())//2,
                                restart_button.y + (restart_button.height - restart_text.get_height())//2))
        pygame.display.update()
        for event in pygame.event.get():
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if exit_button.isOver(mouse_x, mouse_y):
                exit_button.colour = [150, 170, 180]
                if pygame.mouse.get_pressed()[0]:
                    run = False
                    pygame.quit()
                    exit()
            else:
                exit_button.colour = [123, 140, 149]
            if restart_button.isOver(mouse_x, mouse_y):
                restart_button.colour = [150, 170, 180]
                if pygame.mouse.get_pressed()[0]:
                    reset()
                    run = False
            else:
                restart_button.colour = [123, 140, 149]
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

def creditscreen():
    run = True
    win.blit(background, (background_x, 0))
    font = pygame.font.SysFont("tahoma", 20, bold=True)
    text = font.render("Program : Chicken", True, [123, 140, 149])
    win.blit(text, ((screen_width - text.get_width())//2, 100))
    text = font.render("Graphic : Chicken", True, [123, 140, 149])
    win.blit(text, ((screen_width - text.get_width()) // 2, 130))
    text = font.render("Music : Online", True, [123, 140, 149])
    win.blit(text, ((screen_width - text.get_width()) // 2, 160))
    text = font.render("Special Thanks : Fun , Bobby", True, [123, 140, 149])
    win.blit(text, ((screen_width - text.get_width()) // 2, 190))
    return_button = buttons(200, 300, 100, 30, [123, 140, 149])
    return_text = font.render("Back", True, (255,255, 255))
    while run:
        return_button.redraw(win)
        win.blit(return_text,(return_button.x + (return_button.width - return_text.get_width())//2,
                                return_button.y + (return_button.height - return_text.get_height())//2))
        for event in pygame.event.get():
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if return_button.isOver(mouse_x, mouse_y):
                return_button.colour = [150, 170, 180]
                if pygame.mouse.get_pressed()[0]:
                    run = False
                    startscreen()
            else:
                return_button.colour = [123, 140, 149]

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.update()

#increase speed
pygame.time.set_timer(pygame.USEREVENT, 500)
#generate random obstacles
pygame.time.set_timer(pygame.USEREVENT + 1, 1000)
#increase difficulty
pygame.time.set_timer(pygame.USEREVENT + 2, 5000)

font = pygame.font.SysFont("tahoma", 15, bold = True)


#initialization of character
def reset():
    global character_x, character_y, isJump, jumpCount, initjumpCount, isSlide, slideCount, initslideCount, walkCount, speed, obstacles, difficulty
    global  velocity, score, play_slideSound, play_jumpSound
    bgm.play(-1)
    character_x = 50
    character_y = 310
    isJump = False
    jumpCount = 15
    initjumpCount = jumpCount
    isSlide = False
    slideCount = 0
    initslideCount = slideCount
    walkCount = 0
    speed = 30
    obstacles = []
    difficulty = 7
    score = 0
    play_slideSound = False
    play_jumpSound = False
    velocity = 5

reset()
clock = pygame.time.Clock()
highestScore = 0
character_hitbox = hitboxes(character_x + 15, character_y, character[0].get_width()-25, character[0].get_height()-13)
run = True
startscreen()

#main loop
while run:
    clock.tick(speed)
    keys = pygame.key.get_pressed()
    win.blit(background, (background_x, 0))
    win.blit(background, (background_x2, 0))
    score += 1
    win.blit(font.render("Score : "+ str(score), True, (0,0,0)), (380,10))
    #endscreen()

    #draw looping background
    background_x -= 1
    background_x2 = background.get_width() + background_x

    if background_x < -background.get_width():
        background_x = 0

    if not isSlide :
        win.blit(character[walkCount%5],(character_x, character_y))
        walkCount += 1

    if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and not isSlide:
        isJump = True

    if keys[pygame.K_DOWN] and not isJump:
        walkCount = 0
        isSlide = True

    if not keys[pygame.K_DOWN]:
        slideCount = 0
        isSlide = False
        play_slideSound = False
        character_hitbox.height = character[0].get_height()-8

    if isJump:
        jump()

    if isSlide:
        slide()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("You quit the game")
            run = False
            pygame.quit()
            exit()
        if event.type == pygame.USEREVENT:
            speed += 0.3
        if event.type == pygame.USEREVENT +1:
            n = random.randint(0, difficulty)
            if n == 0:
                obstacles.append(spikes(screen_width + 30, 305, velocity))
            elif n == 1:
                obstacles.append(rocks(screen_width + 30, 305, velocity))
            elif n == 2:
                obstacles.append(bees(screen_width + 30, 270, velocity))
        if event.type == pygame.USEREVENT + 2 :
            velocity += 1
            for o in obstacles:
                o.velocity += 1
            if difficulty > 3:
                difficulty -= 1

    #separate into two for loop so that the endscreen can keep all the obstacles
    for o in obstacles:
        o.redraw(win)
    for o in obstacles:
        if o.x + o.width < 0:
            obstacles.pop(obstacles.index(o))
        if (o.hitbox.x < character_hitbox.x + character_hitbox.width < o.hitbox.x + o.hitbox.width) or (o.hitbox.x < character_hitbox.x < o.hitbox.x + o.hitbox.width):
            if (o.hitbox.y < character_hitbox.y + character_hitbox.height < o.hitbox.y + o.hitbox.height) or (o.hitbox.y < character_hitbox.y  < o.hitbox.y + o.hitbox.height):
                #pygame.draw.rect(win, (255, 0, 0), (character_hitbox.x, character_hitbox.y, character_hitbox.width, character_hitbox.height), 2)
                if score > highestScore:
                    highestScore = score
                endscreen()

    #pygame.draw.rect(win, (255, 0, 0), (character_hitbox.x, character_hitbox.y, character_hitbox.width, character_hitbox.height), 2)
    character_hitbox.update(character_x + 15, character_y)
    pygame.display.update()


print("You lose")
pygame.quit()

