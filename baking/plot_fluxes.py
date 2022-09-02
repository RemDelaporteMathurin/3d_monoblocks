import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib import cm
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


def plot_flux(baking_temperature, tmax=None, normalised=True, **kwargs):
    (
        t,
        top_desorption,
        toroidal_desorption,
        poloidal_desorption,
        coolant_desorption,
        top_pipe_desorption,
    ) = get_fluxes(baking_temperature, tmax, normalised)

    total_flux = sum(
        [
            top_desorption,
            toroidal_desorption,
            poloidal_desorption,
            coolant_desorption,
            top_pipe_desorption,
        ]
    )
    plt.plot(t, total_flux, label="{} K".format(baking_temperature), **kwargs)


def plot_fluxes_stacked(
    baking_temperature, tmax=None, normalised=True, contributions=False
):
    (
        t,
        top_desorption,
        toroidal_desorption,
        poloidal_desorption,
        coolant_desorption,
        top_pipe_desorption,
    ) = get_fluxes(baking_temperature, tmax, normalised)

    if contributions:
        total_flux = (
            top_desorption
            + toroidal_desorption
            + poloidal_desorption
            + coolant_desorption
            + top_pipe_desorption
        )
        top_desorption *= 100 / total_flux
        toroidal_desorption *= 100 / total_flux
        poloidal_desorption *= 100 / total_flux
        coolant_desorption *= 100 / total_flux
        top_pipe_desorption *= 100 / total_flux

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


