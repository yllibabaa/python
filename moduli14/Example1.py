import pandas as pd
import matplotlib.pyplot as plt

#getting data from file
df=pd.read_csv('avgIQpercountry.csv')

#filtering the data based on average iq
filtered_df=df[df["Average IQ"]>=100]

#sorting data
filtered_df=filtered_df.sort_values(by='Average IQ', ascending=False)
print(filtered_df)

#creation of the figure of data
plt.figure(figsize=(14,8))
# graphs ofx,y axis
bars=plt.bar(filtered_df["Country"],filtered_df["Average IQ"], color="skyblue")

plt.title("Average IQ per Country (IQ>=100)", fontsize=16)
plt.xlabel('County',fontsize=14)
plt.ylabel("Average IQ",fontsize=14)

plt.bar_label(bars,fmt="%.2f",fontsize=10, color="black")

plt.tight_layout()