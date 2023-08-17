# CSV Mesh Importer Blender Addon
### 

This Blender addon allows you to import points from a CSV file and create a mesh with connected edges or faces. It's particularly useful for visualizing 3D point data captured using tools like 'RenderDoc' to export the CSV file.

**Note:** This addon now supports both edge and face connections. You can choose between the two connection methods during import.

## Features
- Import vertex points from a CSV file.
- Create a mesh with connected edges or faces based on the imported points.
- Automatically remove duplicate vertices.
- Provides a simple way to visualize point data in Blender's 3D view.

## Usage
1. Download the addon by clicking `Code <>` > `Download Zip`.
2. In Blender, open the 'Edit' menu, select 'Preferences', and navigate to the 'Add-ons' section.
3. Click the 'Install' button and choose the downloaded `CSV_Import_Blender-main.zip` file.
4. Now, you can import CSV files containing vertex data by going to 'File > Import' and selecting 'CSV Mesh (.csv)'.

## Programs Used
- [Blender](https://www.blender.org): The open-source 3D creation suite used to run the addon.
- [RenderDoc](https://renderdoc.org/): A graphics debugger, which can be used to export the CSV files for importing.

## Options
- **Scale Factor:** Scale the imported mesh.
- **Connection Method:** Choose between connecting vertices with edges or faces.

## Credits
- Author: Jolly Joe
- Stable Version: 4.0
- Blender Compatibility: 2.93 or later
- Category: Import

Please note that this addon creates a mesh with connected edges or faces based on the imported points. It's important to review the results and refine the mesh as needed after import. This is optimized for Stubbs The Zombie and We Happy Few, csv files come from RenderDoc exports. More information coming soon.
