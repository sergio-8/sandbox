lista=list(range(0,500))

def search(lista, indovinalo):
    low=0
    high=len(lista)-1
    indovinalo=int()

    mid=(low+high)//2

    for low <= high:
        guess=lista[mid]

        if guess==indovinalo:
            print ('bingo! the number is', guess, 'and is in position', lista[mid] )
            break

        if guess<indovinalo:
            low=high+1

        else:
            low=high+1

