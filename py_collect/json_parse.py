import urllib.request, urllib.parse, urllib.error
import json

while True:
    address=input('Enter location: ')
    if len(address)<1:
        address='http://py4e-data.dr-chuck.net/comments_42.json'

    uh=urllib.request.urlopen(address)
    data=uh.read().decode()

    print('retirved ', len(data), 'characters')


    js=json.loads(data)

    print('retirved ', len(js), 'items')
    print('number of comments: ', len(js['comments']))

    total_count=0

    #for item in js:
    i = 0

    for x in range( (len(js['comments']))):
        instance_count=js['comments'][i] ['count']
        instance_count=int(instance_count)
        #print(instance_count)
        total_count=total_count+instance_count
        #print (total_count)
        i=i+1

    print(total_count)



