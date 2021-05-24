"""
Helper functions to aid in reading/writing chemical data
"""

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
    collection = bpy.data.collections.new(collection_name)
    context.scene.collection.children.link(collection)

    # Save a reference to the previous collection, and change to the new one
    # This way, any new objects we spawn wind up in the new collection. Keeps stuff neat and tidy.
    previous_collection = context.view_layer.active_layer_collection
    context.view_layer.active_layer_collection = (
        context.view_layer.layer_collection.children[-1]
    )

    # Create a mesh to hold atomic positions
    mesh = point_cloud_from_atoms(collection_name, atoms, context=context)
    collection.objects.link(bpy.data.objects.new(f"Mesh_{collection_name}", mesh))

    # Determine which atoms are in the system, and create their instances
    for atom_type in set(atoms.get_chemical_symbols()):
        create_atom_instance(atom_type, context)

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

def create_atom_instance(atom_type, context):
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

    