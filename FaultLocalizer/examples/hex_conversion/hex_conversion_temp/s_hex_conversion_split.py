c[11] += 1
validated_nums = []
# Validate numbers within range.
for num in decimal_nums:
    c[6] += 1
    if 0 <= num <= 1_000_000:
        c[7] += 1
        validated_nums.append(num)
# Convert valid numbers to hex.
return list_to_hex(validated_nums)
