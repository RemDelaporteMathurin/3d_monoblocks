import matplotlib.pyplot as plt
from matplotlib import cm
import matplotx
import numpy as np

id_W = 6
id_Cu = 7
id_CuCrZr = 8

Kr_0 = 3.2e-15
E_Kr = 1.16
k_B = 8.617e-5


def plot_inventory(baking_temperature, instant_recomb=True, verbose=False, **kwargs):
    folder = "d:/Logiciels/3d_monoblocks_bis/baking/baking_temperature={:.0f}K/".format(baking_temperature)
    if not instant_recomb:
        folder += "non_instant_recomb_Kr_0={:.2e}_E_Kr={:.2e}/".format(Kr_0, E_Kr)
    data = np.genfromtxt(
        folder + "derived_quantities.csv",
        delimiter=",",
        names=True,
    )

    inventory = sum(
        [
            data["Total_retention_volume_{}".format(vol_id)]
            for vol_id in [id_W, id_Cu, id_CuCrZr]
        ]
    )
    if verbose:
        mass = inventory[0] / 6.022e23 * 1.00794
        print("Initial inventory: {:.2e} H   {:.2e} g".format(inventory[0], mass))

    relative_inventory = inventory / inventory[0] * 100

    plt.plot(data["ts"] / 3600 / 24, relative_inventory, **kwargs)


if __name__ == "__main__":
    T = np.linspace(500, 673, num=100)
    Anderl_recomb = Kr_0 * np.exp(-E_Kr / k_B / T)
    Ogorodnikova_recomb = 3e-25 / T**0.5 * np.exp(2.06 / k_B / T)

    with plt.style.context(matplotx.styles.dufte):
        plt.plot(T, Anderl_recomb, label="Anderl")
        plt.plot(T, Ogorodnikova_recomb, label="Ogorodnikova")
        # plt.ylim(bottom=0)
        plt.yscale("log")
        matplotx.line_labels()
        matplotx.ylabel_top("Recombination \n coefficient \n (m$^4$ s$^{-1}$)")
        plt.xlabel("Temperature (K)")
        plt.tight_layout()
        plt.show()

        plt.figure()
        min_T_colour, max_T_colour = 400, 673
        for T in [550, 600, 673]:
            plot_inventory(
                baking_temperature=T,
                label="{} K".format(T),
                color=cm.Reds((T - min_T_colour) / (max_T_colour - min_T_colour)),
            )
            plot_inventory(
                baking_temperature=T,
                instant_recomb=False,
                linestyle="dashed",
                color=cm.Reds((T - min_T_colour) / (max_T_colour - min_T_colour)),
            )
        matplotx.ylabel_top("Relative \n inventory (%)")
        plt.xlabel("Baking time (days)")
        plt.ylim(bottom=-5)
        matplotx.line_labels()
        plt.tight_layout()
        plt.show()
