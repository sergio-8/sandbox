name = input("Enter file:")
if len(name) < 1:
    name = "2.txt"
handle = open(name)
lst=list()
count=dict()
for line in handle:
    line =line.rstrip()
    if line.startswith("From "):
        line=line.split()
        #print (line)
        hour=line[5]
        hours=hour[:2]
        #print(hours)
        count[hours]=count.get(hours, 0) +1



for  val,key  in count.items():
    newtup=(val, key)
    lst.append(newtup)


lst.sort()



for val, key in lst:
    print ( val, key)
