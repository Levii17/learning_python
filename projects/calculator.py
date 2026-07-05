import sys
import time

# Functions for basic arithmetic operations
def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "Error! Division by zero is a crime against mathematics."
    return x / y

def calculator():
    while True:
        print("\n=========================================")
        print("            PYTHON CALCULATOR           ")
        print("=========================================")
        print("1. Add (+)")
        print("2. Subtract (-)")
        print("3. Multiply (*)")
        print("4. Divide (/)")
        print("5. Exit")
        print("-----------------------------------------")
        
        choice = input("Select an operation (1-5): ").strip()
        
        if choice == '5':
            print("\nShutting down... Goodbye! 👋")
            sys.exit()
            
        if choice in ['1', '2', '3', '4']:
            # Using try-except blocks to catch formatting errors (like entering letters)
            try:
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))
            except ValueError:
                print("\nInvalid input! Please enter numbers only.")
                time.sleep(1.5)
                continue
            
            print("\nCalculating...")
            time.sleep(0.5)
            
            # Perform the chosen operation
            if choice == '1':
                print(f"Result: {num1} + {num2} = {add(num1, num2)}")
            elif choice == '2':
                print(f"Result: {num1} - {num2} = {subtract(num1, num2)}")
            elif choice == '3':
                print(f"Result: {num1} * {num2} = {multiply(num1, num2)}")
            elif choice == '4':
                print(f"Result: {num1} / {num2} = {divide(num1, num2)}")
        else:
            print("\nInvalid choice! Please select a number from 1 to 5.")
        
        # Pause briefly so the user can see the result before the menu redraws
        input("\nPress Enter to return to the menu...")

if __name__ == "__main__":
    calculator()