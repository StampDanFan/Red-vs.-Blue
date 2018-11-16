from tkinter import *
import time

class Player:
  def __init__(self, canvas, color, x, y):
    self.canvas = canvas
    self.id = self.canvas.create_rectangle(0, 0, 50, 50, fill=color)
    self.canvas.move(self.id, x * 50 - 50, y)

tk = Tk()
tk.title("Game")
tk.resizable(0, 0)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=500, height=500, bd=0, highlightthickness=0)
canvas.pack()
tk.update()

p = Player(canvas, "red", 1, 1)
