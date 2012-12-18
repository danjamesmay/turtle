#######################################################
#  http://creativecommons.org/licenses/by-nc-sa/3.0/  #
#######################################################
             # This program was created #
             #       by Daniel May      #
             #       on 26/11/2012      #
             #     last modified on:    #
             #       on 07/12/2012      #
             ############################
### Version 1 ###

#### PROGRAM NOTES:  ADDED TERMINAL FORMATTING THAT ONLY WORKS ON UNIX SYSTEMS!

### Ideas for version 2:
### Create GUI including buttons for all functions using the Tkinter module that
### is part of Python's standard library.
### Fully working directory system, multiple turtles, etc.

## Possible alternative directions that could of been taken/would like to
## explore further:
## Depreciate the use of global values by using a dictionary, this will allow
## for references .__doc__ docstrings for an interactive help function.
## Regular expressions and various other more advanced string tools to
## manipulate file input.
## Also: the ability to take different forms of input with different delimiters.

import turtle
import sys
import os
from tkinter import *

commandList = []

# Program progression choices that are NOT to be saved into the current list of
# commands.
choices = ["new", "save", "load", "undo", "quit", "help", "h", "q", "exit", \
"x", "close", "bye", "printcommandlist", "lengthcommandlist", "dir"]

# Input choices that interact directly with the turtle object and its state and 
# are saved into the file.
interactiveChoices = ["forward", "backward", "left", "right", "goto", "penup", \
"pendown", "write", "color", "colour", "title"]

# Colour choices that restrict the turtle to change to only one of the colours
# in this list
colourChoices = ["red", "blue", "green", "yellow", "magenta", "cyan", "black"]

def printCommandList():
    """Provides the user with a list of available commands for interaction."""
    print(commandList)

def currentLength():
    """Tells the user the number of commands that are in the command list."""
    print("The number of turtle commands you have input:", len(commandList))

def numberUndos():
    """Tells the user the amount of commands that can be undone."""
    print("Range of undos: ", range(0, undobufferentries()))
    print("The total number of undos you are able to perform:", \
undobufferentries())

# For version 2: implement an interactive help function: i.e.
# For more specific information on each command type "help <command>"
def help():  
    """Supplies the user with the list of basic available commands"""
    print("""Type any of the following commands at the prompt to interact with
the program:


             \033[1mControl Commands:\033[0m

             new
             save <filename> (text format)
             load <filename>
             undo
             quit
             printcommandlist
             lengthcommandlist
             help
             dir

             \033[1mTurtle Commands:\033[0m

             forward <distance>
             backward <distance>
             left <angle>
             right <angle>
             goto <x co-ordinate> <y co-ordinate>
             penup
             pendown
             write <text>
             colour <colour>\n\n""")

def new():
    """Aids save and load functionality, and provides a 'blank-slate' method.

    Clears the current command list of all commands, refreshes the screen and
    returns the turtle to home.
    """
    global commandList
    commandList = []
    turtle.reset()

# Requires Python 3.2
def pwd():
    """Save/Load functionality - shows user files available to the program."""
    print("\033[1mFiles in your current directory accessible by this program:\
\033[0m")
    for program in os.listdir():
        print('{}'.format(program))

def save(path, do):
    """Save method.

    Takes the save option (append, over-write) and outputs commands to a
    specified file, delimited by new-lines.

    Upon success, the turtle window displays the saved filename as a title, and
    tells the user where the file is saved on their computer.

    Accounts for I/O errors that may come about from the command being aborted
    prematurely or for other reasons.
    """
    try:
        with open(path, do) as outputFile:
             for command in commandList:
                 outputFile.writelines('{}\n'.format(command))
             outputFile.close()
    except IOError as error:
        print("You cannot save a file with an the illegal character:", error)
    except Exception as error2:
        print("Unknown Error: ", error2)
    turtle.title(path)
    print("{}{}{}{}{}{}".format("""Success!  Your current turtle commands have \
been saved to:\n""", "\033[1m", os.getcwd(), "/", path, "\033[0m"))

def load(path):
    """Load method.

    Loads a each line of a text file (only works if each command is on a
    seperate line) into a list.  Each newline is stripped ready for the commands
    to be assigned to the program command list.

    Accounts for I/O and End of File errors that may come about from corrupt
    files or not closing files correctly.
    """
    try:
        with open(path, 'rt') as inputFile:
            preStrippedList = inputFile.readlines()
            inputFile.close()
        strippedList = []
        normalisedList = []
        for item in preStrippedList:
            strippedList.append(item.strip().rstrip("\n").rstrip().lower())
        blank = ''
        for blank in strippedList:
            strippedList.remove('')