def get_fluxes(baking_temperature, tmax, normalised):
    data = np.genfromtxt(
        "baking_temperature={:.0f}K/derived_quantities.csv".format(baking_temperature),
        delimiter=",",
        names=True,
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

    return (
        t,
        top_desorption,
        toroidal_desorption,
        poloidal_desorption,
        coolant_desorption,
        top_pipe_desorption,
    )


def total_desorbed_quantities(baking_temperature):
    (
        t,
        top_desorption,
        toroidal_desorption,
        poloidal_desorption,
        coolant_desorption,
        top_pipe_desorption,
    ) = get_fluxes(baking_temperature, tmax=30, normalised=False)

    t_in_s = t * 3600 * 24

    total_top = np.trapz(top_desorption, t_in_s)
    total_toroidal = np.trapz(toroidal_desorption, t_in_s)
    total_poloidal = np.trapz(poloidal_desorption, t_in_s)
    total_coolant = np.trapz(coolant_desorption, t_in_s)
    total_top_pipe = np.trapz(top_pipe_desorption, t_in_s)

    return total_top, total_toroidal, total_poloidal, total_coolant, total_top_pipe


def barchart_total_desorption(bake_temps):
    width = 0.2
    total_toks, total_coolants = [], []
    for T_baking in bake_temps:
        (
            total_top,
            total_toroidal,
            total_poloidal,
            total_coolant,
            total_top_pipe,
        ) = total_desorbed_quantities(T_baking)
        total_toks.append(total_top + total_toroidal + total_poloidal + total_top_pipe)
        total_coolants.append(total_coolant)

    # correction for 673K
    # because the flux is so high, this correction is needed to acount for the initial step error
    ind_673 = bake_temps.index(673)
    ind_600 = bake_temps.index(600)

    total_600 = total_toks[ind_600] + total_coolants[ind_600]
    total_673 = total_toks[ind_673] + total_coolants[ind_673]
    diff = total_600 - total_673

    total_toks[ind_673] += diff * 0.85
    total_coolants[ind_673] += diff * 0.25

    pos = np.arange(len(bake_temps))
    plt.bar(pos, total_toks, width=width, color="tab:blue", label="Vessel")
    plt.bar(
        pos,
        total_coolants,
        width=width,
        color="tab:orange",
        label="Coolant",
        bottom=total_toks,
    )

    plt.xticks(pos, bake_temps)


def evolution_fluxes_contributions(T_baking):
    plt.figure(figsize=(6.4 * 1.2, 4.8 * 1.2))

    plot_fluxes_stacked(T_baking, tmax=1.1, contributions=False)
    label_fillbetween(fontsize=12)

    plt.ylim(0, 100)
    plt.xlim(0)

    matplotx.ylabel_top("Relative desorption \n flux (%)")
    plt.xlabel("Baking time (days)")
    plt.tight_layout()

    plt.savefig("flux_contributions_vs_time.pdf")

    plt.figure(figsize=(6.4 * 1.2, 4.8 * 1.2))

    plot_fluxes_stacked(T_baking, tmax=30, contributions=True)
    label_fillbetween(fontsize=12)

    plt.ylim(0, 100)
    plt.xlim(0)

    matplotx.ylabel_top("Relative desorption \n flux (%)")
    plt.xlabel("Baking time (days)")
    plt.tight_layout()


def flux_vs_time(bake_temps, min_T_colour, max_T_colour):
    fig, axs = plt.subplots(
        ncols=1, nrows=len(bake_temps), sharex=True, figsize=(6.4, 4.8)
    )
    for ax, T_baking in zip(axs, bake_temps):
        plt.sca(ax)
        plot_flux(
            T_baking,
            normalised=False,
            color=cm.Reds((T_baking - min_T_colour) / (max_T_colour - min_T_colour)),
        )
        plt.ylim(
            bottom=-plt.gca().get_ylim()[1] * 0.1,
        )
        plt.xlim(left=0)
        matplotx.line_labels()

    # label_fillbetween(fontsize=12)

    plt.sca(axs[1])
    plt.ylabel(
        "Desorption \n flux (H/m2/s) \n",
        rotation=0,
        verticalalignment="center",
        horizontalalignment="right",
    )
    plt.sca(axs[-1])
    plt.xlabel("Baking time (days)")
    plt.tight_layout()


def plot_results():
    bake_temps = [500, 520, 550, 573, 600, 673]
    min_T_colour, max_T_colour = min(bake_temps) - 100, max(bake_temps)

    with plt.style.context(matplotx.styles.dufte):

        # ######### area plots

        for T_baking in [500, 550, 673]:
            evolution_fluxes_contributions(T_baking)
            plt.savefig(
                "flux_contributions_proportion_vs_time_T={:.0f}K.pdf".format(T_baking)
            )

        # ######### Bar chart plot

        plt.figure()
        barchart_total_desorption(bake_temps)
        plt.xlabel("Baking temperature (K)")
        plt.ylabel("Total H desorbed (H)")
        plt.legend()
        plt.tight_layout()

        # ######### All non-normalised fluxes on 1 plot

        plt.figure(figsize=(6.4, 4.8))
        for T_baking in bake_temps:
            plot_flux(
                T_baking,
                normalised=True,
                color=cm.Reds(
                    (T_baking - min_T_colour) / (max_T_colour - min_T_colour)
                ),
            )

        plt.ylim(-10, 100)
        plt.xlim(0)

        matplotx.line_labels()
        matplotx.ylabel_top("Relative desorption \n flux (%)")
        plt.xlabel("Baking time (days)")
        plt.tight_layout()

        sub_bake_temps = bake_temps[1::2]

        # ######### 3 non-normalised fluxes on 3 plots

        flux_vs_time(sub_bake_temps, min_T_colour, max_T_colour)
        plt.savefig("flux_vs_time.pdf")

        # ######### 3 non-normalised fluxes on 1 plot
        plt.figure()
        for T_baking in sub_bake_temps:
            plot_flux(
                T_baking,
                tmax=10,
                normalised=False,
                color=cm.Reds(
                    (T_baking - min_T_colour) / (max_T_colour - min_T_colour)
                ),
            )

        plt.xlim(0)

        matplotx.line_labels()
        matplotx.ylabel_top("Desorption flux")
        plt.xlabel("Baking time (days)")
        plt.tight_layout()

        plt.show()


if __name__ == "__main__":
    plot_results()
