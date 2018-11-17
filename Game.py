from tkinter import *
import time
import random

class Point:
    def __init__(self, canvas, player1, player2, x, y):
        self.canvas = canvas
        self.id = self.canvas.create_rectangle(0, 0, 50, 50, fill="yellow", outline="")
        self.canvas.move(self.id, x * 50 - 50, y * 50 - 50)
        self.player1 = player1
        self.player2 = player2
        self.x = x
        self.y = y
        
    def draw(self):
        if self.touching(self.player1):
            self.player1.points += 1
            print("Red:%s" % self.player1.points)
            self.canvas.itemconfig(self.id, state="hidden")
            self.oldx = self.x
            self.oldy = self.y
            while self.touching(self.player1) or self.touching(self.player2):
                self.x = random.randint(2, 10)
                self.y = random.randint(2, 10)
                while self.same_x(self.player1) or self.same_x(self.player2) or self.same_y(self.player2) or self.same_y(self.player1):
                    self.x = random.randint(2, 10)
                    self.y = random.randint(2, 10)
            self.canvas.move(self.id, (self.x - self.oldx) * 50, (self.y - self.oldy) * 50)
            self.canvas.itemconfig(self.id, state="normal")
        if self.touching(self.player2):
            self.player2.points += 1
            print("Blue:%s" % self.player2.points)
            self.canvas.itemconfig(self.id, state="hidden")
            self.oldx = self.x
            self.oldy = self.y
            while self.touching(self.player1) or self.touching(self.player2):
                self.x = random.randint(2, 10)
                self.y = random.randint(2, 10)
                while self.same_x(self.player1) or self.same_x(self.player2) or self.same_y(self.player2) or self.same_y(self.player1):
                    self.x = random.randint(2, 10)
                    self.y = random.randint(2, 10)
            self.canvas.move(self.id, (self.x - self.oldx) * 50, (self.y - self.oldy) * 50)
            self.canvas.itemconfig(self.id, state="normal")

    def touching(self, player):
        t = False
        if player.x_block == self.x:
            if player.y_block == self.y:
                t = True
        return t

    def same_x(self, player):
        x = False
        if player.x_block == self.x:
            t = True
        return x
    
    def same_y(self, player):
        y = False
        if player.y_block == self.y:
            t = True
        return y
    
class Player:
    def __init__(self, canvas, color, x, y, player):
        self.canvas = canvas
        self.id = self.canvas.create_rectangle(0, 0, 50, 50, fill=color, outline="")
        self.canvas.move(self.id, x * 50 - 50, y * 50 - 50)
        if player == 1:
            self.canvas.bind_all("<KeyPress-w>", self.go_up)
            self.canvas.bind_all("<KeyPress-a>", self.go_left)
            self.canvas.bind_all("<KeyPress-s>", self.go_down)
            self.canvas.bind_all("<KeyPress-d>", self.go_right)
        elif player == 2:
            self.canvas.bind_all("<KeyPress-Left>", self.go_left)
            self.canvas.bind_all("<KeyPress-Right>", self.go_right)
            self.canvas.bind_all("<KeyPress-Up>", self.go_up)
            self.canvas.bind_all("<KeyPress-Down>", self.go_down)
        self.x = 0
        self.y = 0
        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()
        self.points = 0
        
    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        self.pos = self.canvas.coords(self.id)
        self.x = 0
        self.y = 0
        self.x_block = self.pos[2] / 50
        self.y_block = self.pos[3] / 50

    def no_left_collide(self):
        c = True
        if self.x_block * 50 - 50 <= 0:
            c = False
        if self.x_block - 1 == self.other_x_block:
            if self.y_block == self.other_y_block:
                c = False
        return c

    def no_right_collide(self):
        c = True
        if self.x_block * 50 + 50 > self.canvas_width:
            c = False
        if self.x_block + 1 == self.other_x_block:
            if self.y_block == self.other_y_block:
                c = False
        return c

    def no_up_collide(self):
        c = True
        if self.y_block * 50 - 50 <= 0:
            c = False
        if self.y_block - 1 == self.other_y_block:
            if self.x_block == self.other_x_block:
                c = False
        return c

    def no_down_collide(self):
        c = True
        if self.y_block * 50 + 50 > self.canvas_height:
            c = False
        if self.y_block + 1 == self.other_y_block:
            if self.x_block == self.other_x_block:
                c = False
        return c
    
    def go_left(self, event):
        if self.no_left_collide():
            self.x = -50
        
    def go_right(self, event):
        if self.no_right_collide():
            self.x = 50
        
    def go_up(self, event):
        if self.no_up_collide():
            self.y = -50
        
    def go_down(self, event):
        if self.no_down_collide():
            self.y = 50

    def char_pos(self, x, y):
        self.other_x_block = x
        self.other_y_block = y
        
tk = Tk()
tk.title("Game")
tk.resizable(0, 0)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=500, height=500, bd=0, highlightthickness=0)
canvas.pack()
tk.update()

red = Player(canvas, "red", 1, 1, 1)
blue = Player(canvas, "blue", 10, 10, 2)
p = Point(canvas, red, blue, 5, 5)
start = time.time()
while 1:
    red.draw()
    blue.draw()
    p.draw()
    red.char_pos(blue.x_block, blue.y_block)
    blue.char_pos(red.x_block, red.y_block)
    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)
    e = (time.time() - start)
    if e >= 60:
        canvas.itemconfig(red.id, state="hidden")
        canvas.itemconfig(blue.id, state="hidden")
        canvas.itemconfig(p.id, state="hidden")
        break
if red.points > blue.points:
    canvas.create_text(50, 20, text='Red: %s' % red.points)
    canvas.create_text(50, 80, text='Blue: %s' % blue.points)
    canvas.create_text(50, 110, text=("Red Wins!"))
elif blue.points > red.points:
    canvas.create_text(50, 20, text='Red: %s' % red.points)
    canvas.create_text(50, 80, text='Blue: %s' % blue.points)
    canvas.create_text(50, 110, text=("Blue Wins!"))
else:
    canvas.create_text(50, 20, text='Red: %s' % red.points)
    canvas.create_text(50, 80, text='Blue: %s' % blue.points)
    canvas.create_text(50, 110, text=("Tie!"))
    
