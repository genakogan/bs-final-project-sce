# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 13:53:33 2020

@author: Aviel-PC
"""

from tkinter import *
import PIL
from PIL import Image, ImageDraw, ImageTk

def save():
    global image_number
    filename = f'image_{image_number}.png'   # image_number increments by 1 at every save
    image_number += 1


def activate_paint(e):
    global lastx, lasty
    cv.bind('<B1-Motion>', paint)
    lastx, lasty = e.x, e.y


def paint(e):
    global lastx, lasty
    x, y = e.x, e.y
    cv.create_line((lastx, lasty, x, y), width=1)
    #  --- PIL
    draw.line((lastx, lasty, x, y), fill='black', width=1)
    lastx, lasty = x, y


root = Tk()

lastx, lasty = None, None
image_number = 0

cv = Canvas(root, width=640, height=480)
# --- PIL
photo = ImageTk.PhotoImage(Image.open("crop.jpg"))
cv.create_image(20, 20, anchor=NW, image=photo)
image1 = PIL.Image.new('RGB', (640, 480), 'white')
draw = ImageDraw.Draw(image1)

cv.bind('<1>', activate_paint)
cv.pack(expand=YES, fill=BOTH)

btn_save = Button(text="save", command=save)
btn_save.pack()

root.mainloop()