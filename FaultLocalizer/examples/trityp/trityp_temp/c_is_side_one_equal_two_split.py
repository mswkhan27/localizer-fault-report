from src.utils import Count 

def is_side_one_equal_two(type_code):
    Count.incC(20)
    if type_code >= 0:
        Count.incC(3)
        type_code = type_code + 1
        return type_code
