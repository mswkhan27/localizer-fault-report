import re

def validate_password(p):
    x = True
    #print("Now validating password", p)
    #print("Now validating password", len(p))
    while x:  
        if (len(p) < 6 or len(p) > 12):
            print("length fail")
            break
        else:
            #print("Length in valid range")
            if not re.search("[a-z]", p):
                print("lower letter fail")
                break
            else:
                if not re.search("[0-9]", p):
                    print("numbers fail")
                    break
                else:
                    if not re.search("[A-Z]", p):
                        print("upper letter fail")
                        break
                    else:
                        #print("Checking if the password has special characters",p)
                        if re.search("[$#@]", p):
                            print("special character fail")
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

password = input("Enter your password: ")
validate_password(password)
