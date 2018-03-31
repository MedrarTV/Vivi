import tkinter as tk
import sys
from tkinter import filedialog
from tkinter import messagebox
import os
import csv


def choose_directory():
    global csvfile_button
    tempdir = filedialog.askdirectory(
        parent=root,
        title='Please select a directory')
    if len(tempdir) > 0:
        messagebox.showinfo("","You chose %s" % tempdir)
        csvfile_button['state']='normal'
        global rootdir
        rootdir= tempdir
    else:
        messagebox.showerror("Error!!!", "Please Select a Directory")


def choose_csvfile():
    global csv_filename
    global createstructure_button
    csv_filename = filedialog.askopenfilename(parent=root,
                                                title = "Select csv file",
                                                filetypes=(("csv files", "*.csv"),))
                                               ## filePatternList=['.txt'])
    if csv_filename == '':
        messagebox.showerror("Error!", "You must choose the csv file first!")
    else:
        messagebox.showinfo("The Chosen File", "You chose %s" % csv_filename)
        createstructure_button['state']='normal'

def create_dir():
    global rootdir
    if rootdir=='':
        messagebox.showerror("Error","Please Select a Directory First")
    else:
        messagebox.showinfo("", "You chose %s" % rootdir)
        read_csvfile()

def read_csvfile():
    global csv_filename
    global directories_lst
    ##### needs with clause #########
    try:
        csvFile = open(csv_filename,'rb')
        directories_lst = map(list,csv.reader(csvFile))
        csvFile.close()
        for row in directories_lst[1:]:
            print(row)
    except:
        read_csvfile()

## application vars
rootdir = ''
csv_filename = ''
directories_lst = []
root = tk.Tk()
csvfile_button = tk.Button()
createstructure_button = tk.Button()


def main(args):
    global root
    global csvfile_button
    global createstructure_button
    #root = tk.Tk()
    frame = tk.Frame(root)
    frame.pack()
    
    quit_button = tk.Button(frame,
                       text="QUIT",
                       fg="red",
                       command=sys.exit)
    quit_button.pack(side=tk.RIGHT)
    
    directory_button = tk.Button(frame,
                       text="1- Choose A Directory",
                       command=choose_directory)
    directory_button.pack(side=tk.LEFT)
    
    csvfile_button = tk.Button(frame,
                        text = "2- Choose The .csv File",
                        command=choose_csvfile,
                        state='disabled')
    csvfile_button.pack(side=tk.LEFT)
    
    createstructure_button = tk.Button(frame,
                        text="3-Create the Folder Structure",
                        command=create_dir,
                        state='disabled')
    createstructure_button.pack(side=tk.LEFT)
    
    
    root.mainloop()

if __name__ == "__main__":
    main('')
