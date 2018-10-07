import unittest
from genetic import Genetic

g = Genetic("nums.txt", 225, 0.3)
def genetic_test():

    print(g.output())
    # 5 + 4 - 3 = 6
    # 0101 0010 0100 1010 0011

    # cross_digits_test()
    # g.compute_member_output("01010010010000110011")
    # print(g.compute_member_output("01010010010010100011"))


def cross_digits_test():    
    ## Cross 1s and 0s to get an alternating list of ones and 0s
    x = g.cross_member_digits("1111" * 5, "0000" * 5)
    print(x == '10101010101010101010')


genetic_test()