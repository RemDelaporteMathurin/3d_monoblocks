import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import matplotx
from matplotx_proxy import label_fillbetween

id_W_top = 9
id_coolant = 10
id_poloidal_gap = 11
id_toroidal_gap = 12
id_bottom = 13
id_top_pipe = 14
TUNGSTEN_SURFACES = [id_poloidal_gap, id_toroidal_gap, id_bottom, id_W_top]


def plot_fluxes(baking_temperature, tmax=None, normalised=True):
    data = np.genfromtxt(
        "baking_temperature={:.0f}K/derived_quantities.csv".format(baking_temperature),
        delimiter=",",
        names=True,
    )

    total_desorption = -sum(
        [
            data["Flux_surface_{}_solute".format(surf_id)]
            for surf_id in TUNGSTEN_SURFACES + [id_coolant, id_top_pipe]
        ]
    )

    t = data["ts"]
    t = t / 3600 / 24

    if tmax:
        indexes = np.where(t <= tmax)
    else:
        indexes = np.where(np.arange(t.size))

    top_desorption = -data["Flux_surface_{}_solute".format(id_W_top)][indexes]
    bot_desorption = -data["Flux_surface_{}_solute".format(id_bottom)][indexes]
    toroidal_desorption = -data["Flux_surface_{}_solute".format(id_toroidal_gap)][
        indexes
    ]
    poloidal_desorption = -data["Flux_surface_{}_solute".format(id_poloidal_gap)][
        indexes
    ]
    coolant_desorption = -data["Flux_surface_{}_solute".format(id_coolant)][indexes]
    top_pipe_desorption = -data["Flux_surface_{}_solute".format(id_top_pipe)][indexes]

    total_flux = sum(
        [
            top_pipe_desorption,
            coolant_desorption,
            poloidal_desorption,
            toroidal_desorption,
            bot_desorption,
            top_desorption,
        ]
    )
    if normalised:
        top_pipe_desorption *= 1 / total_flux[0] * 100
        coolant_desorption *= 1 / total_flux[0] * 100
        poloidal_desorption *= 1 / total_flux[0] * 100
        toroidal_desorption *= 1 / total_flux[0] * 100
        bot_desorption *= 1 / total_flux[0] * 100
        top_desorption *= 1 / total_flux[0] * 100
    t = t[indexes]

    def blue(lightness):
        blue_rgb = list(mcolors.to_rgb("tab:blue")[:])
        blue_rgb = [c + (1 - c) * lightness for c in blue_rgb]
        return blue_rgb

    def orange(lightness):
        orange_rgb = list(mcolors.to_rgb("tab:orange")[:])
        orange_rgb = [c + (1 - c) * lightness for c in orange_rgb]

        return orange_rgb

    plt.fill_between(t, poloidal_desorption, color=blue(0), label="Poloidal gap")
    plt.fill_between(
        t,
        poloidal_desorption,
        poloidal_desorption + top_desorption,
        color=blue(0.2),
        label="Top",
    )
    plt.fill_between(
        t,
        poloidal_desorption + top_desorption,
        poloidal_desorption + top_desorption + toroidal_desorption,
        color=blue(0.4),
        label="Toroidal gap",
    )
    plt.fill_between(
        t,
        top_desorption + poloidal_desorption + toroidal_desorption,
        top_desorption + poloidal_desorption + toroidal_desorption + coolant_desorption,
        color=orange(0),
        label="Coolant",
    )
    plt.fill_between(
        t,
        top_desorption + poloidal_desorption + toroidal_desorption + coolant_desorption,
        top_desorption
        + poloidal_desorption
        + toroidal_desorption
        + coolant_desorption
        + top_pipe_desorption,
        color=orange(0.5),
        label="Top pipe",
    )

    # plt.plot(data["ts"], total_desorption)


with plt.style.context(matplotx.styles.dufte):
    plt.figure(figsize=(6.4 * 1.2, 4.8 * 1.2))

    plot_fluxes(600, tmax=1.1)
    label_fillbetween(fontsize=12)

    plt.ylim(0, 100)
    plt.xlim(0)

    matplotx.ylabel_top("Relative desorption \n flux (%)")
    plt.xlabel("Baking time (days)")
    plt.tight_layout()

    plt.show()
