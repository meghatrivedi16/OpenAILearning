def greeting():
    {
        print("Hello")
    }

greeting();

def greetUser(usr):
    {
        print("Hello", usr)
    }

greetUser("Megha");

def addNumbers(num1, num2):
    return num1 + num2

result = addNumbers(10, 20);
print("The sum is:", result);


add = lambda a, b: a + b
result = add(5, 3)
print(f"The sum of 5 and 3 with lambdais: {result}")