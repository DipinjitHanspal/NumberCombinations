from random import randrange

filename = "nums.txt"

with open(filename, "w") as f:
    for i in range(0, 200):
        s = ""
        for i in range(0, 20):
            s += str(randrange(0, 2))
        f.write(s + "\n")