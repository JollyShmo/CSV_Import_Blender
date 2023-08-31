##########################################################
#   CSV Mesh Importer Addon
#
#   Description: Import points from a CSV file and create a mesh with connected edges or faces.
#   Author: Jolly Joe
#   Version: 4.2.1
#   Blender: 3.6.0
#   Category: Import-Export
#
#   Usage Instructions:
#   - Enable the addon in Blender's preferences.
#   - Go to "File > Import > CSV Mesh" to access the importer.
#   - Adjust settings such as scale factor, connection method, and more.
#   - Click "Import CSV Mesh" to generate the mesh from the CSV file.
#
#   note: some games work when the remove loose geometry is turned off (unchecked), this is rare.
#   check the POSITION.x, POSITION.y, POSITION.z in the csv file to custom load any other files,
#   it will skip the first row when collecting verts positions. UV part is mostly under construction.
#   
#   Terms of Use:
#   - You are free to use and distribute this addon for both personal and commercial purposes,
#     provided that you credit the original author (Jolly Joe) by including this comment block.
#   - If you make significant modifications let me know also,
#   consider sharing your changes with the community.
#
#   - Original addon by Jolly Joe
#
#   Contact:
#   - Astralpathfinder@protonmail.com
##########################################################

import bpy
import csv
import bmesh
from bpy_extras.io_utils import ImportHelper
from mathutils import Matrix

bl_info = {
    "name": "CSV Mesh Importer",
    "author": "Jolly Joe",
    "version": (4, 2, 1),
    "blender": (3, 6, 0),
    "location": "File > Import",
    "description": "Import points from a CSV file and create a mesh with connected edges or faces.",
    "category": "Import-Export",
}

