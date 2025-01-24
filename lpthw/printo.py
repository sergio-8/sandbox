from sys import argv
from os import path
from_file='/content/sample_data/testo_1.txt' #/content/sample_data/testo_2.txt
to_file='/content/sample_data/testo_2.txt'

print(f'copying from: \n{from_file} \nto: \n{to_file}')

in_file=open(from_file)
indata=in_file.read()

print(f'the input file is {len(indata)} bytes long')


to_file=open(to_file,'w')
to_file.write(indata)


print('all done')
to_file.close()
in_file.close()



with open('/content/sample_data/testo_2.txt') as file:
  for word in file:
    print(word)

filesto = open('/content/sample_data/testo_2.txt', 'r')
contenuto = filesto.read()

print(contenuto)


from sys import argv
from os import path

from_f=input("form: \n>", )
to_f = input("to: \n>", )
from_file=f'/content/sample_data/{from_f}'
to_file=f'/content/sample_data/{to_f}'

print(f'copying from: \n{from_file} \nto: \n{to_file}')

def ripeto(da,a ):
  with open(da) as infile:
    indata=infile.read()
  with open(a,'w') as outfile:
    outfile.write(indata)

  #return infile,outfile

  cont=open(to_file)
  contenuto=cont.read()
  print(contenuto)
  print('well then, \n....all done')

ripeto(from_file,to_file)