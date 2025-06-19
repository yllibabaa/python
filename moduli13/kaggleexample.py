import pandas as pd
df=pd.read_csv("avgIQpercountry.csv")
print(df.info())
print(df.head())

country_data=df["Country"]
print(country_data)

subset=df[["country","avarage IQ"]]
filtered_DF=subset[subset["avarage IQ"]>100]
print(filtered_DF)

#null_mask finding null rows
null_mask=df.isnull()
null_count=null_mask.sum()
print(null_count)