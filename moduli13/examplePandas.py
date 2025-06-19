import pandas as pd

produktet=["apples","bananas","oranges","grapes","pineapples"]
sales=[150,200,180,98,60]

sales_perProducts=pd.Series(sales,index=produktet)
print(sales_perProducts)

#shitja e rrushit
print(sales_perProducts["Grapes"])

best_selling_products=sales_perProducts.idmax()
print(best_selling_products)
