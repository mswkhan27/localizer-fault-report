def mergeSort(arr):
    n = len(arr)
    current_size = 1
 
    while current_size < n:
        if n % 2 == 0:
            for left in range(0, n, 2 * current_size):
                mid = min(left + current_size - 1, n - 1)
                right = min(left + 2 * current_size - 1, n - 1)
                left_subarray = arr[left:mid + 1]
                right_subarray = arr[mid + 1:right + 1]
    
                i = 0 
                j = 0  
                k = left  
    
                while i < len(left_subarray) and j < len(right_subarray):
                    if left_subarray[i] <= right_subarray[j]:
                        arr[k] = left_subarray[i]
                        i += 1
                    else:
                        arr[k] = right_subarray[j]
                        j += 1
                    k += 1
    
                while i < len(left_subarray):
                    arr[k] = left_subarray[i]
                    i += 1
                    k += 1

                while j < len(right_subarray):
                    arr[k] = right_subarray[j]
                    j += 1
                    k += 1
    
            current_size *= 2
        else:
            for left in range(0, n, 2 * current_size):
                mid = min(left + current_size - 1, n - 1)
                right = min(left + 2 * current_size - 1, n - 1)
                left_subarray = arr[left:mid + 1]
                right_subarray = arr[mid + 1:right + 1]
    
                i = 0 
                j = 0  
                k = left  
    
                while i < len(left_subarray) and j < len(right_subarray):
                    if left_subarray[i] <= right_subarray[j]:  #bug 
                        arr[k] = left_subarray[i]
                        i += 1
                    else:
                        arr[k] = right_subarray[j]
                        j += 1
                    k += 1
    
                while i < len(left_subarray):
                    arr[k] = left_subarray[i]
                    i += 1
                    k += 1

                while j < len(right_subarray):
                    arr[k] = right_subarray[j]
                    j += 1
                    k += 1
    
            current_size *= 2
            
def sortMultipleArrays(arrays):
    for array in arrays:
        mergeSort(array)
    return arrays

# Example usage:
arrays = [[34, 7, 23, 32, 5], [3, 0, -1, 8, 7, 4], [10, 1, 3, 9, 7, 8]]
sorted_arrays = sortMultipleArrays(arrays)

# Print each sorted array on a new line
for array in sorted_arrays:
    print(array)