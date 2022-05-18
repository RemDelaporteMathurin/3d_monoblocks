#!/usr/bin/env python

###
### This file is generated automatically by SALOME v9.6.0 with dump python functionality
###

import sys
import salome

salome.salome_init()
import salome_notebook

notebook = salome_notebook.NoteBook()
sys.path.insert(0, r"D:/3d_monoblocks")

###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS

for thickness in [4, 5, 6, 7, 8, 9, 10, 14]:
    print("Meshing thickness {} mm".format(thickness))

    geompy = geomBuilder.New()

    O = geompy.MakeVertex(0, 0, 0)
    OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
    OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
    OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)
    geom_brep_1 = geompy.ImportBREP(
        "{}mm_thickness/monoblock_{}mm_thickness.brep".format(thickness, thickness)
    )
    scaled_geometry = geompy.MakeScaleTransform(geom_brep_1, None, 0.001)

    tungsten = geompy.CreateGroup(scaled_geometry, geompy.ShapeType["SOLID"])
    geompy.UnionIDs(tungsten, [3])
    cu = geompy.CreateGroup(scaled_geometry, geompy.ShapeType["SOLID"])
    geompy.UnionIDs(cu, [94])
    cucrzr = geompy.CreateGroup(scaled_geometry, geompy.ShapeType["SOLID"])
    geompy.UnionIDs(cucrzr, [52])
    top_surface = geompy.CreateGroup(scaled_geometry, geompy.ShapeType["FACE"])
    geompy.UnionIDs(top_surface, [31])
    cooling_surface = geompy.CreateGroup(scaled_geometry, geompy.ShapeType["FACE"])
    geompy.UnionIDs(cooling_surface, [91])
    poloidal_gap = geompy.CreateGroup(scaled_geometry, geompy.ShapeType["FACE"])
    geompy.UnionIDs(poloidal_gap, [22, 96])
    toroidal_gap = geompy.CreateGroup(scaled_geometry, geompy.ShapeType["FACE"])
    geompy.UnionIDs(toroidal_gap, [5])
    bottom = geompy.CreateGroup(scaled_geometry, geompy.ShapeType["FACE"])
    geompy.UnionIDs(bottom, [15])
    face_top_pipe = geompy.CreateGroup(scaled_geometry, geompy.ShapeType["FACE"])
    geompy.UnionIDs(face_top_pipe, [54])

    geompy.addToStudy(O, "O")
    geompy.addToStudy(OX, "OX")
    geompy.addToStudy(OY, "OY")
    geompy.addToStudy(OZ, "OZ")
    geompy.addToStudy(geom_brep_1, "geom.brep_1")
    geompy.addToStudy(scaled_geometry, "Scale_1")
    geompy.addToStudyInFather(scaled_geometry, tungsten, "tungsten")
    geompy.addToStudyInFather(scaled_geometry, cu, "cu")
    geompy.addToStudyInFather(scaled_geometry, cucrzr, "cucrzr")
    geompy.addToStudyInFather(scaled_geometry, top_surface, "top_surface")
    geompy.addToStudyInFather(scaled_geometry, cooling_surface, "cooling_surface")
    geompy.addToStudyInFather(scaled_geometry, poloidal_gap, "poloidal_gap")
    geompy.addToStudyInFather(scaled_geometry, toroidal_gap, "toroidal_gap")
    geompy.addToStudyInFather(scaled_geometry, bottom, "bottom")
    geompy.addToStudyInFather(scaled_geometry, face_top_pipe, "face_top_pipe")

    ###
    ### SMESH component
    ###

    import SMESH, SALOMEDS
    from salome.smesh import smeshBuilder

    smesh = smeshBuilder.New()
    # smesh.SetEnablePublish( False ) # Set to False to avoid publish in study if not needed or in some particular situations:
    # multiples meshes built in parallel, complex and numerous mesh edition (performance)

    Mesh_1 = smesh.Mesh(scaled_geometry)
    NETGEN_1D_2D_3D = Mesh_1.Tetrahedron(algo=smeshBuilder.NETGEN_1D2D3D)
    NETGEN_3D_Parameters_1 = NETGEN_1D_2D_3D.Parameters()
    NETGEN_3D_Parameters_1.SetMaxSize(2.76315)
    NETGEN_3D_Parameters_1.SetMinSize(0.5)
    NETGEN_3D_Parameters_1.SetSecondOrder(0)
    NETGEN_3D_Parameters_1.SetOptimize(1)
    NETGEN_3D_Parameters_1.SetFineness(4)
    NETGEN_3D_Parameters_1.SetChordalError(-1)
    NETGEN_3D_Parameters_1.SetChordalErrorEnabled(0)
    NETGEN_3D_Parameters_1.SetUseSurfaceCurvature(1)
    NETGEN_3D_Parameters_1.SetFuseEdges(1)
    NETGEN_3D_Parameters_1.SetQuadAllowed(0)
    NETGEN_3D_Parameters_1.SetCheckChartBoundary(0)
    tungsten_1 = Mesh_1.GroupOnGeom(tungsten, "tungsten", SMESH.VOLUME)
    cu_1 = Mesh_1.GroupOnGeom(cu, "cu", SMESH.VOLUME)
    cucrzr_1 = Mesh_1.GroupOnGeom(cucrzr, "cucrzr", SMESH.VOLUME)
    top_surface_1 = Mesh_1.GroupOnGeom(top_surface, "top_surface", SMESH.FACE)
    cooling_surface_1 = Mesh_1.GroupOnGeom(
        cooling_surface, "cooling_surface", SMESH.FACE
    )
    poloidal_gap_1 = Mesh_1.GroupOnGeom(poloidal_gap, "poloidal_gap", SMESH.FACE)
    toroidal_gap_1 = Mesh_1.GroupOnGeom(toroidal_gap, "toroidal_gap", SMESH.FACE)
    bottom_1 = Mesh_1.GroupOnGeom(bottom, "bottom", SMESH.FACE)
    face_top_pipe_1 = Mesh_1.GroupOnGeom(face_top_pipe, "face_top_pipe", SMESH.FACE)

    NETGEN_3D_Parameters_1.SetFineness(5)
    NETGEN_3D_Parameters_1.SetGrowthRate(0.05)
    NETGEN_3D_Parameters_1.SetNbSegPerEdge(3)
    NETGEN_3D_Parameters_1.SetNbSegPerRadius(5)
    NETGEN_3D_Parameters_1.SetCheckChartBoundary(0)
    NETGEN_3D_Parameters_1.SetMinSize(0.1e-3)
    NETGEN_3D_Parameters_1.SetCheckChartBoundary(0)
    NETGEN_3D_Parameters_1.SetMaxSize(0.3e-3)
    isDone = Mesh_1.Compute()
    [
        tungsten_1,
        cu_1,
        cucrzr_1,
        top_surface_1,
        cooling_surface_1,
        poloidal_gap_1,
        toroidal_gap_1,
        bottom_1,
        face_top_pipe_1,
    ] = Mesh_1.GetGroups()

    ## Set names of Mesh objects
    smesh.SetName(Mesh_1, "Mesh_1")
    smesh.SetName(NETGEN_1D_2D_3D.GetAlgorithm(), "NETGEN 1D-2D-3D")
    smesh.SetName(NETGEN_3D_Parameters_1, "NETGEN 3D Parameters_1")
    smesh.SetName(top_surface_1, "top_surface")
    smesh.SetName(cooling_surface_1, "cooling_surface")
    smesh.SetName(poloidal_gap_1, "poloidal_gap")
    smesh.SetName(toroidal_gap_1, "toroidal_gap")
    smesh.SetName(bottom_1, "bottom")
    smesh.SetName(face_top_pipe_1, "face_top_pipe")
    smesh.SetName(Mesh_1.GetMesh(), "Mesh_1")
    smesh.SetName(cucrzr_1, "cucrzr")
    smesh.SetName(cu_1, "cu")
    smesh.SetName(tungsten_1, "tungsten")

    try:
        Mesh_1.ExportMED(
            "{}mm_thickness/mesh_3D_{}mm.med".format(thickness, thickness),
            auto_groups=0,
            version=41,
            overwrite=1,
            meshPart=None,
            autoDimension=1,
        )
        pass
    except:
        print("ExportMED() failed. Invalid file name?")

    if salome.sg.hasDesktop():
        salome.sg.updateObjBrowser()
