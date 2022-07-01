import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import matplotx
from labellines import labelLine, labelLines

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


if __name__ == "__main__":
    with plt.style.context(matplotx.styles.dufte):
        min_T_colour, max_T_colour = 500, 673
        for T in [573, 600, 673]:
            # plt.annotate(r"$T_\mathrm{baking}" + " = {} K$".format(T), (0.5e6, 60))
            plot_inventory(
                baking_temperature=T,
                color=cm.Reds((T - min_T_colour) / (max_T_colour - min_T_colour)),
            )

        labelLines(
            plt.gca().get_lines(),
            yoffsets=0.01,
            align=True,
            backgroundcolor="none",
            xvals=[7e5 / 3600 / 24, 3.4e5 / 3600 / 24, 3e5 / 3600 / 24],
        )
        # label axis
        matplotx.ylabel_top("Relative \n inventory (%)")
        plt.xlabel("Baking time (days)")
        plt.ylim(bottom=-5)

        plt.tight_layout()
        plt.show()
