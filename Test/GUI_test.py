# -*- coding: utf-8 -*-

import tkinter as tk


root = tk.Tk()
root.title("List App")
root.geometry("400x400")

def retrievedata():
    "Loads the data at the opening"
    global list_data
    list_data = []
    try:
        with open("save.txt", "r", encoding="utf-8") as file:
            for f in file:
                listbox.insert(tk.END, f.strip())
                list_data.append(f.strip())
                print(list_data)
    except:
        pass

def clicked():
    "When click on a button it adds what is inside the entry box"
    global list_data
    listbox.insert(tk.END, content.get())
    list_data.append(content.get())

def delete():
    "Delete all the items in the list"
    global list_data
    listbox.delete(0, tk.END)
    list_data = []

def delete_selected():
    "Delete the selected file"
    global list_data
    selected = listbox.get(listbox.curselection())
    listbox.delete(tk.ANCHOR)
    #index = list_data[list_data.index(selected)]
    #print(index)
    list_data.pop(list_data.index(selected))

def quit():
    "action performed when you click the button quit and save"
    global root
    with open("save.txt", "w", encoding="utf-8") as file:
        for d in list_data:
            file.write(d + "\n")
    root.destroy()

# LISTBOX - The building of the GUI

# The entry
content = tk.StringVar()
entry = tk.Entry(root, textvariable=content)
entry.pack()

# The button to add items linked to the clicked() function
button = tk.Button(root, text="Add Item", command=clicked)
button.pack()

# the delete button, to delete all -> delete()
button_delete = tk.Button(text="Delete", command=delete)
button_delete.pack()

# the button to delete only selected item
button_delete_selected = tk.Button(text="Delete Selected", command=delete_selected)
button_delete_selected.pack()

# The listbox
listbox = tk.Listbox(root)
listbox.pack()

# the button to quit and save the data in the listbox so that they will stay
bquit = tk.Button(root, text="Quit and save", command=quit)
bquit.pack()

# the function to load the data saved previously
retrievedata()

# the built-in function to start the loop of the window
root.mainloop()