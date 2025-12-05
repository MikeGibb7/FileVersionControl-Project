import tkinter as tk
import os.path as path

def File(x):
    # folder where main.py lives
    dirMain = path.dirname(path.abspath(__file__))

    # project root (go up one directory)
    dirRoot = path.join(dirMain, "..")

    # fp = input("Enter the "+x+" file: ")

    if (x == "old"):
        #New_File_Versions Folder
        dirData = path.join(dirRoot, "New_File_Versions")
        dirPath = path.join(dirData, "NewFile1.txt")
    elif (x == "new"):
        #Old_File_Versions Folder
        dirData = path.join(dirRoot, "Old_File_Versions")
        dirPath = path.join(dirData, "OldFile1.txt")

    try:
        file = open(dirPath, "r")
        return file.read()
    except FileNotFoundError:
        print("File not found.")


root = tk.Tk()

oldFile = File("old")
newFile = File("new")

root.title("Test")
frame = tk.Frame(root)
frame.pack(fill="both", expand=True)

oldText = tk.Text(frame, wrap="word")
oldText.pack(side="left", fill="both", expand=True)
oldText.insert("1.0", oldFile)

newText = tk.Text(frame, wrap="word")
newText.pack(side="right", fill="both", expand=True)
newText.insert("1.0", newFile)

root.mainloop()