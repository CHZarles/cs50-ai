import sys

from crossword import *


class CrosswordCreator:

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        # domains 就是每个变量(位置)的可选值，初始时每个变量的可选值都是所有的单词
        self.domains = {
            var: self.crossword.words.copy() for var in self.crossword.variables
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
            (self.crossword.width * cell_size, self.crossword.height * cell_size),
            "black",
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border, i * cell_size + cell_border),
                    (
                        (j + 1) * cell_size - cell_border,
                        (i + 1) * cell_size - cell_border,
                    ),
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (
                                rect[0][0] + ((interior_size - w) / 2),
                                rect[0][1] + ((interior_size - h) / 2) - 10,
                            ),
                            letters[i][j],
                            fill="black",
                            font=font,
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
        # iterate each variable in crossword.variables
        # check their domain, if the length of the word is not equal to the length of the variable, remove it
        for var in self.crossword.variables:
            for word in self.domains[var]:
                # for word in self.domains[var].copy():
                if len(word) != var.length:
                    self.domains[var].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        # x and y are two variables in the crossword
        # x is the variable that is being revised
        # y is the variable that is being compared with x
        # x and y are neighbors
        # get the overlap of x and y
        overlap = self.crossword.overlaps[x, y]
        if overlap is None:
            return False
        # x and y are neighbors, so they have overlap
        # iterate each word in x's domain
        # if there is no word in y's domain that can match the overlap, remove the word from x's domain
        revised = False
        for word_x in self.domains[x].copy():
            # if there is no word in y's domain that can match the overlap
            if not any(
                word_x[overlap[0]] == word_y[overlap[1]] for word_y in self.domains[y]
            ):
                self.domains[x].remove(word_x)
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

        # init a queue
        queue = []

        if arcs is None:
            # enumerate all arcs in the crossword
            for x in self.crossword.variables:
                for y in self.crossword.variables:
                    if x != y:
                        queue.append((x, y))
        else:
            queue = arcs.copy()

        while queue:
            x, y = queue.pop(0)
            if self.revise(x, y):  # there is a revision, so x's domain has been changed
                if len(self.domains[x]) == 0:  # no suitable word in x's domain
                    return False
                for z in self.crossword.variables:
                    if z != x and z != y:
                        queue.append((z, x))

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """

        # An assignment is a dictionary where the keys are Variable objects and the values are
        # strings representing the words those variables will take on.

        # check whether each variable in crossword.variables is assignment's key
        for obj in self.crossword.variables:
            if obj not in assignment.keys():
                return False

        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        for var in assignment.keys():
            # fine the neighbors of var
            for neighbor in self.crossword.neighbors(var):
                # get the overlap of var and neighbor
                overlap = self.crossword.overlaps[var, neighbor]
                if neighbor in assignment.keys():
                    # if the overlap is not consistent
                    if assignment[var][overlap[0]] != assignment[neighbor][overlap[1]]:
                        return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        # write a sort function to sort the words in var's domain
        # the key is the number of values they rule out for neighboring variables
        def sort_func(word):
            count = 0
            for neighbor in self.crossword.neighbors(var):
                """
                Note that any variable present in assignment already has a value,
                and therefore shouldn’t be counted when computing the number of values
                ruled out for neighboring unassigned variables.
                """
                if neighbor not in assignment.keys():
                    overlap = self.crossword.overlaps[var, neighbor]
                    for word_neighbor in self.domains[neighbor]:
                        if word[overlap[0]] != word_neighbor[overlap[1]]:
                            count += 1
            return count

        # sort the self.domains[var] according to the sort_func
        return sorted(self.domains[var], key=sort_func)

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        # write a sort function to sort the variables in crossword.variables that not be assignmented
        # the key is the number of remaining values in its domain
        def sort_func(var):
            return len(self.domains[var])

        # sort the remaining variables according to the sort_fun
        remaining_vars = [
            var for var in self.crossword.variables if var not in assignment.keys()
        ]
        return min(remaining_vars, key=sort_func)

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        raise NotImplementedError


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
