for i in range(8):
    print(f"session {i+1} Python Programming")

print("=====================================")

for i in range(1, 9):
    print(f"session {i} Python Programming")

print("=====================================")

for i in range(1, 9, 2):
    print(f"session {i} Python Programming")

    list = ["Apple","Banana","Cherry","Date"]

print("=====================================")

for i in list:
    print(f"session {i} Python Programming")

print("==============WHILE LOOP=======================")

j = 0
while j <= 10:
    print(j)
    j += 1

print("Out of while loop j = ", j   )


for i in range(2, num):
    if num % i == 0:
        print(num, "is not a prime number")
        break

else:
    print(num, "is a prime number") 

for i in range(2, 11):
    print(i,end=" , " )
else: 
    print("\nLoop is completed")


print("======================= MONICA CODE =======================")
for i in range(1, 11): # 1,2,3,4,5,6,7,8,9,10
    # 1, 2, 3, 6, 7, (8 is the breaking point)
    # skip 4, 5
    if(i==4 or i==5):
        print("Continue to next iteration")
        continue
    if(i==8):
        print("Breaking the loop")
        break
    print(f"Processing number: {i}")

for i in range(1,11):
    # nothing to do right now, will be coded later
    pass

for i in range(1,11):
    print(i, end=", ")
else:
    print("Loop success")
print("next stmt")


li=["Python","C","C++","Java","C#"]
req=input("Enter your required skill set:")
for i in li:
    if i==req:
        print("The skill is matched")
        print("You are hired as you have the skill")
        break
else:
    print("You are  not hired as you do not have the skill")