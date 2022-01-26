import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="darkgrid")
import numpy as np






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

    def getTotalQuantitySoldByCategory(self):
        f, ax = plt.subplots(figsize=(11, 9))
        sns.barplot(x=self.df.Category.unique(),
                 y=self.df.groupby(['Category'])['Quantity'].sum())
        return f

    def getTotalProfitByCategory(self):
        f, ax = plt.subplots(figsize=(11, 9))
        sns.barplot(x=self.df.Category.unique(),
                 y=self.df.groupby(['Category'])['Profit'].sum())
        return f
    
    def getDF(self):
        return self.df

    def getSummary(self):
        self.df.columns = [c.replace(' ', '_') for c in self.df.columns]
        self.df['year'] = pd.DatetimeIndex(self.df['Order_Date']).year

        all_df=[]
        for y in self.df['year'].unique():      
            temp=self.df[self.df['Order_Date'].dt.year == y]
            all_df.append(temp)
        all_df.append(self.df)    

        for i in range(len(all_df)):
            year=all_df[i]['year'].unique()
            sales = round(sum(all_df[i]['Sales']),0)
            profit = round(sum(all_df[i]['Profit']),0)
            tP=all_df[i]['Product_Name'].nunique()
            tc=all_df[i]['City'].nunique()
            d=all_df[i].groupby('Product_Name').sum()
            d=d[['Sales','Quantity','Profit']]
            d.reset_index(inplace=True)
            Poduct_max_sold=d.sort_values(by=['Quantity'],ascending=False).head(1)
            Poduct_max_sales=d.sort_values(by=['Sales'],ascending=False).head(1)
            Poduct_max_profit=d.sort_values(by=['Profit'],ascending=False).head(1)
            all_df[i]['diff_years'] = all_df[i]['Ship_Date'] - all_df[i]['Order_Date']
            all_df[i]['diff_years']=all_df[i]['diff_years']/np.timedelta64(1,'D')
            avg_stime=int(round(all_df[i]['diff_years'].mean(),0))
            all_df[i]['diff_years'] = all_df[i]['Ship_Date'] - all_df[i]['Order_Date']
            all_df[i]['diff_years']=all_df[i]['diff_years']/np.timedelta64(1,'D')
            avg_stime=int(round(all_df[i]['diff_years'].mean(),0))
            
            print(year)
            print(f'➤The total sales is €{sales} and total profit is €{profit}.')
            print(f'➤Total of {tP} products are sold over {tc} cities.')
            print(f'➤{Poduct_max_sold.iloc[0, 0]} is the most sold product.')
            print(f'➤{Poduct_max_profit.iloc[0, 0]} is the product with a max sales of €{round(Poduct_max_profit.iloc[0, 1],0)} & profit of €{round(Poduct_max_profit.iloc[0, 3],0)}.')
            print(f'➤Average shipping time for an order is {avg_stime} days.')
            
            result_text="{0} \nThe total sales is €{1}  and total profit is €{2}.\nTotal of {3} products are sold over {4} cities.\n{5} is the most sold product.\n{6} is the product with a max sales of €{7} & profit of €{8}.\nAverage shipping time for an order is {9} days.".format(year,sales,profit,tP,tc,Poduct_max_sold.iloc[0, 0],Poduct_max_profit.iloc[0, 0],round(Poduct_max_profit.iloc[0, 1],0),round(Poduct_max_profit.iloc[0, 3],0),avg_stime)
            return result_text