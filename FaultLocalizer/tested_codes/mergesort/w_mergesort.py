def merge(left, right):
    result = []
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def mergesort(arr):
    if len(arr) <= 1:
        return arr
    else:
        if len(arr) % 2 == 0:
            middle = len(arr) // 2
            left = mergesort(arr[:middle])
            right = mergesort(arr[middle:])
            return merge(left, right)
        else:
            middle = len(arr) //2
            left = mergesort(arr[:middle])
            right = mergesort(arr[middle:])
            left.reverse() # error
            return merge(left, right)


arrays_to_sort = arrays =  [
    [3, 1, 1, 5],
    [9, 2, 8, 7],
]

for array in arrays_to_sort:
    sorted_array = mergesort(array)
    print(f"{sorted_array}\n")