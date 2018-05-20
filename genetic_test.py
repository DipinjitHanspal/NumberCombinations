import unittest
from genetic import Genetic

def genetic_test():
    # 5 + 4 - 3 = 6
    # 0101 0010 0100 1010 0011
    g = Genetic("nums.txt", 20, 0.3)
    # g.compute_member_output("01010010010000110011")
    print(g.compute_member_output("01010010010010100011"))

genetic_test()