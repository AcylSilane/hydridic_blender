"""
Helper functions to aid in reading/writing chemical data
"""

from typing import Dict
import re

import ase, ase.data, ase.io
import bpy


def get_atoms(filepath: str) -> ase.Atoms:
    # Read whatever file the atoms are stored in
    atoms = ase.io.read(filepath)

    # Center the atoms
    # TODO: Make centering optional
    if any(atoms.pbc):
        # System is periodic; don't need to center
        pass
    else:
        # System is nonperiodic; we should center it
        atoms.center(about=0)

    return atoms


def add_structure(atoms: ase.Atoms, context: bpy.context):
    """
    Given an ASE atoms object, will add the structure to blender.
    """

    # Create a collection to hold the structure
    # TODO: Add support for multi-image structures
    collection_name = "New Chemical Structure"
    molecule_collection = bpy.data.collections.new(collection_name)
    context.scene.collection.children.link(molecule_collection)

    # Save a reference to the previous collection, and change to the new one
    # This way, any new objects we spawn wind up in the new collection. Keeps stuff neat and tidy.
    prev_collection = context.view_layer.active_layer_collection
    molecule_layer_collection = context.view_layer.layer_collection.children[-1]
    context.view_layer.active_layer_collection = molecule_layer_collection

    # Create a mesh to hold atomic positions. Keep a reference around for the object.
    mesh = point_cloud_from_atoms(collection_name, atoms, context=context)
    molecule_object_name = f"Molecule_{collection_name}"
    molecule_collection.objects.link(bpy.data.objects.new(molecule_object_name, mesh))
    molecule_object = molecule_collection.objects[molecule_object_name]

    # Create a new collection to hold the atoms
    atoms_collection_name = "atom_instances"
    atoms_collection = bpy.data.collections.new(atoms_collection_name)
    molecule_collection.children.link(atoms_collection)
    atoms_layer_collection = molecule_layer_collection.children[-1]
    context.view_layer.active_layer_collection = atoms_layer_collection

    # Determine which atoms are in the system, and create their base instances.
    atom_instances = {}
    for atom_type in set(atoms.get_chemical_symbols()):
        atom_ref = create_atom_instance(atom_type, context)
        atom_instances[atom_type] = atom_ref

    # Create a particle system in the molecule object to hold the instances
    context.view_layer.active_layer_collection = molecule_layer_collection
    particle_system = create_particle_system(molecule_object, atoms_collection, atoms)
    sort_atoms_in_particle_system(particle_system, atoms)

    context.view_layer.active_layer_collection = prev_collection


def point_cloud_from_atoms(
    collection_name: str, atoms: ase.Atoms, context: bpy.context
) -> bpy.types.Mesh:
    """
    Creates a point cloud based on the atomic positions
    """

    mesh = bpy.data.meshes.new(f"Mesh_{collection_name}")
    verts = atoms.get_positions() + context.scene.cursor.location
    # TODO: Derive edges from atomic neighborlist
    edges = []
    faces = []

    mesh.from_pydata(verts, edges, faces)
    mesh.validate()
    mesh.update()

    return mesh


def create_atom_instance(atom_type: str, context: bpy.context) -> bpy.types.Object:
    """
    Spawns NURBs spheres to be instanced later on in the atomic coordinates
    """
    # Look up the covalent radius
    atomic_number = ase.data.atomic_numbers[atom_type]
    covalent_radius = ase.data.covalent_radii[atomic_number]

    # Spawn the atom, set its name, and hide it from renders
    # We're going to put it into a particle system later, so we don't
    # want to actually draw it.
    bpy.ops.surface.primitive_nurbs_surface_sphere_add(
        radius=covalent_radius, location=context.scene.cursor.location
    )
    bpy.context.active_object.name = f"instance_{atom_type}"
    bpy.context.active_object.hide_render = True
    bpy.context.active_object.hide_set(True)

    # Store a reference to the object we created
    current_object = bpy.context.active_object
    return current_object


def create_particle_system(
    molecule_object: bpy.types.Object,
    atoms_collection: bpy.types.Collection,
    atoms: ase.Atoms,
) -> bpy.types.ParticleSystem:
    """
    Creates a particle system in the point cloud for the molecule, and assigns
    atom types to each point.
    """
    # Create the particle system
    bpy.context.view_layer.objects.active = molecule_object
    molecule_object.modifiers.new("Molecule Particle System", type="PARTICLE_SYSTEM")
    particle_system = molecule_object.particle_systems[-1]

    # Set one atom per vert
    settings = particle_system.settings
    settings.type = "HAIR"
    settings.count = len(atoms)
    settings.emit_from = "VERT"
    settings.use_emit_random = False

    # Set the system to instance the collection
    settings.render_type = "COLLECTION"
    settings.hair_length = 1
    settings.particle_size = 1
    settings.instance_collection = atoms_collection
    settings.use_collection_count = True

    return particle_system

def sort_atoms_in_particle_system(particle_system: bpy.types.ParticleSystem, atoms: ase.Atoms):
    """
    Because we've set the collection of atom instances to be what's rendered in the particle system,
    we start out with a list of atoms in the instance weights of the particle system. Seemingly, they're
    in a random order.

    Constraints:
        - We can move the currently-selected index around as much as we'd like.
        - Instance members can be copied, and appear at the start of the list.
        - Copying an instance sets the currently-selected index to be the start of the list.
        - We always start with 1 (and only 1) of each atom.
    """
    
    # Figure out which index things are located in
    settings = particle_system.settings
    particle_locs = {}
    for index, name in enumerate(reversed(settings.instance_weights.keys()), 1):
        symbol = re.search("(?<=_)[A-z]+(?=:?)", name)[0]
        particle_locs[symbol] = -index

    print(particle_locs)

    for atom in atoms:
        index = particle_locs[atom.symbol]
        to_clone = particle_system.settings.instance_weights.keys()[index]

        settings.active_instanceweight_index = index
        print(settings.active_instanceweight_index)
        bpy.ops.particle.dupliob_move_up()
        bpy.ops.particle.dupliob_copy()
    bpy.ops.particle.dupliob_refresh()