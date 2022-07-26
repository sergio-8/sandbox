
hrs = input("Please enter Enter Hours:")
r=input ("Please enter your hourly pay: ")
h=float(hrs)
r=float(r)


def computepay(h, r):

    if h<40:
        total_pay= h * r
        return total_pay
    if h>40 :
        pay= 40 * r
        extra_pay=(h-40)*1.5*r
        total_pay=pay+extra_pay
        return total_pay



p = computepay(h, r)
print("Pay", p)

#newreference
