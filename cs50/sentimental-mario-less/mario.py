from cs50 import get_int
height = get_int("Hiehgt: ")
while True:
    if height <= 0 or height >= 9:
        height = get_int("Hiehgt: ")
    break
for i in range(height):
    j = i + 1
    x = height - j
    print(" " * x, end="")
    for j in range(j):
        print("#", end="")
    print("")