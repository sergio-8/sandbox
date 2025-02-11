import lupino
from pprint import pprint
#pprint(lupino.__dict__)
print("nome:", lupino.name,"\nalto qunato?",lupino.alto, "\nno, altezza vera:",lupino.altezza)

print( f'mi\'ridagli...\nnome:{lupino.name}', f'\nma alto quanto??:{lupino.alto}','\nahhhh mi\' ecco bagonghi....' )
print(f'mi\' un pezzo d\'omo... a {lupino.altezza}cm')
lupino.alto='una mezza sega...'
print(f'praticamente, diciamo la verita\': {lupino.alto} ')




