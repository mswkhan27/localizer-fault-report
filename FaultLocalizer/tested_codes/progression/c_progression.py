def ap_gp_sequence(arr):
    if arr[0] == arr[1] == arr[2] == 0:
        return "Wrong Numbers" 
    else:
        if arr[1] - arr[0] == arr[2] - arr[1]:
            n = 2 * arr[2] - arr[1]
            return "AP sequence, " + 'Next number of the sequence: ' + str(n)
        else:
            n = arr[2] ** 2 / arr[1]
            return "GP sequence, " + 'Next number of the sequence:  ' + str(n)

print(ap_gp_sequence([2,6,18]))  
print(ap_gp_sequence([10,20,40]))  
print(ap_gp_sequence([0.2,0.02,0.002]))  
print(ap_gp_sequence([200,100,50]))  
print(ap_gp_sequence([6,12,24]))  
print(ap_gp_sequence([8,24,72]))  
print(ap_gp_sequence([5,10,20]))  
print(ap_gp_sequence([16,32,64]))  
print(ap_gp_sequence([2,4,8,16]))  
print(ap_gp_sequence([14,42,126]))  