c[9] += 1
if len(arr) <= 1:
    c[4] += 1
    return arr
else:
    c[5] += 1
    if len(arr) % 2 == 0:
        c[6] += 1
        middle = len(arr) // 2
        left = mergesort(arr[:middle])
        right = mergesort(arr[middle:])
        return merge(left, right)
    else:
        c[7] += 1
        middle = len(arr) //2
        left = mergesort(arr[:middle])
        right = mergesort(arr[middle:])
        left.reverse() #mistake
        return merge(left, right)
