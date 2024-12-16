from src.utils import Count 

def is_side_one_equal_three(type_code):
    Count.incC(21)
    if type_code >= 0:
        Count.incC(4)
        type_code = type_code + 2
        return type_code
