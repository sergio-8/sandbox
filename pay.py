hrs = input("Please Enter the Hours you worked:")
hp=input ("Please enteru your hourly pay: ")

try:
    h = float(hrs)
    hourly_pay=float(hp)

    if h <= 40:
        total_pay= h * hourly_pay

    else:
        basic_pay= 40 * hourly_pay
        extra_pay= (h-40) * hourly_pay * 1.5
        total_pay=basic_pay + extra_pay

    print("your total pay is", total_pay)

except:
    print (" the values you enter must be a numbers: ex. 7 or 8 or 100, NOT letters, ex: five, ten etc\n",
    "please try again")