#        strippedList.remove('')
    except IOError as error:
        print("File not found.", error)
    except EOFError as error2:
        print("Cannot read empty lines.", error2)
    except Exception as error3:
        print("Unknown Error: ", error3)
    print("Successfully loaded file into the command list")
    print(strippedList)
    return strippedList

def runLoaded(path):
    """Method to run loaded commands.

    Runs through the command list after loading commands (even if this means
    redrawing commands that have already been drawn before loading subsequent
    commands).  Deletes commands that have been loaded that are invalid 
    commands to leave the command list clean and to keep commands in sync with
    what is drawn on the screen and what is in the command list.

    This method only draws the turtle on the screen and does not alter the
    command list.
    """
    global commandList
    choices = ["run", "r", "do nothing", "d"]
    while True:
        try:
            runLoad = input("""Commands have just been loaded into the command \
list buffer.
Please enter "run" to run these commands now, or "d" to do nothing (leave them
in the buffer with the option to append new commands): """).lower()
            if runLoad == "run" or runLoad == "r":
                initialisePostLoad(path)
                print("Pre-load initialisation complete... Running loaded \
command.....")
                for line in commandList:
                    print(line)
                    commandSplit = line.split()
                    print(commandSplit)
                    try:
                        if commandSplit[0] == "forward":
                            if len(commandSplit) == 2:
                                print("Interactive turtle command recognised")
                                forward(commandSplit[1])
                            else:
                                print("Invalid command, 'forward' takes one \
argument")
                                commandList.remove(line)
                                pass
                        elif commandSplit[0] == "backward":
                            if len(commandSplit) == 2:
                                print("Interactive turtle command recognised")
                                backward(commandSplit[1])
                            else:
                                print("Invalid command, 'backward' takes one \
argument")
                                commandList.remove(line)
                                pass
                        elif commandSplit[0] == "left":
                            if len(commandSplit) == 2:
                                print("Interactive turtle command recognised")
                                left(commandSplit[1])
                            else:
                                print("Invalid command, 'left' takes one \
argument")
                                commandList.remove(line)
                                pass
                        elif commandSplit[0] == "right":
                            if len(commandSplit) == 2:
                                print("Interactive turtle command recognised")
                                right(commandSplit[1])
                            else:
                                print("Invalid command, 'right' takes one \
argument")
                                commandList.remove(line)
                                pass
                        elif commandSplit[0] == "goto":
                            if len(commandSplit) == 3:
                                print("Interactive turtle command recognised")
                                goto(commandSplit[1], commandSplit[2])
                            else:
                                print("Invalid command, 'goto' takes two \
arguments")
                                commandList.remove(line)
                                pass
                        elif commandSplit[0] == "penup":
                            if len(commandSplit) == 1:
                                print("Interactive turtle command recognised")
                                penup()
                            else:
                                print("Invalid command, 'penup' takes no \
arguments")
                                commandList.remove(line)
                                pass
                        elif commandSplit[0] == "pendown":
                            if len(commandSplit) == 1:
                                print("Interactive turtle command recognised")
                                pendown()
                            else:
                                print("Invalid command, 'penup' takes no \
arguments")
                                commandList.remove(line)
                                pass
                        elif commandSplit[0] == "write":
                            if len(commandSplit) >= 2:
                                print("Interactive turtle command recognised")
                                write(commandSplit[1:])
                            else:
                                print("Invalid command, 'write' takes one or \
more arguments")
                                commandList.remove(line)
                                pass
                        elif commandSplit[0] == "colour" or commandSplit[0] == \
"color":
                            if len(commandSplit) == 2:
                                print("Interactive turtle command recognised")
                                colour(commandSplit[1])
                            else:
                                print("Invalid command, 'color' takes one \
arguments")
                                commandList.remove(line)
                                pass
                    except Exception as error:
                        print("You did not enter a valid command! ", error)
                        commandList.remove(line)
                        pass
                break
            elif runLoad == "d" or runLoad == "do nothing":
                break
            elif runLoad not in choices:
                print("Invalid command, please try again!")
        except Exception as error:
            print("Unknown Error: ", error)

