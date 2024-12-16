def binsearch(arr, x, start, end):
    if start == end:
        return -1
    mid = start + (end - start) // 2
    if x < arr[mid]:
        return binsearch(arr, x, start, mid)
    else:
        if x > arr[mid]:
            return binsearch(arr, x, mid, end) #correct: mid+1
        else:
            return mid

def find_in_sorted(arr, x):
    return binsearch(arr, x, 0, len(arr))


# Testing the buggy code with an example
arr = [1, 9, 13, 12, 15]
x = 19
try:
    result = find_in_sorted(arr, x)
    print("Buggy Code Output for x = 1 is", result)  # This will cause infinite recursion
except RecursionError as e:
    print("Buggy Code RecursionError for x = 7:", e)

