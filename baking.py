import festim as F

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


def run_baking(baking_temperature, instantaneous_recomb, Kr_0=None, E_Kr=None):
    my_model.T = F.Temperature(baking_temperature)

    if instantaneous_recomb:
        instantaneous_recomb_everywhere = F.DirichletBC(
            value=0,
            surfaces=TUNGSTEN_SURFACES + [id_coolant, id_top_pipe],
        )
        my_model.boundary_conditions = [instantaneous_recomb_everywhere]
    else:
        recombination_flux_tungsten = F.RecombinationFlux(
            Kr_0=Kr_0,
            E_Kr=E_Kr,
            order=2,
            surfaces=TUNGSTEN_SURFACES,
        )
        recombination_flux_cupper = F.RecombinationFlux(Kr_0=2.9e-14,E_Kr=1.92,order=2,surfaces=TUNGSTEN_SURFACES)
        my_model.boundary_conditions = [
            recombination_flux_tungsten,
            recombination_flux_coolant,
            recombination_flux_cupper,
        ]

    folder_inicond = "baking/steady_state_exposure"
    my_model.initial_conditions = [
        F.InitialCondition(
            field=1,
            value=folder_inicond + "/trap_1_concentration.xdmf",
            label="trap_1_concentration",
            time_step=-1,
        ),
        F.InitialCondition(
            field=2,
            value=folder_inicond + "/trap_2_concentration.xdmf",
            label="trap_2_concentration",
            time_step=-1,
        ),
    ]

    my_model.settings.transient = True
    my_model.settings.final_time = 3600 * 24 * 30.0
    my_model.settings.absolute_tolerance = 1e0

    my_model.dt = F.Stepsize(3000.0, stepsize_change_ratio=1.1)

    export_folder = "baking/baking_temperature={:.0f}K".format(baking_temperature)
    if not instantaneous_recomb:
        export_folder += "/non_instant_recomb_Kr_0={:.2e}_E_Kr={:.2e}".format(
            Kr_0, E_Kr
        )
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
    #        F.XDMFExport(
    #            "solute", filename=export_folder + "/mobile_concentration.xdmf"
    #        ),
    #        F.XDMFExport("1", filename=export_folder + "/trap_1_w.xdmf"),
    #        F.XDMFExport("2", filename=export_folder + "/trap_multi.xdmf"),
    #        F.XDMFExport("retention", filename=export_folder + "/retention.xdmf"),
            derived_quantities,
        ]
    )
    # my_model.log_level = 20
    my_model.initialise()
    my_model.run()


if __name__ == "__main__":
    # run_steady_state_exposure()

    # run_baking(baking_temperature=673, instantaneous_recomb=True)
    run_baking(
        baking_temperature=473, instantaneous_recomb=False, Kr_0=3.2e-15, E_Kr=1.16
    )


#   Anderl  10.1016/S0022-3115(98)00878-2 CuCrZe    Kr_0: 2.9e-14,     "act_energy": 1.92,