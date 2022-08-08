# To run this, download the BeautifulSoup zip file
# http://www.py4e.com/code3/bs4.zip
# and unzip it in the same directory as this file

from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = input('Enter - ')
html = urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, "html.parser")

tags = soup('a')
for item in tags[0:10]:
    item=item.get('href')
    print(item)

for n in range (7):
    url=tags[17]
    url=url.get('href')
    print('one more url: ', url )
    html = urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")
    tags=soup('a')


print(url)







'''




sum=0
count=0
# Retrieve all of the anchor tags


newtag2= tags[3]
url2 = newtag2.get('href', None)


html = urlopen(url2, context=ctx).read()
soup = BeautifulSoup(html, "html.parser")

tags=soup('a')
newtag3=tags[3]

url3=newtag3.get('href', None)

html = urlopen(url3, context=ctx).read()
soup = BeautifulSoup(html, "html.parser")

tags=soup('a')


for tag in tags:
    count= count+1
    while count<5:
        print (tag.get('href', None))
        break



newtag4=tags[3]

url4=newtag4.get('href', None)

print(url4)








:
    
    count=count +1


    while count< 10:


        #count=count+1
    #cont=int(tag.contents[0])
    #print ('content count=  ',  count)



    # Look at the parts of a tag
    #print('TAG:', tag)
        print('URL:', tag.get('href', None))
        #break

    #print('Contents:', tag.contents[0])
    #print('Attrs:', tag.attrs)


#print(count)
#print(sum)

'''