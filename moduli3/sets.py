my_set={1,2,3,2,4,2,4,5,8,7}
print(my_set)

my_set_1=([1,2,2,3,4,5])
print(my_set_1)

A={1,2,3}
B={3,4,5}

#find the union
unioni=A.union(B)
print(unioni)

#intersection
prerja=A.intersection(B)
print(prerja)

#diferenca
diferenca=A.difference(B)
print(diferenca)

#diferenca simetrike
d_simetrike=A.symmetric_difference(B)
print(d_simetrike)


#add.element
A.add(6)
print(A)

#remove element
A.remove(6)

#discard-remove the element without error
A.discard(100)

#removes all elements
A.clear()

#find the length number of elements
print(len(A))


A=(1,2,3,4,5)
numri=1
#operatori i dhe not in
print(numri in A)
print(numri not in A)




#list of duplicate
list=[1,2,3,4,5]
c=set(list)

#two sets
set1={"YLLI","erin","drini"}
set2=("YLLI","TEZJA MERIBAN","KOJSHA")
prerja1=set1.intersection(set2)
print(prerja1)



