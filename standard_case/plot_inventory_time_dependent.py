import numpy as np
import matplotlib.pyplot as plt
import matplotx


data_recomb = np.genfromtxt(
    "instant_recomb/derived_quantities.csv", delimiter=",", names=True
)
data_no_recomb = np.genfromtxt(
    "no_recomb/derived_quantities.csv", delimiter=",", names=True
)

inventory_no_recomb = sum(
    [data_no_recomb["Total_retention_volume_{}".format(vol_id)] for vol_id in [6, 7, 8]]
)
inventory_no_recomb *= 4  # for the whole MB

inventory_recomb = sum(
    [data_recomb["Total_retention_volume_{}".format(vol_id)] for vol_id in [6, 7, 8]]
)
inventory_recomb *= 4  # for the whole MB

difference = [
    100 * abs(w - wo) / w for w, wo in zip(inventory_recomb, inventory_no_recomb)
]

with plt.style.context(matplotx.styles.dufte):
    fig, axs = plt.subplots(2, 1, sharex=True, figsize=(6.4, 4.8 * 1.5))
    plt.sca(axs[0])

    plt.plot(
        data_no_recomb["ts"],
        inventory_no_recomb,
        label="No recombination",
        color="tab:blue",
    )

    plt.plot(
        data_recomb["ts"],
        inventory_recomb,
        label="Instantaneous \n recombination",
        color="tab:blue",
    )
    plt.fill_between(
        data_no_recomb["ts"], inventory_no_recomb, inventory_recomb, alpha=0.2
    )
    plt.yscale("log")
    # plt.ylim(bottom=0)
    plt.ylim(1e14, 1e16)
    matplotx.ylabel_top("Inventory (H)")
    plt.xlabel("Time (s)")
    plt.xscale("log")
    matplotx.line_labels()
    plt.tight_layout()
    plt.sca(axs[1])

    plt.xlabel("Thickness $e$ (mm)")
    plt.plot(data_no_recomb["ts"], difference)
    plt.ylim(bottom=0)
    matplotx.ylabel_top("Relative \n difference (%)")
    plt.tight_layout()
    plt.show()
