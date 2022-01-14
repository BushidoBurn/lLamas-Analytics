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
#from importlib_metadata import files

from info import getAbout
from stats import Analyser

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class MainWindow():
    def __init__(self):
        self.analyserObj=None
        self.OptionList = ["Total Products by category","Total Products by Sub Category","Total Sales by Category","Total Quantity Sold by Category","Total Profit by Category"] 

        self.window=tk.Tk()
        self.variable = tk.StringVar(self.window)
        self.variable.set(self.OptionList[0])
        self.data=None
        self.window.title('lLamas-Analytics')
        self.window.geometry('800x800')
        self.plotFrame = tk.Frame(self.window,bg='white',width=800,height=400)
        self.plotFrame.pack()
        self.opt = tk.OptionMenu(self.window, self.variable, *self.OptionList)
        self.opt.config(width=90, font=('Helvetica', 12))
        self.opt.pack(side="top")
        self.plotFrame1 = tk.Frame(self.window,bg='white',width=500,height=500)
        self.plotFrame1.pack()
        self.menuBar=tk.Menu(self.window)
        self.fileMenu=tk.Menu(self.menuBar,tearoff=0)
        self.fileMenu.add_command(label="Open", command=self.readFile)
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
        self.variable.trace("w", self.dropdown_callback)
        self.window.mainloop()


    def dropdown_callback(self,*args):
        selection=self.variable.get()
        if(selection==self.OptionList[0]):
            self.showTotalProductByCategory()
        elif(selection==self.OptionList[1]):
            self.showTotalProductBySubCategory()
        elif(selection==self.OptionList[2]):
            self.showTotalSalesByCategory()
        else:
            pass
    

    def enable_Calculate(self):
        self.menuBar.entryconfig("Calculate", state="normal")

    def disable_Calculate(self):
        self.menuBar.entryconfig("Calculate", state="disabled")

    def enable_Options(self):
        self.opt.configure(state="normal")

    def disable_Options(self):
        self.opt.configure(state="disabled")


    def readFile(self):
        filename = fd.askopenfilename(filetypes=[("Data files", ".xlsx .xls .csv")])
        self.analyserObj=Analyser(filename)
        self.data=self.analyserObj.getDF()
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
        self.enable_Options()
        self.showTotalProductByCategory()

       

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
        pass

    def showTotalProductByCategory(self):
        fig=self.analyserObj.getTotalProductByCategory()
        self.generatePlotArea(fig)

    def showTotalProductBySubCategory(self):
        fig=self.analyserObj.getTotalProductBySubCategory()
        self.generatePlotArea(fig)

    def showTotalSalesByCategory(self):
        fig=self.analyserObj.getTotalSalesByCategory()
        self.generatePlotArea(fig)


    def generatePlotArea(self,fig):
        canvas = FigureCanvasTkAgg(fig, master=self.plotFrame1)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack()
        

    def save(self):
        files = [('All files', '*.*'),
                    ('Python Files', '*.py'),
                    ('Text Document', '*.txt')]
        file = fd.asksaveasfile(filetypes=files, defaultextension=files)

mw=MainWindow()

