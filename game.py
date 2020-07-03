from functions import SudokuFunctions
from levels import hardboards, easyboards, mediumboards
import random
import pygame
import time

pygame.init()

## BUTTON class ##

class Button:
    def __init__(self,x,y,width,height,color,text=''):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text

    ## Drawing button on screen method ##
    def drawButton(self, window, outline):
        if outline:
            pygame.draw.rect(window, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text!='':
            font = pygame.font.SysFont('arial',20)
            text = font.render(self.text,1,(255,255,255))
            window.blit(text,(int(self.x + (self.width/2 - text.get_width()/2)),int(self.y + (self.height/2) - text.get_height()/2)))

    ## Checking if the button is on cursore ##
    def isOnClick(self,pos):
            if pos[0] > self.x and pos[0] < self.x + self.width:
                if pos[1] > self.y and pos[1] < self.y + self.height:
                    return True
            return False

## GRID class ##

class Grid:
    def __init__(self,rows,cols,width,height,game_mode):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height=height
        self.game_mode = game_mode

        ## Choosing the game mode, depending on which button was pressed ##
        if self.game_mode == "hard":
            self.board = random.choice(hardboards)
        if self.game_mode == "medium":
            self.board = random.choice(mediumboards)
        if self.game_mode == "easy":
            self.board = random.choice(easyboards)

        self.cubes = [[Cube(self.board[i][j],i, j,width, height) for j in range(cols)]for i in range(rows)]
        self.model = None
        self.selected = None

    ## Updating the model ##
    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    ## Checking a placed value ##
    def place(self,val):
        row,col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if SudokuFunctions.isvalide(self.model,val,(row,col)) and SudokuFunctions.solve(self.model):
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    ## Setting temporary value ##
    def sketch(self,val):
        row,col = self.selected
        self.cubes[row][col].set_temp(val)

    ## Drawing the grid ##
    def draw(self,win):
        gap = self.width / 9
        for i in range(self.rows+1):
            if i%3 == 0:
                thick = 6
            else:
                thick = 2
            pygame.draw.line(win,(72,140,154),(0,int(i*gap)),(int(self.width),int(i*gap)),thick)
            pygame.draw.line(win,(72,140,154),(int(i*gap),0),(int(i*gap),int(self.height)),thick)

        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)

    ## Selecting the current box ##
    def select(self,row,col):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False
        self.cubes[row][col].selected = True
        self.selected = (row,col)

    ## Clearing the table ##
    def clear(self):
        row,col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    ## Checking the current click position ##
    def click(self,pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))
        else:
            return None
    ## Checking if the sudoku is solved ##
    def isFinished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True

class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width ,height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    ## Drawing the cubes and the elements ##
    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (41,184,225))
            win.blit(text,(int(x+5), int(y+5)))
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, (255,255,255))
            win.blit(text, (int(x + (gap/2 - text.get_width()/2)), int(y + (gap/2 - text.get_height()/2))))

        if self.selected:
            pygame.draw.rect(win, (255,255,255), (int(x),int(y), int(gap) ,int(gap)), 3)

    ## Setting a value ##
    def set(self, val):
        self.value = val

    ## Setting a temporary value ##
    def set_temp(self, val):
        self.temp = val

## Refreshing the window every time ##
def redraw_window(win, board, time, strikes):
    win.fill((20,80,80))
    # Draw time
    fnt = pygame.font.SysFont("comicsans", 35)
    text = fnt.render("Time: " + format_time(time), 1, (41,184,225))
    win.blit(text, (540 - 180, 570))
    # Draw Strikes
    text = fnt.render("X " * strikes, 1, (41,184,225))
    win.blit(text, (20, 570))
    # Draw grid and board
    board.draw(win)

## Formatting time by minutes and seconds ##
def format_time(secs):
    sec = secs%60
    minute = secs//60
    hour = minute//60

    mat = " " + str(minute) + "m " + str(sec) +"s"
    return mat

## Tutorial GUI ##
def tutorial(game_mode):
    tutorial_screen = pygame.display.set_mode((540,562))
    pygame.display.set_caption("Tutorial")
    image = pygame.image.load(r'C:\Users\Mihai\PycharmProjects\game\tutorial.png')

    letsplay = Button(200,460,150,40,(13,83,83),"Let's play!")
    tutorial = True
    while tutorial:
        tutorial_screen.blit(image,(0,0))
        letsplay.drawButton(tutorial_screen,(255,255,255))
        pygame.display.update()
        for event in pygame.event.get():
            poz = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                tutorial=False
                pygame.quit()
            if event.type == pygame.MOUSEMOTION:
                if letsplay.isOnClick(poz):
                    letsplay.color = (26, 110, 110)
                else:
                    letsplay.color = (13, 83, 83)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if letsplay.isOnClick(poz):
                    tutorial = False
                    play(game_mode)

