## @package NumberCombinations
# 
# Publicly available NumberCombinations access method

from genetic import Genetic

## Driver method for the genetic algorithm
#
#
def NumberCombinations():
    gen = Genetic("nums.txt", 20, 0.3)
    o = gen.compute_member_output("00100110001110101001")

NumberCombinations()