def checkSavePath(path):
    """Save options method.

    Allows the user to specify if they want to append or over-write the commands
    that will be saved into a file, or whether they want to select a new file to
    save to.  If no file exists, it will simply save the file to the file-name
    given.
    """
    choices = ["a", "o", "n", "c", "dir"]
    if os.path.isfile(path) == True:
        print("""\nThe file you are attempting to save to already exists!  \
Please enter one of the following commands to continue:
"a" to append the current the current list of commands to the selected file.
"o" to over-write the current list of commands over the selected file.
"n" to select a new file to write to.
"c" to cancel the save menu and return to the main menu.
"dir" to show a list of files in the current directory.""")
        while True:
            try:
                filePath = input("Enter command: ").lower()
                if filePath == "a":
                    save(path, 'at')
                    break
                elif filePath == "o":
                    save(path, 'wt')
                    break
                elif filePath == "n":
                    newFilePath = input("""Please enter the name of the file you
would like to save to instead""")
                    subsequentExtentionChecks = extentionCheck(newFilePath)
                    checkSavePath(subsequentExtentionChecks)
                    break
                elif filePath == "c":
                    break
                elif filePath == "dir":
                    pwd()
                    pass
                elif filePath not in choices:
                    print("Invalid command, please try again!")
            except Exception as error:
                print("Unknown Error: ", error)
    elif os.path.isfile(path) == False:
        save(path, 'wt')
        print("File does not exist!")  

def checkLoadPath(path):
    """Load options method.

    Checks whether the file to be loaded exists on the system, and provides
    multiple load options for what to do with loaded commands, i.e append to
    current commands, save current commands, etc.
    """
    global commandList
    choices = ["a", "append", "n", "newlist", "y", "yes", "n", "no"]
    if os.path.isfile(path) == True:
        if not commandList:
            commandList = load(path)
        elif commandList:
            print("""You already have commands in your command list.
Command options:
"a" to add commands in the specified file to the end of the current command \
list.
"n" to load commands from a file into an empty list (deletes contents of current
list.""")
            while True:
                try:
                    loadOption = input("Please enter a command: ").lower()
                    if loadOption == "a" or loadOption == "append":
                        print("""Would you like to save the commands in the \
current list before loading extra commands?  You will not lose the current set \
of commands, but if you do not save them you will not be able to return to the \
current state.""")
                        while True:
                            try:
                                saveCheck = input("""Please enter "yes" or "no"\
: """).lower()
                                if saveCheck == "y" or saveCheck == "yes":
                                    checkSavePath(path)
                                    print("Loading commands into command list..\
........")
                                    loadedCommands = load(path)
                                    commandList.extend(loadedCommands)
                                    break
                                elif saveCheck == "n" or saveCheck == "no":
                                    loadedCommands = load(path)
                                    commandList.extend(loadedCommands)
                                    break
                                elif saveCheck not in choices[4:]:
                                    print("Command invalid, please try again!")
                            except Exception as error:
                                print("Unknown Error: ", error)
                        break
                    elif loadOption == "n" or loadOption == "newlist":
                        print("""You are about to delete the contents of your \
current command list.  Would you like to save your current commands and program\
 state?""")
                        while True:
                            try:
                                saveCheck = input("""Please enter "yes" or "no"\
: """).lower()
                                if saveCheck == "y" or saveCheck == "yes":
                                    checkSavePath(path)
                                    print("Deleting current commands from \
command list")
                                    new()
                                    initialisePostLoad()
                                    print("Loading commands into command list..\
...............")
                                    commandList = load(path)
                                    break
                                elif saveCheck == "n" or saveCheck == "no":
                                    print("Deleting current commands from \
command list")
                                    new()
                                    initialisePostLoad(path)
                                    print("Loading commands into command list..\
..............")
                                    commandList = load(path)
                                    break
                                elif saveCheck not in choices[4:]:
                                    print("Invalid command, please try again!")
                            except Exception as error:
                                print("Unknown Error: ", error)
                        break
                    elif loadOption not in choices[:4]:
                        print("Invalid command, please try again!")
                except Exception as error:
                    print("Unknown Error: ", error)
    elif os.path.isfile(path) == False:
        print("""The file you are trying to load does not exist.  Please try to
load another file, or type \"dir\" to see a list of loadable files in the
current directory.""")
        pass

