from tkinter import *
from tkinter import filedialog
from tkinter import font

link = "https://www.youtube.com/watch?v=rUgAC_Ssflw"
root = Tk()
root.title("Text Pad")
# root.iconbitmap()
root.geometry("1200x660")
whitespace = "        "
workdir = "D:/document/lang/"

# Set variable to access
global openStatusName
openStatusName = False

# Create file function
def newFile():
    # Delete previous text
    textBox.delete("1.0", END)
    # Update status bar
    root.title("New file - Text Pad")
    statusBar.config(text=f"New File{whitespace}")

def openFile():
    # Delete previous text
    textBox.delete("1.0", END)

    # Grab filename
    textFile = filedialog.askopenfile(initialdir=workdir, title="Open File",
                                      filetypes=(("Text Files", "*.txt"), ("HTML Files", "*.html"),
                                                 ("All Files", "*.*")))
    # Check file name is true
    if textFile:
        global openStatusName
        openStatusName = textFile

    # Update status bar
    name = textFile.name
    statusBar.config(text=f"{name}{whitespace}")
    name = name.replace(workdir, "")
    root.title(f"{name} - Text Pad")
    # Open file
    textFile = open(textFile.name, 'r', encoding='utf8')
    textFile = open(textFile.name, 'r', encoding='utf8')
    stuff = textFile.read()
    # Add file to textbox
    textBox.insert(END, stuff)
    # Close the opened file
    textFile.close()

# Save file
def saveAsFile():
    textFile = filedialog.asksaveasfilename(defaultextension=".*", initialdir=workdir,
                                            title="Save File", filetypes=(("Text Files", "*.txt"),
                                                                          ("HTML Files", "*.html"),
                                                                          ("All Files", "*.*")))
    if textFile:
        # Update status bar
        name = textFile
        statusBar.config(text=f"Saved: {name}")
        name = name.replace(workdir, "")
        root.title(f"{name} - Text Pad")

        # Save file
        textFile = open(textFile, 'w', encoding='utf8')
        textFile.write(textBox.get(1.0, END))
        # Close file
        textFile.close()


def saveFile():
    global openStatusName
    name = openStatusName.name
    if name:
        # Save file
        textFile = open(name, 'w')
        textFile.write(textBox.get(1.0, END))
        # Close file
        textFile.close()
        # Set file status
        statusBar.config(text=f"Saved: {name}")
    else:
        saveAsFile()


# Create main frame
mainFrame = Frame(root)
mainFrame.pack(pady=5)

# Creat text box scrollbar
textScroll = Scrollbar(mainFrame)
textScroll.pack(side=RIGHT, fill=Y)

# Create text box
textBox = Text(mainFrame, width=97, height=25, font=("Helvetica", 16),
               selectbackground="yellow", selectforeground="black", undo=True,
               yscrollcommand=textScroll.set)
textBox.pack()

# Configure scrollbar
textScroll.config(command=textBox.yview)

# Create menu
myMenu = Menu(root)
root.config(menu=myMenu)

# Add file menu
fileMenu = Menu(myMenu, tearoff=False)
myMenu.add_cascade(label="File", menu=fileMenu)
fileMenu.add_command(label="New", command=newFile)
fileMenu.add_command(label="Open", command=openFile)
fileMenu.add_command(label="Save", command=saveFile)
fileMenu.add_command(label="Save as", command=saveAsFile)
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=root.quit)

# Add edit menu
editMenu = Menu(myMenu, tearoff=False)
myMenu.add_cascade(label="Edit", menu=editMenu)
editMenu.add_command(label="Copy")
editMenu.add_command(label="Paste")
editMenu.add_command(label="Cut")
editMenu.add_command(label="Undo")
editMenu.add_command(label="Redo")

# Add status bar to the bottom of the notepad
statusBar = Label(root, text=f"Ready{whitespace}", anchor=E)
statusBar.pack(fill=X, side=BOTTOM, ipady=5)

root.mainloop()