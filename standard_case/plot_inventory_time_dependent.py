import numpy as np
import matplotlib.pyplot as plt
import matplotx


data_recomb = np.genfromtxt(
    "transient/instant_recomb/derived_quantities.csv", delimiter=",", names=True
)
data_no_recomb = np.genfromtxt(
    "transient/no_recomb/derived_quantities.csv", delimiter=",", names=True
)

data_recomb_s = np.genfromtxt(
    "steady_state/instant_recomb/derived_quantities.csv", delimiter=",", names=True
)
data_no_recomb_s = np.genfromtxt(
    "steady_state/no_recomb/derived_quantities.csv", delimiter=",", names=True
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
    plt.figure(figsize=(7, 5))
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
    plt.ylim(1e13, 1e18)
    matplotx.ylabel_top("Inventory (H)")
    plt.xscale("log")
    plt.xlim(1e3, 1e7)
    plt.xticks([1e3, 1e4, 1e5, 1e6, 1e7])
    matplotx.line_labels()
    plt.xlabel("Time (s)")
    plt.tight_layout()
    plt.savefig("inventory_standard_case_w_wo_recomb.pdf")
    plt.savefig("inventory_standard_case_w_wo_recomb.png")

    plt.show()
