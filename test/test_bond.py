"""
Tests functionality related to bonds
"""
import sys

import pytest
import mock

from fixtures import molecule_ethanol
import config
sys.path.append(config.project_root)

from utils.bond import BondBag

def test_bondbag_caches_bondlist(molecule_ethanol):
    chemical = mock.Mock(atoms=molecule_ethanol)

    bag = BondBag(chemical)
    assert bag._has_calculated_bonds is False and bag._bonds == []
    throwaway = bag.bonds
    assert bag._has_calculated_bonds is True and len(bag._bonds) > 0

