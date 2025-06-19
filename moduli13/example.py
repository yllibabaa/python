from array import array

import numpy as np

#cxreate a 2D Array
arr_2D=np.array([[1,2,3,4,5],[6,7,8,9,10]])
print(arr_2D)

element=arr_2D
print(element)

#dimensions
dimensions=arr_2D.ndim
print(dimensions)

#seperate this array
sub_array=arr_2D[:2,:2]#selects the first two rows and the first two colums
print(sub_array)

sub_array2=arr_2D[-4:,-4:]#selects the last for numbers of each row
print(sub_array2)

sum= np.sum(arr_2D)
print(sum)

mesatarja=np.mean(arr_2D)
print(mesatarja)