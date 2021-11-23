from typing import List
from abc import ABC, abstractmethod
import ase.data

class BondStyle(ABC):
    def __init__(self) -> None:
        super().__init__()
    
    @abstractmethod
    def spawn_bond_from_atoms(self, atom_start: ase.Atom, atom_end: ase.Atom, offset: List[float]) -> BondStyle:
        return self
    
class ConicBond(BondStyle):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
    def spawn_bond_from_atoms(self, atom_start: ase.Atom, atom_end: ase.Atom, offset: List[float]) -> BondStyle:
        start_radius = ase.data.covalent_radii[atom_start.number]
        end_radius = ase.data.covalent_radii[atom_start.number]
        raise NotImplementedError()