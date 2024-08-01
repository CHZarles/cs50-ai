import sys

import nltk

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

# 定义以下非终结符
NONTERMINALS = """
S -> NP VP | NP VP PP| S Conj S
Adjp -> Adj | Adj Adjp
NP -> N | Det N | Det Adjp N | NP Conj NP | NP P NP
PP -> P NP | P NP PP
VP -> V | Adv VP | VP NP | VP PP | VP NP PP | VP Conj VP | VP P VP | VP Adv
""" 

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    word_list = nltk.word_tokenize(sentence.lower())
    # filt out words that do not contain at least one alphabetic character
    word_list = [word for word in word_list if any(char.isalpha() for char in word)]
    return word_list


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """

    res = []
    # define a function check whether the node have np child 
    def Func(node):
        # iterate over all the child node
        Flag = False

        if isinstance(node, nltk.Tree):
            for child in node:
                # if the child node have np child, return True
                if Func(child):
                    Flag = True

        # add to res
        if not Flag:
            if isinstance(node, nltk.Tree) and node.label() == "NP":
                res.append(node)
            
        return Flag


    Func(tree)

    return res



if __name__ == "__main__":
    main()
