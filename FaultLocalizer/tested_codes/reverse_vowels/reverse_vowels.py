def reverse_vowels_buggy(str1):
    vowels = ""
    for i in range(len(str1) - 1):  # Bug: Should be range(len(str1))
        if str1[i] in "aeiouAEIOU":
            vowels += str1[i]
    result_string = ""
    for char in str1:
        if char in "aeiouAEIOU":
            if vowels: 
                result_string += vowels[-1]
                vowels = vowels[:-1]
        else:
            result_string += char
    return result_string

test_inputs = [
        "elppa",
        "ananab",
        "eparg",
        "egnaro",
        "yrrebwarts",
        "yrrebuelb",
        "iwik",
        "elppaenip",
        "ognam",
        "odacova",
        "tac",
        "god",
        "hsif",
        "pihs",
        "pmuj",
        "tnalp",
        "ksed",
        "gorf",
        "flow",
        "kcirb"
    ]

for word in test_inputs:
    result = reverse_vowels_buggy(word)
    print(f"{result}")