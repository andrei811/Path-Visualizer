import os
import time
from tkinter import *
import re
import pygame
import keyboard
from pathlib import Path

pygame.init()

# initializing the matrix
matrix=[[0 for x in range(0,55)] for y in range(0,55)]

image_size = 25 # image size in pixels
win_d = 0 # dimensions of pygame window
n = -1 # number of rows and columns
init_x = -1 # initial x
init_y = -1  # initial y
fin_x = -1  #final x
fin_y = -1  #final y

# function which detects where is added an obstacle
def MouseObstacle(pos):
    # getting mouse position
    x = pos[0]
    y = pos[1]
    
    # calculating at what element of matrix the mouse is pointing
    g1 = x // image_size
    g2 = y // image_size
    
    if ((g1+1)!=init_x or (g2+1)!=init_y) and ((g1+1)!=fin_x or (g2+1)!=fin_y):
        matrix[g1+1][g2+1] = -1
    
# function which manage the GUI window
def input_window():
    # window
    window = Tk()
    window.geometry('400x180')
    window.geometry("+550+300")
    window.title("Path Visualization")


    # labels
    lb = Label(window, text="How big do you want the matrix to be?", font=("Arial", 13))
    lb.place(relx=0.5, rely=0.04, anchor=N)
    
    lbl = Label(window, text="Number of rows (max 30): ", font=("Arial", 10))
    lbl.place(relx=0.25, rely=0.3, anchor= CENTER)
    
    init_pos = Label(window, text="Initial positions (x, y):", font=("Arial", 10))
    init_pos.place(relx=0.25, rely=0.45, anchor=CENTER)
    
    final_pos = Label(window, text="Final positions (x, y):", font=("Arial", 10))
    final_pos.place(relx=0.25, rely=0.6, anchor=CENTER)
    
    
    # text inputs
    n_inp = Entry(window, width=6)
    n_inp.place(relx=0.5, rely=0.3, anchor=CENTER)
    
    pos_inp = Entry(window, width=6)
    pos_inp.place(relx=0.5, rely=0.45, anchor=CENTER)
    
    final_inp = Entry(window, width=6)
    final_inp.place(relx=0.5, rely=0.6, anchor=CENTER)


    # function for getting input
    def clicked():
        # getting global variables
        global n, init_x, init_y, fin_x, fin_y
        
        # finding numbers from string
        numbers = [int(s) for s in re.findall('\d+', n_inp.get())]
        init_coord = [int(s) for s in re.findall('\d+', pos_inp.get())]
        fin_coord = [int(s) for s in re.findall('\d+', final_inp.get())]
        
        # verifying some properties
        if numbers and len(init_coord) > 1 and len(fin_coord)>1:
            
            if numbers[0] in range(1, 31):
                n = numbers[0]
                
                if init_coord[0] in range(1, n + 1) and init_coord[1] in range(1, n + 1):
                    if fin_coord[0] in range(1, n + 1) and fin_coord[1] in range(1, n + 1):
                        
                        init_x = init_coord[0]
                        init_y = init_coord[1]
                        
                        fin_x = fin_coord[0]
                        fin_y = fin_coord[1]
                        
                        window.destroy()

    # button
    btn = Button(window, text="Ok", command=clicked, height=1, width=8)
    btn.place(relx=0.5, rely=0.96, anchor=S)

    window.mainloop()

def valid(x, y):
    # if the element is between 0 and n
    if x < 1 or y < 1 or x > n or y > n:
        return False
    # if the element is unvisited
    if matrix[x][y] != 0:
        return False
    return True


