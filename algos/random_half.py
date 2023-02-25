import random
import datetime


def select_random_half_samples(data):

    half_size = len(data) // 2
    random_indices = random.sample(range(len(data)), half_size)
    return [data[i] for i in random_indices]

data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(select_random_half_samples(data))










