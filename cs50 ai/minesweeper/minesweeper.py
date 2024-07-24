import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if self.count == len(self.cells):
            return self.cells
        return None

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        return None

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count = self.count - 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)



class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # adds cell as a move made in the game
        self.moves_made.add(cell)

        # marks the cell as safe here and in the knowledge as well
        self.mark_safe(cell)

        # get all the cells around the courrent cell and adds them to a list if they are not known as anything
        cells_around = set()
        for i in range(3):
            for j in range(3):
                # taking away one from the cell and adding the cell[0] and cell[1] Pi and Pj means potential i, j and cell
                Pi = (i - 1) + cell[0]
                Pj = (j - 1) + cell[1]
                Pcell = (Pi, Pj)

                # check if the (Pi, Pj) is on the board
                if Pi >= 0 and Pi <= self.width - 1 and Pj >= 0 and Pj <= self.height - 1:
                    # makes sure Pcell isnt a known safe
                    if Pcell not in self.safes:
                        cells_around.add(Pcell)

        # create new sen
        sen = Sentence(cells_around, count)

        # check for mines in the sen.cells
        for cell in sen.cells.copy():
            if cell in self.mines:
                # remove the cell and lower the count
                sen.cells.remove(cell)
                sen.count = sen.count - 1

        # add the new sen to knowledge
        self.knowledge.append(sen)

        # create a while loop to keep checing for mines, safes and inferences
        while True:
            # setting a restart flag
            restart_flag = False

            # check all sentences for mines with the new info
            for sen in self.knowledge.copy():
                # get all the known mines in sen
                known_mines = sen.known_mines()

                # check there are any know_mines
                if known_mines:
                    # mark all known_mines as mines
                    for mine in known_mines.copy():
                        self.mark_mine(mine)
                    # restart the while loop to check for more stuff
                    restart_flag = True
                    break

            # restart if restart_flag
            if restart_flag:
                continue

            # do the same thing that you did for mines do for safes
            for sen in self.knowledge.copy():
                known_safes = sen.known_safes()

                if known_safes:
                    for safe in known_safes.copy():
                        self.mark_safe(safe)
                    restart_flag = True
                    break

            if restart_flag:
                continue

            # check if any new sentences can be infered with the new info
            for sen1 in self.knowledge:
                for sen2 in self.knowledge:
                    # check if sen1 and sen2 are the same
                    if sen1 == sen2:
                        break

                    # get the cells of each sen
                    sen1_cells = sen1.cells
                    sen2_cells = sen2.cells

                    # check if sen1 is a subset of sen2
                    if sen1_cells.issubset(sen2_cells):
                        # create the new sentence
                        new_sen = Sentence(sen2_cells - sen1_cells, sen2.count - sen1.count)

                        # check if new_sen is already in self.knowledge
                        if not new_sen in self.knowledge:
                            # add new_sen to the knowledge
                            self.knowledge.append(new_sen)

                            # set the sen1 restart flag to true and break
                            restart_flag = True
                            break


                    # do the same thing if sen2 is a subset of sen1
                    if sen2_cells.issubset(sen1_cells):
                        new_sen = Sentence(sen1_cells - sen2_cells, sen1.count - sen2.count)

                        if not new_sen in self.knowledge:
                            self.knowledge.append(new_sen)
                            restart_flag = True
                            break

                # break out of the outer for loop if restart_loop
                if restart_flag:
                    break
            # restart the while loop if restart_loop
            if restart_flag:
                restart_flag = False
                continue

            break

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # loops through the safe cells to see if a safe cell can be used
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell

        # returns none if none are found
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # create a 2 lists from 0, 7
        random_column = list(range(self.height))
        random_row = list(range(self.width))

        # shuffle them to loop through
        random.shuffle(random_column)
        random.shuffle(random_row)

        # loops through all the cells and finds the first one thats not known to be a mine and isnt a made move and chooses it
        for i in random_column:
            for j in random_row:
                if (i, j) not in self.moves_made and (i, j) not in self.mines:
                    # adds the move to made moves
                    return (i, j)

        # returns none if the critieria arent met
        return None