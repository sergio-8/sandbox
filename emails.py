fname = input("Enter file name: ")
if len(fname) < 1:
    fname = "2.txt"

fh = open(fname)
count = 0

for line in fh:
    if line.startswith("From "):

            count=count +1
            line=line.split()
            line=line[1]
            print (line)
    else:
        continue




print("There were", count, "lines in the file with From as the first word")
