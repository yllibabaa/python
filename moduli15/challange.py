import pandas as pd
my_dataset=pd.read_cvs("weather_tokyo_data.cvs",)
print(my_dataset)
temp_dataset=my_dataset.groupby('year')['temperature'].mean()
print(temp_dataset)

