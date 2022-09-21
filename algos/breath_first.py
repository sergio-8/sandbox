from collections import deque

def trova_la_belva(nome):
    return nome[-3:]=='hia'
        #return





graph = {}

graph['me'] =['gino','mino', 'lino', 'pino', 'dino', 'rino', 'moccolo']


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



def search(nome):
    search_queue=deque()
    search_queue += graph[nome]
    print(search_queue)
    already_searched=[]
    print(already_searched)
    while search_queue:
        print(search_queue)
        persona=search_queue.popleft()
        print(persona)
        if  persona not in already_searched:
            if  trova_la_belva(persona) :
                print (f"mi!!!!!  la belva umana e' {persona} ! ")
                return True
            else:
                search_queue += graph[persona]
                already_searched.append(persona)
    return False

search('me')
