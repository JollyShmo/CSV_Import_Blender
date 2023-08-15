import bpy
import csv
import bmesh
from bpy_extras.io_utils import ImportHelper
from mathutils import Matrix

bl_info = {
    "name": "CSV Mesh Importer",
    "author": "Jolly Joe",
    "version": (2, 0),
    "blender": (3, 5, 0),
    "location": "File > Import",
    "description": "Import points from a CSV file and create a mesh with connected edges or faces.",
    "category": "Import-Export",
}

class CSVMeshImporterOperator(bpy.types.Operator, ImportHelper):
    bl_idname = "import_mesh.csv"
    bl_label = "Import CSV Mesh"
    bl_description = "Import points from a CSV file and create a mesh with connected edges or faces"

    filter_glob: bpy.props.StringProperty(
        default="*.csv",
        options={'HIDDEN'},
        maxlen=255,
    )
    
    scale_factor: bpy.props.FloatProperty(
        name="Scale Factor",
        default=1.0,
        description="Scale the imported mesh",
    )
    
    connection_method: bpy.props.EnumProperty(
        name="Connection Method",
        items=[
            ('EDGES', "Edges", "Connect vertices with edges"),
            ('FACES', "Faces", "Connect vertices with faces"),
        ],
        default='EDGES',
        description="Method for connecting vertices"
    )

    def execute(self, context):
        try:
            with open(self.filepath, 'r', newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                next(reader)  # Skip the header line
                vertices = []
                for row in reader:
                    if len(row) >= 7:  # Make sure the row has at least 7 values (POSITION 0, POSITION 1, POSITION 2, SV_Position.w)
                        x, y, z, w = map(float, row[2:6])  # Assuming POSITION 0, POSITION 1, POSITION 2, SV_Position.w columns
                        vertices.append((x * self.scale_factor, y * self.scale_factor, z * self.scale_factor))

                # Create a new mesh
                mesh = bpy.data.meshes.new("CSV_Mesh")

                # Create a new BMesh
                bm = bmesh.new()

                # Add vertices to the BMesh
                for vertex in vertices:
                    bm.verts.new(vertex)

                # Connect the vertices based on the selected connection method
                bm.verts.ensure_lookup_table()
                if self.connection_method == 'EDGES':
                    for i in range(len(vertices) - 1):
                        bm.edges.new((bm.verts[i], bm.verts[i + 1]))
                elif self.connection_method == 'FACES':
                    if len(vertices) >= 3:
                        # Triangulate faces around the points
                        for i in range(len(vertices) - 2):
                            bm.faces.new((bm.verts[i], bm.verts[i + 1], bm.verts[i + 2]))

                # Update the BMesh and populate the mesh with BMesh data
                bm.to_mesh(mesh)
                bm.free()

                # Create a new object from the mesh
                obj = bpy.data.objects.new("CSV_Object", mesh)
                context.collection.objects.link(obj)

                # Select the newly created object
                bpy.context.view_layer.objects.active = obj
                obj.select_set(True)

                # Recalculate normals
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.normals_make_consistent(inside=False)
                bpy.ops.object.mode_set(mode='OBJECT')

                # Set object origin and scale
                bpy.ops.object.select_all(action='DESELECT')
                obj.select_set(True)
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
                obj.scale = (1, 1, 1)
            # Merge by distance
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.remove_doubles(threshold=0.001)
            bpy.ops.object.mode_set(mode='OBJECT')
            
            # Show CSV plot points in a text window
            bpy.ops.text.new()
            text = bpy.data.texts[-1]
            for vertex in vertices:
                text.write("Vertex: {}\n".format(vertex))
                
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}

        return {'FINISHED'}

def menu_func_import(self, context):
    self.layout.operator(CSVMeshImporterOperator.bl_idname, text="CSV Mesh (.csv)")

def register():
    bpy.utils.register_class(CSVMeshImporterOperator)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)

def unregister():
    bpy.utils.unregister_class(CSVMeshImporterOperator)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)

if __name__ == "__main__":
    register()
