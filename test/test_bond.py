"""
Tests functionality related to bonds
"""
import sys
import typing
import copy
import pytest
import mock

from fixtures import mock_chemical, mock_atom, molecule_ethanol_bonds, molecule_ethanol
from fixtures import mock_bondstyle
import config

sys.path.append(config.project_root)

from utils.bond import BondBag, Bond
from utils.bond_styles import BondStyle


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


def test_default_bondbag_style(mock_chemical, mock_bondstyle):
    bag = BondBag(chemical=mock_chemical,
                  bond_style=mock_bondstyle())
    assert isinstance(bag.bond_style, mock.Mock)


def test_bondbag_sets_style_of_bonds(bond_bag):
    throwaway = bond_bag.bonds
    original_style = bond_bag.bond_style
    new_style = copy.copy(original_style)

    for bond in bond_bag:
        assert bond.bond_style is original_style

    bond_bag.bond_style = new_style
    for bond in bond_bag:
        assert bond.bond_style is not original_style
        assert bond.bond_style is new_style


def test_bondbag_len(bond_bag, molecule_ethanol_bonds):
    assert len(bond_bag) == molecule_ethanol_bonds.nnz


def test_bond_calls_spawn_from_atoms(mock_bondstyle):
    bond = Bond(source_atom=mock_atom,
                destination_atom=mock_atom,
                bond_style=mock_bondstyle)
    bond.draw()
    assert mock_bondstyle.spawn_bond_from_atoms.called
