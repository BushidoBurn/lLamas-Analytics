import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk

from info import getAbout
from stats import read_excel,read_csv


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
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Exit", command=self.window.quit)
        self.menuBar.add_cascade(label="File", menu=self.fileMenu)
        self.helpMenu = tk.Menu(self.menuBar, tearoff=0)
        self.helpMenu.add_command(label="About...", command=self.showAbout)
        self.menuBar.add_cascade(label="About", menu=self.helpMenu)
        self.window.config(menu=self.menuBar)
        self.window.mainloop()

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

       

    def showAbout(self):
        label = tk.Label(self.plotFrame, text=getAbout()).pack()

mw=MainWindow()

