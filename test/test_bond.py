"""
Tests functionality related to bonds
"""
import sys
import typing
if typing.TYPE_CHECKING:
    import scipy.sparse

import pytest
import mock

from fixtures import molecule_ethanol, molecule_ethanol_bonds
import config
sys.path.append(config.project_root)

from utils.bond import BondBag

def test_bondbag_caches_bondlist(molecule_ethanol):
    chemical = mock.Mock(atoms=molecule_ethanol)
    bag = BondBag(chemical)

    assert bag._has_calculated_bonds is False and bag._bonds == []
    throwaway = bag.bonds
    assert bag._has_calculated_bonds is True and len(bag._bonds) > 0

def test_bondbag_calculates_adjacency(molecule_ethanol, molecule_ethanol_bonds):
    chemical = mock.Mock(atoms=molecule_ethanol)
    bag = BondBag(chemical)

    calculated_bonds = bag.adjacency_matrix
    difference = calculated_bonds - molecule_ethanol_bonds
    # If subtracting the matrices from one-another leads to all 0's, they must be the same
    assert difference.nnz == 0

def test_bondbag_len(molecule_ethanol, molecule_ethanol_bonds):
    chemical = mock.Mock(atoms=molecule_ethanol)
    bag = BondBag(chemical)

    assert len(bag) == molecule_ethanol_bonds.nnz

