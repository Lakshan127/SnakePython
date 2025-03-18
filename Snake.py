import tkinter
import random

ROW = 25
COL = 25
TILE_SIZE = 25

FENSTER_BREITE = COL * TILE_SIZE
FENSTER_HOHE = ROW * TILE_SIZE

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# SpielFenster
window = tkinter.Tk()
window.title("Snake")
window.resizable(False,False)

canvas = tkinter.Canvas(window, bg='gray', width=FENSTER_BREITE,height=FENSTER_HOHE,borderwidth=0, highlightthickness=0)
canvas.pack()
window.update()

#center the window
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width/2) - (window_width/2))
window_y = int((screen_height/2) - (window_height/2))

window.geometry (f"{window_width}x{window_height}+{window_x}+{window_y}")


#Spiel Initialisirung
snake = Tile(5*TILE_SIZE,5*TILE_SIZE)#Kopf der Schlange
food = Tile(10*TILE_SIZE,10*TILE_SIZE)
snake_body = []
velocityX = 0
velocityY = 0

def change_direction(e):
    #print(e)
    #print(e.keysym)
    global velocityX,velocityY

    if(e.keysym == 'Up' and velocityY != 1):
        velocityX = 0
        velocityY = -1
    elif(e.keysym == 'Down' and velocityY != -1):
        velocityX = 0
        velocityY = 1
    elif(e.keysym == 'Left' and velocityX != 1):
        velocityX = -1
        velocityY = 0
    elif(e.keysym == 'Right' and velocityX != -1):
        velocityX = 1
        velocityY = 0


def move():
    global snake
    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE


def draw():
    global snake

    move()
    canvas.delete('all')

    #Essen
    canvas.create_rectangle(food.x,food.y,food.x+TILE_SIZE,food.y+TILE_SIZE,fill='red')

    #Schlange 
    canvas.create_rectangle(snake.x,snake.y,snake.x+TILE_SIZE,snake.y+TILE_SIZE,fill='lime green')
    
    window.after(100,draw)

draw()


window.bind("<KeyRelease>",change_direction)
window.mainloop() 
