import bpy
import csv
import bmesh
from bpy_extras.io_utils import ImportHelper
from mathutils import Matrix

bl_info = {
    "name": "CSV Mesh Importer",
    "author": "Jolly Joe",
    "version": (1, 5),
    "blender": (3, 5, 0),
    "location": "File > Import",
    "description": "Import points from a CSV file and create a mesh with connected edges. Works alongside 'RenderDoc' exporting the cvs file.",
    "category": "Import-Export",
}

class CSVMeshImporterOperator(bpy.types.Operator, ImportHelper):
    bl_idname = "import_mesh.csv"
    bl_label = "Import CSV Mesh"
    bl_description = "Import points from a CSV file and create a mesh with connected edges"

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

                # Connect the vertices to create edges
                bm.verts.ensure_lookup_table()
                bm.edges.ensure_lookup_table()
                for i in range(len(vertices) - 1):
                    bm.edges.new((bm.verts[i], bm.verts[i + 1]))

                # Update the BMesh and populate the mesh with BMesh data
                bm.to_mesh(mesh)
                bm.free()

                # Create a new object from the mesh
                obj = bpy.data.objects.new("CSV_Object", mesh)
                context.collection.objects.link(obj)

                # Select the newly created object
                bpy.context.view_layer.objects.active = obj
                obj.select_set(True)

                # Enter edit mode and remove duplicate vertices
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.remove_doubles()
                bpy.ops.mesh.select_all(action='DESELECT')
                bpy.ops.object.mode_set(mode='OBJECT')

                # Show CSV plot points in a text window
                bpy.ops.text.new()
                text = bpy.data.texts[-1]
                for vertex in vertices:
                    text.write("Vertex: {}\n".format(vertex))
                
                # Set dimensions to (1, 1, 1) before scaling
                
                
                # Set the scale to 1 and relocate object to center
                bpy.ops.object.select_all(action='DESELECT')
                obj.select_set(True)
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
                obj.scale = (1, 1, 1)
                obj.location = (0, 0, 0)
                obj.dimensions = (1, 1, 1)
                obj.rotation_euler = (90, 0, 0)
                
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
