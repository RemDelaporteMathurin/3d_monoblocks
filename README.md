# 3D monoblocks FESTIM application

## 1. Create the geometry

This step requires [CadQuery](https://github.com/CadQuery/cadquery) which can be installed with Anaconda.

```
cd meshes
python make_cad.py
```

This will create a brep file.

## 2. Mesh

Load `mesh_with_salome.py` (with the right paths) in SALOME.

This will create a .med file.

Then to convert the .med file in .xdmf files (readable by FESTIM), run:

```
python convert_mesh.py
```
If needed, install [meshio](https://github.com/nschloe/meshio) with:

```
pip install meshio[all]
```

## 3. Run FESTIM 

Install the dev version of FESTIM:

```
pip install git+https://github.com/RemDelaporteMathurin/FESTIM@dev
```

To run the FESTIM simulation:

```
python main.py
```

This will produce several .xdmf files
