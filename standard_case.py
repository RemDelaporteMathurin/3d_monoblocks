from main import (
    my_model,
    heat_transfer_bcs,
    h_implantation_top,
    recombination_flux_coolant,
    instantaneous_recombination_poloidal,
    instantaneous_recombination_top_pipe,
    instantaneous_recombination_bottom,
    instantaneous_recombination_toroidal,
    tungsten,
    copper,
    cucrzr,
)

import FESTIM as F


def add_bcs(model: F.Simulation, recomb: bool):
    h_transport_bcs = [recombination_flux_coolant]

    h_transport_bcs.append(instantaneous_recombination_toroidal)
    if recomb:
        h_transport_bcs.append(instantaneous_recombination_poloidal)
    # h_transport_bcs.append(instantaneous_recombination_bottom)
    h_transport_bcs.append(instantaneous_recombination_top_pipe)
    h_transport_bcs.append(h_implantation_top)  # add it at the end

    model.boundary_conditions = heat_transfer_bcs + h_transport_bcs


def add_exports(model: F.Simulation, recomb: bool):
    folder = "standard_case"

    if recomb:
        folder += "/instant_recomb"
    else:
        folder += "/no_recomb"

    print(folder)

    derived_quantities = F.DerivedQuantities(
        [
            F.TotalVolume(field="retention", volume=tungsten.id),
            F.TotalVolume(field="retention", volume=copper.id),
            F.TotalVolume(field="retention", volume=cucrzr.id),
            F.SurfaceFlux(
                field="solute", surface=recombination_flux_coolant.surfaces[0]
            ),
            F.SurfaceFlux(
                field="solute", surface=instantaneous_recombination_poloidal.surfaces[0]
            ),
            F.SurfaceFlux(
                field="solute", surface=instantaneous_recombination_top_pipe.surfaces[0]
            ),
            F.SurfaceFlux(
                field="solute", surface=instantaneous_recombination_bottom.surfaces[0]
            ),
            F.SurfaceFlux(
                field="solute", surface=instantaneous_recombination_toroidal.surfaces[0]
            ),
        ],
        filename="{}/derived_quantities.csv".format(folder),
    )

    model.exports = F.Exports(
        [
            derived_quantities,
            F.XDMFExport("T", folder=folder),
            F.XDMFExport("solute", folder=folder),
            F.XDMFExport("retention", folder=folder),
        ]
    )


my_model.settings.transient = True
my_model.settings.final_time = 1e6

# with instantaneous recombination
my_model.t = 0
my_model.dt = F.Stepsize(initial_value=1e3, stepsize_change_ratio=1.1)

add_bcs(my_model, recomb=True)
add_exports(my_model, recomb=True)

my_model.initialise()
my_model.run()


# without instantaneous recombination
my_model.t = 0
my_model.dt = F.Stepsize(initial_value=1e3, stepsize_change_ratio=1.1)

add_bcs(my_model, recomb=False)
add_exports(my_model, recomb=False)

my_model.initialise()
my_model.run()
