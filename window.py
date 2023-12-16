from tkinter import *
import basic


def readTheCode():
    theCode = codeEditor.get("1.0", "end-1c") # gets the code from the codeEditor
    linesOfCode = theCode.split('\n')         # split the content into lines
    
    lex = basic.lexer(linesOfCode)            # calls the lexer function to analyze each line
    printProgramResults(lex)


def printProgramResults(results):
    for obj in results:                       # display the type and their values
        print(obj.type, obj.value, sep=' ')


window = Tk()           # creates a window
window.title("CMSC141") # sets the title of the window

run_button = Button(window, text="Run Code", command=readTheCode) # creates the button
run_button.pack(side=TOP)                                         # adds the button to the window


codeEditor = Text(window)                                                                  # creates and adds codeEditor to the window
codeEditor.configure(background='#1e1e1e', foreground='#a3d5ff', font=('Courier New', 15)) # codeEditor specifications:
codeEditor.pack(expand=True, fill=BOTH, side=LEFT)                                         # adds the codeEditor to the window

console = Text(window)                                                                                    # creates and adds console to the window
console.configure(background='#1e1e1e', foreground='#a3d5ff', font=('Courier New', 15), state='disabled') # console specifications:
console.pack(expand=True, fill=BOTH, side=RIGHT)                                                          # adds the console to the window

window.mainloop() # display window and listens for events