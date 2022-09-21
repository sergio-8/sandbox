from collections import  deque



def trova_la_belva(nome):
    return nome[-3:]=='tto'
        #return



graph = {}

graph['io'] =['gino','mino', 'lino', 'pino', 'dino', 'rino', 'moccolo']


graph['gino']=['paolo','cristina','giacomo'  ]
graph['mino']=['paolazzo', 'desimone_maledetto', 'paolo','fracchia',]
graph['lino']=['capuzzo', 'ginastro', 'gianca']
graph['pino']=[]
graph['dino']=[]
graph['rino']=[]
graph['moccolo']=[]
graph ['cispia']= []
graph ['paolo']=[]
graph ['cristina']=[]
graph ['giacomo']=[]
graph ['capuzzo']=[]
graph ['ginastro']=[]
graph ['paolazzo']=[]
graph ['desimone_maledetto']=[]
graph ['fracchia']=[]
graph ['gianca']=[]
graph ['gianca']=[]
graph ['gianca']=[]
graph ['gianca']=[]
#print(graph['gino'])


def search(name):
    search_queue = deque()
    search_queue += graph[name]
    searched = []
    while search_queue:
        person = search_queue.popleft()
        if person not in searched:
            if trova_la_belva(person):
                    print( f'Mi ecco {person}, trovato!!')
                    return True
            else:
                search_queue += graph[person]
                searched.append(person)
    return False

search('io')




