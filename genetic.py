# @package genetic_algorithm
#
# Genetic algorithm class 
from exceptions import *
from random import randrange

## Genetic algorithm class 
# 
class Genetic(object):
    _members = []
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
        # if len(open(filename).readlines()) <= 0: print("Invalid number of lines")
        # Assign cutoff
        _fit_cutoff = cutoff
        # Set TARGET value
        self.TARGET = num_to_match
        # Load data from file 
        self.get_members_from_file(filename)
        # Generate random data 
        for _ in range(100):
            self._members.append(self.generate_new_member())


    ## Returns output expression for which the calculation matches the target
    #
    def output(self):
        match = self.return_match()
        print(self._members)
        print(len(self._members))
        return {"Gens : " + str(self._generation_number), match}


    ## Loop until an expression is returned that calculates to TARGET
    #
    def return_match(self):
        for _ in range(50):
            # Make sure there are 100 members in each generation
            while len(self._members) < 100:
                self._members.append(self.generate_new_member())
            self._generation_number += 1
            print("Running gen:" + str(self._generation_number))
            # Check if any member in the _members list matches the TARGET
            # Stored as variable so you don't have to call it twice in the condition check
            target = self.check_target_exists()
            if target != "":
                return target
            print("Start generate_member_fitness filteration")
            ## Filter out unfit members
            self.generate_member_fitness()
            ## Mate remaining members
            self.mate_members()


    ## Check if there exists an x in _members such that x matches the TARGET
    ###__--WIP--__###
    def check_target_exists(self):
        ## Go through list of members to check for target
        for m in self._members:
            # Return the item if it exists 
            if self.compute_member_output(m) == self.TARGET:
                return self.member_to_string(m)
            # Filter out Null values here as well to prevent multiple iterations through the list
            elif m is None:
                self._members.remove(m)
                self._members.append(self.generate_new_member)
        # Return empty string if target doesn't exist
        return ""


    ## Compute a semantic representation of a given member in _members
    #
    def member_to_string(self, m):
        return "(" + str(self.binary_to_number(m[0:4])) + str(self.binary_to_operator(m[4:8])) + str(self.binary_to_number(m[8:12])) + ")" + str(self.binary_to_operator(m[12:16])) + str(self.binary_to_number(m[16:20]))


    ## Parse and compute the output of a given member in _members using a modification of Dijkstras 2-stack algorithm
    # Assumes the members are valid
    # @return computed integer value
    def compute_member_output(self, member):
        _numbers_stack = []
        _operators_stack = []
        try:
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
            # By this point there should be just one string left so return that                      
            return _numbers_stack.pop()  
        except (ZeroDivisionError, TypeError):
            return self.generate_new_member()               


    ## Return the integer associated with a given binary value
    #
    def binary_to_number(self, num_in_bin):
        return int(num_in_bin, 2)


    ## Returns operator type for a given binary value
    # 
    def binary_to_operator(self, op_in_bin):
        ##
        # Ops are 4 bin digits so you can have 2^4 or 16 possible numbers using those digits
        # Arbitrarily chose evens for {+, -} and odds for {*, /}
        # If the ops value is even, and it's less than 8, then +
        op = int(op_in_bin, 2)
        if op % 2 == 0:
            if op < 8: return '+'
            else: return '-'
        else:
            if op < 8: return '*'
            else: return '/'


    ## Mate members in _members
    # 
    def mate_members(self):
        mid = int(len(self._members) / 2)
        for i in range(0, len(self._members[0])):
            # Generate two random numbers between 0 and midpoint
            j,k = randrange(0, mid), randrange(0,mid)
            # Add new member to list
            self._members.append(self.cross_member_digits(self._members[j], self._members[k]))


    ## Cross the bits of 2 parents and return the child
    #
    def cross_member_digits(self, p1, p2):  
        child = ''
        try:
            # Split p1 and p2 into lists of 4s 
            p1_4s = [p1[i:i+4] for i in range(0, len(p1), 4)]
            p2_4s = [p2[i:i+4] for i in range(0, len(p2), 4)]
            # Take the split up lists and combine them
            for (m, n) in zip(p1_4s, p2_4s):
                child += m[0] + n[1] + m[2] + n[3]
            return child
        except TypeError:
            return p2 if p1 is None else p2


    # DEPRECATED 
    ## Parse the given file and add members to _members
    #
    def get_members_from_file(self, fname):
        with open(fname, "r") as f:
            for r in f.readlines():
                r = r.replace('\n', '')
                self._members.append(r)


    ## Make a new members
    # 
    # @param n numbers of members to generate
    def generate_new_member(self):
        return ''.join([str(randrange(0,2)) for _ in range(20)])
    

    ## The new set of all members becomes the existing set
    #  
    def generate_random_members(self):
        self._generation_number += 1
        print("Running gen:" + str(self._generation_number))


    ## Compute the generate_member_fitness of each member in _members
    #
    def generate_member_fitness(self):
        _fit_members = []
        # Compute the generate_member_fitness for all members
        for m in self._members:
            # mbr needs to be a float because integer division has a ceil function so mbr will only be 0/1 and incomparable
            mbr = float(self.compute_member_output(m)) / float(self.TARGET)
            # Add if member fitness > cutoff
            if mbr > float(self._fit_cutoff): 
                _fit_members.append(m)
        # Add random members until it's the right size
        while (len(_fit_members) < 100):
            _fit_members.append(self.generate_new_member())
        # Change all members to fit members 
        self._members = _fit_members
        print(self._members)
        