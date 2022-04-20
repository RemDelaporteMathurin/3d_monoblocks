import FESTIM as F
from numpy import isin

import properties

id_W = 6  # volume W
id_Cu = 7  # volume Cu
id_CuCrZr = 8  # volume CuCrZr
id_W_top = 9
id_coolant = 10
id_lateral = 11

my_model = F.Simulation()

# Mesh
folder = "meshes/4mm_thickness"
my_model.mesh = F.MeshFromXDMF(
    volume_file="{}/mesh_cells.xdmf".format(folder),
    boundary_file="{}/mesh_facets.xdmf".format(folder),
)

# Materials
tungsten = F.Material(
    id=id_W,
    D_0=4.1e-7,
    E_D=0.39,
    S_0=1.87e24,
    E_S=1.04,
    thermal_cond=properties.thermal_cond_W,
    heat_capacity=properties.rhoCp_W,
    rho=1,
)

copper = F.Material(
    id=id_Cu,
    D_0=6.6e-7,
    E_D=0.387,
    S_0=3.14e24,
    E_S=0.572,
    thermal_cond=properties.thermal_cond_Cu,
    heat_capacity=properties.rhoCp_Cu,
    rho=1,
)

cucrzr = F.Material(
    id=id_CuCrZr,
    D_0=3.92e-7,
    E_D=0.418,
    S_0=4.28e23,
    E_S=0.387,
    thermal_cond=properties.thermal_cond_CuCrZr,
    heat_capacity=properties.rhoCp_CuCrZr,
    rho=1,
)

my_model.materials = F.Materials([tungsten, copper, cucrzr])

# traps
my_model.traps = F.Traps([])


# traps = [

#     {
#         # W_1
#         "k_0": 8.96e-17,
#         "E_k": 0.39,
#         "p_0": 1e13,
#         "E_p": 0.87,
#         "density": 1.3e-3*atom_density_W,
#         "materials": id_W,
#     },
#     {
#         # conglomérat de piège W_2, piège Cu, piège CuCrZr          # à mettre en commentaire si utilisation des propriétés des MTX indépendemment
#         # permet de réduire le temps de calcul voir PR#291
#         "k_0": [8.96e-17, 6e-17, 1.2e-16],
#         "E_k": [0.39, 0.39, 0.42],
#         "p_0": [1e13, 8e13, 8e13],
#         "E_p": [1.0, 0.5, 0.85],
#         "density": [4e-4*atom_density_W, 5e-5*atom_density_Cu, 5e-5*atom_density_CuCrZr],
#         "materials": [id_W, id_Cu, id_CuCrZr],
#     },

# ]

# parameters["traps"] = traps

# temperature
my_model.T = F.HeatTransferProblem(transient=False)


# boundary conditions
heat_transfer_bcs = [
    F.FluxBC(surfaces=id_W_top, value=10e6, field="T"),
    F.ConvectiveFlux(h_coeff=7e04, T_ext=323, surfaces=id_coolant),
]

h_transport_bcs = [
    F.ImplantationDirichlet(
        surfaces=id_W_top, phi=1.61e22, R_p=9.52e-10, D_0=4.1e-7, E_D=0.39
    ),
    F.RecombinationFlux(Kr_0=2.9e-14, E_Kr=1.92, order=2, surfaces=id_coolant),
    F.DirichletBC(value=0, surfaces=id_lateral),
]


my_model.boundary_conditions = heat_transfer_bcs + h_transport_bcs

my_model.settings = F.Settings(
    absolute_tolerance=1e4,
    relative_tolerance=1e-5,
    maximum_iterations=15,
    traps_element_type="DG",
    chemical_pot=True,
    transient=False,
)

# parametric study thickness
for thickness in [4, 5, 6, 7, 8, 9, 10]:

    print("\n Running for {} mm \n".format(thickness))

    folder = "meshes/{}mm_thickness".format(thickness)
    my_model.mesh = F.MeshFromXDMF(
        volume_file="{}/mesh_cells.xdmf".format(folder),
        boundary_file="{}/mesh_facets.xdmf".format(folder),
    )

    my_model.exports = F.Exports(
        [
            F.XDMFExport("T", folder="results/{}mm_thickness".format(thickness)),
            F.XDMFExport("solute", folder="results/{}mm_thickness".format(thickness)),
        ]
    )

    my_model.initialise()
    my_model.run()
