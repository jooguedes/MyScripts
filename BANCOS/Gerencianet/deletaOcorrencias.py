import pandas as pd
import numpy as np






df1 = pd.read_csv('CSV1.csv')
df2 = pd.read_csv('CSV2.csv')

df1['login'] = np.where(df1['login'] == df2['Login'], 'True', 'False')
df1.index += 1 #resets the index to start from one.

df2_login = df2['Year'] #===> We create this column to store the DF2 year value.
df2_login = pd.Series(df2_login) #Series is a one-dimensional labeled array capable of holding data of any type.

df1 = df1.assign(df2_login=df2_login.values) #= This adds the DF2 year value to the DF1 data frame
print(df1.to_string(index=False))
