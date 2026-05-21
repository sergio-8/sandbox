def trovalo(arr1, target):
  alpha=0
  omega=len(arr1)-1

  arr1.sort()

  while alpha<omega:
    if arr1[alpha]+arr1[omega]==target:
      return (alpha, omega, f"which means: {arr1[alpha]} + {arr1[omega]}")
    elif arr1[alpha]+arr1[omega]<target:
      alpha+=1
    else:
      omega-=1
  return None

print(trovalo([1,2,3,12,9,8,4,14,5],7))


    