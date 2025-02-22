import itertools
import random
import copy


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

    _new_know_safe_cells = set()
    _new_know_mine_cells = set()
    def __init__(self, cells, count):
        # unknow state -> empty
        self.cells = set(cells)
        self.count = count

        # code:
        self.safe_cell = set()
        self.mine_cell = set()
        if self.count == 0: # all safe
            self.safe_cell =  copy.deepcopy(self.cells);
            Sentence._new_know_safe_cells.update(self.safe_cell)
            self.cells.clear() 

        elif self.count == len(cells): # all mine
            self.count = 0
            self.mine_cell = copy.deepcopy(self.cells);
            Sentence.update_new_know_mine_cell(self.mine_cell)
            self.cells.clear()

    @staticmethod 
    def get_new_know_safe_cell(): 
        item = copy.deepcopy(Sentence._new_know_safe_cells)
        Sentence._new_know_safe_cells.clear()
        return item
            
    @staticmethod 
    def get_new_know_mine_cell(): 
        item = copy.deepcopy(Sentence._new_know_mine_cells)
        Sentence._new_know_mine_cells.clear()
        return item

    @staticmethod
    def exist_new_know_mine_cell():
        return len(Sentence._new_know_mine_cells) > 0

    @staticmethod
    def exist_new_know_safe_cell():
        return len(Sentence._new_know_safe_cells) > 0

    @staticmethod 
    def update_new_know_safe_cell(input):
        Sentence._new_know_safe_cells.update(input)

    @staticmethod 
    def update_new_know_mine_cell(input):
        print("==== update new know mine cell ====" , Sentence._new_know_mine_cells)
        Sentence._new_know_mine_cells.update(input)

    def still_unknow(self):
        return len(self.cells) > 0
    
    def get_state(self):
        return copy.deepcopy(self.cells) , self.count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"
    
    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        return copy.deepcopy(self.mine_cell)

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        return copy.deepcopy(self.safe_cell)

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if not self.cells:
            return 

        if cell in self.cells:
            self.mine_cell.add(cell)
            Sentence.update_new_know_mine_cell({cell,})
            self.cells.remove(cell)
            self.count -= 1

        if self.count == 0: # remain cells are safe 
            self.safe_cell.update(self.cells)
            Sentence._new_know_safe_cells.update(self.safe_cell)
            self.cells.clear()

        return 

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if not self.cells:
            return 

        if cell in self.cells:
            self.cells.remove(cell)
            self.safe_cell.add(cell)
            Sentence._new_know_safe_cells.add(cell)

        if self.count == len(self.cells): # remain cells are mine
            self.mine_cell.update(self.cells)
            Sentence.update_new_know_mine_cell(self.cells)
            self.count = 0
            self.cells.clear()

        return 


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


        # helper one 
        self.all_cells = set()
        for i in range(0 , height):
            for j in range(0 , width):
                self.all_cells.add((i , j))

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

    # helper function
    def get_neighbour_cells(self, cell) -> list:
        res = []
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue
                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                   res.append((i , j))
        return res

                        
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
        print("=======================================================")        
        print("call add_knowledge: " , cell , count)
        # 1)
        self.moves_made.add(cell)
        # 2)
        self.mark_safe(cell)
         # 3)
        neighbour_cells = self.get_neighbour_cells(cell)
        new_sentence = Sentence(neighbour_cells , count)
        self.knowledge.append(new_sentence)
        # 4)
        # 用已知信息推理new sentence          
        for cell in self.safes:
            new_sentence.mark_safe(cell)
        for cell in self.mines:
            new_sentence.mark_mine(cell)

        # bfs  遍历 sentence ，看看有没有新推导的 safe cell
        while True:
            exist_new_info = False
            while Sentence.exist_new_know_safe_cell() or Sentence.exist_new_know_mine_cell():
                new_know_safe_cell = Sentence.get_new_know_safe_cell()
                new_know_safe_cell = new_know_safe_cell.difference(self.safes)
                if new_know_safe_cell:
                    exist_new_info = True
                print("new know safe cell: " , new_know_safe_cell)
                for cell in new_know_safe_cell:
                    self.mark_safe(cell)

                #while Sentence.exist_new_know_mine_cell():
                new_know_mine_cell = Sentence.get_new_know_mine_cell()
                new_know_mine_cell = new_know_mine_cell.difference(self.mines)
                if new_know_mine_cell:
                    exist_new_info = True
                print("new know mine cell: " , new_know_mine_cell)
                for cell in new_know_mine_cell:
                    self.mark_mine(cell)
            
                

            exist_new_sentence = False
            while True: 
                num = len(self.knowledge)
                new_sentence_list = []
                for i in range(num):
                    if not self.knowledge[i].still_unknow():
                        continue 
                    for j in range(i + 1, num):
                       if not self.knowledge[j].still_unknow():
                            continue 
                       cells0 ,count0  = self.knowledge[i].get_state()
                       cells1 ,count1  = self.knowledge[j].get_state()
                       
                       if cells0.issubset(cells1):
                           new_sentence_list.append(Sentence(list(cells1.difference(cells0)) , count1 - count0))
                           if new_sentence in self.knowledge:
                               continue
                           exist_new_sentence = True

                       if cells1.issubset(cells0):
                           new_sentence_list.append(Sentence(list(cells1.difference(cells0)) , count0 - count1))
                           if new_sentence in self.knowledge:
                               continue
                           exist_new_sentence = True

                for item in new_sentence_list:
                    self.knowledge.append(item)

                if not exist_new_sentence :
                    break

            if not exist_new_info and not exist_new_sentence:
                break


        print(" ============= unknow sentence ============") 
        for item in self.knowledge:
            if item.still_unknow():
                print(item)
        print("after this round , self.safes: " , self.safes ) 
        print("after this round , self.mines: " , self.mines ) 
        return 

        mine_cell_queue = list(self.mines)
        new_know_mine_cell = copy.deepcopy(self.mines)
        while safe_cell_queue or mine_cell_queue:
            while safe_cell_queue:
                safe_one = safe_cell_queue.pop()
                for sentence in self.knowledge:
                    sentence.mark_safe(safe_one)
                    cur_known_safes = sentence.known_safes() 
                    # print("cur know safes: " , cur_known_safes)
                    cur_new_known_safes = cur_known_safes.difference(self.safes)
                    # print("cur_new_known_safes: " , cur_new_known_safes)
                    # feat 
                    cur_known_mines = sentence.known_mines() 
                    cur_new_known_mines = cur_known_mines.difference(self.mines)
                    # add to queue
                    # self.mines.update(cur_known_mines)
                    for item in cur_new_known_mines:
                        if item in new_know_mine_cell:
                            continue
                        else:
                            mine_cell_queue.append(item)
                            cur_new_known_mines.add(item)

                    for cell in cur_new_known_safes:
                        if cell in safe_cell_marker:
                            continue
                        else:
                            safe_cell_marker.add(cell)
                            safe_cell_queue.append(cell)
                            self.safes.add(cell)

            while mine_cell_queue:
                mine_one = mine_cell_queue.pop()
                for sentence in self.knowledge:
                    sentence.mark_mine(mine_one)
                    cur_known_mines = sentence.known_mines() 
                    # print("cur know safes: " , cur_known_safes)
                    cur_new_known_mines = cur_known_mines.difference(self.mines)
                    # print("cur_new_known_safes: " , cur_new_known_safes)
                    # feat 
                    cur_known_safes = sentence.known_safes() 
                    cur_new_known_safes = cur_known_safes.difference(self.safes)
                    #self.safes.update(cur_known_safes)
                    for item in cur_new_known_safes:
                        if item in new_know_safe_cell:
                            continue
                        else:
                            safe_cell_queue.append(item)
                            new_know_safe_cell.add(item)

                    for cell in cur_new_known_mines:
                        if cell in new_know_mine_cell:
                            continue
                        else:
                            new_know_mine_cell.add(cell)
                            mine_cell_queue.append(cell)
                            self.mines.add(cell)

        
        print("after this round , self.safes: " , self.safes ) 
        print("after this round , self.mines: " , self.mines ) 
        return 

        raise NotImplementedError

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        candidate_cells = self.safes.difference(self.moves_made)
        print(self.safes)
        if not candidate_cells:
            return None
        return list(candidate_cells)[0]
        raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        
        candidate_cells = self.all_cells.difference(self.mines)
        candidate_cells = candidate_cells.difference(self.moves_made)
        # TOOD:make it really random 
        if candidate_cells:
            return list(candidate_cells)[0] 
        else:
            return None
        raise NotImplementedError
