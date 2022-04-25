from main import (
    my_model,
    heat_transfer_bcs,
    h_implantation_top,
    recombination_flux_coolant,
    instantaneous_recombination_lateral,
    tungsten,
    copper,
    cucrzr
)
import FESTIM as F


def run_mb(thickness: float, instant_recomb: bool, transient: bool):
    print("\n Running for {} mm  Transient: {} Recomb: {} \n".format(thickness, transient, instant_recomb))

    folder = "meshes/{}mm_thickness".format(thickness)
    my_model.mesh = F.MeshFromXDMF(
        volume_file="{}/mesh_cells.xdmf".format(folder),
        boundary_file="{}/mesh_facets.xdmf".format(folder),
    )

    folder = "results/{}mm_thickness".format(thickness)
    if transient:
        folder += "/transient"
    else:
        folder += "/steady_state"

    if instant_recomb:
        folder += "/instant_recomb"
    else:
        folder += "/no_recomb"

    print(folder)

    derived_quantities = F.DerivedQuantities(
        [
            F.TotalVolume(field="retention", volume=tungsten.id),
            F.TotalVolume(field="retention", volume=copper.id),
            F.TotalVolume(field="retention", volume=cucrzr.id),
            F.SurfaceFlux(field="solute", surface=recombination_flux_coolant.surfaces[0]),
            F.SurfaceFlux(field="solute", surface=instantaneous_recombination_lateral.surfaces[0]),
        ],
        filename="{}/derived_quantities.csv".format(folder),
    )

    my_model.exports = F.Exports(
        [
            derived_quantities,
            F.XDMFExport("T", folder=folder),
            F.XDMFExport("solute", folder=folder),
            F.XDMFExport("retention", folder=folder),
        ]
    )

    h_transport_bcs = [h_implantation_top, recombination_flux_coolant]
    my_model.boundary_conditions = heat_transfer_bcs + h_transport_bcs

    if instant_recomb:
        my_model.boundary_conditions.append(instantaneous_recombination_lateral)


    if transient:
        my_model.dt = F.Stepsize(initial_value=1e4, stepsize_change_ratio=1.1)
        my_model.settings.transient = True
        my_model.settings.final_time = 1e4
    else:
        my_model.dt = None
        my_model.settings.transient = False
        my_model.settings.final_time = None


    my_model.initialise()
    my_model.run()


# parametric study thickness
for instant_recomb in [True, False]:
    for transient in [True, False]:
        for thickness in [4, 5, 6, 7, 8, 9, 10, 14]:
            run_mb(thickness, instant_recomb=False, transient=True)
