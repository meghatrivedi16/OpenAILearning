t=(1,2,3)
# t.append(4)
# t[0]=10

# x = 100/0
try:
    x=int(input("Enter a number:"))
    y=int(input("Enter the denominator:"))
    res=x/y
    print(res)
except ZeroDivisionError:
    print("Denominator can not be 0")
# except ValueError:
#     print("Enter only int values")
# except Exception as e:
#     print("Generic exception")
else:
    print("Things went smooth with try")
finally:
    print("Finally the code, runs come whatever")


print("Program continues..")