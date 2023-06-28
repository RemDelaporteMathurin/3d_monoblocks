# 3D monoblocks FESTIM application

## 1. Create the geometry

This step requires [CadQuery](https://github.com/CadQuery/cadquery) which can be installed with Anaconda.

```
cd meshes
python make_cad.py
```

This will create a brep file.

## 2. Mesh

To mesh the brep files, run:
```
C:\SALOME-9.6.0\run_salome.bat -t mesh_with_salome.py
```
You may need to replace the path to `run_salome.bat`.

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

Run a FEniCS container:

```
docker run -ti -v ${PWD}:/home/fenics/shared quay.io/fenicsproject/stable:latest
```

Install FESTIM:

```
pip install festim==0.10.2
```

To run the FESTIM simulation:

```
python main.py
```

This will produce several .xdmf files