## Menu GUI ##
def menu():
    screen = pygame.display.set_mode((540, 620))
    pygame.display.set_caption("Menu")
    white = (255, 255, 255)
    image = pygame.image.load(r'C:\Users\Mihai\PycharmProjects\game\GUI.png')

    hard = Button(195, 230, 150, 50, (13, 83, 83), 'Hard')
    medium = Button(195, 310, 150, 50, (13, 83, 83), 'Medium')
    easy = Button(195, 390, 150, 50, (13, 83, 83), 'Easy')

    playing = True
    gameModeNotFound = True
    while playing:
        if gameModeNotFound:
            screen.blit(image, (0, 0))
            hard.drawButton(screen, white)
            medium.drawButton(screen, white)
            easy.drawButton(screen, white)
        else:
            break

        pygame.display.update()

        for event in pygame.event.get():

            poz = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if hard.isOnClick(poz):
                    game_mode = "hard"
                    gameModeNotFound = False
                    tutorial(game_mode)
                if medium.isOnClick(poz):
                    game_mode = "medium"
                    gameModeNotFound = False
                    tutorial(game_mode)
                if easy.isOnClick(poz):
                    game_mode = "easy"
                    gameModeNotFound = False
                    tutorial(game_mode)

            if event.type == pygame.MOUSEMOTION:
                if hard.isOnClick(poz):
                    hard.color = (26, 110, 110)
                else:
                    hard.color = (13, 83, 83)
                if medium.isOnClick(poz):
                    medium.color = (26, 110, 110)
                else:
                    medium.color = (13, 83, 83)
                if easy.isOnClick(poz):
                    easy.color = (26, 110, 110)
                else:
                    easy.color = (13, 83, 83)

            if event.type == pygame.QUIT:
                playing = False
                pygame.quit()

## GameOver GUI ##
def gameover(play_time):
    alert = pygame.display.set_mode((540,620))
    pygame.display.set_caption("Mihai's sudoku")
    white=(255,255,255)
    pop = pygame.image.load(r'C:\Users\Mihai\PycharmProjects\game\gameover.png')
    gotomenu = Button(180, 330, 180, 50, (13, 83, 83), 'Menu')
    exit = Button(180, 420, 180, 50, (13, 83, 83), 'Exit')
    fnt = pygame.font.SysFont("comicsans", 30)
    text = fnt.render("Your time: " + format_time(play_time), 1, white)
    onscreen = True
    while onscreen:
        alert.blit(pop, (0, 0))
        gotomenu.drawButton(alert,white)
        exit.drawButton(alert,white)
        alert.blit(text, (180, 540))
        pygame.display.update()
        for event in pygame.event.get():
            poz = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                onscreen = False
            if event.type == pygame.MOUSEMOTION:
                if gotomenu.isOnClick(poz):
                    gotomenu.color = (26, 110, 110)
                else:
                    gotomenu.color = (13,83,83)
                if exit.isOnClick(poz):
                    exit.color = (26, 110, 110)
                else:
                    exit.color = (13,83,83)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if gotomenu.isOnClick(poz):
                    onscreen = False
                    menu()
                if exit.isOnClick(poz):
                    onscreen = False
                    pygame.quit()

## You won GUI ##
def youwon(play_time):
    alert = pygame.display.set_mode((540, 620))
    pygame.display.set_caption("Mihai's sudoku")
    white = (255, 255, 255)
    pop = pygame.image.load(r'C:\Users\Mihai\PycharmProjects\game\won.png')
    gotomenu = Button(180, 330, 180, 50, (13, 83, 83), 'Menu')
    exit = Button(180, 420, 180, 50, (13, 83, 83), 'Exit')
    fnt = pygame.font.SysFont("comicsans", 30)
    text = fnt.render("Your time: " + format_time(play_time), 1, white)
    onscreen = True
    while onscreen:
        alert.blit(pop, (0, 0))
        gotomenu.drawButton(alert, white)
        exit.drawButton(alert, white)
        alert.blit(text, (180, 540))
        pygame.display.update()
        for event in pygame.event.get():
            poz = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                onscreen = False
            if event.type == pygame.MOUSEMOTION:
                if gotomenu.isOnClick(poz):
                    gotomenu.color = (26, 110, 110)
                else:
                    gotomenu.color = (13, 83, 83)
                if exit.isOnClick(poz):
                    exit.color = (26, 110, 110)
                else:
                    exit.color = (13, 83, 83)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if gotomenu.isOnClick(poz):
                    onscreen = False
                    menu()
                if exit.isOnClick(poz):
                    onscreen = False
                    pygame.quit()

## Sudoku GUI ##
def play(game_mode):
    screen = pygame.display.set_mode((540, 620))
    pygame.display.set_caption("Mihai's sudoku")
    board = Grid(9,9,540,540,game_mode)
    key = None
    playing = True
    start = time.time()
    strikes = 0
    while playing:

        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_BACKSPACE:
                    board.clear()
                    key = None
                if event.key == pygame.K_RETURN :
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp) == 0:
                            strikes += 1
                        key = None

                        if board.isFinished():
                            playing = False
                            youwon()
                        if strikes == 5:
                            playing=False
                            gameover(play_time)


            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # LeftClick
                    pos = pygame.mouse.get_pos()
                    clicked = board.click(pos)
                    if clicked:
                        board.select(clicked[0], clicked[1])
                        key = None
                if event.button == 3: # Right Click
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp) == 0:
                            strikes += 1
                        key = None

                        if board.isFinished():
                            playing = False
                            youwon()
                        if strikes == 5:
                            playing = False
                            gameover(play_time)
                if event.button == 2:
                    board.clear()
                    key = None

        if board.selected and key != None:
            board.sketch(key)
        if playing:
            redraw_window(screen, board, play_time, strikes)
            pygame.display.update()

menu()
pygame.quit()