"""
Tests functionality related to bonds
"""
import sys
import typing

import pytest
import mock

from fixtures import molecule_ethanol, molecule_ethanol_bonds
import config

sys.path.append(config.project_root)

from utils.bond import BondBag


@pytest.fixture()
def mock_chemical(molecule_ethanol):
    yield mock.Mock(atoms=molecule_ethanol)


@pytest.fixture()
def bond_bag(mock_chemical):
    yield BondBag(mock_chemical)


def test_bondbag_caches_bondlist(bond_bag):
    assert bond_bag._has_calculated_bonds is False and bond_bag._bonds == []
    throwaway = bond_bag.bonds
    assert bond_bag._has_calculated_bonds is True and len(bond_bag._bonds) > 0


def test_bondbag_calculates_adjacency(bond_bag, molecule_ethanol_bonds):
    calculated_bonds = bond_bag.adjacency_matrix
    difference = calculated_bonds - molecule_ethanol_bonds
    # If subtracting the matrices from one-another leads to all 0's, they must be the same
    assert difference.nnz == 0


def test_bondbag_len(bond_bag, molecule_ethanol_bonds):
    assert len(bond_bag) == molecule_ethanol_bonds.nnz
