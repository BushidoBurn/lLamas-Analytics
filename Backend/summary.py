import pandas as pd
import folium
import os
import numpy as np
import warnings
warnings.filterwarnings("ignore")

os.chdir('D:\\projects')

df=pd.read_excel("sample.xlsx")
df.columns = [c.replace(' ', '_') for c in df.columns]
df['year'] = pd.DatetimeIndex(df['Order_Date']).year

all_df=[]
for y in df['year'].unique():      
    temp=df[df['Order_Date'].dt.year == y]
    all_df.append(temp)
all_df.append(df)    

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
    
