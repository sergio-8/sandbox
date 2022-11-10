score = input("Enter Score: ")

score=float(score)

if score<0 or score>1:
    print(" the score you enterd is invalid, it must be a numeric value between 0 and 1")

elif score >= 0.9:
    print ("A")

elif score >= 0.8:
    print ("B")

elif score >= 0.7:
    print ("C")

elif score >= 0.6:
    print ("D")

elif score < 0.5:
    print ("F")



else:
    print(" the score must be a numeric value between 0 and 1")
