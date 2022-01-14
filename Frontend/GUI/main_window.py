from tkinter import*
from argparse import FileType
from cProfile import label
from distutils import command
#from msilib.schema import SelfReg
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter import simpledialog
from tkinter import font
from turtle import bgcolor
from importlib_metadata import files

from info import getAbout
from stats import read_excel,read_csv
import matplotlib.pyplot as plt

class MainWindow():
    def __init__(self):
        self.window=tk.Tk()
        self.data=None
        self.window.title('lLamas-Analytics')
        self.window.geometry('800x800')
        self.plotFrame = tk.Frame(self.window,bg='white',width=800,height=400)
        self.plotFrame.pack()
        self.menuBar=tk.Menu(self.window)
        self.fileMenu=tk.Menu(self.menuBar,tearoff=0)
        self.fileMenu.add_command(label="Open", command=self.read_excel)
        self.fileMenu.add_command(label="Save as", command=self.save)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Exit", command=self.window.quit)
        self.menuBar.add_cascade(label="File", menu=self.fileMenu)
        self.helpMenu = tk.Menu(self.menuBar, tearoff=0)

        #Adding Edit button to the menu bar, which will have copy, cut and paste
        self.Menuba=tk.Menu(self.menuBar, tearoff=0)
        self.Menuba.add_command(label="Copy", command=self.copy)
        self.Menuba.add_command(label="Cut", command=self.cut)
        self.Menuba.add_command(label="Paste", command=self.paste)
        self.Menuba.add_separator()
        self.menuBar.add_cascade(label="Edit", menu=self.Menuba)

        self.helpMenu.add_command(label="About...", command=self.showAbout)
        self.menuBar.add_cascade(label="About", menu=self.helpMenu)
        self.calculateMenu = tk.Menu(self.menuBar, tearoff=0)
        self.calculateMenu.add_command(label="Calculate Percentage", command=self.calculatePercentage)
        self.menuBar.add_cascade(label="Calculate", menu=self.calculateMenu)
        self.window.config(menu=self.menuBar)
        self.disable_Calculate()
        self.window.mainloop()


    def enable_Calculate(self):
        self.menuBar.entryconfig("Calculate", state="normal")

    def disable_Calculate(self):
        self.menuBar.entryconfig("Calculate", state="disabled")

    def read_csv(self):
        filename = fd.askopenfilename(filetypes=[("Data files", ".xlsx .xls .csv")])
        df=read_csv(filename)
        self.data=df
        self.showDF()

    def read_excel(self):
        filename = fd.askopenfilename(filetypes=[("Data files", ".xlsx .xls .csv")])
        df=read_excel(filename)
        self.data=df
        self.showDF()
    
    def showDF(self):
        cols = list(self.data.columns)

        tree = ttk.Treeview(self.plotFrame)
        tree.pack()
        tree["columns"] = cols
        for i in cols:
            tree.column(i, anchor="w")
            tree.heading(i, text=i, anchor='w')

        for index, row in self.data.iterrows():
            tree.insert("",0,text=index,values=list(row))
        self.enable_Calculate()

       

    def showAbout(self):
        label = tk.Label(self.plotFrame, text=getAbout()).pack()
        
    def copy(self, event=None):
        self.clipboard_clear()
        text = self.get("sel.first", "sel.last")
        self.clipboard_append(text)

    def cut(self, event):
        self.copy()
        self.delete("sel.first", "sel.last")
        
    def paste(self, event):
        text = self.selection_get(selection='CLIPBOARD')
        self.insert('insert', text)

    def calculatePercentage(self):
        USER_INP1 = simpledialog.askstring(title="Calculate Percentage",
                                  prompt="Enter Name Of Column To Calculate")
        self.data['sums'] = self.data.groupby(USER_INP1)['Sales'].transform('sum')
        self.data['proportion'] = self.data['Sales'] / self.data['sums']
        labels = self.data[USER_INP1]
        
        #explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

        fig1, ax1 = plt.subplots()
        ax1.pie(self.data['proportion'], labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        plt.show()
    def save(self):
        files = [('All files', '*.*'),
                    ('Python Files', '*.py'),
                    ('Text Document', '*.txt')]
        file = fd.asksaveasfile(filetypes=files, defaultextension=files)

mw=MainWindow()

