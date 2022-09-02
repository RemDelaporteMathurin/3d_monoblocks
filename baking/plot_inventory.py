import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import matplotx

id_W = 6
id_Cu = 7
id_CuCrZr = 8


def plot_inventory(baking_temperature, **kwargs):

    data = np.genfromtxt(
        "baking_temperature={:.0f}K/derived_quantities.csv".format(baking_temperature),
        delimiter=",",
        names=True,
    )

    inventory = sum(
        [
            data["Total_retention_volume_{}".format(vol_id)]
            for vol_id in [id_W, id_Cu, id_CuCrZr]
        ]
    )

    relative_inventory = inventory / inventory[0] * 100

    plt.plot(
        data["ts"] / 3600 / 24,
        relative_inventory,
        label="{} K".format(baking_temperature),
        **kwargs
    )


def plot_results():
    with plt.style.context(matplotx.styles.dufte):
        plt.figure(figsize=(6.4, 6))
        min_T_colour, max_T_colour = 400, 673
        for T in [500, 673, 573, 550, 520, 600]:
            plot_inventory(
                baking_temperature=T,
                color=cm.Reds((T - min_T_colour) / (max_T_colour - min_T_colour)),
            )

        # label axis
        matplotx.ylabel_top("Relative \n inventory (%)")
        plt.xlabel("Baking time (days)")
        plt.ylim(bottom=-5)

        matplotx.line_labels()
        plt.tight_layout()
        plt.savefig("relative_inventory_vs_time.pdf")

        plt.show()


if __name__ == "__main__":
    plot_results()
