from tkinter import *
from tkinter import filedialog
from tkinter import font

root = Tk()
root.title("Text Pad")
# root.iconbitmap()
root.geometry("1200x660")
whitespace = "        "
workdir = "D:/document/lang/"

# Set variable to access
global openStatusName
openStatusName = False
global selected
selected = False

# Create file function

def new_file():
    # Delete previous text
    textBox.delete("1.0", END)
    # Update status bar
    root.title("New file - Text Pad")
    statusBar.config(text=f"New File{whitespace}")


def open_file():
    # Delete previous text
    textBox.delete("1.0", END)

    # Grab filename
    text_file = filedialog.askopenfile(initialdir=workdir, title="Open File",
                                       filetypes=(("Text Files", "*.txt"), ("HTML Files", "*.html"),
                                                  ("All Files", "*.*")))
    # Check file name is true
    if text_file:
        global openStatusName
        openStatusName = text_file

    # Update status bar
    name = text_file.name
    statusBar.config(text=f"{name}{whitespace}")
    name = name.replace(workdir, "")
    root.title(f"{name} - Text Pad")
    # Open file
    text_file = open(text_file.name, 'r', encoding='utf8')
    text_file = open(text_file.name, 'r', encoding='utf8')
    stuff = text_file.read()
    # Add file to textbox
    textBox.insert(END, stuff)
    # Close the opened file
    text_file.close()


# Save file

def save_as_file():
    text_file = filedialog.asksaveasfilename(defaultextension=".*", initialdir=workdir,
                                             title="Save File", filetypes=(("Text Files", "*.txt"),
                                                                           ("HTML Files", "*.html"),
                                                                           ("All Files", "*.*")))
    if text_file:
        # Update status bar
        name = text_file
        statusBar.config(text=f"Saved: {name}")
        name = name.replace(workdir, "")
        root.title(f"{name} - Text Pad")

        # Save file
        text_file = open(text_file, 'w', encoding='utf8')
        text_file.write(textBox.get(1.0, END))
        # Close file
        text_file.close()


def save_file():
    global openStatusName
    name = openStatusName.name
    if name:
        # Save file
        text_file = open(name, 'w')
        text_file.write(textBox.get(1.0, END))
        # Close file
        text_file.close()
        # Set file status
        statusBar.config(text=f"Saved: {name}")
    else:
        save_as_file()


# Copy Texts


def copy_text(e):
    pass


def cut_text(e):
    if textBox.selection_get():
        # Grab selected text
        selected = textBox.selection_get()
        # Delete selected text
        textBox.delete("sel.first", "sel.last")


def paste_text(e):
    if selected:
        position = textBox.index(INSERT)
        textBox.insert(position, selected)


# Create main frame
mainFrame = Frame(root)
mainFrame.pack(pady=5)

# Create text box scrollbar
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
fileMenu.add_command(label="New", command=new_file)
fileMenu.add_command(label="Open", command=open_file)
fileMenu.add_command(label="Save", command=save_file)
fileMenu.add_command(label="Save as", command=save_as_file)
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=root.quit)

# Add edit menu
editMenu = Menu(myMenu, tearoff=False)
myMenu.add_cascade(label="Edit", menu=editMenu)
editMenu.add_command(label="Copy", command=lambda: copy_text(False))
editMenu.add_command(label="Paste", command=lambda: paste_text(False))
editMenu.add_command(label="Cut", command=lambda: cut_text(False))
editMenu.add_command(label="Undo")
editMenu.add_command(label="Redo")

# Add status bar to the bottom of the notepad
statusBar = Label(root, text=f"Ready{whitespace}", anchor=E)
statusBar.pack(fill=X, side=BOTTOM, ipady=5)

root.mainloop()
