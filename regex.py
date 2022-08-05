import re

file1 = "all.txt"
file2 = "me.txt"
file3 = "mix.txt"
handle = open(file2)
num_list = list()
count = 0
for line in handle:
    line=line.rstrip()
    str_num = re.findall('([0-9]+)', line)
    if len(str_num) <= 0:
        continue
    # print(str_num)
    count = count + 1
    for i in range(len(str_num)):
        num = float(str_num[i])
        num_list.append(num)

print(count, len(num_list), sum(num_list))
