# CSV Mesh Importer Blender Addon

This Blender addon allows you to import points from a CSV file and create a mesh with connected edges. It's particularly useful for visualizing 3D point data captured using tools like 'RenderDoc' to export the cvs file.

! At the moment it just creates edges not faces, you will need to select everything and fill in the faces manually. This is a pet projected made by myself to better understand 3d game development. Let me know with any questions, updates, or issue.

## Features
- Import vertex points from a CSV file.
- Create a mesh with connected edges based on the imported points.
- Automatically remove duplicate vertices.
- Provides a simple way to visualize point data in Blender's 3D view.

## Usage
1. Download by clicking `Code <>` > `Download Zip`.
2. In Blender, open the 'Edit' menu, select 'Preferences', and navigate to the 'Add-ons' section.
3. Click the 'Install' button and choose the `CSV_Import_Blender-main.zip` file.
4. Enable the addon by checking the corresponding checkbox.
5. Now, you can import CSV files containing vertex data by going to 'File > Import' and selecting 'CSV Mesh (.csv)'.

## Credits
- Author: Jolly Joe
- Stable Version: 1.5
- Blender Compatibility: 2.93 or later
- Category: Import-Export

Please note that this addon creates a mesh with connected edges based on the imported points. It's important to review the results and refine the mesh as needed after import.
For more information, visit [Blender](https://www.blender.org) and [RenderDoc](https://renderdoc.org/).
