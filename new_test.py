file=input("enter file name ")

if len(file) <1:
    file= "romeo.txt"

fh= open(file)

# count=0

for items in fh:
    items =items.rstrip()
    words=items.split()

print (len (words))
