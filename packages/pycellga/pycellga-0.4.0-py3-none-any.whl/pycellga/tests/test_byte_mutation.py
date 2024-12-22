import pytest
import numpy as np

from pycellga.individual import Individual
from pycellga.common import GeneType
from pycellga.problems.abstract_problem import AbstractProblem
from pycellga.mutation.byte_mutation import ByteMutation 


class MockProblem(AbstractProblem):
    """
    A mock problem class for testing purposes.
    """
    def __init__(self, n_var):

        super().__init__(
            gen_type=GeneType.BINARY,
            n_var=n_var,
            xl=0, 
            xu=1
        )

    def f(self, x: list) -> float:
        """
        A mock fitness function that simply sums the chromosome values.

        Parameters
        ----------
        x : list
            A list of float variables.

        Returns
        -------
        float
            The sum of the list values.
        """
        return sum(x)

@pytest.fixture
def setup_individual():
    """
    Fixture for creating a sample Individual instance.

    Returns
    -------
    Individual
        An individual instance with a predefined chromosome and size.
    """
    ind = Individual(GeneType.REAL, 5)
    ind.chromosome = [1.0, 2.0, 3.0, 4.0, 5.0]
    ind.ch_size = 5
    return ind

@pytest.fixture
def setup_problem():
    """
    Fixture for creating a mock problem instance.

    Returns
    -------
    MockProblem
        An instance of the mock problem.
    """
    return MockProblem(n_var=5)

def test_byte_mutation(setup_individual, setup_problem):
    """
    Test the ByteMutation function implementation.

    This test checks the byte-wise mutation on an individual's chromosome by verifying the mutation
    operation and the integrity of the chromosome.

    Parameters
    ----------
    setup_individual : fixture
        The fixture providing the sample individual.
    setup_problem : fixture
        The fixture providing the mock problem instance.
    """
    # Set seed for reproducibility
    np.random.seed(0)

    # Perform the mutation
    mut = ByteMutation(setup_individual, setup_problem)
    new_individual = mut.mutate()

    # Log the chromosomes for debugging
    print("Original chromosome:", setup_individual.chromosome)
    print("Mutated chromosome:", new_individual.chromosome)

    # Assertions to check correctness
    assert isinstance(new_individual, Individual)
    assert len(new_individual.chromosome) == setup_individual.ch_size
    assert new_individual.chromosome != setup_individual.chromosome  # Ensure mutation has occurred

    # Additional checks to verify the mutation logic
    original_ch = setup_individual.chromosome
    mutated_ch = new_individual.chromosome

    # Ensure only one value in the chromosome has been mutated
    differences = [i for i in range(len(original_ch)) if original_ch[i] != mutated_ch[i]]
    assert len(differences) == 1

    # Check that the mutated value is a float
    mutated_value = mutated_ch[differences[0]]
    assert isinstance(mutated_value, float)

if __name__ == "__main__":
    pytest.main()
