grade = int(input("Enter your grade: "))

print("You entered grade is", grade)

if grade > 0 and grade <= 100:
    if grade >= 90:
        print("Your grade is A")
    elif grade >= 80:
        print("Your grade is B")
    elif grade >= 70:
        print("Your grade is C")
    elif grade >= 60:
        print("Your grade is D")
    else:
        print("Your grade is F")
else:
    print("You have entered an invalid grade.")

areYou = input("Are you a student(Yes/No): ")

if areYou == "Yes":
    print("You are a student.")
else:
    areYou = input("Are you a developer(Yes/No): ")
    if areYou == "Yes":
        print("You are a developer.")
