

def quadrati(x, y):

    #print(x % y)




    if x > y:
        new_num=x % y
        if new_num==0:
            print("found it, the ideal size is {} by {}".format(y , y))
        else:
            y=new_num
            quadrati(x, y)

    else:
        new_num = y % x
        if new_num==0:
            print("found it, the ideal size is {} by {}".format(x , x))
        else:
            x = new_num
            quadrati(x, y)



print (quadrati (1996, 1152))