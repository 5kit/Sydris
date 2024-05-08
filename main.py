import pygame
import random
import time
import copy

blocks = [
        [[0]],
        
        [[0,1,0,0],
         [0,1,0,0],
         [0,1,0,0],
         [0,1,0,0]],
        
        [[1,1],
         [1,1]],
            
        [[0,1,0],
         [1,1,1],
         [0,0,0]],

        [[0,0,1],
         [1,1,1],
         [0,0,0]],

        [[1,0,0],
         [1,1,1],
         [0,0,0]],
            
        [[1,1,0],
         [0,1,1],
         [0,0,0]],
            
        [[0,1,1],
         [1,1,0],
         [0,0,0]]
]

n = 7
cl = [(40,40,40), (30, 255, 255), (255, 255, 30), (80, 30, 180), (255, 135, 30), (30, 150, 255), (255, 30, 30), (30, 255, 135)]

class Tetris():        
    def __init__(self, sp=10, code=random.randint(1,n)):
        self.speed = max(sp,0)
        self.code = code
        self.pos = [4,-1]
        self.rotation = 0
        self.graceTime = 1
    
    def get_image(self):
        while self.rotation < 0:
            self.rotation += 4
        self.rotation %= 4
        
        positions = {}
        bk = blocks[self.code]
        for _ in range(self.rotation):
            bk = [[i[j] for i in bk[::-1]] for j in range(len(bk))]
        for dy in range(len(bk)):
            for dx in range(len(bk[0])):
                adjX = self.pos[0] + dx
                adjY = self.pos[1] + dy
                positions[adjY*100 + adjX] = bk[dy][dx]
        return positions

class Game():
    def __init__(self, lvl=0):
        self.lvl = lvl
        self.board = [[0 for _ in range(10)] for _ in range(20)]
        self.active = Tetris(10-lvl)
        self.next = [random.randint(1,n) for _ in range(4)]
        self.store = 0
        self.points = 0
        self.clrT = 0
        self.canSwitch = True
        self.play = True
        
    def draw(self, screen):
        start = 30,100
        size = 30
        blk = self.active.get_image()
        for x in range(10):
            for y in range(20):
                dispX = start[0] + x * (size+2)
                dispY = start[1] + y * (size+2)
                if self.board[y][x] == 0 and y == 0:
                    pygame.draw.rect(screen, (80,40,40), pygame.Rect(dispX, dispY, size, size),0,5)
                else:
                    pygame.draw.rect(screen, cl[self.board[y][x]], pygame.Rect(dispX, dispY, size, size),0,5)
                
                if y*100 + x in blk:
                    if blk[y*100 + x] == 1:
                        pygame.draw.rect(screen, cl[self.active.code], pygame.Rect(dispX, dispY, size, size),5,5)
        
    def update(self, tick):
        if tick % self.active.speed == 0 and self.play:
            if self.forecast(0,1):
                self.active.pos[1] += 1
            else:
                if self.active.graceTime != 0:
                    self.active.graceTime -= 1
                else:
                    build = self.active.get_image()
                    for cords in build: 
                        if build[cords] == 1:
                            x = cords % 100
                            y = cords // 100
                            if y >= 0:
                                self.board[y][x] = self.active.code
                    self.active = Tetris(10-self.lvl, self.next.pop())
                    self.next.insert(0,random.randint(1,n))
                    self.canSwitch = True
            self.clearRows()
        
    def switch(self):
        if self.canSwitch == True:
            temp = self.active.code
            if self.store == 0:
                self.active = Tetris(10-self.lvl, self.next.pop())
                self.next.insert(0,random.randint(1,n))
                self.store = temp
            else:
                self.active = Tetris(10-self.lvl, self.store)
                self.store = temp
                self.canSwitch = False
    
    def clearRows(self):
        global highScore
        clr = 0
        for y in range(20):
            f = True
            for j in self.board[y]:
                if j == 0:
                    f = False
            if f == True:
                clr += 1
                self.board.pop(y)
                self.board.insert(0,[0 for _ in range(10)])
        pnt = 0
        pnt = 40 if clr == 1 else pnt
        pnt = 100 if clr == 2 else pnt
        pnt = 300 if clr == 3 else pnt
        pnt = 1200 if clr == 4 else pnt
        self.points +=  pnt * (self.lvl+1)
        
        self.clrT += clr
        
        if self.clrT // 10 > 0:
            self.clrT %= 10
            self.lvl += 1
            self.active.speed -= 1
            
        for k in self.board[0]:
            if k in [l for l in range(1,n+1)]:
                self.play = False
                if self.points > highScore:
                    highScore = self.points
        
    def forecast(self, dx,dy, r=0):
        blk = copy.deepcopy(self.active)
        blk.pos[0] += dx
        blk.pos[1] += dy
        blk.rotation += 4 if game.active.rotation < 0 else 0
        blk.rotation = (blk.rotation + r) % 4
        fork = blk.get_image()
        for key in fork:
            Fx = key%100
            Fy = key//100
            if fork[key] == 1 and Fy >= 0:
                if 0 <= Fx < 10 and Fy < 20:
                    if self.board[Fy][Fx] in range(1,n+1):
                        return False
                else:
                    return False
        return True

