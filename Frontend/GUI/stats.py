import pandas as pd




def read_csv(fileName):
    df = pd.read_csv(fileName, sep = ',')
    return df

def read_excel(fileName):
    df=pd.read_excel(fileName)
    return df