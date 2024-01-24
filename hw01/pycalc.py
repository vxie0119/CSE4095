def add(x,y):
    return x + y

def subtract(x,y):
    return x - y

def multiply(x,y):
    return x*y

def divide(x,y):
    if y != 0:
        return x/y
    else:
        return "Cannot divide by zero!"
    
def calculator():
    print("Command-Line Calculator")

    while True:
        print("\nChoose an operation:")
        print("1. Addition (+)")
        print("2. Subtraction (-)")
        print("3. Multiplication (*)")
        print("4. Division (/)")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '5':
            print("Closing application. Goodbye!")
            break

        if choice in ('1', '2', '3', '4'):
            try:
                num1 = float(input("Enter operand 1: "))
                num2 = float(input("Enter operand 2: "))
            except ValueError:
                print("Input is invalid. Enter proper numeric values")
                continue

            if choice == '1':
                result = add(num1, num2)
                print(f"The answer of {(num1)} + {num2} is {result}")

            elif choice == '2':
                result = subtract(num1, num2)
                print(f"The answer of {num1} - {num2} is {result}")

            elif choice == '3':
                result = multiply(num1, num2)
                print(f"The answer of {num1} * {num2} is {result}")

            elif choice == '4':
                result = divide(num1, num2)
                print(f"The answer of {num1} / {num2} is {result}")
        else:
            print("Invalid option. Choose a number from 1 to 5.")

if __name__ == "__main__":
    calculator()