# CSV Mesh Importer 
`Blender addon` `RenderDoc csv`

This Blender addon allows you to import points from a CSV file and create a mesh by connected edges or faces. It's particularly useful for visualizing 3D point data captured using tools like 'RenderDoc' to export the CSV file.

## Features
- Import vertex plot points from a CSV file as a mesh.
- Creates a mesh with connected edges or faces based on the imported points.
- Automatically remove duplicate vertices and edges.
- Corrects the normals to face outside.
- Ability to select what column from the csv files for the coords for `POSITION.x, POSITION.y, POSITION.z` plus an option for 2 additional coords I call `POSITION.ux, POSITION.uy`. (This can be found in `Other`)

## Install and Usage
1. Download the addon by clicking `Code <>` > `Download Zip`.
2. In Blender, open the 'Edit' menu, select 'Preferences', and navigate to the 'Add-ons' section.
3. Click the 'Install' button and choose the downloaded `CSV_Import_Blender-main.zip` file.
4. Check the box to have it apply the changes.
5. Now, you can import CSV files containing vertex data by going to 'File > Import' and selecting 'CSV Mesh (.csv)'.

## Programs Used/Need
- [`Blender`](https://www.blender.org) The open-source 3D creation suite used to run the addon.
- [`RenderDoc`](https://renderdoc.org/) A graphics debugger, which can be used to export the CSV files for importing.

## Options
- **Scale Factor:** Scale the imported mesh.
- **Connection Method:** Choose between connecting vertices with edges or faces.
- **Format:** Choose between game sets or other. (Stubbs the Zombie, Bioshock 1 & 2 + WHF +, Bioshock INF +, Other)\
- **Auto-Smooth(checkbox):** Have it use the default auto-smooth shading on import.
- **Center Object(checkbox):** This will center the object base on origin (middle of mesh usually) if unchecked it will be the coords from the RenderDoc capture location or default.
- **UV smart Unwrapping:** just does a unwrap, wanting to use the info from the csv file (under construction only for Stubbs atm)
 
## Credits
- Author: `Jolly Joe`
- Stable Version: 4.2.1
- Blender Compatibility: 2.93 or later
- Category: Import

`note:` This addon creates a mesh with connected edges or faces based on the imported points. It's important to review the results and refine the mesh as needed after import. This is optimized for `Bioshock Remastered 1 & 2 & Infinte, Stubbs The Zombie, We Happy Few` while using RenderDoc csv exports.

`note:` When trying a new game not listed try it under `Bioshock 1&2 + WHF +` with the rest at default, if that doesn't work you can use `Other` to pin point the verts. 

`note:` `Bioshock INF + is only last resort its better to use Other in some cases.`
