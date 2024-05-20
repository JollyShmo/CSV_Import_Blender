`click to download Blender addon 💾🔻` 
> *Updated 1/31/2024*

[![download](https://github.com/JollyShmo/CSV_Import_Blender/blob/Beta/version_csv_import_beta2.png)](https://github.com/JollyShmo/CSV_Import_Blender/releases/download/v4.2.1-beta/csv_mesh_importer.zip)

This Blender addon allows you to import a CSV file and it will auto create a 3d mesh by connected points, edges and faces. It's particularly useful for visualizing point data captured using tools like 'RenderDoc' to export the CSV file as a 3D Mesh. Works for a number of games including Bioshock Series, We Happy Few, and more.

| RenderDoc | Blender|
| :-------- | :----- |
| ![Image 1](https://github.com/JollyShmo/CSV_Import_Blender/blob/main/step1.png) | ![Image 2](https://github.com/JollyShmo/CSV_Import_Blender/blob/main/step2%20(2).png) |
|`Export` the VS Input csv file | `Import` the csv file into Blender |

## Features
🗃 Import vertex plot points from a CSV file as a 3d mesh object.

📐 Creates the mesh by connecting edges and faces based on the settings.

⛏ Automatically remove duplicate vertices and edges with *Clean Up Loose Geometry*.

😇 Corrects the normals to face outside for you on import.

🖇 Option `Other` to select what column from the csv files for the verts for *(POSITION.x, POSITION.y, POSITION.z)* plus an option for 2 additional verts *(TEXTURE.x, TEXTURE.y)*. 

## Programs Used:
| Blender 4.0 |
| :---------- |
🌐 [`Blender website`](https://www.blender.org)
💾 [Download Blender](https://www.blender.org/download/release/Blender4.0/blender-4.0.2-windows-x64.msi/) The open-source 3D creation suite used to run the addon.

| RenderDoc 1.31 |
| :------------- |
🌐 [`RenderDoc website`](https://renderdoc.org/)
💾 [Download RenderDoc x64](https://renderdoc.org/stable/1.31/RenderDoc_1.31_64.msi) A versitile graphics debugger, which can also be used to export the CSV files.

## Install Addon and Usage
1. Download the addon by clicking the header CSV Mesh Importer v4.2.1 picutre.
2. In Blender, `Edit > Preferences > Add-ons > Install`
3. Click the 'Install' button and choose the downloaded `csv_mesh_importer.zip` file.
4. Check the box to have it apply the changes ☑.
5. Now, you can import CSV files containing vertex data by going to `File > Import' > 'CSV Mesh (.csv)`.

## Settings

<details>
 <summary>⚙ Addon Options</summary>

 | Title | Discription |
 | :---- | :----------- |
| **`Scale Factor`**| Scale the imported mesh. (0.01 - 10.00)|
| **`Connection Method`**| Choose between connecting vertices with edges or faces.|
| **`Format`**| Choose between game sets or other. (Stubbs the Zombie, Bioshock 1 & 2 + WHF +, Bioshock INF +, Other)|
| **`Name Obj`**| Name the mesh on import. (default "Object")|
| **`Auto-Smooth(checkbox)`**| Have it use the default auto-smooth shading on import.|
| **`Center Object(checkbox)`**| This will center the object base on origin (middle of mesh usually) if unchecked it will be the verts from the RenderDoc capture location.|
| **`UV smart Unwrapping(checkbox)`**| just does a smart unwrap (only for Stubbs The Zombie atm)|
</details>

## Formats
<details>
<summary>🤯Bioshock 1 & 2 + WHF +</summary>
 
 `✔ Main Choice`
| Title | Recommended Setting |
| :---- | :------------------ |
| Scale: | `0.01` - `1.0`|
| Connection Method: | `Faces`|
| Format: | `Bioshock 1 & 2 + WHF +`|
| Name Obj: | `optional` `default "Object"`|
| Clean Up Loose Geometry: | `Required to work as intended` `only uncheck to debug`|
| Auto-Smooth: | `optional` `auto-smooth shading 30°`|
| Center Object: | `optional` `mesh to 3d curser`|
</details>
<details>
 
<summary>🧟‍♂️Stubbs the Zombie</summary>

`⚠ Stubbs The Zombie Game Only`

| Title | Recommended Setting |
| -- | -- |
| Scale: | `10.0` |
| Connection Method: | `Faces`|
| Format: | `Stubbs The Zombie`|
| Name Obj: | `optional` `default "Object"`| 
| Clean Up Loose Geometry: | `Required to work as intended` `only uncheck to debug`|
| Auto-Smooth: | `optional` `auto-smooth shading 30°`|
| Center Object: | `optional`|
| Beta: UV Unwrapping: |⚠ `optional` `smart uv unwraps`|
</details>

<details>
<summary>🦺Bioshock INF +</summary>

 `⚠ work in progress`
> Scale: `0.01` - `1.0`
> Connection Method: `Faces`
> Format: `Bioshock INF +`
> Name Obj `optional` `default "Object"`
> Clean Up Loose Geometry `Required to work as intended` `only uncheck to debug`
> Auto-Smooth: `optional` `auto-smooth shading 30°`
> Center Object: `optional` `mesh to 3d curser`
</details> 

## Credits

| Author: | `Jolly Joe` |
| :-------| :---------- |
| Stable Version:| `4.2.1` |
| Blender Compatibility:| `2.93 or later` |
| Category:| `Import` |
| Compatibility Game List:| **[`💿 Game List`](/GameList.md)** |

<details>
<summary><h3> ⚠ More Info:</h3></summary>

`notes:` 

>```This addon creates a mesh with connected edges or faces based on the imported points. It's important to review the results and refine the mesh as needed after import.```

```⚠ This is optimized for games that work with RenderDoc and the csv files it can export.```

- `Custom Imports: [Bioshock 1 & 2 + WHF +] should be the default when trying a new game not listed. You can also use [Other].` 

- `[Bioshock INF +] is only last resort. It is better to use Other in some cases.`

- `(TEXTURE.x, TEXTURE.y) currently only works under [Other]!`
</details>


