import tkinter as tk
import os.path as path

def InputGUI(frame, message, row):
    tk.Label(frame, text=message).grid(row=row, column=0, sticky="w")
    entry = tk.Entry(frame, width=30)
    entry.grid(row=row, column=1, padx=5)
    return entry

def ButtonGUI(oldEntry, newEntry, oldText, newText):
    fpOld = oldEntry.get().strip()
    fpNew = newEntry.get().strip()

    oldFile = File("old", fpOld)
    newFile = File("new", fpNew)

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
        print("File not found.")
        exit(1)


root = tk.Tk()
root.title("LHdiff")

top = tk.Frame(root)
top.pack(fill="x", padx=10, pady=10)

oldEntry = InputGUI(top, "Enter the old file: ", 0)
newEntry = InputGUI(top, "Enter the new file: ", 1)

bottom = tk.Frame(root)
bottom.pack(fill="both", expand=True)

oldText = tk.Text(bottom, wrap="word")
oldText.pack(side="left", fill="both", expand=True)

newText = tk.Text(bottom, wrap="word")
newText.pack(side="right", fill="both", expand=True)

tk.Button(top, text="Enter", command=lambda:ButtonGUI(oldEntry, newEntry, oldText, newText)).grid(row=2, column=0, columnspan=2, pady=5)

root.mainloop()