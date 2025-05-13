from traceback import print_tb

names=["alma","blerta","dhurata","shpati"]
for name in names:
    print(name)
#shembulli 2
    sentence_shembulli="hello,world"
    for char in sentence_shembulli:
        if char.isalpha():#kthen true or false if char is a letter
            print(char)

#shembulli 3 ne range functtion
for numri in range(1,6):
    print(numri)

#menyra ma primitive me gjet maksimumin
numrat=[33,45,55,23,12,94,100,101]
max=numrat[0]
for num in numrat:
    if num>max:
        max=num
    print("the max value of the list is",max)

