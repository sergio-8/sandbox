import random

def trovalo(arr1, target):
    alpha = 0
    omega = len(arr1) - 1

    arr1.sort()

    while alpha < omega:
        if arr1[alpha] + arr1[omega] == target:
            print(f'Position {alpha} and position {omega}', f"which means: {arr1[alpha]} + {arr1[omega]}, results in {target}")
            print (arr1)
            alpha +=1 
            omega -=1
        elif arr1[alpha] + arr1[omega] < target:
            alpha += 1
        else:
            omega -= 1
    return None


# Generate 10 random positive integers between 1 and 20
random_arr = [random.randint(1, 10) for _ in range(10)]
print(f"Initial unsorted list: {random_arr}")

trovalo(random_arr, 15)
