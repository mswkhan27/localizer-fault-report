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
