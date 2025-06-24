import pandas as pd
import matplotlib.pyplot as plt

from moduli13.kaggleexample import avg_iq_per_country

#getting data from file
df=pd.read_csv('avgIQpercountry.csv')

avg_iq=df.groupby("Continent")["Avarage IQ"].mean()
plt.figure(figsize=(10,6))
avg_iq.plot(kind="line",marker="o",color="skyblue")
plt.title("Average IQ by Continent ")
plt.xlabel('Continent')
plt.ylabel("Average IQ")

plt.show()