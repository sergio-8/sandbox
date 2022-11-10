
while True:
    inputto=input(">> ")

    print('Not Done!')

    if inputto != "moccolo":

        print('Mi!! \nCeppo tho detto: Not Done!')
        line = input('> ')
        if line[0] == '#':
            print (" e'.. la peppa")
            continue
        if line == 'done':
            break
        print(line)

    else:
        break


print('Done!')
