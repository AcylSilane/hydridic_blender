"""
Re-usable text fixtures
"""
import os

import mock
import pytest
import ase.io
import ase.neighborlist

from config import fixtures_root


@pytest.fixture()
def protein_1l2y():
    """This fixture is the Trp-Cage protein, the (at time of writing) smallest protein, and is found in the
    saliva of gila monsters.
    Useful for stress-testing organic systems as it has about 300 atoms.
    Ref: https://www.rcsb.org/structure/1L2Y"""
    return ase.io.read(os.path.join(fixtures_root, "1l2y.pdb"))


@pytest.fixture()
def superconductor_123():
    """This fixture is the crystal cell of YBa2Cu3O7, a superconductor.
    Useful for testing periodic inorganic systems.
    Ref: https://materialsproject.org/materials/mp-20674/"""
    return ase.io.read(os.path.join(fixtures_root, "Ba2YCu3O7_mp-20674_conventional_standard.cif"))


@pytest.fixture()
def molecule_ethanol():
    """This fixture is ethanol, a solvent with great industrial and cultural significance.
    Useful for testing behavior with small nonperiodic molecular system.
    Ref: (Made this by hand in Avogadro)"""
    return ase.io.read(os.path.join(fixtures_root, "ethanol.xyz"))


@pytest.fixture()
def molecule_ethanol_bonds(molecule_ethanol):
    neighborlist = ase.neighborlist.NeighborList(
        cutoffs=ase.neighborlist.natural_cutoffs(molecule_ethanol),
        self_interaction=False,
        primitive=ase.neighborlist.NewPrimitiveNeighborList
    )
    neighborlist.update(molecule_ethanol)
    return neighborlist.get_connectivity_matrix(sparse=True)


@pytest.fixture()
def mof_nmgc():
    """This fixture is a MOF obtained from the NMGC database.
    Useful for testing periodic systems with both organic and inorganic components.
    Ref: http://nmgc.umn.edu/software/"""
    return ase.io.read(os.path.join(fixtures_root, "NMGC-530221.cif"))

@pytest.fixture()
def mock_chemical(molecule_ethanol):
    yield mock.Mock(atoms=molecule_ethanol)

@pytest.fixture()
def mock_atom():
    yield mock.create_autospec(ase.Atom)

@pytest.fixture()
def mock_bond(mock_atoms):
    mock_bond = mock.Mock()
    mock.source_atom = mock_atoms
    mock.destination_atom = mock_atoms
    mock.bond_style = mock_bondstyle

@pytest.fixture()
def mock_bondstyle():
    yield mock.Mock()