def main_window():
    
    # getting global veriables
    global n, init_x, init_y, fin_x, fin_y, matrix, win_d
    
    # calculeting window dimentions
    win_d = image_size * n
    
    # window config
    # os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (480, 150)
    screen = pygame.display.set_mode([win_d, win_d])
    
    #importing photos
    path = Path("")
    parent_path = str(path.parent.absolute())
    print(parent_path)
    red_img = pygame.image.load(parent_path + "/Sprites/red.jpg")
    cyan_img = pygame.image.load(parent_path +"/Sprites/cyan.jpg")
    white_img = pygame.image.load(parent_path +"/Sprites/white.jpg")
    black_img=pygame.image.load(parent_path +"/Sprites/black.jpg")
    blue_img=pygame.image.load(parent_path +"/Sprites/blue.jpg")
    
    Q = [] # queue
    dx = [0, 1, 0, -1] #directional vectors
    dy = [1, 0, -1, 0]
    
    Q.append([init_x, init_y])
    
    matrix[init_x][init_y] = 1 
    
    running = True
    looping_for_obs = True 
    found = False # True- if we reached final position
    
    # obstacle 
    while looping_for_obs:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                looping_for_obs = False
                running = False
                pygame.quit()
                quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    looping_for_obs = False
                    
            elif pygame.mouse.get_pressed()[0]:
                MouseObstacle(pygame.mouse.get_pos())
        
        
        for i in range(0, n + 1):
            for j in range(0, n + 1):
                
                if (i + 1 == fin_x and j + 1 == fin_y) or matrix[i + 1][j + 1] == 1:
                    screen.blit(blue_img, (i * image_size, j * image_size))
                    
                elif matrix[i + 1][j + 1] == 0:
                    screen.blit(white_img, (i * image_size, j * image_size))
                    
                elif matrix[i + 1][j + 1] == -1:
                    screen.blit(black_img, (i * image_size, j * image_size))
                    
        pygame.display.update()
         
    # Lee's algorithm
    while running and Q and not found:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if not found: 
            x, y = Q.pop()
            
            for i in range(0, 4):
                newx = x + dx[i]
                newy = y + dy[i]
                
                if valid(newx, newy):
                    matrix[newx][newy] = matrix[x][y] + 1
                    Q.insert(0, [newx, newy])
                    
                if newx == fin_x and newy == fin_y:
                    found = True
                    break
        
            for i in range(0, n+1):
                for j in range(0, n + 1):
                    # if the position is the initial one or final one... 
                    if (i + 1 == init_x and j + 1 == init_y) or (i + 1 == fin_x and j + 1 == fin_y):
                        screen.blit(blue_img, (i * image_size, j * image_size))
                    
                    # else if the position should be a blank space...
                    elif matrix[i + 1][j + 1] == 0:
                        screen.blit(white_img, (i * image_size, j * image_size))
                        
                    # else if the position is a obstacle
                    elif matrix[i + 1][j + 1] == -1:
                        screen.blit(black_img, (i * image_size, j * image_size))
                    
                    else:
                        screen.blit(red_img, (i * image_size, j * image_size))    
            
        time.sleep(0.03)
        
        pygame.display.update()
    
    # recursion path reconstrucion
    def rec(x, y, R):
        if matrix[x][y] == 1:
            R.append([x, y])
            return
        else:
            for i in range(0, 4):
                new_x = x + dx[i]
                new_y = y + dy[i]
                
                if new_x in range(1, n + 1) and new_y in range(1, n + 1):
                    if (matrix[new_x][new_y] + 1 == matrix[x][y]):
                        rec(new_x, new_y, R)
                        break
            R.append([x, y])
    
    R = []
    
    rec(fin_x, fin_y, R)
    
    k = 0
    
    # visual path construction
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if k < len(R):
            x, y = R[k]
            k += 1
        
        for i in range(0, n+1):
            for j in range(0, n + 1):
                if (i + 1 == x and j + 1 == y) or (i + 1 == fin_x and j + 1 == fin_y):
                    matrix[i + 1][j + 1] = -3
                    screen.blit(blue_img, (i * image_size, j * image_size))
                    
                elif matrix[i + 1][j + 1] == -3 :
                    screen.blit(cyan_img, (i * image_size, j * image_size))
                    
                elif matrix[i + 1][j + 1] == -1:
                    screen.blit(black_img, (i * image_size, j * image_size))
                    
                else:
                    screen.blit(white_img, (i * image_size, j * image_size))
        
        time.sleep(0.3)
        pygame.display.update()
    
# main function
def main():
    matrix[init_x][init_y] = -3
    input_window()
    
    if n != -1:
        main_window()
    
    

main()