

class Button:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 100
        self.height = 100
        self.color = (25,25,25)
        self.border = 0
        self.radius = 10
        self.clicked = False
        self.open = True
    def draw(self):
        from main import pygame,win
        if self.open is False:
            print("hi")
            pygame.draw.rect(win, self.color, pygame.Rect(10, 10, self.width, self.height), self.border,
                             self.radius)
            if 10 < pygame.mouse.get_pos()[0] < 10 + self.width and 10 < pygame.mouse.get_pos()[
                1] < 10 + self.height and pygame.mouse.get_pressed()[0] is True:
                self.clicked = True
        else:
            pygame.draw.rect(win,self.color,pygame.Rect(self.x,self.y,self.width,self.height),self.border,self.radius)
            if self.x < pygame.mouse.get_pos()[0] < self.x+self.width and self.y < pygame.mouse.get_pos()[1] < self.y+self.height and pygame.mouse.get_pressed()[0] is True:
                self.clicked = True
class Store:
    def __init__(self):
        from main import w,h
        self.open = True
        self.width = w
        self.height = h*.2
        self.money = 0
        self.closing_button = Button()
    def draw(self):
        from main import win,pygame,w,h
        if self.open is False:
            self.closing_button.draw()
            if self.closing_button.clicked is True:
                self.open = True
                self.closing_button.clicked = False
                self.closing_button.open = self.open
        else:
            pygame.draw.rect(win,(132,132,132),pygame.Rect(self.width*.1,h*.05,self.width*.8,self.height),0,(int)(w/1000)*10)
            pygame.draw.rect(win, (50, 50, 50), pygame.Rect(self.width * .1, h * .05, self.width * .8, self.height),
                             (int)(w / 1000) * 10, (int)(w / 1000) * 10)
            self.closing_button.x = self.width * .11
            self.closing_button.y = h * .065
            self.closing_button.width = 50
            self.closing_button.height = 50
            self.closing_button.draw()
            if self.closing_button.clicked is True:
                self.open = False
                self.closing_button.clicked = False
                self.closing_button.open = self.open












