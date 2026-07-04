def verify_card_number(card_number: str) -> str:
    cleaned_number = card_number.replace(" ", "").replace("-", "")
    
    if not cleaned_number.isdigit():
        return "INVALID!"
        
    total_sum = 0
    reversed_digits = cleaned_number[::-1]
    
    for index, char in enumerate(reversed_digits):
        digit = int(char)
        
        if index % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
                
        total_sum += digit

    if total_sum % 10 == 0:
        return "VALID!"
    else:
        return "INVALID!"


if __name__ == "__main__":
    tests = [
        "453914889",           
        "4111-1111-1111-1111", 
        "1234 5678 9012 3456", 
        "453914881"            
    ]
    
    for test in tests:
        result = verify_card_number(test)
        print(f"Card Number: {test:20} Message: {result}")