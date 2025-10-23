def check_username(Username = input("Enter your username: ")):
    if Username == "admin":
        return True
    else:
        return False

if check_username():
    print("Access Granted")
else:
    print("Access Denied")

# Example of using functions in if statements