def extentionCheck(name):
    """File extention normalisation method.

    Converts the given input file format to .txt regardless of what input
    format the file was in.  This makes passing files that are not convertible
    to a text format pointless.
    """
    root, ext = os.path.splitext(name)
    print("""Please note: any file that is not text based or convertable to .txt
format will not load correctly""")
    print("Your file name: ", root)
    print("Your file extention: ", ext)
    if ext != ".txt":
        ext = ".txt"
    elif ext == ".txt":
        pass
    checkedName = '{}{}'.format(root, ext)
    print('{}{}'.format("Your normalised (file extention added/changed) will \
be: ", checkedName))
    return checkedName

def undo():
    global commandList
    print("The number commands that can be undone: ", \
turtle.undobufferentries())
    undoInput = input("""If you would like to undo just one command type \
"undo".\n\n
Alternatively, if you would like to retrace all the turtle's steps to the \
beginning then please type "reversetimeloop".""")
    if undoInput == "undo":
        turtle.undo()
        commandList.pop()
    elif undoInput == "reversetimeloop":
        while turtle.undobufferentries():
            turtle.undo()
        pass
    else:
        print("Command not recognised")

def endProgram():
    """Program exit method.

    Prompts user to save their work before exiting, as a safety measure.

    Alternative call words "exit" "q" "x" "close" "bye".
    """
    choices = ["yes", "y", "no", "n", "save", "s"]
    while True:
        prompt = input("""Are you sure you wish to exit the program? (data will\
 not be saved).  Type "yes" (exits the program losing current command list), \
"no" (returns to main menu) or "save" to continue... """).lower()
        try:
            if prompt == "yes" or prompt == "y":
                sys.exit('Thank you for using Turtle Graphics. :)')
            elif prompt == "no" or prompt == "n":
                print("Returning to main menu.......")
                break
            elif prompt == "save" or prompt == "s":
                fileName = input("""Please type the name of the file you wish \
to save to: """)
                sExtentionChecked = extentionCheck(fileName)
                confirmSave = checkSavePath(sExtentionChecked)
                while True:
                    try:
                        exitCheck = input("""Now you have saved, are you sure \
you would like to quit?  Type \"yes\" or \"no\": """)
                        if exitCheck == "yes" or exitCheck == "y":
                            sys.exit("""Thank you for using Turtle Graphics.  \
Your file is saved at location: {}.  See you again soon'.format(location)""")
                        elif exitCheck == "no" or exitCheck == "n":
                            print("Returning to main menu........")
                            break
                        elif exitCheck not in choices[:4]:
                            print("Invalid command, please try again!")
                    except Exception as error:
                        print("Unknown Error: ", error)
            elif prompt not in choices:
                print("Invalid command, please try again!")
        except Exception as error:
            print("Unknown Error: ", error)

### TURTLE COMMAND TRANSLATIONS ###

def getScreenResolution():
    """Usability function.

    Uses the tkinter module to discover the width and height of the users screen
    to adapt the turtle drawing box to that of the users personal screen.

    Returns the discovered width and height to the initialisation process, to
    provide 'full-screen' functionality.
    """
    root = Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    print('{}{}{}{}{}'.format("Screen width = ", width, "\n", \
"Screen height = ", height))
    return width, height

def initialise():
    """Program start-up initialisation.

    Provides full-screen or selection of resolution by user input.

    Normalises the turtle to a generic starting setting: a picture of a turtle
    for the turtle object, coloured black.  Sets the turtle to draw at a fast
    but not not extreme speed, and sets the turtle to draw lines in the box.
    """
    choices = ["yes", "y", "no", "n"]
    while True:
        try:
            fullScreen = input("""Would you like to run the turtle program \
full-screen?
Enter "yes" or "no" (you will be able to enter a custom resolution if "no"): \
""")
            if fullScreen == "yes" or fullScreen == "y":
                screenResolution = getScreenResolution()
                turtle.setup(screenResolution[0], screenResolution[1])
                print("Full-screen enabled")
                break
            elif fullScreen == "no" or fullScreen == "n":
                width = int(input("Enter the width of the turtle display: "))
                height = int(input("Enter the height of the turtle display: "))
                resolution = (width, height)
                print(resolution)
                turtle.setup(resolution[0], resolution[1])
                break
            elif fullScreen not in choices:
                print("Invalid command, try again....")
        except Exception as error:
            print("Unknown Error: ", error)
    turtle.title("Untitled Turtle Program")
    turtle.shape("turtle")
    turtle.color("black")
    turtle.speed(7)
    turtle.pendown()
    print("Ready to take commands and draw on the screen...")

def initialisePostLoad(path):
    """See: initialise method: same process without screen resolution process

    Adds extra 'title' functionality, displaying the name of the loaded file as
    the title.
    """
    turtle.title(path)
    turtle.shape("turtle")
    turtle.color("black")
    turtle.speed(7)
    turtle.pendown()

