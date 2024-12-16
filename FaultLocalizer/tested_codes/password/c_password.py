import re

def validate_password(p):
    x = True
    while x:  
        if (len(p) < 6 or len(p) > 12):
            break
        else:
            if not re.search("[a-z]", p):
                break
            else:
                if not re.search("[0-9]", p):
                    break
                else:
                    if not re.search("[A-Z]", p):
                        break
                    else:
                        if not re.search("[$#@]", p):
                            break
                        else:
                            if re.search(r"\s", p):
                                break
                            else:
                                print("Valid Password")
                                x = False
                                break

    if x:
        print("Not a Valid Password")

# Receive input from the user
password = input("Enter your password: ")
validate_password(password)
