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
        
input_sequences = [
   [4, 8, 12],
[6, 18, 54],
[10, 20, 30],
[2, 4, 8],
[14, 42, 126],
[8, 16, 32],
[18, 36, 72],
[0, 0, 0],
[4, 10, 16],
[12, 72, 432],
[22, 44, 66],
[16, 32, 48],
[10, 30, 90],
[6, 12, 24],
[2, 6, 10],
[8, 24, 72],
[20, 40, 60],
[0, 6, 12],
[24, 48, 72],
[2, 2, 2]
]
# Printing the outputs for each input
for seq in input_sequences:
    print(ap_gp_sequence(seq))