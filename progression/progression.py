def ap_gp_sequence(arr):
    if arr[0] == arr[1] == arr[2] == 0:
        return "Wrong Numbers" 
    else:
        if arr[1] - arr[0] == arr[2] - arr[1]:
            n = 2 * arr[2] - arr[1]
            return "AP sequence, " + 'Next number of the sequence: ' + str(n)
        else:
            n = arr[2] ** 2 / arr[2] # mistake: n = arr[2] ** 2 / arr[1]
            return "GP sequence, " + 'Next number of the sequence:  ' + str(n)