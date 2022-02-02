from time import time
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
from tkinter import messagebox
from urllib import response
#from importlib_metadata import files

from info import getAbout
from stats import Analyser
from PIL import Image, ImageTk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import sys
# insert at 1, 0 is the script path (or '' in REPL)
#sys.path.insert(1, '/path/to/application/app/folder')
#sys.path.append('../')
#import Backend.summary as summary

class MainWindow():
    def __init__(self):
        self.summary_label=None
        self.is_summary_written=None
        self.selectedOptionCategory=None
        self.allGraphOptions={"Sales Performance Analyzes":["Total Products by category","Total Products by Sub Category","Total Sales by Category","Total Quantity Sold by Category","Total Profit by Category"],"Sales Trend Analyses":["Opt1","Opt2","Opt3"]}
        self.analyserObj=None
        #self.OptionList =  self.allGraphOptions["sales_performance_analyse"]
        self.OptionList = None
        self.variable =None
        self.canvas=None
        self.window=tk.Tk()
        #self.variable = tk.StringVar(self.window)
        #self.variable.set(self.OptionList[0])
        self.data=None
        self.window.title('lLamas-Analytics')
        self.window.geometry('800x800')
        self.plotFrame = tk.Frame(self.window,bg='white',width=800,height=400)
        self.plotFrame.pack()
        self.opt = None


        self.img=Image.open("LLAMAS.png")
        self.img=self.img.resize((400, 400), Image.ANTIALIAS)
        self.img_holder = ImageTk.PhotoImage(self.img)
        self.img_label = tk.Label(self.window,image=self.img_holder)
        self.img_label.image = self.img_holder
        self.img_label.pack()

        #self.opt = tk.OptionMenu(self.window, self.variable, *self.OptionList)
        #self.opt.config(width=90, font=('Helvetica', 12))
        #self.opt.pack(side="top")
        self.plotFrame1 = None#tk.Frame(self.window,bg='white',width=500,height=500)
        #self.plotFrame1.pack()
        self.menuBar=tk.Menu(self.window)
        self.fileMenu=tk.Menu(self.menuBar,tearoff=0)
        self.fileMenu.add_command(label="Open", command=self.readFile)
        self.fileMenu.add_command(label="Save as", command=self.save)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Exit", command=self.window.quit)
        self.menuBar.add_cascade(label="File", menu=self.fileMenu)
        self.helpMenu = tk.Menu(self.menuBar, tearoff=0)

        self.pb = ttk.Progressbar(self.plotFrame1,
        orient='horizontal',
        mode='indeterminate',
        length=280)
        

        #Adding Edit button to the menu bar, which will have copy, cut and paste
        self.Menuba=tk.Menu(self.menuBar, tearoff=0)
        self.Menuba.add_command(label="Copy", command=self.copy)
        self.Menuba.add_command(label="Cut", command=self.cut)
        self.Menuba.add_command(label="Paste", command=self.paste)
        self.Menuba.add_separator()
        self.menuBar.add_cascade(label="Edit", menu=self.Menuba)


        # Adding Analyse MenuItem
        self.analyseMenu=tk.Menu(self.menuBar, tearoff=0)
        #self.analyseMenu.add_command(label="Sales Trend Analyzes", command= lambda:self.generateOptions("Sales Trend Analyzes"))
        self.analyseMenu.add_command(label="Sales Performance Analyzes", command= lambda:self.generateOptions("Sales Performance Analyzes"))
        #self.analyseMenu.add_command(label="Customer Analyzes", command= lambda:self.generateOptions("Customer Analyzes"))
        ######self.analyseMenu.add_command(label="Summary", command= lambda:self.generateOptions("Summary"))
        self.analyseMenu.add_command(label="Summary", command=self.generateSummary)
        self.menuBar.add_cascade(label="Analyze", menu=self.analyseMenu)

        # self.opt = tk.OptionMenu(self.window, self.variable, *self.OptionList)
        # self.opt.config(width=90, font=('Helvetica', 12))
        # self.opt.pack()
        ######self.disable_Options()

        self.helpMenu.add_command(label="About...", command=self.showAbout)
        self.menuBar.add_cascade(label="About", menu=self.helpMenu)
        self.calculateMenu = tk.Menu(self.menuBar, tearoff=0)
        self.calculateMenu.add_command(label="Calculate Percentage", command=self.calculatePercentage)
        self.menuBar.add_cascade(label="Calculate", menu=self.calculateMenu)
        self.window.config(menu=self.menuBar)
        self.disable_Calculate()
        #self.variable.trace("w", self.dropdown_callback)
        self.window.mainloop()


    def dropdown_callback(self,*args):
        if(self.selectedOptionCategory=="Sales Performance Analyzes"):
            selection=self.variable.get()
            if(selection==self.OptionList[0]):
                self.showTotalProductByCategory()
            elif(selection==self.OptionList[1]):
                self.showTotalProductBySubCategory()
            elif(selection==self.OptionList[2]):
                self.showTotalSalesByCategory()
            elif(selection==self.OptionList[3]):
                self.showTotalQuantitySoldByCategory()
            elif(selection==self.OptionList[4]):
                self.showTotalProfitByCategory()
            else:
                pass
        # elif(self.selectedOptionCategory=="Sales Trend Analyzes"):
        #     selection=self.variable.get()
        #     if(selection==self.OptionList[0]):
        #         pass
        #     else:
        #         pass      

    def generateOptions(self,selected):
        if self.opt:
            self.opt.destroy()
            self._clear()
        if self.is_summary_written:
            self.is_summary_written=False
            for widgets in self.plotFrame1.winfo_children():
                print(widgets.winfo_class())
                if widgets.winfo_class()=="Label":
                    widgets.destroy()
                    
                    #self.plotFrame1.destroy()
                    #self.plotFrame1=None
                    #self.plotFrame1 = tk.Frame(self.window,bg='gray',width=500,height=500)
                    #self.plotFrame1.pack()
        #time.sleep(1000)
        self.selectedOptionCategory=selected
        self.OptionList =  self.allGraphOptions[self.selectedOptionCategory]
        self.variable = tk.StringVar(self.window)
        self.variable.set(self.OptionList[0])
        self.opt = tk.OptionMenu(self.window, self.variable, *self.OptionList)
        self.opt.config(width=90, font=('Helvetica', 12))
        self.opt.pack(side="top")
        self.variable.trace("w", self.dropdown_callback)
        #if not self.plotFrame1:
        #    self.plotFrame1 = tk.Frame(self.window,bg='gray',width=500,height=500)
        #    self.plotFrame1.pack()


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
        #self.pb.pack(pady=10)
        #self.bar()
        if self.analyserObj:
            self.plotFrame.destroy()
            self._clear()
            if self.opt:
                self.opt.destroy()
            self._clear()
            self.plotFrame = tk.Frame(self.window,bg='white',width=500,height=500)
            self.plotFrame.pack()
        self.analyserObj=Analyser(filename)
       


        self.data=self.analyserObj.getDF()
        self.showDF()
        self.pb.destroy()
        if self.img_label:
            self.img_label.destroy()


    # def read_csv(self):
    #     filename = fd.askopenfilename(filetypes=[("Data files", ".xlsx .xls .csv")])
    #     df=read_csv(filename)
    #     self.data=df
    #     self.showDF()

    # def read_excel(self):
    #     filename = fd.askopenfilename(filetypes=[("Data files", ".xlsx .xls .csv")])
    #     df=read_excel(filename)
    #     self.data=df
    #     self.showDF()

    
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
        #########self.enable_Options()
        #self.showTotalProductByCategory()
       
    def quit(self):
        self.window.response = messagebox.askyesno('Exit', 'Are you sure you want to exit')
        if response:
            self.window.destroy()

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
        self._clear()
        fig=self.analyserObj.getTotalProductByCategory()
        self.generatePlotArea(fig)

    def showTotalProductBySubCategory(self):
        self._clear()
        fig=self.analyserObj.getTotalProductBySubCategory()
        self.generatePlotArea(fig)

    def showTotalSalesByCategory(self):
        self._clear()
        fig=self.analyserObj.getTotalSalesByCategory()
        self.generatePlotArea(fig)

    def showTotalQuantitySoldByCategory(self):
        self._clear()
        fig=self.analyserObj.getTotalQuantitySoldByCategory()
        self.generatePlotArea(fig)       

    def showTotalProfitByCategory(self):
        self._clear()
        fig=self.analyserObj.getTotalProfitByCategory()
        self.generatePlotArea(fig)   


    def generatePlotArea(self,fig):
        self.plotFrame1 = tk.Frame(self.window,bg='white',width=500,height=500)
        self.plotFrame1.pack()
        self.canvas = FigureCanvasTkAgg(fig, master=self.plotFrame1)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()



    def _clear(self):
        if self.canvas:
            self.plotFrame1.destroy()
            #self.canvas.get_tk_widget().destroy()
            #for widgets in self.plotFrame1.winfo_children():
            #    widgets.destroy()
         
    def generateSummary(self):
        if self.opt:
            self.opt.destroy()
            self._clear()
        self.plotFrame1 = tk.Frame(self.window,bg='white',width=500,height=500)
        self.plotFrame1.pack()
        summary=self.analyserObj.getSummary()
        self.is_summary_written=True
        self.summary_label = tk.Label(self.plotFrame1, text=summary,anchor="e", justify=LEFT,font=("Arial Black",8)).pack()

    def save(self):
        files = [('All files', '*.*'),
                    ('Python Files', '*.py'),
                    ('Text Document', '*.txt')]
        file = fd.asksaveasfile(filetypes=files, defaultextension=files)


    def bar(self):
        import time
        self.pb['value'] = 20
        self.window.update_idletasks()
        time.sleep(0.5)
    
        self.pb['value'] = 40
        self.window.update_idletasks()
        time.sleep(0.5)
    
        self.pb['value'] = 50
        self.window.update_idletasks()
        time.sleep(0.5)
    
        self.pb['value'] = 60
        self.window.update_idletasks()
        time.sleep(0.5)
    
        self.pb['value'] = 80
        self.window.update_idletasks()
        time.sleep(0.5)
    
        self.pb['value'] = 100
        self.window.update_idletasks()
        time.sleep(0.5)
    
        self.pb['value'] = 80
        self.window.update_idletasks()
        time.sleep(0.5)
    
        self.pb['value'] = 60
        self.window.update_idletasks()
        time.sleep(0.5)
    
        self.pb['value'] = 50
        self.window.update_idletasks()
        time.sleep(0.5)
    
        self.pb['value'] = 40
        self.window.update_idletasks()
        time.sleep(0.5)
    
        self.pb['value'] = 20
        self.window.update_idletasks()
        time.sleep(0.5)
        self.pb['value'] = 0

mw=MainWindow()

