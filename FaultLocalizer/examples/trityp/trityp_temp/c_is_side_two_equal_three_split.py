from src.utils import Count 

def is_side_two_equal_three(type_code):
    Count.incC(19)
    if type_code >= 0:
        Count.incC(2)
        type_code = type_code + 4 # bug, should be 3
        return type_code
