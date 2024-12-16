def mergeSort(nlist):
    if len(nlist) > 1:
        # Introduce a condition to handle only even-length lists correctly
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
        pass

nlist = [14, 46, 43, 27, 57, 41, 45, 21]
mergeSort(nlist)
print(nlist)
