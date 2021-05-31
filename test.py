
import ase.io

to_read = "test/assets/ethanol.xyz"
atoms = ase.io.read(to_read)

initial_positions = {'H': 'instance_H', 'C': 'instance_C', 'O': 'instance_O'}
end_indexes = {'O': -1, 'C': -2, 'H': -3}

positions =["H", "C", "O"]

for atom in atoms:
    index = end_indexes[atom.symbol] % 3
    print(f"Clone {atom.symbol} at {index}, is really a {positions[index]}")
    assert atom.symbol == positions[index]
    positions.append(positions[index%3])
for i in range(1,4):
    print(f"Delete {-i}")
positions = positions[3:]
    

print(list(reversed(positions)))
