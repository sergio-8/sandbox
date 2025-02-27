import random

def nuova():
    lista = [random.randint(1, 100) for _ in range(10)]
    return lista

print(nuova())

rainfall_mi = "1.65, 1.46, 2.05, 3.03, 3.35, 3.46, 2.83, 3.23, 3.5, 2.52, 2.8, 1.85"

numeri = rainfall_mi.split(', ')
num_rainy_months = 0

for x in numeri:
    x = float(x)
    if x > 3:
        num_rainy_months += 1

print(num_rainy_months)


sentence = "students flock to the arb for a variety of outdoor activities such as jogging and picnicking"
sent_list=sentence.split(' ')
same_letter_count = 0
letter_starters = []
for x in sent_list:
    starter=x[0]
    ender=x[-1]
    if starter ==ender:
        same_letter_count+=1
print(letter_starters)
print(same_letter_count)


items = ["whirring", "wow!", "calendar", "wry", "glass", "", "llama","tumultuous","owing"]

acc_num=0
for x in items:
    if 'w' in x :
        acc_num += 1
print(acc_num)

sentence = "python is a high level general purpose programming language that can be applied to many different classes of problems."
num_a_or_e = 0
for word in sentence.split():
    if 'a' in word or 'e' in word:
        num_a_or_e += 1
print('num_a_or_e =', num_a_or_e)


s = "singing in the rain and playing in the rain are two entirely different situations but both can be fun"
vowels = ['a','e','i','o','u']

num_vowels = 0
par=s.split(' ')

for x in par:
    for char in x:
        if  char in vowels:
            num_vowels += 1


print('num_vowels=', num_vowels)

w = "Friendship is a wonderful human experience!"
c=w.split(' ')
wrd=[]
if "Friendly" in c:
    wrd.append("Friendly is in here")
elif "Friend" in c :
        wrd.append("Friendly is in here")
else:
    wrd.append('No variation of friend is in here.')

print(wrd)


