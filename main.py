
import tkinter as tk
from tkinter import messagebox
import turtle

TOOL = 6    # tool diameter for compensation

list_of_rectangles = []


def draw_rectangle():
    x = float(w_enter.get()) + TOOL
    y = float(h_enter.get()) + TOOL
    collision_check = tt.pos()
    if list_of_rectangles:
        previous_start = list_of_rectangles[-1][-1]

        if previous_start == collision_check:
            if not tk.messagebox.askyesno(title='Wrong position!', message="Rectangle already there, are You sure?"):
                return

    tt.begin_poly()
    for _ in range(2):
        tt.forward(x)
        tt.left(90)
        tt.forward(y)
        tt.left(90)
    tt.end_poly()
    rect = tt.get_poly()

    list_of_rectangles.append(rect)


def go_to_pos(x, y):
    tt.penup()
    tt.setposition(x, y)
    tt.pendown()


def undo():
    if list_of_rectangles:
        undo_poly = list_of_rectangles.pop()
        start_pos = undo_poly[0]
        go_to_pos(start_pos[0], start_pos[1])
        tt.pencolor('white')
        for i in undo_poly:
            tt.goto(i[0], i[1])
        tt.pencolor('black')


def save():
    print(list_of_rectangles)
    f17_string = ('N20G91G21G28X0Y0Z0\n'
                  'N30G40G17G80G49\n'
                  'N40T1M6\n'
                  'N70G43Z50.000H1\n'
                  'N80G0X0.000Y0.000S18000M3\n'
                  'N90G0X-2.121Y-2.121Z50.000\n'
                  'N100G1Z-15.000F5000.0\n')

    count = enumerate(list_of_rectangles, 11)

    for sq in list_of_rectangles:
        
        for point in sq:
            x = ('%.3f' % point[0])
            y = ('%.3f' % point[1])
            print(x)
            print(y)

    with open('f17.nc', 'w') as file:
        file.write(f17_string)


window = tk.Tk()
window.minsize(width=400, height=300)
window.config(padx=20, pady=20)

canvas = tk.Canvas(width=480, height=240)
canvas.grid(column=4, row=1, padx=20, pady=20)

screen = turtle.TurtleScreen(canvas)
screen.setworldcoordinates(0, 0, 2440, 1220)
screen.mode('world')
tt = turtle.RawTurtle(screen)
tt.setundobuffer(150)

title_label = tk.Label(text='Enter rectangular size:', justify='center')
title_label.grid(column=0, row=0, columnspan=4)

w_label = tk.Label(text='width(x):')
w_label.grid(column=0, row=1)

w_enter = tk.Entry()
w_enter.insert(0, '0')
w_enter.grid(column=1, row=1)

h_label = tk.Label(text='height(y):')
h_label.grid(column=2, row=1)

h_enter = tk.Entry()
h_enter.insert(0, '0')
h_enter.grid(column=3, row=1)

create = tk.Button(text='Create', command=draw_rectangle)
create.grid(column=1, row=2)
undo = tk.Button(text='Undo', command=undo)
undo.grid(column=2, row=2)
save = tk.Button(text='Save', command=save)
save.grid(column=3, row=2)
go_to_pos(20, 20)

screen.onclick(go_to_pos)

window.mainloop()
