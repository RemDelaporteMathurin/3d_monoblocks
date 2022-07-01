import FESTIM as F

from main import (
    my_model,
    id_poloidal_gap,
    id_toroidal_gap,
    id_bottom,
    id_W_top,
    id_top_pipe,
    id_coolant,
    recombination_flux_coolant,
)


TUNGSTEN_SURFACES = [id_poloidal_gap, id_toroidal_gap, id_bottom, id_W_top]


def run_steady_state_exposure():
    folder = "baking/steady_state_exposure"
    my_model.exports = F.Exports(
        [
            F.XDMFExport("solute", filename=folder + "/mobile_concentration.xdmf"),
            F.XDMFExport("1", filename=folder + "/trap_1_w.xdmf", label="trap_1_w"),
            F.XDMFExport("2", filename=folder + "/trap_multi.xdmf", label="trap_multi"),
            F.XDMFExport("retention", filename=folder + "/retention.xdmf"),
        ]
    )

    my_model.initialise()
    my_model.run()


def run_baking(baking_temperature, instantaneous_recomb, Kr_0_W, E_Kr_W):
    my_model.T = F.Temperature(baking_temperature)

    recombination_flux_tungsten = F.RecombinationFlux(
        Kr_0=Kr_0_W,
        E_Kr=E_Kr_W,
        order=2,
        surfaces=TUNGSTEN_SURFACES,
    )

    instantaneous_recomb_everywhere = F.DirichletBC(
        value=0,
        surfaces=TUNGSTEN_SURFACES + [id_coolant, id_top_pipe],
    )
    if instantaneous_recomb:
        my_model.boundary_conditions = [instantaneous_recomb_everywhere]
    else:
        my_model.boundary_conditions = [
            recombination_flux_tungsten,
            recombination_flux_coolant,
        ]

    folder_inicond = "baking/steady_state_exposure"
    my_model.initial_conditions = [
        F.InitialCondition(
            field=1,
            value=folder_inicond + "/trap_1_w.xdmf",
            label="trap_1_w",
            time_step=-1,
        ),
        F.InitialCondition(
            field=2,
            value=folder_inicond + "/trap_multi.xdmf",
            label="trap_multi",
            time_step=-1,
        ),
    ]

    my_model.settings.transient = True
    my_model.settings.final_time = 3600 * 24 * 30
    my_model.settings.absolute_tolerance = 1e0

    my_model.dt = F.Stepsize(3600, stepsize_change_ratio=1.1)

    export_folder = "baking/baking_temperature={:.0f}K".format(baking_temperature)
    derived_quantities = F.DerivedQuantities(
        [
            F.TotalVolume(field=field, volume=mat.id)
            for mat in my_model.materials.materials
            for field in ["solute", "1", "2", "retention"]
        ]
        + [
            F.SurfaceFlux(field="solute", surface=id_surf)
            for id_surf in [
                id_poloidal_gap,
                id_toroidal_gap,
                id_bottom,
                id_W_top,
                id_top_pipe,
                id_coolant,
            ]
        ],
        filename=export_folder + "/derived_quantities.csv",
        nb_iterations_between_exports=1,
    )
    my_model.exports = F.Exports(
        [
            F.XDMFExport(
                "solute", filename=export_folder + "/mobile_concentration.xdmf"
            ),
            F.XDMFExport("1", filename=export_folder + "/trap_1_w.xdmf"),
            F.XDMFExport("2", filename=export_folder + "/trap_multi.xdmf"),
            F.XDMFExport("retention", filename=export_folder + "/retention.xdmf"),
            derived_quantities,
        ]
    )
    # my_model.log_level = 20
    my_model.initialise()
    my_model.run()


if __name__ == "__main__":
    run_steady_state_exposure()
    run_baking(
        baking_temperature=200 + 273.15, instantaneous_recomb=True, Kr_0_W=1, E_Kr_W=0
    )
    run_baking(
        baking_temperature=300 + 273.15, instantaneous_recomb=True, Kr_0_W=1, E_Kr_W=0
    )
    run_baking(baking_temperature=500, instantaneous_recomb=True, Kr_0_W=1, E_Kr_W=0)
