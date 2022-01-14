import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="darkgrid")






class Analyser():
    def __init__(self,filename):
        self.fileName=filename
        self.df=self.readFile()
        self.df = self.df.sort_values(by=['Order Date'])
        self.df['day'] = self.df['Order Date'].dt.day
        self.df['year'] = self.df['Order Date'].dt.year
        self.df['month'] = self.df['Order Date'].dt.month
        self.df['month'] = self.df['Order Date'].dt.month_name(locale = 'en_GB.UTF-8')




    def read_csv(self,fileName):
        df = pd.read_csv(fileName, sep = ',')
        return df

    def read_excel(self,fileName):
        df=pd.read_excel(fileName)
        
        return df

    def readFile(self):
        ext=self.fileName.split('.')[1]
    
        if (ext=='csv'):
            return  self.read_csv(self.fileName)
        else:
            return self.read_excel(self.fileName)

    def getTotalProductByCategory(self):
        f, ax = plt.subplots(figsize=(11, 9))
        ax = sns.countplot(x="Category", data=self.df)
        return f

    def getTotalProductBySubCategory(self):
        f, ax = plt.subplots(figsize=(11, 9))
        sns.set(rc={'figure.figsize':(17.7,6)})
        ax = sns.countplot(x="Sub-Category", data=self.df)
        return f
    def getTotalSalesByCategory(self):
        f, ax = plt.subplots(figsize=(11, 9))
        sns.barplot(x=self.df.Category.unique(),
        y=self.df.groupby(['Category'])['Sales'].sum())
        return f

    
    def getDF(self):
        return self.df

