from src.utils import Count 

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
