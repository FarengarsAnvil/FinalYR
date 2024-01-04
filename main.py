import os
import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.ttk import *
import platform
import psutil
import re


def overrideClose():
    pass


def getDocs():
    os.system("start \"\" https://github.com/FarengarsAnvil/FinalYR")


def blockMode():
    # TODO:: Init Blocker Mode Window, Close Timer Window.
    window.destroy()
    global Window2
    Window2 = Tk()
    Window2.protocol("WM_DELETE_WINDOW", overrideClose)
    Window2.geometry("500x510")
    Window2.title("Blocker Mode: Disable Distractions")
    menubar2 = Menu(Window2)
    Window2.config(menu=menubar2)
    optionMenu2 = Menu(menubar2, tearoff=0, font=("Helvetica", 9))
    menubar2.add_cascade(label="Options", menu=optionMenu2)
    optionMenu2.add_command(label="Help", command=displayHelp)
    optionMenu2.add_separator()
    optionMenu2.add_command(label="Tutorial", command=messageFive)
    optionMenu2.add_separator()
    optionMenu2.add_command(label="Documentation", command=getDocs)
    optionMenu2.add_separator()
    optionMenu2.add_command(label="Exit", command=exitProg)
    start = Button(Window2, text="Start Blocker", command=startBlock2).pack(pady=35)
    selectButton = Button(Window2, text="Select Applications to Block", command=blockFile).pack()
    saveButton2 = Button(Window2, text = "Save Blocklist", command=saveBlockList).pack()
    Window2.mainloop()


def startBlock():
    # TODO:: Starts Blocker Mode after the timer has ended.
    global timeList
    try:
        for process in psutil.process_iter():
            if process.name() in timeList:
                process.kill()
        window.after(1000, startBlock)
    except psutil.NoSuchProcess:
        window.after(1000, startBlock)
    except NameError:
        pass


def startBlock2():
    # TODO:: Starts Blocker Mode after Programs are Selected.
    try:
        for process in psutil.process_iter():
            if process.name() in fileList:
                process.kill()
        Window2.after(1000, startBlock2)
    except psutil.NoSuchProcess:
        Window2.after(1000, startBlock2)
    except NameError:
        messagebox.showinfo("Info", "Choose Applications before starting.")
    except TypeError:
        messagebox.showinfo("Info", "Blocker has been stopped.")
        return


def blockFile():
    # TODO:: fetches the Program Processes name in a string from Filemenu and appends it to  fileList
    global fileList
    fileList = []
    while True:
        global file
        filepath = askopenfilename(title="Select File")
        checker = [".exe"]  # Used to Check if File String is an .exe by Comparison
        file = os.path.basename(filepath)
        if filepath == "":
            break
            # If the user presses Cancel in file-menu it will return to Main GUI Window
        if any([x in file for x in checker]):
            # Checks Program is an .exe and adds it to the fileList Array if so.
            fileList.append(file)
            messagebox.showinfo("Program Selected", "You have added " + file + " to blocklist")
        else:
            messageTwo()


def main():
    # TODO:: Initialise Main GUI Window, Initialise Widgets.
    global window
    global programTime
    global progress
    loadTimeList()
    window = Tk()
    window.protocol("WM_DELETE_WINDOW", overrideClose)  # Overrides default close button
    window.geometry("500x510")
    window.title("Program Timer")
    programTime = tkinter.IntVar()  # Holds userInput from timeEntry
    menubar = Menu(window)
    window.config(menu=menubar)
    optionMenu = Menu(menubar, tearoff=0, font=("Helvetica", 9))
    menubar.add_cascade(label="Options", menu=optionMenu)
    optionMenu.add_command(label="Blocker Mode", command=blockMode)
    optionMenu.add_separator()
    optionMenu.add_command(label="Help", command=displayHelp)
    optionMenu.add_separator()
    optionMenu.add_command(label="Documentation", command=getDocs)
    optionMenu.add_separator()
    optionMenu.add_command(label="Exit", command=exitProg)
    startButton = Button(window, text="Start Timer", command=start, width=15).pack(side=TOP, pady=15)
    programButton = Button(window, text="Select Apps", command=openfile, width=15).pack(side=TOP)
    submitButton = Button(window, text="Confirm Timer", command=submit, width=15).pack(side=TOP, pady=10)
    timerPrompt = Label(window, text="Enter Time Duration", font=("Helvetica", 9)).pack()
    timeEntry = Entry(window, width=25, textvariable=programTime)
    timeEntry.pack(pady=5)
    progress = DoubleVar()
    progressBar = Progressbar(window, orient=HORIZONTAL, mode="determinate", variable=progress).pack(pady=15)
    showTimeListButton = Button(window, text="Show Timelist", command=displayTime, width=15).pack(pady=10)
    saveListButton = Button(window, text="Save Timelist", command=saveTimeList, width=15).pack(pady=5)
    clrButton = Button(window, text="Clear Timelist", command=resetTimeList, width=15).pack(pady=10)
    # Progress Variable is for updating the Progressbar as time goes on.
    window.mainloop()


def exitProg():
    # TODO:: Exit application
    exit()


