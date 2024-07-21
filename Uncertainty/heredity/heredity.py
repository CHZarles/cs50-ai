import csv
import itertools
import sys

PROBS = {
    # Unconditional probabilities for having gene
    "gene": {2: 0.01, 1: 0.03, 0: 0.96},
    "trait": {
        # Probability of trait given two copies of gene
        2: {True: 0.65, False: 0.35},
        # Probability of trait given one copy of gene
        1: {True: 0.56, False: 0.44},
        # Probability of trait given no gene
        0: {True: 0.01, False: 0.99},
    },
    # Mutation probability
    "mutation": 0.01,
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])
    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {"gene": {2: 0, 1: 0, 0: 0}, "trait": {True: 0, False: 0}}
        for person in people
    }

    # print(
    #     joint_probability(
    #         {
    #             "Harry": {
    #                 "name": "Harry",
    #                 "mother": "Lily",
    #                 "father": "James",
    #                 "trait": None,
    #             },
    #             "James": {
    #                 "name": "James",
    #                 "mother": None,
    #                 "father": None,
    #                 "trait": True,
    #             },
    #             "Lily": {
    #                 "name": "Lily",
    #                 "mother": None,
    #                 "father": None,
    #                 "trait": False,
    #             },
    #         },
    #         {"Harry"},
    #         {"James"},
    #         {"James"},
    #     )
    # )
    # exit()
    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (
                people[person]["trait"] is not None
                and people[person]["trait"] != (person in have_trait)
            )
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (
                    True
                    if row["trait"] == "1"
                    else False if row["trait"] == "0" else None
                ),
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s)
        for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


# a helper function
def calc_gene_pass_probability(father: int, mother: int, child: int) -> float:
    """
    Calculate the probability of a child inheriting a certain number of genes from their parents.

    Parameters:
    father (int): The number of genes the father has.
    mother (int): The number of genes the mother has.
    child (int): The number of genes the child has.

    Returns:
    float: The probability of the child inheriting the specified number of genes from their parents.

    """
    # pass_gene_prob[k] = v
    # means if one person have k gene, the probability of pass gene to child is v
    pass_gene_prob = {
        0: PROBS["mutation"],
        1: 0.5 * (1 - PROBS["mutation"]) + 0.5 * PROBS["mutation"],
        2: 1 - PROBS["mutation"],
    }
    father_pass_one = pass_gene_prob[father]
    mother_pass_one = pass_gene_prob[mother]
    # the probability of child have 0,1,2 gene
    prob_of_pass = [
        # child no gene
        (1 - father_pass_one) * (1 - mother_pass_one),
        # child has 1 gene
        father_pass_one * (1 - mother_pass_one)
        + mother_pass_one * (1 - father_pass_one),
        # child has 2 gene
        father_pass_one * mother_pass_one,
    ]

    return prob_of_pass[child]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    # record joint condition for each person
    conditions = {
        person: {
            "gene": 1 if person in one_gene else 2 if person in two_genes else 0,
            "trait": person in have_trait,
        }
        for person in people
    }
    # calc for each person
    result = 1.0
    for person in set(people):
        # probability of this person
        prob = 1.0
        person_gene_num = conditions[person]["gene"]
        # gene part
        if people[person]["father"] == None and people[person]["mother"] == None:
            prob = PROBS["gene"][person_gene_num]
        else:
            # get parents' gene
            father_gene_num = conditions[people[person]["father"]]["gene"]
            mother_gene_num = conditions[people[person]["mother"]]["gene"]
            # get gene pass probability
            prob = calc_gene_pass_probability(
                father_gene_num, mother_gene_num, person_gene_num
            )
        # trait part
        if conditions[person]["trait"]:
            prob *= PROBS["trait"][person_gene_num][True]
        else:
            prob *= PROBS["trait"][person_gene_num][False]

        result *= prob

    return result


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in one_gene:
        probabilities[person]["gene"][1] += p
    for person in two_genes:
        probabilities[person]["gene"][2] += p
    for person in have_trait:
        probabilities[person]["trait"][True] += p
    no_gene = set(probabilities) - one_gene - two_genes
    no_trait = set(probabilities) - have_trait
    for person in no_gene:
        probabilities[person]["gene"][0] += p
    for person in no_trait:
        probabilities[person]["trait"][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    # print(probabilities)
    for person in probabilities:
        # normalize the trait probability
        trait_sum = sum(probabilities[person]["trait"].values())
        for trait in probabilities[person]["trait"]:
            if trait_sum == 0:
                break
            probabilities[person]["trait"][trait] /= trait_sum

        # normalize the gene probability
        gene_sum = sum(probabilities[person]["gene"].values())
        for gene in probabilities[person]["gene"]:
            if gene_sum == 0:
                break
            probabilities[person]["gene"][gene] /= gene_sum


if __name__ == "__main__":
    main()
