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
    folder = "4mm-baking_temperature={:.0f}K/".format(baking_temperature)
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
    T = np.linspace(473, 673, num=100)
    Anderl_recomb = Kr_0 * np.exp(-E_Kr / k_B / T)
    Ogorodnikova_recomb = 3e-25 / T**0.5 * np.exp(2.06 / k_B / T)
    Cupper_recomb = 2.9e-14 * np.exp(-1.92 / k_B / T)

    #with plt.style.context(matplotx.styles.dufte):
    plt.plot(T, Anderl_recomb, label="W (Anderl)")
    plt.plot(T, Ogorodnikova_recomb, label="W (Ogorodnikova)")
    plt.plot(T, Cupper_recomb, label="Cu (Anderl)")
    # plt.ylim(bottom=0)
    plt.yscale("log")
    #matplotx.line_labels()
    plt.legend()
    plt.grid()
    plt.xlim(473,673)
    plt.ylabel("Recombination coefficient (m$^4$ s$^{-1}$)")
    plt.xlabel("Temperature (K)")
    plt.tight_layout()
    plt.savefig('coef_recom.png',dpi=300)
    plt.show()


    plt.figure()
    min_T_colour, max_T_colour = 453, 693
    for T in [473,498,513,538,573,598,623,673]:
        plot_inventory(
            baking_temperature=T,
            label="{} K ({}°C)".format(T,T-273),
            color=cm.jet((T - min_T_colour) / (max_T_colour - min_T_colour)),
        )
        plot_inventory(
            baking_temperature=T,
            instant_recomb=False,
            linestyle="dashed",
            color=cm.jet((T - min_T_colour) / (max_T_colour - min_T_colour)),
        )
    plt.xlabel("Baking time (days)")
    plt.ylabel("Relative inventory (%)")
    plt.ylim(bottom=-5)
    plt.grid()
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    #plt.subplots_adjust(right=0.75)
    plt.show()
