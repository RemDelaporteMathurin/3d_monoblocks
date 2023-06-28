import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib import cm
import numpy as np
import matplotx
from matplotx_proxy import label_fillbetween

instant_recomb = True

id_W_top = 9
id_coolant = 10
id_poloidal_gap_W = 11
id_poloidal_gap_Cu = 12
id_toroidal_gap = 13
id_bottom = 14
id_top_pipe = 15
TUNGSTEN_SURFACES = [id_poloidal_gap_W, id_toroidal_gap, id_bottom, id_W_top]


def plot_flux(baking_temperature, tmax=None, normalised=False, **kwargs):
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
    baking_temperature, tmax=None, normalised=False, contributions=False
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

    labels = ["Poloidal gap", "Top", "Toroidal gap", "Coolant", "Top pipe",]
    colors = [blue(0), blue(0.2), blue(0.4), orange(0), orange(0.5),]
    plt.stackplot(t, poloidal_desorption, top_desorption, toroidal_desorption, coolant_desorption, top_pipe_desorption, labels=labels, colors=colors)


def get_fluxes(baking_temperature, tmax, normalised):

    if instant_recomb:
        data = np.genfromtxt(
            "4mm-baking_temperature={:.0f}K/derived_quantities.csv".format(baking_temperature),
            delimiter=",",
            names=True,
        )
    else:
        data = np.genfromtxt(
            "4mm-baking_temperature={:.0f}K/non_instant_recomb_Kr_0=3.20e-15_E_Kr=1.16e+00/derived_quantities.csv".format(baking_temperature),
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
    poloidal_desorption = -data["Flux_surface_{}_solute".format(id_poloidal_gap_W)][
        indexes
    ]-data["Flux_surface_{}_solute".format(id_poloidal_gap_Cu)][
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
    width = 0.9
    total_toks, total_coolants, normalized_toks = [], [], []
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
        normalized_toks.append((total_top + total_toroidal + total_poloidal + total_top_pipe)/(total_top + total_toroidal + total_poloidal + total_top_pipe+total_coolant))

    print(normalized_toks)

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
    


    plt.xticks(pos, ["{:.0f} K".format(T) for T in bake_temps])


def evolution_fluxes_contributions(T_baking):

    plt.figure(figsize=(6.4 * 1.2, 4.8 * 1.2))

    plot_fluxes_stacked(T_baking, tmax=30, contributions=True)
    label_fillbetween(fontsize=10)

    plt.ylim(0, 100)
    plt.xlim(0,30)

    matplotx.ylabel_top("Relative \n desorption (%)")
    plt.xlabel("Baking time (days)")
    plt.tight_layout()


def plot_results():
    bake_temps = [473,498,513,538,573,598,623,673]

    # ######### area plots

    for T_baking in [498,623]:
        evolution_fluxes_contributions(T_baking)
        if instant_recomb:
            plt.savefig(f'flux_contributions_proportion_vs_time_T={T_baking:.0f}K.pdf')
        else:
            plt.savefig(f'flux_contributions_proportion_vs_time_T={T_baking:.0f}K_noninstant_recomb.pdf')

    plt.figure()
    barchart_total_desorption(bake_temps)
    plt.xlabel("Baking temperature")
    plt.ylabel("Total H desorbed (H)")
    plt.legend()
    plt.ylim([0, 1.6e14])
    plt.tight_layout()
    if instant_recomb:
        plt.title('Instantaneous recombination')
        plt.savefig('baking_total_desorption.png',dpi=300)
    else:
        plt.title('Non instantaneous recombination')
        plt.savefig('recomb_baking_total_desorption.png',dpi=300)
    plt.show()


if __name__ == "__main__":
    with plt.style.context(matplotx.styles.dufte):
        plot_results()
