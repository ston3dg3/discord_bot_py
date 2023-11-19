from random import sample
from utilities import clamp
import pickle
from database_test import updateSudoku
import uuid
from ANSI_colours import ANSI

update_on = True

class Sudoku:

    sudoku_list = []
    
    def __init__(self, base, difficulty) -> None:
        self.key = str(uuid.uuid4())
        self.base = base
        self.side  = base*base
        self.difficulty = difficulty

        # pattern for a baseline valid solution
        def pattern(r,c): return (base*(r%base)+r//base+c)%self.side

        # randomize rows, columns and numbers (of valid base pattern)
        def shuffle(s): return sample(s,len(s)) 
    
        rBase = range(base)
        rows  = [ g*base + r for g in shuffle(rBase) for r in shuffle(rBase) ] 
        cols  = [ g*base + c for g in shuffle(rBase) for c in shuffle(rBase) ]
        nums  = shuffle(range(1,base*base+1))
        # produce board using randomized baseline pattern
        self.board = [ [nums[pattern(r,c)] for c in cols] for r in rows ]
        self.removeNums(difficulty)
        self.insertedPositions = []
        Sudoku.sudoku_list.append(self)

    def __str__(self) -> str:
        return f"key: {self.key}"

    def removeNums(self, to_clear):
        # remove some numbers
        to_clear = clamp(to_clear, 25, 75)
        squares = self.side*self.side
        empties = squares * to_clear//100
        for p in sample(range(squares),empties):
            self.board[p//self.side][p%self.side] = 0
        

    def testprint(self):
        numSize = len(str(self.side))
        for line in self.board:
            print(*(f"{n or '.':{numSize}} " for n in line))

    def prettyPrint(self):
        symbol = " 1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        nums   = [ [""]+[symbol[n] for n in row] for row in self.board ]

        for inserted_num in self.insertedPositions:
            if (inserted_num is not None):

                    row = inserted_num[0] 
                    col = inserted_num[1]

                    new_num = str(inserted_num[2]).translate("".maketrans("0123456789", "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵"))
                    # new_num = ANSI.text_colour(text=new_num, color="cyan")
                    if (inserted_num == self.insertedPositions[-1]):
                        new_num = str(inserted_num[2]).translate("".maketrans("0123456789", "𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡"))
                        # new_num = ANSI.text_colour(text=new_num, color="yellow")
                    nums[row][col+1] = new_num

        # display pretty
        def expandLine(line):
            return line[0]+line[5:9].join([line[1:5]*(self.base-1)]*self.base)+line[9:13]
        line0  = expandLine("╔═══╤═══╦═══╗")
        line1  = expandLine("║ . │ . ║ . ║")
        line2  = expandLine("╟───┼───╫───╢")
        line3  = expandLine("╠═══╪═══╬═══╣")
        line4  = expandLine("╚═══╧═══╩═══╝")

        final_string=line0+"\n"
        for r in range(1,self.side+1):
            str1 = "".join(n+s for n,s in zip(nums[r-1],line1.split(".")))
            str2 = [line2,line3,line4][(r%self.side==0)+(r%self.base==0)]
            strr = "\n".join([str1,str2])
            final_string += strr+"\n"
        return final_string

    def inputNum(self, group, square, num):

        group = clamp(group,1,self.side)
        square = clamp(square,1,self.side)
        num = clamp(num,1,self.side)
        
        row_start = (group - 1) // self.base * self.base
        col_start = (group - 1) % self.base * self.base
        row = row_start + (square - 1) // self.base
        col = col_start + (square - 1) % self.base

        # Remember which fields are insered to display them differently
        self.insertedPositions.append([row,col,num])
        self.board[row][col] = num
        Sudoku.sudoku_list.append(self)

    def store(self):
        # Serialize the data
        serial_data = pickle.dumps(self)
        # Add an entry in the database
        if(update_on):
            updateSudoku(serial_sudoku=serial_data, sudoku_ID=self.key)

    @classmethod
    def addBoard(self, board):
        Sudoku.sudoku_list.append(board)
