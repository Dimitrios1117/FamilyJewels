﻿import pygame
from tkinter import *
from pygame.locals import *
import random, math
from myMath import get_u
from boss import KingKnight
from player import Player
from minions import Peon
import values
from Interface import Interface
import tkinter.messagebox
import pickle
import os
import os.path
import string
from parse_rest.connection import register, ParseBatcher
from parse_rest.datatypes import Object as ParseObject

APPLICATION_ID = "aGzQrhKhuykuoieMzyeFpBbyJhXYBuqEz9MZzGes"
REST_API_KEY = "cDO9qCxAJeYrnh7g0NkfYzDzGkG7I9Qw2Cy99wIQ"
register(APPLICATION_ID, REST_API_KEY)

bossNum = 0

def makeWave(timer, enemy_sprites, spawnWave, spawnRate, wave, screen):
    # Spawn king knight/enter battle    
        if timer >= 0.5 and spawnWave == 0:
            spawnWave = 1
            spawnCount = 0
            global bossNum
            #spawn waves
            while 1:
                peon = Peon(screen)
                enemy_sprites.add(peon)
                spawnCount += 1
                if spawnCount >= spawnRate+bossNum*2:
                    break
            if wave % 3 == 0 :
                bossNum += 1
                for x in range(bossNum):
                    enemy_sprites.add(KingKnight(screen))
                
                

def main(self):
    #close tkinter
    userName = tEntry.get()
    root.withdraw()

    # 1 - Initialize the game
    pygame.init()
    #timer
    timer = 0
    #screen
    
    screen = pygame.display.set_mode((640,480))
    screenx = screen.get_width()
    screeny = screen.get_height()
    screeny = 480
    running = True
    #sprites lists
    player_sprites = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    enemy_sprites = pygame.sprite.Group()
    projectile_sprites = pygame.sprite.Group()
    item_sprites = pygame.sprite.Group()
    #enemy data
    bossPos = [screenx/2, screeny/2]
    #player
    playerPos = [250, 250]
    global player
    player = Player(playerPos)
    interface = Interface(screen)
    all_sprites.add(player)
    player_sprites.add(player)
    # 2 - Load resources
    hit = pygame.mixer.Sound("resources/audio/explode.wav")
    enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
    hit.set_volume(0.05)
    enemy.set_volume(0.05)
    pygame.mixer.music.load('resources/audio/moonlight.wav')
    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.set_volume(0.25)
    smallFireball = pygame.image.load("resources/images/flame_verysmall.png")
    dragon = pygame.image.load("resources/images/DragonAttack_small.png")
    background = pygame.image.load("resources/images/rock_ground.jpg")
    gold_pile = pygame.image.load("resources/images/gold_pile.png")
    chest = pygame.image.load("resources/images/treasure.png")

    clock = pygame.time.Clock()
    LEFT = 1
    spawnWave = 0
    #kingKnight = None
    wave = 1
    spawnRate = 5
    while running:
        while player.pause:
            for event in pygame.event.get():
                 if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                     player.pause = 0
        while not player.pause:
            screen.fill(0)
            # Draw background
            for x in range(int(screen.get_width()/background.get_width())+1):
                for y in range(int(screen.get_height()/background.get_height())+1):
                    screen.blit(background,(x*100,y*100))
        
            #draw gold pile
            for x in range(1,8):
                #if x == 1 or x == 6:
                if x % 2 == 0:
                    screen.blit(chest, (-5, screen.get_height()/8*x-30 ))
                else:
                    screen.blit(gold_pile, (-10, screen.get_height()/8*x-30 ))
            
            #spawn waves
            if not enemy_sprites:
                   makeWave(timer, enemy_sprites, spawnWave, spawnRate, wave, screen)
                   wave += 1
                   player.rightclick_cd = 0

            # 5 - Draw screen and update sprites
            enemy_sprites.draw(screen)
            projectile_sprites.draw(screen)
            player_sprites.draw(screen)  
            item_sprites.draw(screen)
        
        
            player.update(player, dragon, enemy_sprites, projectile_sprites, item_sprites, screen, interface)
            projectile_sprites.update(projectile_sprites, timer, enemy_sprites, all_sprites, screen)
            enemy_sprites.update(screen, timer, player, enemy_sprites, item_sprites, interface)
            interface.update(player, screen)
         

            # Draw timer display
            seconds = clock.tick()/1000.0
            timer += seconds
            player.flycd -= seconds
            player.rightclick_cd -= seconds
            player.flyDuration -= seconds
            displayTimer = round(timer,1)

            gamefont = pygame.font.Font(None, 24)
            timertext = gamefont.render(str(displayTimer), 1, [0,0,0])
            screen.blit(timertext, [screen.get_width()-50, 5])
            # Draw player health
            pygame.draw.rect(screen, (0,0,0), (5, 5, 206, 18))
            pygame.draw.rect(screen, (255,0,0), (8,8,200, 12))
            if player.hitPoints:
                pygame.draw.rect(screen, (0,255,0), (8,8,player.hitPoints*2, 12))
            else:
                save(userName,player)
                running = 0
                gameover(screen)
    
            pygame.display.flip()
            #limit to 30 frames per second
            clock.tick(30)

