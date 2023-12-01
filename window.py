from tkinter import *

# get the code from the text box
def get_code():
    theCode = textbox.get("1.0", "end-1c") # gets the text
    print(theCode)                         # prints it out to the console


window = Tk() # creates a window

window.title("CMSC141")    # sets the title of the window
window.geometry("800x800") # sets the size of the window

textbox = Text(window, width = 190, height = 35) # creates and adds textbox to the window

# textbox specifications:
textbox.configure(background='#1e1e1e', foreground='#007acc', font=('Courier New', 15)) 

textbox.pack() # adds the textbox to the window

run_button = Button(window, text="Run Code", command=get_code) # creates the button
run_button.pack() # adds the button to the window

window.mainloop() # display window and listens for events