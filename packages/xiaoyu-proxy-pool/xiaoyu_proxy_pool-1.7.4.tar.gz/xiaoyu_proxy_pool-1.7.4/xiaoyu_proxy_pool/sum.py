def sums(value,value2,sum:str):
    if sum=='/':
        if value2==0:
            print('不能/0')
        else:
            return value/value2
    if sum=='+':
        return value+value2
    if sum=='-':
        return value-value2
    if sum=='*':
        return value*value2