def gameover(screen):    
    gameover = pygame.image.load("resources/images/gameover.png")
    screen.blit(gameover,(0,0))
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
        pygame.display.flip()

def erase(self):
    tEntry.delete(0,END)

def close(self):
    root.withdraw()
    sys.exit()
    
def checker(self):
    if not (0<len(tEntry.get()) <11):
        tkinter.messagebox.showinfo("Error!", "Invalid Username")
    else:
        main(self)

"""def save(userName,player):
     fh = None
     tempfilename = "0"
     try:
         ListofFiles = [f for f in os.listdir("Saves") if os.path.isfile("Saves/" + f) and '.sav' in f]
         for file in ListofFiles:
             if userName in file:
                 namelength = len(userName)
                 tempname = file[namelength:]
                 tempname = tempname[:-4]
                 if tempname.isdigit():
                     if tempfilename < tempname:
                         tempfilename = tempname
         if tempfilename >= "0":
             tempfilename = str(int(tempfilename)+1)
         data = [userName,player.totalPoints]
         fh = open("Saves/" + userName + tempfilename+".sav", "wb")
         pickle.dump(data, fh, pickle.HIGHEST_PROTOCOL)
     except (EnvironmentError, pickle.PicklingError) as err:
         raise SaveError(str(err))
     finally:
         if fh is not None:
             fh.close()"""

"""def load():
    ListofFiles = [f for f in os.listdir("Saves") if os.path.isfile("saves/" + f) and '.sav' in f]
    fh = None
    ListofUsersandScores = []

    try:
        for file in ListofFiles: 
           fh = open("Saves/"+ file, "rb")
           data = pickle.load(fh)
           ListofUsersandScores.append((data[0],data[1]))
    except (EnvironmentError, pickle.UnpicklingError) as err:
        raise LoadError(str(err))
    finally:
        if fh is not None:
            fh.close()
    ListofUsersandScores.sort(key = lambda x: x[1], reverse = True)
    return ListofUsersandScores[:10]"""

def save(userName, player):
    userobject = ParseObject()
    userobject.Username = userName
    userobject.Score = player.totalPoints
    userobject.save()

def load():
    ListofUserObjects = list(ParseObject.Query.all())
    ListofUsersandScores = []
    for userobject in ListofUserObjects:
        ListofUsersandScores.append((userobject.Username,userobject.Score))
    ListofUsersandScores.sort(key = lambda x: x[1], reverse = True)
    return ListofUsersandScores[:10]

def scoreChecker(self):
    scoreList = load()
    spacer = "                " ## 16 spaces here
    rootTwo = Tk()
    rootTwo.title('Top 10 Scores')
    S = Scrollbar(rootTwo)
    T = Text(rootTwo, height = 13, width = 30)
    S.pack(side = RIGHT, fill = Y)
    T.pack(side = LEFT, fill = Y)
    S.config(command = T.yview)
    T.config(yscrollcommand = S.set)
    T.insert(END,"USER" + spacer + "SCORE\n\n")
    
    for score in scoreList:
        spaceNumber = len(score[0])
        if spaceNumber < 4:
            spaceNumber = ((spaceNumber - 4) * -1) + 16
        else:
            spaceNumber = 16 - (spaceNumber - 4)
        T.insert(END, str(score[0]) + " "*spaceNumber + str(score[1]) + "\n")
            
    T.config(state = DISABLED)
    rootTwo.mainloop()

if __name__ == "__main__":
    root = Tk()
    background_image=PhotoImage(file = "resources/images/titlePic.png")
    background_label = Label(root, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    root.wm_geometry("1024x680+20+40")
    root.title('Menu')
    playButton = Button(root, text='Play', width = "8", height = "2",background = "goldenrod1")
    playButton.place(x = 500, y = 500)
    playButton.bind("<Button-1>", checker)
    scoreButton = Button(root,text = "Top Scores",background = "goldenrod1")
    scoreButton.place(x = 498.5, y = 543)
    scoreButton.bind("<Button-1>", scoreChecker)
    tEntry = Entry(root)
    tEntry.place(x = 470, y = 580)
    tEntry.insert(0,"Enter Username:")
    tEntry.bind("<Button-1>", erase)
    ##root.bind("<Escape>",close)
    root.mainloop()