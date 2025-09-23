import pygame, random, sys

pygame.init()
SIZE, TILE, GAP, MARGIN = 4, 60, 5, 20
FONT = pygame.font.SysFont(None, 32)

def is_solvable(tiles):
    arr = [t for t in tiles if t != 0]
    inv = sum(arr[i] > arr[j] for i in range(len(arr)) for j in range(i+1, len(arr)))
    blank_row = SIZE - (tiles.index(0) // SIZE)
    return (inv + blank_row) % 2 == 0

def new_board():
    while True:
        tiles = list(range(1, SIZE*SIZE)) + [0]
        random.shuffle(tiles)
        if is_solvable(tiles):
            return tiles

class Board:
    def __init__(self,pos): self.tiles,new_pos=new_board(),pos; self.pos=pos
    def draw(self,screen):
        x0,y0=self.pos
        for i,v in enumerate(self.tiles):
            r,c=divmod(i,SIZE)
            rect=pygame.Rect(x0+c*(TILE+GAP),y0+r*(TILE+GAP),TILE,TILE)
            pygame.draw.rect(screen,(60,60,60) if v==0 else (200,200,200),rect)
            if v: screen.blit(FONT.render(str(v),True,(0,0,0)),rect.move(15,10))
    def move(self,key,keys):
        blank=self.tiles.index(0); r,c=divmod(blank,SIZE); t=None
        if key==keys['up']and r<SIZE-1:t=blank+SIZE
        if key==keys['down']and r>0:t=blank-SIZE
        if key==keys['left']and c<SIZE-1:t=blank+1
        if key==keys['right']and c>0:t=blank-1
        if t is not None:self.tiles[blank],self.tiles[t]=self.tiles[t],self.tiles[blank]
    def solved(self): return self.tiles==list(range(1,SIZE*SIZE))+[0]

W=2*(SIZE*TILE+(SIZE-1)*GAP)+3*MARGIN; H=SIZE*TILE+(SIZE-1)*GAP+2*MARGIN+40
screen=pygame.display.set_mode((W,H)); clock=pygame.time.Clock()
b1=Board((MARGIN,MARGIN)); b2=Board((W-(SIZE*TILE+(SIZE-1)*GAP)-MARGIN,MARGIN))
c1={'up':pygame.K_w,'down':pygame.K_s,'left':pygame.K_a,'right':pygame.K_d}
c2={'up':pygame.K_UP,'down':pygame.K_DOWN,'left':pygame.K_LEFT,'right':pygame.K_RIGHT}
winner=None

while True:
    for e in pygame.event.get():
        if e.type==pygame.QUIT or(e.type==pygame.KEYDOWN and e.key==pygame.K_ESCAPE): sys.exit()
        if e.type==pygame.KEYDOWN: b1.move(e.key,c1); b2.move(e.key,c2)
    if not winner:
        if b1.solved():winner=1
        if b2.solved():winner=2
    screen.fill((30,30,30)); b1.draw(screen); b2.draw(screen)
    if winner: screen.blit(FONT.render(f"Игрок {winner} победил!",True,(0,255,0)),(W//2-100,H-30))
    pygame.display.flip(); clock.tick(30)
