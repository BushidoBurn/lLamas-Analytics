import tkinter as tk
from tkinter import filedialog as fd



class MainWindow():
    def __init__(self):
        self.window=tk.Tk()
        self.window.title('lLamas-Analytics')
        self.window.geometry('800x800')
        self.menuBar=tk.Menu(self.window)
        self.fileMenu=tk.Menu(self.menuBar,tearoff=0)
        self.fileMenu.add_command(label="Open", command=self.read_csv)
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
        print(filename)

    def showAbout():
        pass

mw=MainWindow()

