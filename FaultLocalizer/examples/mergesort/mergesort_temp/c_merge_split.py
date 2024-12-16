from src.utils import Count 

def merge(left, right):
    Count.incC(8)
    result = []
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        Count.incC(1)
        if left[i] <= right[j]:
            Count.incC(2)
            result.append(left[i])
            i += 1
        else:
            Count.incC(3)
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
