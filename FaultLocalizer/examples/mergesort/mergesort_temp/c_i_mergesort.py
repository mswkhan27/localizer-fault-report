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

def mergesort(arr):
    Count.incC(9)
    if len(arr) <= 1:
        Count.incC(4)
        return arr
    else:
        Count.incC(5)
        if len(arr) % 2 == 0:
            Count.incC(6)
            middle = len(arr) // 2
            left = mergesort(arr[:middle])
            right = mergesort(arr[middle:])
            return merge(left, right)
        else:
            Count.incC(7)
            middle = len(arr) //2
            left = mergesort(arr[:middle])
            right = mergesort(arr[middle:])
            left.reverse() #mistake
            return merge(left, right)
