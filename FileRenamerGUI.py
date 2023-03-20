"""
Last Update:26-Dec-2022
"""

# Import the Libraries
import pandas as pd
import os
import sys
from tkinter import *
from tkinter import filedialog, messagebox

# Commands for widgets
# Select files and store in global variable.
filenames = []
output_filenames = []
rootDirectory = ''
listOfFolders = []

def ResetContainers():
    filenames = []
    output_filenames = []
    rootDirectory = ''
    listOfFolders = []

def SwitchButtonState(mode):
    ## To switch buttons states to prevent rerunning into an error without proper file selection as input
    ## i.e. Have to click on Select Files button first, then the other two buttons will be set to NORMAL
    global root, Frame_01, Frame_NestedRenamer, Frame_02, changefilename_button, changeext_button, nestRenameButton
    
    if mode == 1:
        if (changefilename_button['state'] == DISABLED):
            changefilename_button['state'] = NORMAL
        else:
            changefilename_button['state'] = DISABLED

        if (changeext_button['state'] == DISABLED):
            changeext_button['state'] = NORMAL
        else:
            changeext_button['state'] = DISABLED
            
    if mode == 2:
        if (nestRenameButton['state'] == DISABLED):
            nestRenameButton['state'] = NORMAL
        else:
            nestRenameButton['state'] = DISABLED
        
def RefreshFrame02():
    ## To refresh the view if conducting batch of renaming.
    for index, widget in enumerate(Frame_02R.winfo_children()):
            widget.destroy()

def SelectFile():
    global filenames, output_filenames, rootDirectory, listOfFolders
    global root, Frame_01, Frame_02, Frame_02L
    ResetContainers()
    
    ## Load filedialog window for selecting files. Initial directory will be at Desktop
    filetypes = (('All files', '*.*'), ('text files', '*.txt'))
    filenames = filedialog.askopenfilenames(title='Select files', initialdir='D:\\Desktop', filetypes=filetypes)
    
    ## Error checking for number of files selected. 
    ## If there are >= 1 files selected, print the output number in the status widget.
    if len(filenames) > 0:
        ## Create 1-liner summary
        filenameset_lbl = Label(Frame_02L, text = f"{len(filenames)} files selected.", width = 20, relief = RIDGE, bg = "black", fg ="white")
        filenameset_lbl.grid(row = 0, column = 0, sticky = W, padx = 5, pady = 1)
        ## Create Listbox of files name selected.
        file_listbox = Listbox(Frame_02L, width = 50)
        for index, name in enumerate(filenames):
            file_listbox.insert(END, name.rsplit('/', 1)[-1])
        file_listbox.grid(row = 1, column = 0, sticky = W, padx = 5, pady = 1)
        SwitchButtonState(1)
    else:
        messagebox.showerror("ERROR MESSAGE", "No files selected.")
        filenames = []
    
    RefreshFrame02()
    
def SelectDirectory():
    global filenames, output_filenames, rootDirectory, listOfFolders
    global root, Frame_NestedRenamer, Frame_02, Frame_02L, Frame_02R
    ResetContainers()
    
    ## Load filedialog window for selecting files. Initial directory will be at Desktop
    rootDirectory = filedialog.askdirectory(title='Select Directory', initialdir='D:\\Desktop')
    os.chdir(rootDirectory)
    listOfFolders = [fld for fld in os.listdir() if not os.path.isfile(fld)]
    
    ## Error checking for number of Folders within rootDirectory. 
    ## If there are >= 1 folders selected, print the output number in the status widget.
    if len(listOfFolders) > 0:
        ## Create 1-liner summary
        filenameset_lbl = Label(Frame_02L, text = f"{len(listOfFolders)} folders found.", width = 20, relief = RIDGE, bg = "black", fg ="white")
        filenameset_lbl.grid(row = 0, column = 0, sticky = W, padx = 5, pady = 1)
        ## Create Listbox of files name selected.
        file_listbox = Listbox(Frame_02L, width = 50)
        for index, name in enumerate(listOfFolders):
            file_listbox.insert(END, name.rsplit('/', 1)[-1])
        file_listbox.grid(row = 1, column = 0, sticky = W, padx = 5, pady = 1)
        SwitchButtonState(2)
    elif len(listOfFolders) == 0:
        messagebox.showerror("ERROR MESSAGE", f"0 folders found in {rootDirectory}.")
        listOfFolders = []
    else:
        messagebox.showerror("ERROR MESSAGE", "No rootDirectory selected.")
        listOfFolders = []
    
    RefreshFrame02()
    
