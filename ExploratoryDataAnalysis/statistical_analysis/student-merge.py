import pandas as pd

df1 = pd.read_csv('/Users/romanregmi/desktop/statistical_analysis/student-mat.csv',sep=';')
df2 = pd.read_csv('/Users/romanregmi/desktop/statistical_analysis/student-por.csv',sep=';')


df3 = pd.merge(df1,df2,on=["school","sex","age","address","famsize","Pstatus","Medu","Fedu",
                            "Mjob","Fjob","reason","nursery","internet","guardian"],suffixes=['_math','_portuguese'])