class CSVMeshImporterOperator(bpy.types.Operator, ImportHelper):
    bl_idname = "import_mesh.csv"
    bl_label = "Import CSV Mesh"
    bl_description = "Import points from a CSV file and create a mesh with connected edges or faces."
    bl_options = {'REGISTER', 'UNDO'}
    
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
            ('EDGES', "Edges (Debugging)", "Connect vertices with edges"),
        ],
        default='FACES',
        description="Method for connecting vertices with faces"
    )
    
    cleanup_check: bpy.props.BoolProperty(
        name="Clean Up Loose Geometry",
        default=True,
        description="Lets you clean up geometry by selecting the loose edges. (Recomended for most imports)",
        #options={'HIDDEN'},
    )
    
    center_obj: bpy.props.BoolProperty(
        name="Center Object",
        default=False,
        description="Centers the Object, otherwise it will be places as it was during the RenderDoc Capture.",
    )

    hide_option_uv: bpy.props.BoolProperty(
        name="Hide UV options",
        default=True,
        description="Hide UV options.",
    )
        
    rename_option: bpy.props.StringProperty(
        name="Obj Name",
        default="",
        description="Rename the object.",
    )
    
    pos_x_column: bpy.props.IntProperty(
        name="POSITION.x",
        default=2,
        description="Column index for X coordinate",
        min=0,
    )

    pos_y_column: bpy.props.IntProperty(
        name="POSITION.y",
        default=3,
        description="Column index for Y coordinate",
        min=0,
    )

    pos_z_column: bpy.props.IntProperty(
        name="POSITION.z",
        default=4,
        description="Column index for Z coordinate",
        min=0,
    )
    
    pos_ux_column: bpy.props.IntProperty(
        name="TEXTURE.x",
        default=5,
        description="Column index for uv X coordinate",
        min=0,
    )

    pos_uy_column: bpy.props.IntProperty(
        name="TEXTURE.y",
        default=6,
        description="Column index for uv Y coordinate",
        min=0,
    )
    
    set_z: bpy.props.BoolProperty(
        name="Set TEXCOORD.z = 1.0",
        default=True,
        description="Set texture Coordinate to Z = 1.0",
        options={'HIDDEN'},

    )
    smooth_finish: bpy.props.BoolProperty(
        name="Shade Smooth",
        default=False,
        description="Auto Smooth Finish",
    )
    csv_format: bpy.props.EnumProperty(
        name="CSV Format",
        items=[
            ('STUBBS', "Stubbs The Zombie", "CSV format for STZ"),
            ('WE_HAPPY_FEW', "Bioshock 1 & 2 + WHF +", "CSV format POS [2,3,4] [x,y,z]"),
            ('BIOSHOCK', "Bioshock INF +", "CSV format POS [18,19,20] [x,y,z]"),
            ('OTHER', "Other", "For any csv file with x, y, z"),       
        ],
        default='STUBBS',
        description="Choose the CSV format",
    )
    beta_test: bpy.props.EnumProperty(
        name="Beta",
        items=[
            ('NONE', "UV testing OFF", "No testing"),
            ('BETA', "UV testing ON", "UV testing"),
        ],
        default='BETA',
        description="Testing and Debugging"
    )
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # Inside the beta testing section
        if self.beta_test == 'BETA':
            self.report({'INFO'}, "This is beta ON.")        
        else:
            #layout.prop(self, "csv_file_preview")
            self.report({'WARNING'}, "This is beta OFF")
    
        if self.csv_format == 'STUBBS':
            info = scene.get("readme_info", "Stubbs The Zombie: 1.0 - 10.0")
        elif self.csv_format == 'WE_HAPPY_FEW':
            info = scene.get("readme_info", "Bioshock 1 & 2 + WHF Scale: 0.01")
        elif self.csv_format == 'BIOSHOCK':
            info = scene.get("readme_info", "Bioshock Inf: 0.01 - 0.10")
        else:
            info = scene.get("readme_info", "Other: Any csv file: 0.01 - 1.0")
            
        layout.label(text="Scale Info:")
        layout.label(text=info)

        # Layout options
        if self.connection_method == 'FACES':
            layout.prop(self, "scale_factor")
        else:
            self.cleanup_check = False
        layout.prop(self, "csv_format")
        layout.prop(self, "rename_option")
        layout.prop(self, "connection_method")
        layout.prop(self, "cleanup_check")
        layout.prop(self, "smooth_finish")
        layout.prop(self, "center_obj")
        
        if self.csv_format == 'STUBBS':
            layout.prop(self, "beta_test")
        else:
            self.beta_test = 'NONE'
        
        if self.csv_format == 'OTHER':
            layout.prop(self, "pos_x_column")
            layout.prop(self, "pos_y_column")
            layout.prop(self, "pos_z_column")
            layout.prop(self, "hide_option_uv")
            
            if self.hide_option_uv:
                self.set_z = True
                layout.prop(self, "pos_ux_column")
                layout.prop(self, "pos_uy_column")          
            else:
                self.set_z = False
                
    def execute(self, context):
        try:
            with open(self.filepath, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                # Game Headers to name the rows in the file for script
                headers = {}
                if self.csv_format == 'STUBBS':
                    headers = {
                        'POSITION.x': 2,
                        'POSITION.y': 3,
                        'POSITION.z': 4,
                        'TEXCOORD.x': 14,
                        'TEXCOORD.y': 15,   
                    }
                elif self.csv_format == 'WE_HAPPY_FEW':
                    headers = {
                        'POSITION.x': 2,
                        'POSITION.y': 3,
                        'POSITION.z': 4,
                        'TEXCOORD.x': 13,
                        'TEXCOORD.y': 14,   
                    }
                elif self.csv_format == 'BIOSHOCK':
                    headers = {
                        'POSITION.x': 18,
                        'POSITION.y': 19,
                        'POSITION.z': 20,
                        'TEXCOORD0.x': 21,
                        'TEXCOORD0.y': 22,
                    }
                elif self.csv_format == 'OTHER':
                    headers = {
                        'POSITION.x': self.pos_x_column,
                        'POSITION.y': self.pos_y_column,
                        'POSITION.z': self.pos_z_column,
                        'TEXCOORD.x': self.pos_ux_column,
                        'TEXCOORD.y': self.pos_uy_column,
                    }
                else:
                    self.report({'ERROR'}, "Invalid CSV format")
                    return {'CANCELLED'}
                
                next(reader)
                
                vertices = []
                uv = []
                
                for row in reader:                        
                    x = float(row[headers['POSITION.x']])
                    y = float(row[headers['POSITION.y']])
                    
                    if self.set_z and self.csv_format == 'OTHER':
                        z = 1.0
                    else:
                        z = float(row[headers['POSITION.z']])               
                    vertices.append((x * self.scale_factor, y * self.scale_factor, z * self.scale_factor))
                    # WHF UV
                    if self.csv_format == 'WE_HAPPY_FEW':
                        
                        if self.hide_option_uv == False:
                            self.hide_option_uv = False
                            tx = float(row[headers['TEXCOORD.x']])
                            ty = float(row[headers['TEXCOORD.y']])
                            uv.append((tx, ty, 1.0))
                    # STZ UV
                    elif self.csv_format == 'STUBBS':
                        tx = float(row[headers['TEXCOORD.x']])
                        ty = float(row[headers['TEXCOORD.y']])
                        uv.append((tx, ty, 1.0))
                    # BIO UV
                    elif self.csv_format == 'BIOSHOCK':
                        
                        if self.hide_option_uv == False:
                            self.hide_option_uv = False
                            tx = float(row[headers['TEXCOORD0.x']])
                            ty = float(row[headers['TEXCOORD0.y']])
                            uv.append((tx, ty, 1.0))
                    # OTHER XYZ + UV        
                    elif self.csv_format == 'OTHER':
                        x = float(row[self.pos_x_column])
                        y = float(row[self.pos_y_column])
                        
                        if self.set_z:
                            z = 1.0
                        else:
                            z = float(row[self.pos_z_column])
                            
                        if self.hide_option_uv:
                            tx = float(row[headers['TEXCOORD.x']])
                            ty = float(row[headers['TEXCOORD.y']])
                            uv.append((tx, ty, 1.0))
                            vertices.append((x * self.scale_factor, y * self.scale_factor, z * self.scale_factor))
                            
                mesh = bpy.data.meshes.new("CSV_Mesh")
                bm = bmesh.new()
                
                for vertex in vertices:
                    bm.verts.new(vertex)
                # Connect the vertices based on the selected connection method
                bm.verts.ensure_lookup_table()
                # Edges
                if self.connection_method == 'EDGES':
                    if self.csv_format == 'STUBBS':
                        corner_indices = list(range(0, len(vertices) - 1))
                        for i in corner_indices:
                            bm.edges.new((bm.verts[i], bm.verts[i + 1]))
                            
                    elif self.csv_format == 'WE_HAPPY_FEW':
                        corner_indices = list(range(0, len(vertices) - 1, 3))
                        for i in corner_indices:
                            if i + 1 < len(vertices):
                                bm.edges.new((bm.verts[i], bm.verts[i + 1]))
                    else:
                        corner_indices = list(range(0, len(vertices) - 1))                        
                        for i in corner_indices:
                            if i + 1 < len(vertices):
                                bm.edges.new((bm.verts[i], bm.verts[i + 1]))

                # Faces
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
                                    
                        elif self.csv_format == 'BIOSHOCK':
                            corner_indices = list(range(0, len(vertices) - 2, 3))
                            for i in corner_indices:
                                if i + 2 < len(vertices):
                                    bm.faces.new((bm.verts[i], bm.verts[i + 1], bm.verts[i + 2]))

                        elif self.csv_format == 'OTHER':
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
                # Set object origin and scale
                bpy.ops.object.select_all(action='DESELECT')
                obj.select_set(True)
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
                # Adjust this line based on the property's actual name
                bpy.types.Scene.scale_factor = 1.0
            # Merge by distance
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.remove_doubles(threshold=0.001)
            bpy.ops.object.mode_set(mode='OBJECT')
            
            # If Clean up loose geometry option checked
            if self.cleanup_check:
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_mode(type='EDGE')
                bpy.ops.mesh.select_all(action='DESELECT')
                bpy.ops.mesh.select_loose()
                bpy.ops.mesh.delete(type='EDGE')
                bpy.ops.object.mode_set(mode='OBJECT')
                # Recalculate normals
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.normals_make_consistent(inside=False)
                bpy.ops.object.mode_set(mode='OBJECT')
                
            # If Shade Smooth option checked
            if self.smooth_finish:
                # Get the active object (selected object)
                active_object = bpy.context.active_object
                
                if active_object and active_object.type == 'MESH':
                    # Access the object's mesh data
                    mesh = active_object.data
                    # Enable smooth shading for each polygon
                    for polygon in mesh.polygons:
                        polygon.use_smooth = True                    
                    # Set shading mode to smooth
                    bpy.ops.object.shade_smooth()
                    
            # Scale checked
            if self.center_obj:
                # Set object origin and scale
                bpy.ops.object.location_clear(clear_delta=False)
                
            # Inside the beta testing section
            if self.beta_test == 'BETA':
                self.report({'INFO'}, "This is beta ON.")
                # Get active object
                active_obj = bpy.context.active_object
                # Switch to Edit Mode and perform smart UV unwrapping
                bpy.context.view_layer.objects.active = active_obj
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.uv.smart_project(angle_limit=66, island_margin=0.001)
                bpy.ops.object.mode_set(mode='OBJECT')
            else:
                self.report({'WARNING'}, "This is beta OFF")                
                
            # Create a new material
            material = bpy.data.materials.new(name="Material")
            
            # Configure material properties
            if self.csv_format == 'STUBBS':
                # Set the diffuse color Greenish
                material.diffuse_color = (0.375999, 0.782452, 0.15231, 1.0)  
            elif self.csv_format == 'BIOSHOCK':
                # Set the diffuse color Blueish
                material.diffuse_color = (0.066149, 0.255212, 0.979846, 1.0)  
            elif self.csv_format == 'WE_HAPPY_FEW':
                # Set the diffuse color Yellowish
                material.diffuse_color = (0.979846, 0.907275, 0.065402, 1.0)  
            else:
                material.diffuse_color = (0.8, 0.5, 0.8, 1.0)
            # Assign the material to the mesh
            mesh.materials.append(material)
            # Show CSV plot points in a text window
            bpy.ops.text.new()
            text = bpy.data.texts[-1]
            
            # Write UV coordinates to text
            uv_text = "UV Coordinates:\n"
            for uv_coords in uv:
                uv_text += f"({uv_coords[0]}, {uv_coords[1]}, {uv_coords[2]})\n"
            
            # Write vertices to text
            text.write("Vertices:\n")
            for vertex in vertices:
                text.write("({}, {}, {})\n".format(vertex[0], vertex[1], vertex[2]))
            # Append the UV text to text 
            text.write(uv_text)
            
            # END OF PROGRAM
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}
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