def NestedRename():
    global filenames, output_filenames, rootDirectory, listOfFolders
    global root, Frame_NestedRenamer, Frame_02, Frame_02L, Frame_02R
    os.chdir(rootDirectory)
    nestedContentCount = 0
    
    for folderName in listOfFolders:
        ## 1. Store folder name and path
        activeFolderName = folderName
        activeFolderPath = f"{rootDirectory}\{activeFolderName}"
        ## 2. Look into folder content with os.listdir(), ignores further nesting.
        activeFolderContent = [fld for fld in os.listdir(os.chdir(activeFolderPath)) if os.path.isfile(fld)]
        activeFolderContent_folders = [fld for fld in os.listdir(os.chdir(activeFolderPath)) if not os.path.isfile(fld)]
        ## 3. Rename each content file in activeFolder
        for index, content in enumerate(activeFolderContent):
            oldext = f"{content.rsplit('.', 1)[-1]}" ## Preserve original file extension
            oldname = f"{activeFolderPath}\{content}"
            newname = f"{activeFolderPath}\{activeFolderName}_{str(index).zfill(3)}.{oldext}"
            os.rename(oldname, newname)
            nestedContentCount += 1
        if len(activeFolderContent_folders) <= 0:
            output_filenames.append(f"{len(activeFolderContent)} files renamed. ")
        else:
            output_filenames.append(f"{len(activeFolderContent)} files renamed. {len(activeFolderContent_folders)} nested folders skipped.")
        
    if len(listOfFolders) > 0:
        ## Create 1-liner summary
        output_lbl = Label(Frame_02R, text = f"{len(listOfFolders)} folders & {nestedContentCount} nested files renamed.", relief = RIDGE, bg = "black", fg ="white")
        output_lbl.grid(row = 0, column = 0, sticky = W, padx = 5, pady = 1)
    
    ## Create Listbox of output files name.
    outputfile_listbox = Listbox(Frame_02R, width = 50)
    for index, name in enumerate(output_filenames):
        outputfile_listbox.insert(END, name.rsplit('/', 1)[-1])
    outputfile_listbox.grid(row = 1, column = 0, sticky = W, padx = 5, pady = 1)
    SwitchButtonState(2)
    
def ChangeName():
    global filenames, output_filenames, rootDirectory, listOfFolders
    global root, Frame_01, Frame_02, Frame_02R
    newname_entry = filename_entry.get()
    
    if len(filenames) > 0:
        ## Create 1-liner summary
        output_lbl = Label(Frame_02R, text = f"{len(filenames)} files renamed.", width = 20, relief = RIDGE, bg = "black", fg ="white")
        output_lbl.grid(row = 0, column = 0, sticky = W, padx = 5, pady = 1)
        
    ## Iterate through selected files paths, and rename them.
    ## String slice to find the exact position of the file name excluding directory path
    for index, name in enumerate(filenames):
        oldname = name.rsplit('/', 1)[-1].rsplit('.', 1)[0]
        oldname_pos = name.rfind(oldname)
        oldname_ext = name.rsplit('.', 1)[-1]
        if newname_entry != '':
            newname = name[0:oldname_pos] + f'{newname_entry}_{str(index).zfill(3)}' + f'.{oldname_ext}'
        else:
            newname = name[0:oldname_pos] + f'{str(index).zfill(3)}' + f'.{oldname_ext}'
        os.rename(name, newname)
        output_filenames.append(newname)
        
    ## Create Listbox of output files name.
    outputfile_listbox = Listbox(Frame_02R, width = 50)
    for index, name in enumerate(output_filenames):
            outputfile_listbox.insert(END, name.rsplit('/', 1)[-1])
    outputfile_listbox.grid(row = 1, column = 0, sticky = W, padx = 5, pady = 1)
    SwitchButtonState(1)
        
