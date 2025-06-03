def add(x,y):
    return (x+y)

def concatenate(x,y):
    return str(x) + str(y)

def operator(operation, x,y):
    return operation(x,y)

result_sum=operator(add,5,2)
result_con=operator(concatenate,"Hello", "YLLI")

print(result_sum)
print(result_con)