def drawTet(screen,sx,sy,code, s=16):
    grid = blocks[code]
    c = cl[code]
    sz = len(grid)
    for x in range(sz):
        for y in range(sz):
            if grid[y][x] == 1:
                pygame.draw.rect(screen, c, pygame.Rect(sx+x*(s+2),sy+y*(s+2),s,s), 0, 3)
    
SCREEN_HEIGHT = 800
SCREEN_WIDTH = 600

pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Sydris")

game = Game()
highScore = 0
game.play = False
st, et = 0, 0
tk = 0
rate = 20

font = pygame.font.Font('freesansbold.ttf', 32)
btn = pygame.Rect(200, 450, 200, 100)

running = True
while running:
    if game.play:
        st = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.play = False
                running = False
            k = pygame.key.get_pressed()
            if k[pygame.K_DOWN] or k[pygame.K_c]:
                tk = game.active.speed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if game.forecast(-1,0):
                        game.active.pos[0] -= 1
                if event.key == pygame.K_RIGHT:
                    if game.forecast(1,0):
                        game.active.pos[0] += 1
                if event.key == pygame.K_UP or event.key == pygame.K_z:
                    game.switch()
                if event.key == pygame.K_s:
                    tst = [(0,0),(-1,0),(-1,1),(0,-2),(-1,-2)] if game.active.code in [1,2] else [(0,0),(1,0),(1,-1),(0,2),(1,2)]
                    if game.active.code == 2:
                        tst = [(0,0),(2,0),(-1,0),(2,1),(-1,-2)] if game.active.rotation == 1 else tst
                        tst = [(0,0),(1,0),(-2,0)(1,-2),(-2,1)] if game.active.rotation == 2 else tst
                        tst = [(0,0),(2,0),(1,0)(-2,-1),(1,2)] if game.active.rotation == 3 else tst
                        tst = [(0,0),(-1,0),(2,0),(-1,2),(2,-1)] if game.active.rotation == 0 else tst
                    for D in tst:
                        if game.forecast(D[0],D[1],1):
                            game.active.rotation = (game.active.rotation+1)%4
                            game.active.pos[0] += D[0]
                            game.active.pos[1] += D[1]
                            break
                if event.key == pygame.K_d:
                    tst = [(0,0),(-1,0),(-1,1),(0,-2),(-1,-2)] if game.active.code in [0,3] else [(0,0),(1,0),(1,-1),(0,2),(1,2)]
                    if game.active.code == 2:
                        tst = [(0,0),(2,0),(-1,0),(2,1),(-1,-2)] if game.active.rotation == 0 else tst
                        tst = [(0,0),(1,0),(-2,0)(1,-2),(-2,1)] if game.active.rotation == 3 else tst
                        tst = [(0,0),(2,0),(1,0)(-2,-1),(1,2)] if game.active.rotation == 2 else tst
                        tst = [(0,0),(-1,0),(2,0),(-1,2),(2,-1)] if game.active.rotation == 1 else tst
                    for D in tst:
                        if game.forecast(D[0],D[1],-1):
                            game.active.rotation -= 1
                            game.active.rotation += 4 if game.active.rotation < 0 else 0
                            game.active.pos[0] += D[0]
                            game.active.pos[1] += D[1]
                            break
                if event.key == pygame.K_q:
                    ps = True
                    while ps:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                ps = False
                                game.play = False
                                running = False
                            if pygame.key.get_pressed()[pygame.K_q]:
                                ps = False
        screen.fill((70,70,70))
        
        game.update(tk)
        game.draw(screen)
        
        pygame.draw.rect(screen, (100,100,100), pygame.Rect(150, 20, 150, 50), 0,15)
        pygame.draw.rect(screen, (100,100,100), pygame.Rect(400, 100, 100, 100), 0,15)
        pygame.draw.rect(screen, (100,100,100), pygame.Rect(400, 230, 100, 400), 0,15)
        
        t1 = font.render('Score: ', True, (255,255,255))
        screen.blit(t1, (20, 30))
        t2 = font.render(str(int(game.points)), True, (255,255,255))
        screen.blit(t2, (170, 30))
        t5 = font.render('level: ' + str(game.lvl), True, (255,255,255))
        screen.blit(t5, (400, 30))

        drawTet(screen,420,120,game.store)
        drawTet(screen,420,260,game.next[3])
        drawTet(screen,420,340,game.next[2])
        drawTet(screen,420,420,game.next[1])
        drawTet(screen,420,500,game.next[0])
        
        pygame.display.flip()
        et = time.time()
        dt = et-st
        tk += 1
        time.sleep(max(1/rate - 1/rate*dt,0))
        
    else:
        screen.fill((70,70,70))
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn.collidepoint(event.pos):
                    game = Game()
        
        t0 = font.render('SYDtris', True, (255,255,255))
        screen.blit(t0, (250, 235))
        
        if btn.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (80,80,80), btn, 0,15)
        else:
            pygame.draw.rect(screen, (150,50,50), btn, 0,15)
        t0 = font.render('Play', True, (255,255,255))
        screen.blit(t0, (270, 485))
        
        pygame.draw.rect(screen, (100,100,100), pygame.Rect(180, 300, 250, 100), 0,15)
        
        t0 = font.render('highScore: ' + str(highScore), False, (255,255,255))
        screen.blit(t0, (210, 315))
        t0 = font.render('score: ' + str(game.points), False, (255,255,255))
        screen.blit(t0, (210, 345))
        
        pygame.display.flip()
    
pygame.quit()
