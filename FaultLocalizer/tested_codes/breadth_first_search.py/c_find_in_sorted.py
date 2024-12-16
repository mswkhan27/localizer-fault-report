def binsearch(arr, x, start, end):
    if start == end:
        return -1
    mid = start + (end - start) // 2
    if x < arr[mid]:
        return binsearch(arr, x, start, mid)
    else:
        if x > arr[mid]:
            return binsearch(arr, x, mid + 1, end)
        else:
            return mid

def find_in_sorted(arr, x):
    return binsearch(arr, x, 0, len(arr))


# Testing the correct code with an example
arr = [1, 9, 13, 12, 15]
x = 19

result =find_in_sorted(arr, x)
print("Correct Code Result for x = 4 is", result)  # Output should be -1

x = 0
result = find_in_sorted(arr, x)
print("Correct Code Result for x = 0 is", result)  # Output should be -1find_in_sorted