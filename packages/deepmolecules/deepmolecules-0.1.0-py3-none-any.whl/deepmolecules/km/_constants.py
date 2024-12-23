import numpy as np

__all__ = [
    "AROMATIC",
    "ATOMIC_NUMBER",
    "BOND_TYPE",
    "CHARGE",
    "CHIRALITY",
    "CONJUGATED",
    "F1",
    "F2",
    "HYBRID",
    "H_BONDS",
    "IN_RING",
    "NUM_BONDS",
    "STEREO",
    "F",
]

# Model parameters
F1 = 32  # feature dimensionality of atoms
F2 = 10  # feature dimensionality of bonds
F = F1 + F2


# Create dictionaries for the bond features:
BOND_TYPE = {
    "AROMATIC": np.array([0, 0, 0, 1], dtype=int),
    "DOUBLE": np.array([0, 0, 1, 0], dtype=int),
    "SINGLE": np.array([0, 1, 0, 0], dtype=int),
    "TRIPLE": np.array([1, 0, 0, 0], dtype=int),
}

CONJUGATED = {
    0.0: np.array([0], dtype=int),
    1.0: np.array([1], dtype=int),
}

IN_RING = {
    0.0: np.array([0], dtype=int),
    1.0: np.array([1], dtype=int),
}

STEREO = {
    "STEREOANY": np.array([0, 0, 0, 1], dtype=int),
    "STEREOE": np.array([0, 0, 1, 0], dtype=int),
    "STEREONONE": np.array([0, 1, 0, 0], dtype=int),
    "STEREOZ": np.array([1, 0, 0, 0], dtype=int),
}

##Create dictionaries, so the atom features can be easiliy converted into a numpy array

# all the atomic numbers with a total count of over 200 in the data set are getting their own one-hot-encoded
# vector. All the otheres are lumped to a single vector.
ATOMIC_NUMBER = {
    0.0: np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=int),
    1.0: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=int),
    3.0: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=int),
    4.0: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=int),
    5.0: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=int),
    6.0: np.array([0, 1, 0, 0, 0, 0, 0, 0, 0, 0], dtype=int),
    7.0: np.array([0, 0, 1, 0, 0, 0, 0, 0, 0, 0], dtype=int),
    8.0: np.array([0, 0, 0, 1, 0, 0, 0, 0, 0, 0], dtype=int),
    9.0: np.array([0, 0, 0, 0, 1, 0, 0, 0, 0, 0], dtype=int),
    11.0: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=int),
    12.0: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=int),
    13.0: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=int),
    14.0: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=int),
    15.0: np.array([0, 0, 0, 0, 0, 1, 0, 0, 0, 0], dtype=int),
    16.0: np.array([0, 0, 0, 0, 0, 0, 1, 0, 0, 0], dtype=int),
    17.0: np.array([0, 0, 0, 0, 0, 0, 0, 1, 0, 0], dtype=int),
    19.0: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=int),
    20.0: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=int),
    23.0: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=int),
    24.0: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=int),
    25.0: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=int),
    26.0: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=int),
    27.0: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=int),
    28.0: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=int),
    29.0: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=int),
    30.0: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=int),
    32.0: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=int),
    33.0: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=int),
    34.0: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=int),
    35.0: np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 0], dtype=int),
    37.0: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=int),
    38.0: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=int),
    42.0: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=int),
    46.0: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=int),
    47.0: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=int),
    48.0: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=int),
    50.0: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=int),
    51.0: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=int),
    52.0: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=int),
    53.0: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=int),
    54.0: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=int),
    56.0: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=int),
    57.0: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=int),
    74.0: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=int),
    78.0: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=int),
    79.0: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=int),
    80.0: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=int),
    81.0: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=int),
    82.0: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=int),
    83.0: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=int),
    86.0: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=int),
    88.0: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=int),
    90.0: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=int),
    94.0: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], dtype=int),
}

# There are only 5 atoms in the whole data set with 6 bonds and no atoms with 5 bonds. Therefore I lump 4, 5 and 6 bonds
# together
NUM_BONDS = {
    0.0: np.array([0, 0, 0, 0, 1], dtype=int),
    1.0: np.array([0, 0, 0, 1, 0], dtype=int),
    2.0: np.array([0, 0, 1, 0, 0], dtype=int),
    3.0: np.array([0, 1, 0, 0, 0], dtype=int),
    4.0: np.array([1, 0, 0, 0, 0], dtype=int),
    5.0: np.array([1, 0, 0, 0, 0], dtype=int),
    6.0: np.array([1, 0, 0, 0, 0], dtype=int),
}

# Almost alle charges are -1,0 or 1. Therefore I use only positiv, negative and neutral as features:
CHARGE = {
    -4.0: np.array([1, 0, 0], dtype=int),
    -3.0: np.array([1, 0, 0], dtype=int),
    -2.0: np.array([1, 0, 0], dtype=int),
    -1.0: np.array([1, 0, 0], dtype=int),
    0.0: np.array([0, 1, 0], dtype=int),
    1.0: np.array([0, 0, 1], dtype=int),
    2.0: np.array([0, 0, 1], dtype=int),
    3.0: np.array([0, 0, 1], dtype=int),
    4.0: np.array([0, 0, 1], dtype=int),
    5.0: np.array([0, 0, 1], dtype=int),
    6.0: np.array([0, 0, 1], dtype=int),
}

HYBRID = {
    "S": np.array([0, 0, 0, 0, 1], dtype=int),
    "SP": np.array([0, 0, 0, 1, 0], dtype=int),
    "SP2": np.array([0, 0, 1, 0, 0], dtype=int),
    "SP3": np.array([0, 1, 0, 0, 0], dtype=int),
    "SP3D": np.array([1, 0, 0, 0, 0], dtype=int),
    "SP3D2": np.array([1, 0, 0, 0, 0], dtype=int),
    "UNSPECIFIED": np.array([1, 0, 0, 0, 0], dtype=int),
}

AROMATIC = {
    0.0: np.array([0], dtype=int),
    1.0: np.array([1], dtype=int),
}

H_BONDS = {
    0.0: np.array([0, 0, 0, 1], dtype=int),
    1.0: np.array([0, 0, 1, 0], dtype=int),
    2.0: np.array([0, 1, 0, 0], dtype=int),
    3.0: np.array([1, 0, 0, 0], dtype=int),
    4.0: np.array([1, 0, 0, 0], dtype=int),
    5.0: np.array([1, 0, 0, 0], dtype=int),
    6.0: np.array([1, 0, 0, 0], dtype=int),
}

CHIRALITY = {
    "CHI_TETRAHEDRAL_CCW": np.array([1, 0, 0], dtype=int),
    "CHI_TETRAHEDRAL_CW": np.array([0, 1, 0], dtype=int),
    "CHI_UNSPECIFIED": np.array([0, 0, 1], dtype=int),
}
