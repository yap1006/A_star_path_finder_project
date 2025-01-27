import pygame
import math
from queue import PriorityQueue
WIDTH = 600
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("A* path finding Algo")
ORANGE=(255,165,0)
RED=(255,0,0)
BLUE=(0,255,0)
GREEN=(0,255,0)
GREY=(64,224,208)
PURPLE=(128,0,128)
YELLOW=(255,255,0)
WHITE=(255,255,255)
BLACK=(0,0,0)
TURQUOISE=(64,224,208)
class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row=row
        self.col=col
        self.x=row*col
        self.y=col*width
        self.color=WHITE
        self.neighbors=[]
        self.width=width
        self.total_rows=total_rows
    def get_pos(self):
        return self.row,self.col
    def is_open(self):
        return self.color==WHITE
    def make_start(self):
        self.color=GREEN
    def is_closed(self):
        return self.color==RED ##red check
    def is_barrier(self):
        return self.color==BLACK
    def is_start(self):
        return self.color==ORANGE
    def is_end(self):
        return self.color==PURPLE
    def reset(self):
        self.color=WHITE
    def make_closed(self):
        self.color=RED
    def make_open(self):
        self.color=GREEN
    def make_barrier(self):
        self.color=BLACK
    def make_end(self):
        self.color=TURQUOISE
    def make_path(self):
        self.color=PURPLE
    def draw(self,win):  #where to draw hence win is given in argument
        pygame.draw.rect(win,self.color,(self.x, self.y, self.width, self.width))
    def update_neighbours(self,grid):
        self.neighbors=[]
        if self.row<self.total_rows-1 and not grid[self.row+1][self.col].is_barrier(): #down
            self.neighbors.append(grid[self.row+1][self.col])

        if self.row > 0 and not grid[self.row-1][self.col].is_barrier(): #up
            self.neighbors.append(grid[self.row-1][self.col])

        if self.col<self.total_rows-1 and not grid[self.row][self.col+1].is_barrier(): #right
            self.neighbors.append(grid[self.row][self.col+1])

        if self.col> 0 and not grid[self.row][self.col-1].is_barrier(): #left
            self.neighbors.append(grid[self.row][self.col-1])

    def __lt__(self,other): 
        #lt stands for less than
        return False
def h(point1,point2):  #heuristic function
    row1,col1=point1
    row2,col2=point2
    return abs(row1-row2)+abs(col1-col2)
def reconstruct_path(came_from,current,draw): #traversing from current which is basically end node here to the start node
    while current in came_from:
        current= came_from[current]
        current.make_path()
        draw()

def algorithm(draw, grid, start, end):
    count=0
    open_set=PriorityQueue()
    open_set.put((0,count,start))
    came_from={}
    g_score={spot: float("inf") for row in grid for spot in row}
    g_score[start]=0
    f_score={spot: float("inf") for row in grid for spot in row}
    f_score[start]=h(start.get_pos(),end.get_pos())
    open_set_hash={start}
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
        current = open_set.get()[2]
        open_set_hash.remove(current)
        if current == end :
            reconstruct_path(came_from,end,draw)
            end.make_end()
            return True 
        for neighbor in current.neighbors:
            temp_g_score = g_score[current]+1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor]=current
                g_score[neighbor]=temp_g_score
                f_score[neighbor]=temp_g_score+h(neighbor.get_pos(),end.get_pos())
                if neighbor not in open_set_hash:
                    count+=1
                    open_set.put((f_score[neighbor],count,neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()
        if current!=start:
            current.make_closed()
    return False

def make_grid(rows,width):
    grid=[]
    gap=width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i,j,gap,rows)
            grid[i].append(spot)
    return grid
def draw_grid(win,rows,width):
    gap=width // rows
    for i in range(rows):
        pygame.draw.line(win,GREY,(0,i*gap),(width,i*gap))
        for j in range(rows):
            pygame.draw.line(win,GREY,(j*gap,0),(j*gap,width))
def draw(win,grid,rows,width):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win,rows,width)
    pygame.display.update()
def get_clicked_pos(pos,rows,width):
    gap = width // rows
    y,x=pos
    row=y // gap
    col=x // gap
    return row,col
def main(win,width):
    ROWS = 30
    grid=make_grid(ROWS,width)
    start=None
    end=None
    run=True
    started=False
    while run:
        draw(win,grid,ROWS,width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
            if pygame.mouse.get_pressed()[0]: #if left button is  pressed 
                pos=pygame.mouse.get_pos()
                row,col=get_clicked_pos(pos,ROWS,width)
                spot=grid[row][col]
                if not start and spot!=end:
                    start=spot
                    start.make_start()
                elif not end and spot!=start:
                    end=spot
                    end.make_end()
                elif spot!=end and spot!=start:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]: # right
                pos=pygame.mouse.get_pos()
                row,col=get_clicked_pos(pos,ROWS,width)
                spot=grid[row][col]
                spot.reset()
                if spot==start: # reseting start and end
                    start=None 
                elif spot==end:
                    end=None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbours(grid)
                    algorithm(lambda : draw(win, grid, ROWS, width),grid,start,end)  # lambda is used for function inside function



    pygame.quit()
main(WIN,WIDTH)

    
 
