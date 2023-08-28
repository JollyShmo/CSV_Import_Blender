# CSV Mesh Importer Blender Addon
### 

This Blender addon allows you to import points from a CSV file and create a mesh with connected edges or faces. It's particularly useful for visualizing 3D point data captured using tools like 'RenderDoc' to export the CSV file.

**Note:** This addon now supports both edge and face connections. You can choose between the two connection methods during import.

## Features
- Import vertex plot points from a CSV file as a mesh.
- Create a mesh with connected edges or faces based on the imported points.
- Automatically remove duplicate vertices.
- Corrects the normals to face out.

## Usage
1. Download the addon by clicking `Code <>` > `Download Zip`.
2. In Blender, open the 'Edit' menu, select 'Preferences', and navigate to the 'Add-ons' section.
3. Click the 'Install' button and choose the downloaded `CSV_Import_Blender-main.zip` file.
4. Check the box to have it apply the changes.
5. Now, you can import CSV files containing vertex data by going to 'File > Import' and selecting 'CSV Mesh (.csv)'.

## Programs Used
- [Blender](https://www.blender.org): The open-source 3D creation suite used to run the addon.
- [RenderDoc](https://renderdoc.org/): A graphics debugger, which can be used to export the CSV files for importing.

## Options
- **Scale Factor:** Scale the imported mesh.
- **Connection Method:** Choose between connecting vertices with edges or faces.

## Credits
- Author: Jolly Joe
- Stable Version: 4.2.1
- Blender Compatibility: 2.93 or later
- Category: Import

Please note: This addon creates a mesh with connected edges or faces based on the imported points. It's important to review the results and refine the mesh as needed after import. This is optimized for `Bioshock Remastered 1 & 2 & Infinte, Stubbs The Zombie, We Happy Few` while using RenderDoc csv exports. Some games like `Sludge Life 2` they use the `Bioshock 1 & 2` and at (scale of >= 1.0). If it looks like a mess try it under different settings, document it and let me know. 
