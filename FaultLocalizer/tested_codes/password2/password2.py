import re

def validate_password(p):
    valid = True
    print("FIRST")
    if len(p) < 6 or len(p) > 12:
        valid = False
    else:
        print("SECOND")
        if not re.search("[a-z]", p):
            valid = False
        else:
            if not re.search("[0-9]", p):
                valid = False
            else:
                if not re.search("[A-Z]", p):
                    valid = False
                else:
                    if re.search("[$#@]", p): #bug 
                        valid = False
                    else:
                        if re.search(r"\s", p):
                            valid = False
                        else:
                            print("Valid Password")
                            return  # Exit after a valid password is found

    if not valid:
        print("Not a Valid Password")


#import re

#def validate_password(p):
  #  x = True
 #   print("FIRST")
 #   if (len(p) < 6 or len(p) > 12):
  #      print("Not a Valid Password")
  #      x = False
  #  else:
   #     print("SECOND")
   #     if not re.search("[a-z]", p):
    #        print("Not a Valid Password")
    #        x = False
    #    else:
   #         if not re.search("[0-9]", p):
     #           print("Not a Valid Password")
     #           x = False
     #       else:
      #          if not re.search("[A-Z]", p):
        #            print("Not a Valid Password")
       #             x = False
      #          else:
       #             if re.search("[$#@]", p): #bug
        #                print("Not a Valid Password")
         #               x = False
         #           else:
          #              if re.search(r"\s", p):
          #                  print("Not a Valid Password")
           #                 x = False
           #             else:
           #                 print("Valid Password")
           #                 x = False


