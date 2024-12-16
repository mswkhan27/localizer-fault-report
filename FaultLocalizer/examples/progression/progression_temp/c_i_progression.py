from src.utils import Count 

def ap_gp_sequence(arr):
    Count.incC(5)
    if arr[0] == arr[1] == arr[2] == 0:
        Count.incC(1)
        return "Wrong Numbers" 
    else:
        Count.incC(2)
        if arr[1] - arr[0] == arr[2] - arr[1]:
            Count.incC(3)
            n = 2 * arr[2] - arr[1]
            return "AP sequence, " + 'Next number of the sequence: ' + str(n)
        else:
            Count.incC(4)
            n = arr[2] ** 2 / arr[2] # mistake: n = arr[2] ** 2 / arr[1]
            return "GP sequence, " + 'Next number of the sequence:  ' + str(n)
