import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import matplotx

id_W = 6
id_Cu = 7
id_CuCrZr = 8


def plot_inventory(baking_temperature, verbose=False, **kwargs):

    if recomb:
        data = np.genfromtxt(
            "4mm-baking_temperature={:.0f}K/non_instant_recomb_Kr_0=3.20e-15_E_Kr=1.16e+00/derived_quantities.csv".format(baking_temperature),
            delimiter=",",
            names=True,
        )
    else:
        data = np.genfromtxt(
            "4mm-baking_temperature={:.0f}K/derived_quantities.csv".format(baking_temperature),
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

    plt.plot(
        data["ts"] / 3600 / 24,
        relative_inventory,
        label="{} K".format(baking_temperature),
        **kwargs
    )


def plot_results(verbose=False):
    with plt.style.context(matplotx.styles.dufte):
        plt.figure(figsize=(6.4, 6))
        min_T_colour, max_T_colour = 400, 673
        for T in [473,498,513,538,573,598,623,673]:
            plot_inventory(
                baking_temperature=T,
                color=cm.Reds((T - min_T_colour) / (max_T_colour - min_T_colour)),
                verbose=verbose,
            )

        # label axis
        matplotx.ylabel_top("Relative \n inventory (%)")
        plt.xlabel("Baking time (days)")
        plt.ylim(bottom=-2)
        plt.xlim([0, 30])
        
        matplotx.line_labels()

        #plt.savefig("relative_inventory_vs_time.pdf")

        if recomb:
            plt.tight_layout()
            plt.savefig("noninstant_recomb_relative_inventory_vs_time.pdf")
        else:
            plt.tight_layout()
            plt.savefig("instant_recomb_relative_inventory_vs_time.pdf")


        plt.show()

if __name__ == "__main__":

    for recomb in [True, False]:
        plot_results(verbose=True)
