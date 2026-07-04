while True:
    print("Menu: \n1.Item1\n2.Item2\n3.Item3\n4.Exit")
    choice = int(input("Enter your choice: "))
    if choice == 4:
        break
    elif choice == 1:
        print("You selected Item 1")
    elif choice == 2:
        print("You selected Item 2")
    elif choice == 3:
        print("You selected Item 3")
    elif choice < 1 or choice > 4:
        print("Invalid choice. Please try again.")