count=0
senders=list()
count=dict()
file=input('enter a file: ')

if len(file) < 1:
    file = "mbox-short.txt"
fh= open(file)
#for items in fh:
#    count=count+1



for lines in fh:

    if lines.startswith("From "):
        lines=lines.split()
        senders.append(lines[1])

for items in senders:
    count[items]= count.get(items,0)+1
freq_key=None
high_value=None

for k,v in count.items():
    if freq_key is None or v>high_value:
        high_value=v
        freq_key=k



print (freq_key,high_value)
