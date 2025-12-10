import tkinter as tk
import os.path as path

def InputGUI(frame, message, row):
    tk.Label(frame, text=message).grid(row=row, column=0, sticky="w")
    entry = tk.Entry(frame, width=30)
    entry.grid(row=row, column=1, padx=5)
    return entry

def ButtonGUI(oldEntry, newEntry, oldText, newText, error):
    fpOld = oldEntry.get().strip()
    fpNew = newEntry.get().strip()
    # Clears the previous message
    error.config(text="")

    if fpOld == "" or fpNew == "":
        error.config(text="Please enter both files") 
        return

    oldFile = File("old", fpOld)
    newFile = File("new", fpNew)

    if not(oldFile) and not(newFile):
        error.config(text="Old and new files not found, please try again")
        return
    elif not(oldFile):
        error.config(text="Old file not found, please try again")
        return
    elif not(newFile):
        error.config(text="New file not found, please try again")
        return

    oldText.delete("1.0", tk.END)
    oldText.insert("1.0", oldFile)

    newText.delete("1.0", tk.END)
    newText.insert("1.0", newFile)

def File(x, fp):
    # Folder with the GUI's directory. 
    dirGUI = path.dirname(path.abspath(__file__))

    # Root directory.
    dirRoot = path.join(dirGUI, "..")

    #fp = input("Enter the "+x+" file: ")

    if (x == "old"):
        #New_File_Versions Folder.
        dirData = path.join(dirRoot, "Old_File_Versions")
        dirPath = path.join(dirData, fp)
    elif (x == "new"):
        #Old_File_Versions Folder.
        dirData = path.join(dirRoot, "New_File_Versions")
        dirPath = path.join(dirData, fp)

    try:
        file = open(dirPath, "r")
        return file.read()
    except FileNotFoundError:
        return 0


root = tk.Tk()
root.title("LHdiff")

top = tk.Frame(root)
top.pack(fill="x", padx=10, pady=10)

oldEntry = InputGUI(top, "Enter the old file: ", 0)
newEntry = InputGUI(top, "Enter the new file: ", 1)

error = tk.Label(top, text="", fg="red")
error.grid(row=2, column=0, columnspan=2, pady=(0,5))

bottom = tk.Frame(root)
bottom.pack(fill="both", expand=True)

left = tk.Frame(bottom)
right = tk.Frame(bottom)
left.pack(side="left", fill="both", expand=True)
right.pack(side="right", fill="both", expand=True)

tk.Label(left, text="Old File:", font=("Arial", 16, "bold")).pack(anchor="w")
tk.Label(right, text="New File:", font=("Arial", 16, "bold")).pack(anchor="w")

oldText = tk.Text(left, wrap="word")
oldText.pack(side="left", fill="both", expand=True)

newText = tk.Text(right, wrap="word")
newText.pack(side="right", fill="both", expand=True)

tk.Button(top, text="Enter", command=lambda:ButtonGUI(oldEntry, newEntry, oldText, newText, error)).grid(row=3, column=0, columnspan=2, pady=5)

root.mainloop()