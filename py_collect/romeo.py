fname = input("Enter file name: ")
fh = open(fname)
lst = list()
for line in fh:


    newline=line.rstrip()
    newline=newline.split()
    #print (newline)
    for words in newline:

            if words in lst:
                continue

            else:
                lst.append(words)

lst.sort()

print(lst)
