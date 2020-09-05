from tkinter import *

root = Tk()
e=Entry(root,width=20)#Creating Input Fields
e.pack()
e.get()
def myClick():
    myLabel=Label(root,text=e.get()).pack()
    
# creating a label widget and shoving it onto the screen
#myLabel1=Label(root,text="Hello Word")#.grid(row=0,column=0)
#myLabel2=Label(root,text="GK")#.grid(row=1,column=0)
myBotton=Button(root,text="Enter your name",pady=50,padx=50,command=myClick,fg="red",bg="black")#.grid(row=2,column=0)
myBotton.pack()
#myBotton.grid()
root.mainloop()