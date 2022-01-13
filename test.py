import pandas as pd

df = pd.read_csv( './train2.csv', header=None )
df[63] = df[63] + 9
print(df[63])
df.to_csv( './train3.csv', header=False, index=False )

