largest = None
smallest = None


while True:
    num = input("Enter a number: ")


    if num == "done":
        break

    else:
        try:
            num=int(num)

            if largest is None:
                largest = num

            if smallest is None:
                smallest =num

            if num > largest:
                    largest=num

            if num < smallest:
                    smallest=num

        except:
            print ("Invalid input")
            continue


print("Invalid input" )
print("Maximum is ", largest)
print("Minimum is ", smallest)
