import bpy
import csv
import bmesh
from bpy_extras.io_utils import ImportHelper
from mathutils import Matrix

bl_info = {
    "name": "CSV Mesh Importer",
    "author": "Jolly Joe",
    "version": (4, 0, 0),
    "blender": (3, 6, 0),
    "location": "File > Import",
    "description": "Import points from a CSV file and create a mesh with connected edges or faces.",
    "category": "Import-Export",
}

class CSVMeshImporterOperator(bpy.types.Operator, ImportHelper):
    bl_idname = "import_mesh.csv"
    bl_label = "Import CSV Mesh"
    bl_description = "Import points from a CSV file and create a mesh with connected edges or faces."
    
    filter_glob: bpy.props.StringProperty(
        default="*.csv",
        options={'HIDDEN'},
        maxlen=255,
    )
    
    scale_factor: bpy.props.FloatProperty(
        name="Scale Factor",
        default=1.0,
        description="Scale the imported mesh",
        min=0.01,
        max=10.0,
    )
    
    connection_method: bpy.props.EnumProperty(
        name="Connection Method",
        items=[
            ('FACES', "Faces", "Connect vertices with faces"),
            ('EDGES', "Edges", "Connect vertices with edges"),
        ],
        default='FACES',
        description="Method for connecting vertices with faces"
    )
    
    cleanup_check: bpy.props.BoolProperty(
        name="Clean Up Loose Geometry",
        default=True,
        description="Lets you clean up geometry by selecting the loose edges.",
    )

    rename_option: bpy.props.StringProperty(
        name="Mesh Name",
        default="",
        description="Rename the object.",
    )

    csv_format: bpy.props.EnumProperty(
        name="CSV Format",
        items=[
            ('STUBBS', "Stubbs The Zombie", "CSV format STZ"),
            ('WE_HAPPY_FEW', "We Happy Few", "CSV format for WHF"),
        ],
        default='STUBBS',
        description="Choose the CSV format",
    )

    def draw(self, context):
        layout = self.layout

        # Existing properties
        layout.prop(self, "rename_option")
        layout.prop(self, "scale_factor")
        layout.prop(self, "connection_method")
        layout.prop(self, "csv_format")
        
        # Hide Clean Up from Edges
        if self.connection_method == 'FACES':
            layout.prop(self, "cleanup_check")
        if self.connection_method == 'EDGES':
            self.cleanup_check = False
            
    def execute(self, context):
        try:
            with open(self.filepath, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')

                # Set the appropriate header dictionary based on the selected format
                headers = {}
                if self.csv_format == 'STUBBS':
                    headers = {
                        'POSITION.x': 2,
                        'POSITION.y': 3,
                        'POSITION.z': 4,

                        # ... add other headers ...
                    }
                elif self.csv_format == 'WE_HAPPY_FEW':
                    headers = {
                        'POSITION.x': 2,
                        'POSITION.y': 3,
                        'POSITION.z': 4,

                        # ... add other headers ...
                    }
                else:
                    self.report({'ERROR'}, "Invalid CSV format")
                    return {'CANCELLED'}
                
                next(reader)  # Skip the header line
                vertices = []
                for row in reader:
                    x = float(row[headers['POSITION.x']])
                    y = float(row[headers['POSITION.y']])
                    z = float(row[headers['POSITION.z']])
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
                    if self.csv_format == 'STUBBS':
                        for i in range(len(vertices) - 1):
                            bm.edges.new((bm.verts[i], bm.verts[i + 1]))
                    elif self.csv_format == 'WE_HAPPY_FEW':
                        corner_indices = list(range(0, len(vertices) - 1, 3))
                        for i in corner_indices:
                            if i + 1 < len(vertices):
                                bm.edges.new((bm.verts[i], bm.verts[i + 1]))

                elif self.connection_method == 'FACES':
                    if len(vertices) >= 3:
                        if self.csv_format == 'STUBBS':
                            for i in range(len(vertices) - 2):
                                bm.faces.new((bm.verts[i], bm.verts[i + 1], bm.verts[i + 2]))
                        elif self.csv_format == 'WE_HAPPY_FEW':
                            corner_indices = list(range(0, len(vertices) - 2, 3))
                            for i in corner_indices:
                                if i + 2 < len(vertices):
                                    bm.faces.new((bm.verts[i], bm.verts[i + 1], bm.verts[i + 2]))

                # Update the BMesh and populate the mesh with BMesh data
                bm.to_mesh(mesh)
                bm.free()

                # Create a new object from the mesh
                obj = bpy.data.objects.new(self.rename_option, mesh)
                context.collection.objects.link(obj)
                self.rename_option = ""
                # Select the newly created object
                bpy.context.view_layer.objects.active = obj
                obj.select_set(True)



                # Set object origin and scale
                bpy.ops.object.select_all(action='DESELECT')
                obj.select_set(True)
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
                bpy.types.Scene.scale_factor = 1.0  # Adjust this line based on the property's actual name
            # Merge by distance
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.remove_doubles(threshold=0.001)
            bpy.ops.object.mode_set(mode='OBJECT')
            # Clean up loose geometry
            if self.cleanup_check:
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_mode(type='EDGE')  # Switch to edge selection mode
                bpy.ops.mesh.select_all(action='DESELECT')
                bpy.ops.mesh.select_loose()
                bpy.ops.mesh.delete(type='EDGE')
                bpy.ops.object.mode_set(mode='OBJECT')
                # Recalculate normals
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.normals_make_consistent(inside=False)
                bpy.ops.object.mode_set(mode='OBJECT')
            # Show CSV plot points in a text window
            bpy.ops.text.new()
            text = bpy.data.texts[-1]
            for vertex in vertices:
                text.write("Vertex: {}\n".format(vertex))
                
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}
        # Finish message
        self.report({'INFO'}, "Mesh imported successfully.")
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
