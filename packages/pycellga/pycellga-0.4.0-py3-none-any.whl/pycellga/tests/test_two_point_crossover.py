import numpy as np

from pycellga.problems.single_objective.discrete.binary.one_max import OneMax
from pycellga.recombination.two_point_crossover import TwoPointCrossover
from pycellga.individual import Individual
from pycellga.common import GeneType

def test_two_point_crossover():
    """
    Test the TwoPointCrossover class implementation.

    This test verifies the functionality of the TwoPointCrossover class for binary chromosomes.
    It ensures that the crossover operation produces valid offspring with the expected chromosome size.

    The test performs the following checks:
    1. Both offspring have the same chromosome size as the parents.
    2. The chromosomes of the offspring contain only valid binary values (0 or 1).

    Raises
    ------
    AssertionError
        If any of the conditions for the crossover operation are not met.
    """
    CHSIZE = 10

    # Create two parent individuals with binary chromosomes of the specified size
    indv1 = Individual(gen_type=GeneType.BINARY, ch_size=CHSIZE)
    indv2 = Individual(gen_type=GeneType.BINARY, ch_size=CHSIZE)

    # Randomly initialize the chromosomes of the parents
    indv1.randomize()
    indv2.randomize()

    parents = [indv1, indv2]

    # Initialize the TwoPointCrossover with the parent individuals and problem
    theproblem = OneMax()
    ucx = TwoPointCrossover(parents, theproblem)

    # Perform the crossover to get two offspring
    child1, child2 = ucx.get_recombinations()

    # Check that the chromosome size of both offspring matches the parents
    assert child1.ch_size == child2.ch_size, "Offspring chromosome sizes do not match."
    assert child1.ch_size == CHSIZE, "Offspring chromosome size does not match expected size."

    # Verify that the chromosomes of the offspring contain only binary values
    for i in range(CHSIZE):
        assert child1.chromosome[i] in [0, 1], f"Invalid value in child1 chromosome at index {i}."
    
    for i in range(CHSIZE):
        assert child2.chromosome[i] in [0, 1], f"Invalid value in child2 chromosome at index {i}."

if __name__ == "__main__":
    test_two_point_crossover()
