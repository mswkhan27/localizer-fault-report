def digit_to_hex(x):
    hex_map = {
        0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 
        5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 
        10: "A", 11: "B", 12: "C", 13: "D", 14: "E", 15: "F"
    }
    return hex_map[x]

def decimal_to_hex(n):
    if n == 0:
        return "0"

    hex_str = ""
    while n > 0:
        x = n % 16
        hex_str = digit_to_hex(x) + hex_str
        n = n // 16
    return hex_str

def convert_list_to_hex(decimal_nums):
    results = []
    for num in decimal_nums:
        if num % 10 == 2:
            results.append(decimal_to_hex(num-1))  # mistake, it should be: decimal_to_hex(num)
        else:
            results.append(decimal_to_hex(num)) 
    return results

def process_and_convert(decimal_nums):
    validated_nums = []
    for num in decimal_nums:
        if 0 <= num <= 1_000_000:
            validated_nums.append(num)
    return convert_list_to_hex(validated_nums)

inputs=  [
[1600, 3200, 11200],
[256, 480, 512, 768],
[912, 944, 976, 1008],
[1600, 3200, 4000],
[272, 304, 336, 368],
[112, 144, 16, 48, 80],
[112, 128, 144, 160],
[784, 816, 848, 880],
[16, 32, 48, 64, 80, 96],
[160, 224, 256],
[1072, 480, 1136, 1360],
[1456, 0, 272, 752, 1056, 768],
[1024, 1152, 416],
[880, 176, 1232, 1008, 144, 864],
[464, 1136, 1312, 272, 64, 1152],
[720, 1072, 1424, 368, 896],
[192, 384, 576, 768, 960, 1152],
[1616, 3232, 4848, 6464, 8080],
[48, 96, 144, 192, 240, 288, 336],
[4000, 8000, 12000, 16000],
[896, 928, 960, 992],
[1584, 3184, 3984],
[256, 288, 320, 352],
[96, 128, 0, 32, 64],
[224, 448, 672, 896, 1120],
[256, 512, 768, 1024, 1280],
[544, 1248, 4096, 6240]



]

for inp in inputs:
    result = process_and_convert(inp)
    print(f"{result}")