# Use words.txt as the file name





fname = input("Enter file name: ")
fh = open(fname)
count=0
conf_tot=0

for line in fh:
    if not line.startswith("X-DSPAM-Confidence:"):
        continue
    count = count + 1
    line= line.rstrip()
    line= float(line [-6:])
    conf_tot= conf_tot+ line



print("Average spam Confidence: ", conf_tot/count)
