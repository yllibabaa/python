import pandas as pd
import matplotlib.pyplot as plt

#getting data from file
df=pd.read_csv('avgIQpercountry.csv')

plt.figure(figsize=(10,6))
plt.scatter(df["Mean years of schooling - 2021"], df["Average IQ"],color="purple", alpha=0.7)
plt.title("Scatter plot of mean years of schooling vs IQ")

plt.xlabel("Mean Years of Schooling")
plt.ylabel("Average IQ")

plt.grid(True, linestyle="--",alpha=0.7)
plt.show()
plt.tight_layout()