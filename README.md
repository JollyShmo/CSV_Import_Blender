`click to download addon>>`
[![download](https://github.com/JollyShmo/CSV_Import_Blender/blob/main/version_csv_import.png)](https://github.com/JollyShmo/CSV_Import_Blender/releases/download/v4.2.1/csv_mesh_importer.zip)

This Blender addon allows you to import points from a CSV file and create a mesh by connected edges or faces. It's particularly useful for visualizing 3D point data captured using tools like 'RenderDoc' to export the CSV file.

| RenderDoc| Blender|
| ---------| -------|
| ![Image 1](https://github.com/JollyShmo/CSV_Import_Blender/blob/main/step1.png)    | ![Image 2](https://github.com/JollyShmo/CSV_Import_Blender/blob/main/step2%20(2).png?raw=true)    |
|`Export` the VS Input csv file | `Import` the csv file into Blender |

## Features
- Import vertex plot points from a CSV file as a mesh.
- Creates a mesh with connected edges or faces based on the imported points.
- Automatically remove duplicate vertices and edges.
- Corrects the normals to face outside.
- Ability to select what column from the csv files for the coords for `POSITION.x, POSITION.y, POSITION.z` plus an option for 2 additional coords I call `POSITION.ux, POSITION.uy`. (This can be found in `Other`)

## Programs Used/Need
| Blender |
|---------|
- [`Blender website`](https://www.blender.org)
- [Download Blender](https://www.blender.org/download/release/Blender3.6/blender-3.6.2-windows-x64.msi/) The open-source 3D creation suite used to run the addon.

| RenderDoc |
|-----------|
- [`RenderDoc website`](https://renderdoc.org/)
- [Download RenderDoc x64](https://renderdoc.org/stable/1.28/RenderDoc_1.28_64.msi) A graphics debugger, which can be used to export the CSV files for importing to Blender.

## Install Addon and Usage
1. Download the addon by clicking the header CSV Mesh Importer picutre.
2. In Blender, `Edit > Preferences > Add-ons > Install`
3. Click the 'Install' button and choose the downloaded `csv_mesh_importer.zip` file.
4. Check the box to have it apply the changes.
5. Now, you can import CSV files containing vertex data by going to `File > Import' > 'CSV Mesh (.csv)`.

## Options
<details>
 <summary>⚙ Addon Options</summary>
 
- **`Scale Factor`** Scale the imported mesh. (0.01 - 10.00)
- **`Connection Method`** Choose between connecting vertices with edges or faces.
- **`Format`** Choose between game sets or other. (Stubbs the Zombie, Bioshock 1 & 2 + WHF +, Bioshock INF +, Other)
- **`Auto-Smooth(checkbox)`** Have it use the default auto-smooth shading on import.
- **`Center Object(checkbox)`** This will center the object base on origin (middle of mesh usually) if unchecked it will be the coords from the RenderDoc capture location.
- **`UV smart Unwrapping(checkbox)`** just does a smart unwrap (only for Stubbs The Zombie atm)
</details>

## Formats
<details>
<summary>Stubbs the Zombie</summary>

`Stubbs Only`
- Scale: `10.0`
- Connection Method: `Faces`
- Format: `Stubbs The Zombie`
- Auto-Smooth: `optional` `auto-smooth shading 30°`
- Center Object: `optional`
- Beta: UV Unwrapping: `optional` `smart uv unwraps`
</details>

<details>
<summary>Bioshock 1 & 2 + WHF +</summary>
 
 `main`
- Scale: `0.01` - `1.0`
- Connection Method: `Faces`
- Format: `Bioshock 1 & 2 + WHF +`
- Auto-Smooth: `optional` `auto-smooth shading 30°`
- Center Object: `optional` `mesh to 3d curser`
</details>

<details>
<summary>Bioshock INF +</summary>

 `beta`
> Scale: `0.01` - `1.0`

> Connection Method: `Faces`

> Format: `Bioshock 1 & 2 + WHF +`

> Auto-Smooth: `optional` `auto-smooth shading 30°`

> Center Object: `optional` `mesh to 3d curser`
</details> 

## Credits
- Author: `Jolly Joe`
- Stable Version: 4.2.1
- Blender Compatibility: 2.93 or later
- Category: Import

**[`⚙ Game List`](/GameList.md)**
<details>
 <summary>More Info:</summary>
 
`note:` ```This addon creates a mesh with connected edges or faces based on the imported points. It's important to review the results and refine the mesh as needed after import. This is optimized for games that work with RenderDoc and the csv files it can export.```

`note:` `'Bioshock 1 & 2 + WHF +' should be the default when trying a new game not listed.` 

`note:` `'Bioshock INF +' is only last resort its better to use Other in some cases.`
</details>


