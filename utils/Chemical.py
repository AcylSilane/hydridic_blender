"""
Definition for the Chemical class, acting as an interface between ASE and Blender
"""

import ase, ase.data, ase.io
import bpy


class Chemical(ase.Atoms):
    def __init__(self, atoms: ase.Atoms, context: bpy.context):
        # TODO: Add support for multi-image structures
        self.atoms = atoms
        self.__context = context
        self.name = self.get_chemical_formula()

        # Create a new working directory for the molecule
        self.collection_name = f"Chemical Structure: {self.name}"
        self.collection = bpy.data.collections.new(self.collection_name)
        context.scene.collection.children.link(self.collection)

    # ======
    # Public
    # ======

    @classmethod
    def from_file(cls, filepath: str, context: bpy.context):
        """
        Constructor for when we've got a filepath specified. Reads from disk.

        Args:
            filepath (str): Path to the file containing chemical data.
            context (bpy.context): Object containing blender's current context

        Notes:
            The filepath argument must be readable by ase in order for the chemical to be loaded.

        Returns:
            Chemical: A new instance of the Chemical class.
        """
        atoms = ase.io.read(filepath)

        # Center the atoms
        # TODO: Make centering optional
        if any(atoms.pbc):
            # System is periodic; don't need to center
            pass
        else:
            # System is nonperiodic; we should center it
            atoms.center(about=0)

        return cls(atoms, context)

    def add_structure_to_scene(self) -> None:
        """
        Adds the stored atoms object into the scene.
        """
        # TODO: This can be refactored into a dectorator that steps into a collection and leaves

        # Save a reference to the previous collection, and change to the new one
        # This way, any new objects we spawn wind up in the new collection. Keeps stuff neat and tidy.

        prev_collection = self.__context.view_layer.active_layer_collection
        molecule_layer_collection = self.__context.view_layer.layer_collection.children[-1]
        self.__context.view_layer.active_layer_collection = molecule_layer_collection

        self.__create_molecule_object()

        # And then, finally, return to the collection we started out in
        self.__context.view_layer.active_layer_collection = prev_collection

    # =======
    # Private
    # =======

    @property
    def __active_collection(self) -> bpy.types.Collection:
        """Finds the current active collection.

        Returns:
            bpy.types.Collection: The currently active collection.
        """
        return self.__context.view_layer.active_layer_collection.collection

    def __create_molecule_object(self) -> None:
        """
        This will create a molecule object from the atoms object stored in this class.
        """
        unique_symbols = set(self.atoms.get_chemical_symbols())
        for symbol in unique_symbols:
            # Create the mesh
            selected_atoms = self.atoms[self.atoms.symbols == symbol]
            homonuclear_mesh = self.__mesh_from_atoms(selected_atoms)

            # Add the mesh to the collection
            homonuclear_positions_name = f"PointCloud_{symbol}_{self.collection_name}"
            homonuclear_object = bpy.data.objects.new(homonuclear_positions_name, homonuclear_mesh)
            homonuclear_object.instance_type = "VERTS"
            self.__active_collection.objects.link(homonuclear_object)

            # Create and bind instances for the atomic type
            nurbs = self.__spawn_nurbs_from_atomic_symbol(symbol)
            nurbs.parent = homonuclear_object

    def __mesh_from_atoms(self, atoms: ase.Atoms, mesh_name: str = None) -> bpy.types.Mesh:
        """
        Creates a point cloud based on the atomic positions passed in.

        Args:
            atoms (ase.Atoms): An ASE Atoms object that will be used to generate the mesh.
            mesh_name (str, optional): Name that will be given to the mesh in Blender. Defaults to None.

        Returns:
            bpy.types.Mesh: A mesh representing the chemical species in the atoms object.
        """
        if mesh_name is None:
            mesh_name = f"Mesh_{self.collection_name}"

        verts = atoms.get_positions() + self.__context.scene.cursor.location
        edges = []  # TODO: Derive edges from atomic neighborlist
        faces = []

        mesh = bpy.data.meshes.new(mesh_name)
        mesh.from_pydata(verts, edges, faces)
        mesh.validate()
        mesh.update()

        return mesh

    def __spawn_nurbs_from_atomic_symbol(self, atom_type: str) -> bpy.types.Object:
        """Spawns a NURBs sphere at the cursor with radius proportional to the element's covalent radius.

        Args:
            atom_type (str): Chemical symbol (e.g. "Fe" for iron, "C" for carbon, etc.) representing the atom.

        Returns:
            bpy.types.Object: The NURBs sphere that was created.
        """
        # Look up the covalent radius
        atomic_number = ase.data.atomic_numbers[atom_type]
        covalent_radius = ase.data.covalent_radii[atomic_number]

        # Spawn the atom, set its name, and hide it from renders
        bpy.ops.surface.primitive_nurbs_surface_sphere_add(radius=covalent_radius,
                                                           location=self.__context.scene.cursor.location)
        bpy.context.active_object.name = f"instance_{atom_type}"
        bpy.context.active_object.hide_render = True
        bpy.context.active_object.hide_set(True)

        # Store a reference to the object we created
        current_object = bpy.context.active_object
        return current_object