def ChangeExt():
    global filenames, output_filenames, rootDirectory, listOfFolders
    global root, Frame_01, Frame_02, Frame_02R
    newext_entry = ext_entry.get()
    
    if len(filenames) > 0:
        ## Create 1-liner summary
        output_lbl = Label(Frame_02R, text = f"{len(filenames)} extensions renamed.", width = 20, relief = RIDGE, bg = "black", fg ="white")
        output_lbl.grid(row = 0, column = 0, sticky = W, padx = 5, pady = 1)
    
    if newext_entry != '':
        for index, ext in enumerate(filenames):
            oldext = f".{ext.rsplit('.', 1)[-1]}"
            newext = ext.replace(oldext, f".{newext_entry}")
            os.rename(ext, newext)
            output_filenames.append(newext)
            
        ## Create Listbox of output files name.
        outputfile_listbox = Listbox(Frame_02R, width = 50)
        for index, name in enumerate(output_filenames):
                outputfile_listbox.insert(END, name.rsplit('/', 1)[-1])
        outputfile_listbox.grid(row = 1, column = 0, sticky = W, padx = 5, pady = 1)
        SwitchButtonState(1)
        
    else:
        messagebox.showerror("ERROR MESSAGE", "No input given in entry field.")
        
root = Tk()
root.title("File Renamer") # creating the window name
# root.geometry('{}x{}'.format(500, 200)) # creating the window size on startup, comment it for auto-resizing

# create all of the main containers
Frame_01 = Frame(root, width = 1, height = 30, bg = "CadetBlue1", pady = 3)
Frame_NestedRenamer = Frame(root, width = 1, height = 30, bg = "CadetBlue2", pady = 3)
Frame_02 = Frame(root, width = 1, height = 1, bg = "Black", pady = 3)
Frame_02L = Frame(Frame_02, width = 1, height = 1, bg = "CadetBlue3", pady = 3)
Frame_02R = Frame(Frame_02, width = 1, height = 1, bg = "CadetBlue4", pady = 3)
root.grid_rowconfigure(2, weight=1) # the stretch is given priority to row 2
root.grid_columnconfigure(0, weight=1) # the stretch is given priority to col 0

# layout all of the main containers
Frame_01.grid(row = 0, column = 0, columnspan = 5, sticky = NSEW)
Frame_NestedRenamer.grid(row = 1, column = 0, columnspan = 5, sticky = NSEW)
Frame_02.grid(row = 2, column = 0, columnspan = 5, sticky = NSEW)
Frame_02L.grid(row = 0, column = 0, sticky = NSEW)
Frame_02R.grid(row = 0, column = 1, sticky = NSEW)

# Creating and placing the widgets - Frame_01
selectfile_button = Button(Frame_01, text = "Select Files", height = 3, command = SelectFile)
selectfile_button.grid(row = 0, column = 0, rowspan = 2, sticky = W, padx = 5, pady = 10)
filename_entry = Entry(Frame_01, background = "white", width = 40)
filename_entry.grid(row = 0, column = 1, sticky = W, padx = 5, pady = 10)
changefilename_button = Button(Frame_01, text = "Change File Name", command = ChangeName, state = DISABLED)
changefilename_button.grid(row = 0, column = 2, sticky = W, padx = 5, pady = 10)
ext_entry = Entry(Frame_01, background = "white", width = 40)
ext_entry.grid(row = 1, column = 1, sticky = W, padx = 5, pady = 10)
changeext_button = Button(Frame_01, text = "Change Extension (Do not include .)", command = ChangeExt, state = DISABLED)
changeext_button.grid(row = 1, column = 2, sticky = W, padx = 5, pady = 10)

# Creating and placing the widgets - Frame_NestedRenamer
selectFolderButton = Button(Frame_NestedRenamer, text = "Select Directory", height = 3, command = SelectDirectory)
selectFolderButton.grid(row = 0, column = 0, rowspan = 2, sticky = W, padx = 5, pady = 10)
nestRenameButton = Button(Frame_NestedRenamer, text = "Make sure that all nested folders in rootDirectory has been \n renamed correctly before proceeding.", command = NestedRename, state = DISABLED)
nestRenameButton.grid(row = 0, column = 2, rowspan = 2, sticky = W, padx = 5, pady = 10)


root.mainloop()