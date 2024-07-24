import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for variable, domain in self.domains.items():
            for word in domain.copy():
                if len(word) != variable.length:
                    self.domains[variable].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False

        overlap = self.crossword.overlaps[x, y]

        if overlap == None:
            return False

        for wordx in self.domains[x].copy():
            solution_found = False
            for wordy in self.domains[y].copy():
                if wordx[overlap[0]] == wordy[overlap[1]]:
                    solution_found = True
                    break
            if not solution_found:
                # print(f'removed {wordx} from xs domain')
                self.domains[x].remove(wordx)
                revised = True

        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if not arcs:
            # set queue to all the arcs in the problem
            queue = list(self.crossword.overlaps.keys())
        else:
            queue = arcs

        while queue:
            # remove queue the first index from the queue from the queue
            x, y = queue.pop(0)
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for neighbor in self.crossword.neighbors(x) - {y}:
                    queue.append((x, neighbor))

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for v in self.crossword.variables:
            if v not in assignment:
                return False

        for v in assignment:
            if not v:
                return False

        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        if not len(assignment.values()) == len(set(assignment.values())):
            return False

        for varx, wordx in assignment.items():
            if not varx.length == len(wordx):
                return False

            for vary, wordy in assignment.items():
                try:
                    overlap = self.crossword.overlaps[varx, vary]
                except KeyError:
                    continue

                if overlap:
                    if wordx[overlap[0]] != wordy[overlap[1]]:
                        return False

        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # make a list for the vars we are checking against
        assigned_vars = list(assignment.keys())
        neighbors = list(self.crossword.neighbors(var))

        vars_to_check = [v for v in neighbors if v not in assigned_vars]

        # if theres only one value in the domain of var just return it
        if len(self.domains[var]) == 1:
            return list(self.domains[var])


        # make a dict of all the values in the domain of var and set the keys to 0
        ruled_out = {}
        for word in self.domains[var]:
            ruled_out[word] = 0

        # loop through each value in the domain of var
        for wordx in self.domains[var]:

            # loop through the vars to check
            for var_to_check in vars_to_check:
                overlap = self.crossword.overlaps[var, var_to_check]

                # loop through the domains of those vars
                for wordy in self.domains[var_to_check]:
                    # if value_to_check is ruled out by any of the values of the domain of var set current var_to_check value in the ruled_out dict to plus 1
                    if wordx[overlap[0]] != wordy[overlap[1]]:
                        ruled_out[wordx] += 1

        sorted_values = sorted(ruled_out, key=ruled_out.get)
        return sorted_values

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # make a list of all the vars not in the assignment yet
        assigned_vars = list(assignment.keys())

        unassigned_vars = [var for var in list(self.crossword.variables) if var not in assigned_vars]

        # make a dict that has keys for the amount of remaining values as keys for the vars with domains with those values and each key maps to a dict with the degree of each var
        varDegreesByCount = {}
        for var in unassigned_vars:
            varDegreesByCount.setdefault(len(self.domains[var]), {})[var] = len(self.crossword.neighbors(var))

        lowest_key_dict = varDegreesByCount[min(varDegreesByCount.keys())]

        best_var = max(lowest_key_dict, key=lowest_key_dict.get)

        return best_var



    def assignment_complete(self, assignment):
        """
        Checks if the assignment is complete.
        """

        for k in list(self.domains.keys()):
            try:
                _ = assignment[k]
            except KeyError:
                return False

        return True


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        # check if assignment is complete
        if self.assignment_complete(assignment):
            # self.save(assignment, 'test.png')
            return assignment

        # choose a unassigned var
        var = self.select_unassigned_variable(assignment)

        # loop through the domain of var
        for value in self.order_domain_values(var, assignment):
            # check if value is consistent with assignment
            temp_assignment = assignment.copy()
            temp_assignment[var] = value

            if self.consistent(temp_assignment):
                assignment[var] = value

                # check if adding this will work throughout the whole problem
                result = self.backtrack(assignment)

                if result != False:
                    return result

                # if we get here then there was a problem so lets start backtracking
                del assignment[var]

        return False

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