def convertfloat(value):
    """Converts the passed string argument to a floating-point value"""
    quantity = float(value)
    return quantity

def forward(quantity):
    """Turtle animation function.

    Moves the turtle forwards by the amount of the passed quantity (converted
    from a string to a floating-point value).
    """
    convertedQuantity = convertfloat(quantity)
    turtle.forward(convertedQuantity)

def backward(quantity):
    """Turtle animation function.

    Moves the turtle backwards by the amount of the passed quantity (converted
    from a string to a floating-point value).
    """
    convertedQuantity = convertfloat(quantity)
    turtle.backward(convertedQuantity)

def left(quantity):
    """Turtle animation function.

    Rotates the turtle to the left by the number of degrees of the quantity
    passed to the function.
    """
    convertedQuantity = convertfloat(quantity)
    turtle.left(convertedQuantity)

def right(quantity):
    """Turtle animation function.

    Rotates the turtle to the right by the number of degrees of the quantity
    passed to the function.
    """
    convertedQuantity = convertfloat(quantity)
    turtle.right(convertedQuantity)

def goto(x, y):
    """Turtle animation function.

    Moves the turtle relative to its current position by the passed x-coordinate
    and y-coordinate, which are converted to floating-point values before being
    animated.
    """
    convertedQuantity1 = convertfloat(x)
    convertedQuantity2 = convertfloat(y)
    turtle.goto(convertedQuantity1, convertedQuantity2)

def penup():
    """Notifies the turtle module that subsequent inputs will not be drawn"""
    turtle.penup()

def pendown():
    """Notifies the turtle module that subsequent inputs will be drawn"""
    turtle.pendown()

def write(quantity):
    """Turtle animation function.

    Writes the passed string of text directly above the position of the turtle
    on the screen, with extra parameters defining the font for extra
    readability.
    """
    joined = ' '.join(quantity)
    turtle.write(joined, font = ("Comic Sans", 12, "bold"))

# Could expand this so that the turtle program can accept an RGB colorcode
def colour(color):
    """Turtle animation function.

    Directly changes the colour of the turtle on the screen to one of specified
    colours.  Will not accept any colours that are not included in the selected
    list.
    """
    try:
        if color in colourChoices:
            turtle.color(color)
        elif color not in colourChoices:
            print("""Invalid colour selection. Please enter a valid colour: \
"red", "blue", "green", "yellow", "magenta", "cyan" or "black"\
""")
    except turtle.TurtleGraphicsError as error:
        print('Invalid colour ', error, 'Please enter a valid colour: "red"\
        , "blue", "green", "yellow", "magenta", "cyan" or "black"')


############################## MAIN PROGRAM ####################################

# I made the screen resolution a requirement of the initialisation stage because
# of previous issues with previous turtle programs I have made where the
# difference in screen sizes has meant that in some cases the box that the
# turtle draws in has gone beyond the resolution of some users.

# Because I now give the option for the user to go full-screen, or select their
# own resolution, the trade-off between functionality and the size of the screen
# is now left up to the user.
def main():
    global commandSplit
    global command
    print('''\n\033[1mWelcome to Turtle Graphics.\033[0m  Please type any of \
the following commands to interact with the program, or type \033[1m"help" \
\033[0mto prompt the list of commands at any time:


             \033[1mControl Commands:\033[0m

             new
             save <filename[extention added/modifed regardless of input]>
             load <filename>
             undo
             quit
             printcommandlist
             lengthcommandlist
             help
             dir


             \033[1mTurtle Commands:\033[0m

             forward <distance>
             backward <distance>
             left <angle>
             right <angle>
             goto <x co-ordinate> <y co-ordinate>
             penup
             pendown
             write <text>
             colour <colour>\n\n''')
    print("Initialising program......")
    initialise()
    if len(sys.argv) == 2:
        lExtentionChecked = extentionCheck(sys.argv[1])
        confirmLoad = checkLoadPath(lExtentionChecked)
        runLoaded(lExtentionChecked)
    while True:
        try:
            command = input('What would you like to do? ').lower()
            commandSplit = command.strip().split()
            if commandSplit[0] in choices:
                print('Command recognised')
                try:
                    if commandSplit[0] == "help" or commandSplit[0] == "h":
                        help()
                    elif commandSplit[0] == "printcommandlist":
                        printCommandList()
                    elif commandSplit[0] == "lengthcommandlist":
                        currentLength()
                    elif commandSplit[0] == "dir":
                        pwd()
                    elif commandSplit[0] == "new":
                        new()
                    elif commandSplit[0] == "save":
                        sExtentionChecked = extentionCheck(commandSplit[1])
                        confirmSave = checkSavePath(sExtentionChecked)
                    elif commandSplit[0] == "load":
                        lExtentionChecked = extentionCheck(commandSplit[1])
                        confirmLoad = checkLoadPath(lExtentionChecked)
                        runLoaded(lExtentionChecked)
                    elif commandSplit[0] == "undo":
                        undo()
                    elif commandSplit[0] == "quit" or commandSplit[0] == \
