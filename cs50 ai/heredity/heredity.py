import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
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
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.
    """

    joint_prob = 1.0

    # Determine the probability of receiving a gene from a parent
    def prob_from_parent(parent, child_gene_count):
        if parent in two_genes:
            return 1 - PROBS["mutation"] if child_gene_count > 0 else PROBS["mutation"]
        elif parent in one_gene:
            return 0.5  # 50% chance regardless of child's gene count
        else:
            return PROBS["mutation"] if child_gene_count > 0 else 1 - PROBS["mutation"]

    for person in people:
        mother = people[person]['mother']
        father = people[person]['father']

        if person in two_genes:
            genes = 2
        elif person in one_gene:
            genes = 1
        else:
            genes = 0

        trait = person in have_trait

        if mother and father:  # If the person has parents
            if genes == 2:
                joint_prob *= prob_from_parent(mother, 1) * prob_from_parent(father, 1)
            elif genes == 1:
                joint_prob *= prob_from_parent(mother, 1) * prob_from_parent(father, 0) + \
                             prob_from_parent(mother, 0) * prob_from_parent(father, 1)
            else:
                joint_prob *= prob_from_parent(mother, 0) * prob_from_parent(father, 0)
        else:  # If person doesn't have parents, directly use the gene probabilities
            joint_prob *= PROBS["gene"][genes]

        # Factor in the probability of having/not having a trait based on genes
        joint_prob *= PROBS["trait"][genes][trait]

    return joint_prob


# checks if someone has parents in the database
def parents(people, person):
    if people[person]['father'] is None and people[person]['mother'] is None:
        return False
    else:
        return True


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """

    # Loop over every person in probabilities
    for person in probabilities:

        # Update gene probabilities
        if person in one_gene:
            probabilities[person]['gene'][1] += p
        elif person in two_genes:
            probabilities[person]['gene'][2] += p
        else:   # If person is not in one_gene or two_genes, they have zero genes
            probabilities[person]['gene'][0] += p

        # Update trait probabilities
        if person in have_trait:
            probabilities[person]['trait'][True] += p
        else:   # If person does not have the trait
            probabilities[person]['trait'][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    # loop through each person
    for person in probabilities:
        # normalize the genes
        sum = probabilities[person]['gene'][0] + probabilities[person]['gene'][1] + probabilities[person]['gene'][2]

        probabilities[person]['gene'][0] = probabilities[person]['gene'][0]/sum
        probabilities[person]['gene'][1] = probabilities[person]['gene'][1]/sum
        probabilities[person]['gene'][2] = probabilities[person]['gene'][2]/sum

        # normalize the trait
        trait_sum = probabilities[person]['trait'][True] + probabilities[person]['trait'][False]

        probabilities[person]['trait'][True] = probabilities[person]['trait'][True]/trait_sum
        probabilities[person]['trait'][False] = probabilities[person]['trait'][False]/trait_sum


if __name__ == "__main__":
    main()
