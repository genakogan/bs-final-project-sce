from tkinter import *

root = Tk()
root.geometry("400x400")

bImage = PhotoImage(file="C:/Users/Aviel-PC/Pictures/btn-cayan1.png")
lblImage = Label(image=bImage, text="< Prev")

btnSegmentPreview = Button(root, image=bImage, text="Preview", command="", borderwidth=0)
btnSegmentPreview.grid(column = 0, row = 0, sticky='sw')
btnSegmentPreview = Button(root, image=bImage, text="Preview", command="", borderwidth=0)
btnSegmentPreview.grid(column = 1, row = 0, sticky='sw')
btnSegmentPreview = Button(root, image=bImage, text="Preview", command="", borderwidth=0)
btnSegmentPreview.grid(column = 2, row = 0, sticky='sw')

root.mainloop()