"q" or commandSplit[0] == "exit" or commandSplit[0] == "x" or commandSplit[0] \
== "close" or commandSplit[0] == "bye":
                        endProgram()
                except Exception as error:
                    print("Unknown Error", error)
            elif commandSplit[0] in interactiveChoices:
                try:
                    if commandSplit[0] == "forward":
                        if len(commandSplit) == 2:
                            print("Interactive turtle command recognised")
                            forward(commandSplit[1])
                            toSave = ' '.join(commandSplit)
                            commandList.append(toSave)
                        else:
                            print("Invalid command, 'forward' takes one \
argument")
                            pass
                    elif commandSplit[0] == "backward":
                        if len(commandSplit) == 2:
                            print("Interactive turtle command recognised")
                            backward(commandSplit[1])
                            toSave = ' '.join(commandSplit)
                            commandList.append(toSave)
                        else:
                            print("Invalid command, 'backward' takes one \
argument")
                            pass
                    elif commandSplit[0] == "left":
                        if len(commandSplit) == 2:
                            print("Interactive turtle command recognised")
                            left(commandSplit[1])
                            toSave = ' '.join(commandSplit)
                            commandList.append(toSave)
                        else:
                            print("Invalid command, 'left' takes one \
argument")
                            pass
                    elif commandSplit[0] == "right":
                        if len(commandSplit) == 2:
                            print("Interactive turtle command recognised")
                            right(commandSplit[1])
                            toSave = ' '.join(commandSplit)
                            commandList.append(toSave)
                        else:
                            print("Invalid command, 'right' takes one \
argument")
                            pass
                    elif commandSplit[0] == "goto":
                        if len(commandSplit) == 3:
                            print("Interactive turtle command recognised")
                            goto(commandSplit[1], commandSplit[2])
                            toSave = ' '.join(commandSplit)
                            commandList.append(toSave)
                        else:
                            print("Invalid command, 'goto' takes two \
arguments")
                            pass
                    elif commandSplit[0] == "penup":
                        if len(commandSplit) == 1:
                            print("Interactive turtle command recognised")
                            penup()
                            toSave = ' '.join(commandSplit)
                            commandList.append(toSave)
                        else:
                            print("Invalid command, 'penup' takes no \
arguments")
                            pass
                    elif commandSplit[0] == "pendown":
                        if len(commandSplit) == 1:
                            print("Interactive turtle command recognised")
                            pendown()
                            toSave = ' '.join(commandSplit)
                            commandList.append(toSave)
                        else:
                            print("Invalid command, 'penup' takes no \
arguments")
                            pass
                    elif commandSplit[0] == "write":
                        if len(commandSplit) >= 2:
                            print("Interactive turtle command recognised")
                            write(commandSplit[1:])
                            toSave = ' '.join(commandSplit)
                            commandList.append(toSave)
                        else:
                            print("Invalid command, 'write' takes one or \
more arguments")
                            pass
                    elif commandSplit[0] == "colour" or commandSplit[0] == \
"color":
                        if len(commandSplit) == 2 and commandSplit[1] in \
colourChoices:
                            print("Interactive turtle command recognised")
                            colour(commandSplit[1])
                            toSave = ' '.join(commandSplit)
                            commandList.append(toSave)
                        else:
                            print("Invalid command, 'color' takes one \
arguments")
                            pass
                except Exception as error:
                    print("You did not enter a valid command! ", error)
            elif commandSplit[0] not in choices or commandSplit[0] not in \
interactiveChoices:
                print("""The command you entered is not allowed.  Try \
again, or type "help" for a list of available commands.""")
        except IndexError as error:
            print("You cannot do nothing... Please enter a command")
        except Exception as error2:
            print("Unknown Error: ", error2)


if __name__ == "__main__":
    main()
