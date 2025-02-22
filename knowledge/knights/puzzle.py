from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
Asentence0 = And(AKnight, AKnave)
knowledge0 = And(
    # TODO
    Implication(AKnight , Asentence0),
    # Implication(AKnave, Not(Asentence)), # how about remove this 
    Biconditional(AKnight , Not(AKnave)) 
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
Asentence1 = And(AKnave , BKnave)
knowledge1 = And(
    # TODO
    Biconditional(AKnight , Not(AKnave)) ,
    Biconditional(BKnight , Not(BKnave)) ,
    Biconditional(AKnight , Asentence1),
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
Asentence2 = Or(And(AKnave , BKnave) , And(AKnight ,BKnight))
Bsentence2 = Or(And(AKnight , BKnave) , And(AKnave ,BKnight))
knowledge2 = And(
    # TODO
    Biconditional(AKnight , Not(AKnave)) ,
    Biconditional(BKnight , Not(BKnave)) ,
    Biconditional(AKnight , Asentence2),
    Biconditional(BKnight , Bsentence2),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which. 
# B says "A said 'I am a knave'." 
# B says "C is a knave."
# C says "A is a knight."

knowledge3 = And( # dont't know
    Biconditional(BKnight , Not(BKnave)) ,
    Biconditional(CKnight , Not(CKnave)) ,
    Biconditional(AKnight , Not(AKnave)) ,

    # TODO
    Or(
    And(AKnight, # A said I am a knight
    Biconditional(BKnight , AKnave),
    Biconditional(BKnight , CKnave),
    Biconditional(CKnight , AKnight)) ,
    And(AKnave, 
    Biconditional(AKnave, Not(AKnave)),
    Biconditional(BKnight , AKnave),
    Biconditional(BKnight , CKnave),
    Biconditional(CKnight , AKnight)) 
    )
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3),
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
