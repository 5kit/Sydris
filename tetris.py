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
            
        [[1,1,1],
         [0,1,0],
         [0,0,0]],

        [[1,1,1],
         [1,0,0],
         [0,0,0]],

        [[1,1,1],
         [0,0,1],
         [0,0,0]],
            
        [[1,1,0],
         [0,1,1],
         [0,0,0]],
            
        [[0,1,1],
         [1,1,0],
         [0,0,0]],
]

class Tetris():        
    def __init__(self, sp=10, code=random.randint(1,7)):
        self.speed = max(sp,0)
        self.code = code
        self.pos = [5,0]
        self.rotation = 0
    
    def get_image(self):
        positions = {}
        bk = blocks[self.code]
        for _ in range(self.rotation):
            bk = [[i[j] for i in bk[::-1]] for j in range(len(bk))]
        for dy in range(len(bk)):
            for dx in range(len(bk[0])):
                adjX = self.pos[0] - dx
                adjY = self.pos[1] - dy
                positions[adjY*100 + adjX] = bk[dy][dx]
        return positions

class Game():
    def __init__(self, lvl=0):
        self.lvl = lvl
        self.board = [[0 for _ in range(10)] for _ in range(20)]
        self.active = Tetris(10-lvl)
        self.next = [random.randint(1,7) for _ in range(4)]
        self.store = 0
        self.points = 0
        self.play = True
        
    def draw(self, screen):
        start = 30,100
        size = 30
        blk = self.active.get_image()
        for x in range(10):
            for y in range(20):
                dispX = start[0] + x * (size+2)
                dispY = start[1] + y * (size+2)
                if self.board[y][x] == 0:
                    pygame.draw.rect(screen, (40,40,40), pygame.Rect(dispX, dispY, size, size),0,5)
                elif self.board[y][x] == 1:
                    pygame.draw.rect(screen, (180,30,80), pygame.Rect(dispX, dispY, size, size),0,5)
                
                if y*100 + x in blk:
                    if blk[y*100 + x] == 1:
                        pygame.draw.rect(screen, (80,30,180), pygame.Rect(dispX, dispY, size, size),5,5)
        
    def update(self, tick):
        if tick % self.active.speed == 0 and self.play:
            if self.forecast(0,-1):
                self.active.pos[1] += 1
            else:
                build = self.active.get_image()
                for cords in build:
                    if build[cords] == 1:
                        x = cords % 100
                        y = cords // 100
                        self.board[y][x] = 1
                self.active = Tetris(10-self.lvl, self.next.pop())
                self.next.insert(0,random.randint(1,7))
            self.clearRows()
    
    def switch(self):
        temp = self.active.code
        if self.store == 0:
            self.active = Tetris(10-self.lvl, self.next.pop())
            self.next.insert(0,random.randint(1,7))
            self.store = temp
        else:
            self.active = Tetris(10-self.lvl, self.store)
            self.store = temp
    
    def clearRows(self):
        clr = 0
        for y in range(20):
            if self.board[y] == [1 for _ in range(10)]:
                clr += 1
                self.board.pop(y)
                self.board.insert(0,[0 for _ in range(10)])
        if clr == 4:
            clr += 1
        self.points +=  clr * (1 + self.lvl * 0.2)  * 100
        
        if self.points > 1000 * (self.lvl + 1):
            self.lvl += 1
            self.points -= 1000 * (self.lvl + 1)
            self.active.speed -= 1
            
        if 1 in self.board[0]:
            self.play = False
        
    def forecast(self, dx,dy, r=0):
        blk = copy.deepcopy(self.active)
        blk.pos[0] += dx
        blk.pos[1] += dy
        blk.rotation = (blk.rotation + r) % 4
        fork = blk.get_image()
        for key in fork:
            Fx = key%100
            Fy = key//100 + 2
            if fork[key] == 1 and Fy >= 0:
                if 0 <= Fx < 10 and Fy < 20:
                    if self.board[Fy][Fx] == 1:
                        return False
                else:
                    return False
        return True
    
SCREEN_HEIGHT = 800
SCREEN_WIDTH = 600

pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Sydris")

game = Game()
st, et = 0, 0
tk = 0
rate = 20

font = pygame.font.Font('freesansbold.ttf', 32)
trmno = ['- ', ' |', '[]', 'T ', '_|', '|_', ' <', ' >']

running = True
while running:
    st = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        k = pygame.key.get_pressed()
        if k[pygame.K_DOWN] or k[pygame.K_c]:
            tk = game.active.speed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if game.forecast(-1,-2):
                    game.active.pos[0] -= 1
            if event.key == pygame.K_RIGHT:
                if game.forecast(1,-2):
                    game.active.pos[0] += 1
            if event.key == pygame.K_UP or event.key == pygame.K_z:
                game.switch()
            if event.key == pygame.K_s:
                for Dx in [0,-1,1]:
                    if game.forecast(Dx,-2,1):
                        game.active.rotation = (game.active.rotation+1)%4
                        game.active.pos[0] += Dx
            if event.key == pygame.K_d:
                for Dx in [0,-1,1]:
                    if game.forecast(Dx,-2,-1):
                        game.active.rotation = (game.active.rotation-1)%4
                        game.active.pos[0] += Dx

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
    
    t3 = font.render(trmno[game.store], True, (255,255,255))
    screen.blit(t3, (430, 130))
    
    t4 = font.render(trmno[game.next[0]], True, (255,255,255))
    screen.blit(t4, (430, 280))
    
    t4 = font.render(trmno[game.next[1]], True, (255,255,255))
    screen.blit(t4, (430, 350))
    
    t4 = font.render(trmno[game.next[2]], True, (255,255,255))
    screen.blit(t4, (430, 420))
    
    t4 = font.render(trmno[game.next[3]], True, (255,255,255))
    screen.blit(t4, (430, 490))
    
    pygame.display.flip()
    et = time.time()
    dt = et-st
    tk += 1
    time.sleep(max(1/rate - 1/rate*dt,0))
    
pygame.quit()
