mean_SP = []
max_interest = []

with open("SNP500.txt", "r") as file:
    lines = file.readlines()
    for line in lines[1:]:
        date = line.strip().split(',')[0]
        sp = line.split(',')[1]
        intr = line.strip().split(',')[-5]
        data = date.split("/")
        # print(data)
        mese = int(data[0])
        giorno = int(data[1])
        anno = int(data[2])

        if anno == 2016 and mese >= 6:

            mean_SP.append(float(sp))
            max_interest.append(float(intr))


        elif anno == 2017 and mese <= 5:
            mean_SP.append(float(sp))
            max_interest.append(float(intr))

mean_SP = sum(mean_SP) / len(mean_SP)
max_interest = max(max_interest)
print(mean_SP)
print(max_interest)