def messageOne():
    # TODO:: Displays message telling user the Purpose and function of the Buttons and order.
    messagebox.showinfo("Help",
                        "Enter the timer amount in the Textbox, press the confirm timer button in order for timer to work.\n"
                        "This can be done before or After choosing Programs.")


def messageTwo():
    # TODO:: Displays Message telling User Filetype must be .exe and exe only.
    messagebox.showinfo("Help",
                        "When selecting a program it must be of the Filetype '.exe' Executable.\n"
                        "Select all applications before pressing Cancel to return.")


def messageThree():
    # TODO:: Displays message telling user that Textbox is for entering Number of Minutes to time application.
    messagebox.showinfo("Help",
                        "The Number you enter into the textbox is the number of Minutes until the Program is timed to Close.")


def messageFour():
    # TODO:: Displays message after Invalid input into Timer entrybox.
    messagebox.showerror("Error", "User must enter a Whole Number ONLY.")


def messageFive():
    # TODO:: Displays a message to the user on how to use Blocker Mode.
    messagebox.showinfo("Tutorial",
                        "Blocker mode is used to disable processes and applications from running by killing them automatically."
                        "\n"
                        "\nChoose the programs you want to disable, and then press start button."
                        "\n"
                        "\nBlocker mode is ended by closing the application.\nThen you can resume usage of the Programs that were blocked."
                        "\n"
                        "\nBlocker mode also resets on close, so you have to re-add the programs you want to disable everytime for now.")


def displayHelp():
    # TODO::Calls all 3 messages when the user clicks on the Help button in the options menu.
    messageOne()
    messageTwo()
    messageThree()


def start():
    # TODO:: function for the start button that starts the timer, and is responsible for progressBar and counter updating.
    try:
        global counter
        global progress
        global timeList
        global timeInput
        if counter == timeInput:
            for i in range(len(timeList)):
                if platform.system() == "Windows":
                    os.system("TASKKILL /F /IM " + timeList[i])  # OS Shell Command
                elif platform.system() == "Linux":
                    os.system("killall -KILL" + timeList[i])
                elif platform.system() == "Darwin":
                    os.system("pkill -9" + timeList[i])
            messagebox.showinfo("Success", "All programs Terminated.")
            progress.set(0)
            startBlock()
        else:
            progress.set((counter / timeInput) * 100)
            counter = counter + 1
            window.after(1000, start)
    except NameError:
        messagebox.showinfo("Info", "Submit timer and choose Programs before pressing start.")


def submit():
    # TODO:: Takes userInput and saves it, user must enter Timer value >= 1, as 1 Minute is the Minimum.
    try:
        global counter
        minuteToSecond = 60
        counter = 0
        global timeInput
        timeInput = programTime.get() * minuteToSecond
        if programTime.get() < 1 or programTime.get() > 60:
            messagebox.showerror("Error", "Time Limit must be between 1 and 60 Minutes")
            programTime.set(0)
    except TclError:
        messageFour()
        programTime.set(0)


def openfile():
    # TODO::Opens the File Menu, allowing the User to select the Applications they want to time.
    global timeList
    timeList = []
    while True:
        global file
        filepath = askopenfilename(title="Select File")
        checker = [".exe"]
        # Checker array used to check if the Program selected is an .exe
        file = os.path.basename(filepath)
        if filepath == "":
            break
        if any([x in file for x in checker]):
            timeList.append(file)
            messagebox.showinfo("Program Selected", "You have selected " + file)
        else:
            messageTwo()


def getBlocklist():
    # TODO:: Returns Blocklist and all it's contents
    return fileList


def getTimeList():
    # TODO:: Returns timeList and all it's Contents
    return timeList


def displayTime():
    # TODO:: Mapped to Button that displays all Timed Applications On Click.
    try:
        global timeList
        messagebox.showinfo("Applications", "Timed Apps: " + str(timeList))
    except NameError:
        messagebox.showinfo("Info", "Timelist is Empty.")


def resetTimeList():
    # TODO:: Mapped to Button that clears all Timed Applications on click and clears Saved Timelist.
    try:
        global timeList
        timeList.clear()
        messagebox.showinfo("Info", "Timelist Cleared.")
        if os.path.exists("Timelist.txt"):
            os.remove("Timelist.txt")
        else:
            pass
    except NameError:
        pass


def saveTimeList():
    # TODO:: Writes the Timelist to file.
    timeFile = open("Timelist.txt", "w")
    timeFile.write(str(timeList))
    timeFile.close()
    messagebox.showinfo("Saved", "The Timelist has been saved.")


def saveBlockList():
    # TODO:: Writes the fileList Array to File, which contains the Applications that have been added to the blocklist for Blocker mode.
    blockFile = open("Blocklist.txt", "w")
    blockFile.write(str(fileList))
    blockFile.close()
    messagebox.showinfo("Saved", "The Blocklist has been saved.")


def loadTimeList():
    # TODO:: Loads the Timelist from the File back into the application. Checks if Empty.
    try:
        global timeList
        loadTime = open("Timelist.txt", "r")
        timeList = loadTime.read()
    except FileNotFoundError:
        pass


def loadBlockList():
    # TODO:: Loads the Blocklist from thw File back into Blockermode. Checks if it is Empty initially.
    pass


if __name__ == '__main__':
    main()
