from tkinter import W
from main import (
    my_model,
    heat_transfer_bcs,
    h_implantation_top,
    recombination_flux_coolant,
    instantaneous_recombination_poloidal_W,
    instantaneous_recombination_poloidal_Cu,
    instantaneous_recombination_top_pipe,
    instantaneous_recombination_bottom,
    instantaneous_recombination_toroidal,
    recombination_poloidal_W,
    recombination_poloidal_Cu,
    recombination_toroidal,
    recombination_top_pipe,
    tungsten,
    copper,
    cucrzr,
)
import festim as F
import fenics as f


class AverageSurface(F.DerivedQuantity):
    def __init__(self, field, surface) -> None:
        super().__init__(field)
        self.surface = surface
        self.title = "Average {} surface {}".format(self.field, self.surface)

    def compute(self):
        return f.assemble(self.function * self.ds(self.surface)) / f.assemble(
            1 * self.ds(self.surface)
        )


def run_mb(thickness: float, instant_recomb: int, transient: bool, gap: bool):
    print(
        "\n Running for {} mm  Transient: {} Recomb: {} Gap : {} \n".format(
            thickness, transient, instant_recomb, gap
        )
    )

    folder = "meshes/{}mm_thickness".format(thickness)
    if not gap:
        volume_file = "{}/mesh_cells_no_gap.xdmf".format(folder)
        boundary_file = "{}/mesh_facets_no_gap.xdmf".format(folder)
    else:
        volume_file = "{}/mesh_cells.xdmf".format(folder)
        boundary_file = "{}/mesh_facets.xdmf".format(folder)

    my_model.mesh = F.MeshFromXDMF(volume_file=volume_file, boundary_file=boundary_file)

    folder = "results/{}mm_thickness".format(thickness)
    if transient:
        folder += "/transient"
    else:
        folder += "/steady_state"

    if instant_recomb==1:
        folder += "/instant_recomb"
    else:
        if instant_recomb==2:
            folder += "/recomb"
        else:
            folder += "/no_recomb"


    if not gap:
        folder += "/no_gap"

    print(folder)

    derived_quantities = F.DerivedQuantities(
        [
            F.TotalVolume(field="retention", volume=tungsten.id),
            F.TotalVolume(field="retention", volume=copper.id),
            F.TotalVolume(field="retention", volume=cucrzr.id),
            F.TotalVolume(field="solute", volume=tungsten.id),
            F.TotalVolume(field="solute", volume=copper.id),
            F.TotalVolume(field="solute", volume=cucrzr.id),
            F.SurfaceFlux(
                field="solute", surface=recombination_flux_coolant.surfaces[0]
            ),
            F.SurfaceFlux(
                field="solute", surface=instantaneous_recombination_poloidal_W.surfaces[0]
            ),
            F.SurfaceFlux(
                field="solute", surface=instantaneous_recombination_poloidal_Cu.surfaces[0]
            ),
            F.SurfaceFlux(
                field="solute", surface=instantaneous_recombination_bottom.surfaces[0]
            ),
            F.SurfaceFlux(
                field="solute", surface=instantaneous_recombination_toroidal.surfaces[0]
            ),
            AverageSurface(field="T", surface=recombination_flux_coolant.surfaces[0]),
        ],
        filename="{}/derived_quantities.csv".format(folder),
    )
    if gap:
        derived_quantities.derived_quantities.append(
            F.SurfaceFlux(
                field="solute", surface=instantaneous_recombination_top_pipe.surfaces[0]
            )
        )
    my_model.exports = F.Exports(
        [
            derived_quantities,
            F.XDMFExport("T", folder=folder),
            F.XDMFExport("solute", folder=folder),
            F.XDMFExport("retention", folder=folder),
            F.XDMFExport("1", folder=folder,checkpoint=True),
            F.XDMFExport("2", folder=folder,checkpoint=True),
        ]
    )

    h_transport_bcs = [recombination_flux_coolant]
    my_model.boundary_conditions = heat_transfer_bcs + h_transport_bcs

    if instant_recomb==0:
        my_model.boundary_conditions.append(instantaneous_recombination_toroidal)

    if instant_recomb==1:
        my_model.boundary_conditions.append(instantaneous_recombination_toroidal)
        my_model.boundary_conditions.append(instantaneous_recombination_poloidal_W)
        my_model.boundary_conditions.append(instantaneous_recombination_poloidal_Cu)
        # my_model.boundary_conditions.append(instantaneous_recombination_bottom)
        if gap:
            my_model.boundary_conditions.append(instantaneous_recombination_top_pipe)

    if instant_recomb==2:     
        my_model.boundary_conditions.append(instantaneous_recombination_toroidal)
        my_model.boundary_conditions.append(instantaneous_recombination_poloidal_W)
        my_model.boundary_conditions.append(recombination_poloidal_Cu)
        # my_model.boundary_conditions.append(instantaneous_recombination_bottom)
        if gap:
            my_model.boundary_conditions.append(recombination_top_pipe)

    my_model.boundary_conditions.append(h_implantation_top)  # add it at the end

    if transient:
        my_model.t = 0
        my_model.dt = F.Stepsize(initial_value=1e5, stepsize_change_ratio=1.1)
        my_model.settings.transient = True
        my_model.settings.final_time = 1e5
    else:
        my_model.dt = None
        my_model.settings.transient = False
        my_model.settings.final_time = None

    my_model.initialise()
    my_model.run()


# parametric study thickness
for thickness in [4, 5, 6, 7, 8, 9, 10, 14]:
    for gap in [True]:
        for recomb in [0,1,2]:
            run_mb(thickness, instant_recomb=recomb, transient=True, gap=gap)
