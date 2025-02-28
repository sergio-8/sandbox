import random

def insertion_sort(data_list):
    """
    Sorts a list of numbers in ascending order using the insertion sort algorithm.

    Args:
        data_list: A list of numbers to be sorted.

    Returns:
        The sorted list.
    """
    # Iterate over the list, starting from the second element (index 1).
    for i in range(1, len(data_list)):
        # Store the current element in a variable called 'key'.
        key = data_list[i]
        # Initialize a variable 'j' to the index of the element before 'key'.
        j = i - 1

        # Move elements of data_list[0..i-1] that are greater than key
        # to one position ahead of their current position
        while j >= 0 and data_list[j] > key:
            data_list[j + 1] = data_list[j]
            j -= 1

        # Insert the 'key' into its correct position in the sorted portion of the list.
        data_list[j + 1] = key
    return data_list

if __name__ == "__main__":
    # Generate a list of 20 random integers between 0 and 100.
    random_list = [random.randint(0, 100) for _ in range(20)]
    print("Unsorted list:", random_list)

    # Sort the list using insertion sort.
    sorted_list = insertion_sort(random_list)
    print("Sorted list:", sorted_list)



