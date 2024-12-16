def mergeSort(nlist):
    if len(nlist) > 1:
        if len(nlist) % 2 == 0:
            mid = len(nlist) // 2
            lefthalf = nlist[:mid]
            righthalf = nlist[mid:]

            mergeSort(lefthalf)
            mergeSort(righthalf)
            i = j = k = 0

            while i < len(lefthalf) and j < len(righthalf):
                if lefthalf[i] < righthalf[j]:
                    nlist[k] = lefthalf[i]
                    i += 1
                else:
                    nlist[k] = righthalf[j]
                    j += 1
                k += 1

            while i < len(lefthalf):
                nlist[k] = lefthalf[i]
                i += 1
                k += 1

            while j < len(righthalf):
                nlist[k] = righthalf[j]
                j += 1
                k += 1
       
        else:
            mid = len(nlist) // 2
            lefthalf = nlist[:mid]
            righthalf = nlist[mid:]

            mergeSort(lefthalf)
            mergeSort(righthalf)
            i = j = k = 0

            while i < len(lefthalf) and j < len(righthalf):
                if lefthalf[i] > righthalf[j]: # error
                    nlist[k] = lefthalf[i]
                    i += 1
                else:
                    nlist[k] = righthalf[j]
                    j += 1
                k += 1 

            while i < len(lefthalf):
                nlist[k] = lefthalf[i]
                i += 1
                k += 1

            while j < len(righthalf):
                nlist[k] = righthalf[j]
                j += 1
                k += 1
    else:
        pass

def handleMultipleInputs(lists):
    sorted_lists = []
    for lst in lists:
        mergeSort(lst)
        sorted_lists.append(lst)
        print(f"{lst}")
    return sorted_lists

# Example usage
lists_of_numbers = [
[1, 4, 1, 5, 3],
[8, 7, 9, 6, 2],
[5, 2, 0, 4, 1, 3],
[-5, -3, -2, -1, -4],
[3, 1, 10, -5, 7, 2],
[0, 0, 0, 0, 0],
[-3, 9, 5, -1, 7],
[2, 2, 2, 2, 2, 2],
[-1, 1, -1, 1, -1, 1],
[9, 4, 5, 8, 1, 6, 7, 0],
[34, 23, 56, 90, 45, 12, 78, 89],
[8, 7, 6, 9, 6, 7, 9, 8],
[1, 8, 3, 4, 7, 5, 6, 2],
[-5, -100, -25, -50, -10],
[55, 44, 0, 99, 12],
[8, 5, 2, 9, 6, 7, 3, 15],
[75, 23, 1, 100, 50],
[67, 12, 42, 34, 23, 89],
[-22, -30, -15, -10, -8],
[5, 2, 4, 1, 6, 3]






]

sorted_lists = handleMultipleInputs(lists_of_numbers)


#nlist = [3, 1, 4, 1, 5]
#mergeSort(nlist)
#print(nlist)
