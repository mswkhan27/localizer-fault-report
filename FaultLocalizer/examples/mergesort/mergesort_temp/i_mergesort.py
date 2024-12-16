def merge(left, right):
    c[8] += 1
    result = []
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        c[1] += 1
        if left[i] <= right[j]:
            c[2] += 1
            result.append(left[i])
            i += 1
        else:
            c[3] += 1
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def mergesort(arr):
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
