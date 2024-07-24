from minesweeper import *
import sys

ai = MinesweeperAI(height=3, width=3)

sen1 = ai.add_knowledge((0,0), 1)
sen2 = ai.add_knowledge((0,1), 1)
sen3 = ai.add_knowledge((0,2), 1)
sen4 = ai.add_knowledge((2,1), 2)

print(f"mines: {ai.mines}")
print(f"safes {ai.safes}")

for sen in ai.knowledge:
    print(sen)