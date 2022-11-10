lista=list(range(21,500))

indovinalo=input("dimmela: ")
indovinalo=int(indovinalo)
low=0
high=len(lista)-1
#indovinalo=int()



while low <= high:

    mid = (low + high) // 2
    guess = lista[mid]


    if guess==indovinalo:
        print ('bingo! the number is', guess, 'and is in position', lista.index(guess) )
        break

    if guess<indovinalo:
        low = mid + 1


    else:
        high = mid - 1





