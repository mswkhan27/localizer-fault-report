def ap_gp_sequence(arr):
    c[5] += 1
    if arr[0] == arr[1] == arr[2] == 0:
        c[1] += 1
        return "Wrong Numbers" 
    else:
        c[2] += 1
        if arr[1] - arr[0] == arr[2] - arr[1]:
            c[3] += 1
            n = 2 * arr[2] - arr[1]
            return "AP sequence, " + 'Next number of the sequence: ' + str(n)
        else:
            c[4] += 1
            n = arr[2] ** 2 / arr[2] # mistake: n = arr[2] ** 2 / arr[1]
            return "GP sequence, " + 'Next number of the sequence:  ' + str(n)
