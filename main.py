import pygame, os, re, sys, threading
from random import randint
import store


pygame.init()

#Creating Window
w = 1400
h = 800
win = pygame.display.set_mode((w,h))

#Sprites

backgrounds = {}
character_types = {}
characters = {}

def custom_sort_key(file_name):
    # Extract the numeric portion using regular expressions
    match = re.match(r'(\D+)(\d+)', file_name)
    if match:
        prefix, number = match.groups()
        return (prefix, int(number))
    else:
        return (file_name,)


def loadGame():
    backgrounds["castle"]=pygame.transform.scale(pygame.image.load("backgrounds/castle.png"),(w,h))
    backgrounds["forest"]=pygame.transform.scale(pygame.image.load("backgrounds/forest.png"),(w,h))
    backgrounds["castle_pale"]=pygame.transform.scale(pygame.image.load("backgrounds/castle_pale.png"),(w,h))
    backgrounds["forest_pale"]=pygame.transform.scale(pygame.image.load("backgrounds/forest_pale.png"),(w,h))
    for c in os.listdir("characters"):
        if c != ".DS_Store":
            for animation in os.listdir("characters/"+c):
                characters[c.lower()+"_"+animation.lower()] = []

    for type in os.listdir("characters"):
        if type != ".ds_store" and type != ".DS_Store":
            character_types[type.lower()] = {}
            for folder in os.listdir("characters/"+type):
                if folder != ".DS_Store":
                    for image in sorted(os.listdir("characters/"+type+"/"+folder), key=custom_sort_key):
                        #print(image)
                        characters[type.lower()+"_"+folder.lower()].append(pygame.transform.scale(pygame.image.load("characters/"+type+"/"+folder+"/"+image),(.1*w,(1/6)*h)))
                    character_types[type.lower()][type.lower()+"_"+folder.lower()] = characters[type.lower()+"_"+folder.lower()]


#character class
class character:
    def __init__(self):
        self.type = "rogue"
        self.hp = randint(20,80)
        self.attack = 4
        self.hp_max = 100
        self.speed = (2/1000)*w
        self.x = 0
        self.y = (350/600)*h
        self.fight = False
        self.index = 0
        self.animation = "walk"
        self.animation_complete = False
        self.sprites = character_types[self.type]
        self.alive = True
        self.hitbox = {}     # x, x2, y, y2
        self.hitbox["x"] = self.x
        self.hitbox["x2"] = self.x+(.1*w)
        self.hitbox["y"] = self.y
        self.hitbox["y2"] = self.y+((1/6)*h)

    def move(self):
        if self.fight is False:
            self.x+=self.speed
            for e in enemies:
                #print(str(self.x+.1*w-self.speed*39)+" <= "+str(e.x)+" <= "+str( self.x-self.speed*35+.1*w))
                if self.x+.1*w-self.speed*39<= e.x<=self.x-self.speed*35+.1*w:
                    self.fight = True
                    self.animation = "attack"
        elif self.alive is True and self.fight is True:
            alone = True
            for e in enemies:
                if self.x + .1 * w - self.speed * 39 <= e.x <= self.x - self.speed * 35 + .1 * w:
                    alone = False
                    e.hp -= self.attack
                    if e.hp <= 0:
                        if e.alive is True:
                            e.index = 0
                        e.alive = False
            if alone is True:
                self.fight = False
                self.animation = "walk"

    def draw(self):
        if self.alive is True:
            win.blit(self.sprites[self.type+"_"+self.animation][self.index],(self.x-screen_pos,self.y))
            pygame.draw.rect(win,(15, 15, 15),pygame.Rect(self.x+(6/1000)*w-screen_pos,self.y+(30/600)*h,(50/1000)*w,(12/600)*h),0,4)
            #pygame.draw.rect(win, (0, 0, 255),pygame.Rect(self.x+(6/1000)*w-screen_pos+(.1*w),self.y+(30/600)*h,5,100))# testing hitbox
            #pygame.draw.rect(win, (0, 0, 0),pygame.Rect(self.x + (6 / 1000) * w - screen_pos-(.06*w), self.y + (30 / 600) * h, 5,100))  # testing hitbox
            if self.hp >= self.hp_max*.6:
                pygame.draw.rect(win, (40, 200, 77),pygame.Rect(self.x + (9 / 1000) * w - screen_pos, self.y + (32 / 600) * h,((44 / 1000) * w) * (self.hp / self.hp_max), (8 / 600) * h),0,4)
            elif self.hp >= self.hp_max*.3:
                pygame.draw.rect(win, (200, 192, 40), pygame.Rect(self.x + (9/1000)*w-screen_pos, self.y + (32/600)*h, ((44/1000)*w)*(self.hp/self.hp_max), (8/600)*h),0,4)
            else:
                pygame.draw.rect(win, (200, 47, 40),pygame.Rect(self.x + (9 / 1000) * w - screen_pos, self.y + (32 / 600) * h,((44 / 1000) * w) * (self.hp / self.hp_max), (8 / 600) * h),0,4)
            self.index += 1
            if self.index >= 1:
                self.animation_complete = False
            if self.index == len(self.sprites[self.type+"_"+self.animation]):
                self.index=0
                self.animation_complete = True
            self.move()
        else:
            self.animation = "death"
            win.blit(self.sprites[self.type+"_"+self.animation][self.index],(self.x-screen_pos,self.y))
            self.index += 1
            if self.index >= 1:
                self.animation_complete = False
            if self.index == len(self.sprites[self.type + "_" + self.animation]):
                self.index = 0
                self.animation_complete = True


