colors = ['black', 'white']
sizes = ['S', 'M', 'L']
maglione=[]

for maglia in (f'{c} {s}'for c in colors for s in sizes  ):
    #maglione.append(maglia)
    print(maglia)



print(maglione)