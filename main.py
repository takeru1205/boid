from tkinter import *
import random
from fish import Bird

root = Tk()

WIDTH = 1000
HEIGHT = 1000

fish_radian = 10
bird_num = 30
SPEED = 5
VIEW = 50

c = Canvas(root, width=WIDTH, height=HEIGHT)
c.pack()


fish_list = [Bird(random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(-SPEED, SPEED),
                  random.randint(-SPEED, SPEED), i, (WIDTH, HEIGHT, fish_radian, SPEED), [], VIEW) for i in range(bird_num)]
[fish.set_others(fish_list) for fish in fish_list]


def animate():
    c.delete("all")
    for fish in fish_list:
        fish.draw()
        c.create_oval(fish.x - fish_radian, fish.y - fish_radian, fish.x+fish_radian, fish.y+fish_radian)
        c.create_line(fish.x, fish.y, fish.x + fish.vx * 3, fish.y + fish.vy * 3)
    [fish.set_others(fish_list) for fish in fish_list]
    root.after(20, animate)

animate()
root.mainloop()




