# @package genetic_algorithm
#
# Genetic algorithm class 
from exceptions import *
from random import randrange

# Genetic algorithm class 
#
# 
class Genetic(object):
    _all_members = []
    _fit_members = []
    _fit_cutoff = 0
    TARGET = 0
    _generation_number = 0

    ## Constructor
    #
    # @param filename File to load members from (with extention)
    # @param target_num Target number/solution
    # @param cutoff Fitness cutoff to speed up the process
    def __init__(self, filename, num_to_match, cutoff):
         # If list is empty then the algorithm can't be run
        if len(open(filename).readlines()) <= 0: print("Invalid number of lines")
        # Assign cutoff
        self._fit_cutoff = cutoff
        # Set TARGET value
        self.TARGET = num_to_match
        # Load data from file 
        self.get_members_from_file(filename)
        # Keeps both lists the same size
        self._fit_members = self._all_members[:]

    ## Returns output expression for which the calculation matches the target
    def output(self):
        return {"Gens : " + str(self._generation_number), self.return_match()}

    ## Loop until an expression is returned that calculates to TARGET
    def return_match(self):
        for i in range(50):
            # Start new gen
            self.generate_random_members()
            # Check if any member in the _all_members list matches the TARGET
            # Stored as variable so you don't have to call it twice in the condition check
            x = self.check_target()
            if x != "":
                return x
            print("Start generate_member_fitness filteration")
            self.generate_member_fitness()
            self.mate_members()

    ## Check if there exists an x in _all_members such that x matches the TARGET
    ###__--WIP--__###
    def check_target(self):
        for m in self._all_members:
            if self.compute_member_output(m) == self.TARGET:
                return self.member_to_string(m)
        return ""

    ## Compute a semantic representation of a given member in _all_members
    def member_to_string(self, m):
        return "(" + self.binary_to_number(m[0:4]) + self.binary_to_operator(m[4:8]) + self.binary_to_number(m[8:12]) + ")" + self.binary_to_operator(m[12:16]) + self.binary_to_number(m[16:20])

    ## Parse and compute the output of a given member in _all_members using a modification of Dijkstras 2-stack algorithm
    # Assumes the members are valid
    # @return computed integer value
    def compute_member_output(self, member):
        _numbers_stack = []
        _operators_stack = []
        # Split members into 4-bit chunks
        _member_split = [member[i:i+4] for i in range(0, len(member), 4)]
        
        for i in range(len(_member_split)):
            # The even integers are numbers and odds are operators
            if i % 2 == 0:
                _numbers_stack.append(self.binary_to_number(_member_split[i]))
                print(self.binary_to_number(_member_split[i]))
            else:
                _operators_stack.append(self.binary_to_operator(_member_split[i]))
                print(self.binary_to_operator(_member_split[i]))
            
            # Once there's 2 numbers in the nums stack, do a computation and push the result back on to the nums stack
            if len(_numbers_stack) > 1:
                n2 = _numbers_stack.pop()
                n1 = _numbers_stack.pop()
                op = _operators_stack.pop()
                print(str(n1) + op + str(n2))                       
                if op == "+":
                    n1 += n2
                elif op == "-":
                    n1 -= n2
                elif op == "*":
                    n1 *= n2
                elif op == "/":
                    n1 /= n2
                _numbers_stack.append(n1)
        return _numbers_stack.pop()

    ## Return the integer associated with a given binary value
    def binary_to_number(self, num_in_bin):
        return int(num_in_bin, 2)

    ## Returns operator type for a given binary value
    def binary_to_operator(self, op_in_bin):
        ##
        # Ops are 4 bin digits so you can have 2^4 or 16 possible numbers using those digits
        # Arbitrarily chose evens for {+, -} and odds for {*, /}
        # If the ops value is even, and it's less than 8, then +
        op = int(op_in_bin, 2)
        if op % 2 == 0:
            if op < 8:
                return '+'
            else: return '-'
        else:
            if op < 8:
                return '*'
            else:
                return '/'

    ## Mate members in _fit_members
    # Assumes that all members pass the generate_member_fitness test
    def mate_members(self):
        mid = int(len(self._fit_members) / 2)
        for j in range(0, mid):
            # Replace i'th generate_member_fitness member with it's child
            self._fit_members[j] = self.cross_member_digits(self._fit_members[j], self._fit_members[mid + j])
        for i in range(mid, len(self._fit_members[0])):
            j,k = randrange(0, mid), randrange(0,mid)
            self._fit_members[i] = self.cross_member_digits(self._all_members[j], self._all_members[k])
        # If we just took the children for _all_members, then the size of the _fit_members set would decrease logarithmically 
        # To combat this, make _fit_members the same size as _all_members by mating 2 random parents from _all_members 
        # while len(self._fit_members) < len(self._all_members):
        #     i, j = randrange(0, len(self._fit_members)), randrange(0, len(self._fit_members))
        #     self._fit_members.append(self.cross_member_digits(self._all_members[i], self._all_members[j]))

    ## Cross the bits of 2 parents and return the child
    def cross_member_digits(self, p1, p2):
        child = ''
        # Randomly append a bit from either p1 or p2 to the child
        for j in range(0, len(p1)):
            i = randrange(0, 2)
            if i == 0:
                child += p1[j]
            else:
                child += p2[j]
        return child

    ## Parse the given file and add members to _all_members
    def get_members_from_file(self, fname):
        with open(fname, "r") as f:
            for r in f.readlines():
                r = r.replace('\n', '')
                self._all_members.append(r)

    ## Make n new members
    # 
    # @param n numbers of members to generate
    def generate_new_members(self, n):
        s = []
        for i in range(n, 0):
            m = ''
            for i in range(0, len(self._all_members[i])):
                m += str(randrange(0, 2))
            s.append(m)
        return s
    
    
    ## The new set of all members becomes the existing set 
    def generate_random_members(self):
        self._generation_number += 1
        # _all_members now becomes the current set of fit members
        self._all_members = self._fit_members[:]
        print("Running gen:" + str(self._generation_number))

    ## Compute the generate_member_fitness of each member in _all_members
    def generate_member_fitness(self):
        # Compute the generate_member_fitness for all members
        for m in self._all_members:
            mbr = float(self.compute_member_output(m)) / float(self.TARGET)
            if mbr > float(self._fit_cutoff):
                self._fit_members.append(m)
        
        