# Enemies Class
class enemy(character):
    def __init__(self):
        self.type = "demon"
        self.hp = randint(20, 80)
        self.attack = 2
        self.hp_max = 100
        self.speed = (2 / 1000) * w
        self.x = w/4
        self.y = (350 / 600) * h
        self.fight = False
        self.index = 0
        self.animation = "walk"
        self.animation_complete = False
        self.sprites = character_types[self.type]
        self.alive = True
        self.hitbox = {}  # x, x2, y, y2
        self.hitbox["x"] = self.x
        self.hitbox["x2"] = self.x + (.1 * w)
        self.hitbox["y"] = self.y
        self.hitbox["y2"] = self.y + ((1 / 6) * h)
    def move(self):
        if self.fight is False:
            self.x-=self.speed
            for h in heroes:
                #print(str(self.x+.1*w+self.speed*35)+" <= "+str(h.x+(.1*w))+" <= "+str(self.x+self.speed*39+.1*w))
                if (self.x+(.070*w) <= h.x+(.1*w) <= self.x+self.speed*39+.1*w):
                    self.fight = True
                    self.animation = "attack"
        elif self.alive is True and self.fight is True:
            alone = False
            for h in heroes:
                if (self.x + (.070 * w) <= h.x + (.1 * w) <= self.x + self.speed * 39 + .1 * w):
                    alone = True
                    h.hp -= self.attack
                    if h.hp <= 0:
                        if h.alive is True:
                            h.index = 0
                        h.alive = False
            if alone is False:
                self.fight = False
                self.animation = "walk"
    def draw(self):
        if self.alive is True:
            win.blit(pygame.transform.flip(self.sprites[self.type+"_"+self.animation][self.index],True,False),(self.x-screen_pos,self.y))
            pygame.draw.rect(win,(15, 15, 15),pygame.Rect(self.x+(6/1000)*w-screen_pos+(32/1000)*w,self.y+(30/600)*h,(50/1000)*w,(12/600)*h),0,4)
            #pygame.draw.rect(win, (255, 0, 0),pygame.Rect(self.x+(6/1000)*w-screen_pos,self.y+(30/600)*h,5,100))# testing hitbox
            #pygame.draw.rect(win, (0, 0, 0),pygame.Rect(self.x + (6 / 1000) * w - screen_pos +(.065*w), self.y + (30 / 600) * h, 5,100))  # testing hitbox
            if self.hp >= self.hp_max*.6:
                pygame.draw.rect(win, (40, 200, 77),pygame.Rect(self.x + (9 / 1000) * w - screen_pos+(32/1000)*w, self.y + (32 / 600) * h,((44 / 1000) * w) * (self.hp / self.hp_max), (8 / 600) * h),0,4)
            elif self.hp >= self.hp_max*.3:
                pygame.draw.rect(win, (200, 192, 40), pygame.Rect(self.x + (9/1000)*w-screen_pos+(32/1000)*w, self.y + (32/600)*h, ((44/1000)*w)*(self.hp/self.hp_max), (8/600)*h),0,4)
            else:
                pygame.draw.rect(win, (200, 47, 40),pygame.Rect(self.x + (9 / 1000) * w - screen_pos+(32/1000)*w, self.y + (32 / 600) * h,((44 / 1000) * w) * (self.hp / self.hp_max), (8 / 600) * h),0,4)
            self.index += 1
            if self.index >= 1:
                self.animation_complete = False
            if self.index == len(self.sprites[self.type+"_"+self.animation]):
                self.index=0
                self.animation_complete = True
            self.move()
        else:
            #print(self.index)
            self.animation = "death"
            win.blit(pygame.transform.flip(self.sprites[self.type+"_"+self.animation][self.index],True,False),(self.x-screen_pos,self.y))
            self.index += 1
            if self.index >= 1:
                self.animation_complete = False
            if self.index == len(self.sprites[self.type + "_" + self.animation]):
                self.index = 0
                self.animation_complete = True







#Draw function for game
def draw():
    screen_pos=0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        mouse = pygame.mouse.get_pos()
        if mouse[0] >= .9 * w and screen_pos <= w - (25 / 1000) * w:
            screen_pos += (25 / 1000) * w
        elif mouse[0] <= .1 * w and screen_pos >= -w + (25 / 1000) * w and mouse[1] >= 50:
            screen_pos -= (25 / 1000) * w
        """try:
            draw(mouse)
            if spawned == False:
                t1 = threading.Thread(target=drawChar, args=())
                t1.start()
                spawned = True
        except:
            pass"""
        pygame.display.update()
        framerate.tick(13)
        clock = (pygame.time.get_ticks() / 1000) - startTime
        win.blit(backgrounds["castle_pale"],(-screen_pos,0))
        win.blit(backgrounds["castle_pale"], (-screen_pos-w, 0))
        win.blit(backgrounds["castle_pale"], (-screen_pos+w, 0))
        for h in heroes:
            h.draw()
            if h.hp <= 0 and h.animation_complete is True:
                heroes.remove(h)
        for e in enemies:
            e.draw()
            #print(e.index)
            if e.hp <= 0 and e.animation_complete is True:
                enemies.remove(e)
        shop.draw()


def drawChar():
    c = enemies[0]
    while True:
        c.draw()
        framerate.tick(13)


#Game Loop
framerate = pygame.time.Clock()
startTime = pygame.time.get_ticks()/1000
loadGame()
screen_pos = 0
shop = store.Store()
enemies = []
enemies.append(enemy())
heroes = []
heroes.append(character())
spawned = False
def main():
    t0 = threading.Thread(target=(draw()),args=())
    t0.start()
    #if clock > 10:
        #heroes[0].fight = True
        #k.hp -= 100
main()
