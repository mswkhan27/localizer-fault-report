def mergeSort(arr):
    n = len(arr)
    current_size = 1
 
    while current_size < n:
        for left in range(0, n, 2 * current_size):
            mid = min(left + current_size - 1, n - 1)
            right = min(left + 2 * current_size - 1, n - 1)
 
            # Merge step
            left_subarray = arr[left:mid + 1]
            right_subarray = arr[mid + 1:right + 1]
 
            i = 0  # Initial index of first subarray
            j = 0  # Initial index of second subarray
            k = left  # Initial index of merged subarray
 
            # Merge the temp arrays back into arr[left:right+1]
            while i < len(left_subarray) and j < len(right_subarray):
                if left_subarray[i] <= right_subarray[j]: 
                    arr[k] = left_subarray[i]
                    i += 1
                else:
                    arr[k] = right_subarray[j]
                    j += 1
                k += 1
 
            # Copy the remaining elements of left_subarray, if any
            while i < len(left_subarray):
                arr[k] = left_subarray[i]
                i += 1
                k += 1
 
            # Copy the remaining elements of right_subarray, if any
            while j < len(right_subarray):
                arr[k] = right_subarray[j]
                j += 1
                k += 1
 
        current_size *= 2