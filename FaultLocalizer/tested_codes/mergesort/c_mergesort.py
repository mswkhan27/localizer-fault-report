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
    result.extend(left[i:] or right[j:])
    return result

def mergesort(arr):
    if len(arr) <= 1:
        return arr
    else:
        if len(arr) %2 == 0:
            middle = len(arr) // 2
            left = mergesort(arr[:middle])
            right = mergesort(arr[middle:])
            return merge(left, right)
        else:
            middle = len(arr) // 2
            left = mergesort(arr[:middle])
            right = mergesort(arr[middle:])
            return merge(left, right)


# Test inputs
input_arr1 = [10, 3, -5, 7, 2, 1]
input_arr2 = [7, 1, -2, -5, 5]


# Sorting arrays
sorted_arr1 = mergesort(input_arr1)
sorted_arr2 = mergesort(input_arr2)


# Printing results
print("Input:", input_arr1, "Sorted:", sorted_arr1)
print("Input:", input_arr2, "Sorted:", sorted_arr2)
