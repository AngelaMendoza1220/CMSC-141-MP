from tkinter import *
import basic


def readTheCode():
    theCode = codeEditor.get("1.0", "end-1c") # gets the code from the codeEditor
    linesOfCode = theCode.split('\n')         # split the content into lines
    
    lex = basic.lexer(linesOfCode)            # calls the lexer function to analyze each line
    printProgramResults(lex)


def printProgramResults(results):

    console.configure(state='normal')         # set the textbox state to normal to be able to configure it
    console.delete("1.0", END)                # clear the console of any text

    for obj in results:                       # display the type and their values
        print(obj.type, obj.value, sep=' ')
        console.insert(END,  obj.value + '\n')

    console.configure(state='disabled')       # disable textbox so that the contents of the console cannot be modified


window = Tk()           # creates a window
window.title("CMSC141") # sets the title of the window

run_button = Button(window, text="Run Code", command=readTheCode) # creates the button
run_button.pack(side=TOP)                                         # adds the button to the window


codeEditor = Text(window)                                                                  # creates and adds codeEditor to the window
codeEditor.configure(background='#1e1e1e', foreground='#a3d5ff', font=('Courier New', 15)) # codeEditor specifications
codeEditor.pack(expand=True, fill=BOTH, side=LEFT)                                         # adds the codeEditor to the left side of window

console = Text(window)                                                                                    # creates and adds console to the window
console.configure(background='#1e1e1e', foreground='#a3d5ff', font=('Courier New', 15), state='disabled') # console specifications
console.pack(expand=True, fill=BOTH, side=RIGHT)                                                          # adds the console to the right side of window

window.mainloop() # display window and listens for events