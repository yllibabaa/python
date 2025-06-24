from unittest.mock import inplace

import pandas as pd

df=pd.read_csv("../moduli14/avgIQpercountry.csv")
print(df.info()) # we see the columns of this dataset
print(df.head()) # we see the first 5 rows

country_data=df['Country']
print(country_data)

subset=df[["Country","Average IQ"]]
filtered_DF=subset[subset['Average IQ']>100]
print(subset)
print(filtered_DF)



#Null_mask finding null rows
null_mask=df.isnull()
null_count=null_mask.sum()
print(null_count)


#Removing duplicates
df.drop_duplicates(keep="first",inplace=True)
df["Population-2023"]=df["Population - 2023"].apply(lambda x: float(x.replace(",","")))
avg_iq_per_country=df.groupby('continent')['Avarage IQ'].mean()
print(avg_iq_per_country)

avg_iq_per_country=avg_iq_per_country.sort_values(ascending=False)
print(avg_iq_per_country)

#calculate nobel prizes by country and show countries only with more than 1 nobel
#you have to use Group By,sum and sort values
total_nobel_by_country=df.groupby('continent')['Nobel Prices'].sum()
sorted_total_nobel_by_country=total_nobel_by_country.sort_values(ascending=False)
sorted_total_nobel_by_country=sorted_total_nobel_by_country[sorted_total_nobel_by_country!=0]
print(sorted_total_nobel_by_country)

