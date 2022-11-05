
colors = ['black', 'white']
sizes = ['S', 'M', 'L']
tshirts = [(color, size) for size in sizes for color in colors ]
print(tshirts)

unshirt = [(size, color) for color in colors for size in sizes]
print(unshirt)