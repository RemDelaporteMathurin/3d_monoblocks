import matplotlib.pyplot as plt
import numpy as np
import matplotx

id_W = 6
id_Cu = 7
id_CuCrZr = 8

baking_temperature = 600
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

total_w = sum([data["Total_{}_volume_{}".format(trap_id, id_W)] for trap_id in [1, 2]])
total_cu = data["Total_{}_volume_{}".format(2, id_Cu)]
total_cucrzr = data["Total_{}_volume_{}".format(2, id_CuCrZr)]
# total_mobile = sum(
#     [
#         data["Total_solute_volume_{}".format(mat_id)]
#         for mat_id in [id_W, id_Cu, id_CuCrZr]
#     ]
# )

relative_total_w = total_w / inventory[0]  # * 100
relative_inventory = inventory / inventory[0]  # * 100
# relative_mobile = total_mobile  # / retention[0]  # * 100

with plt.style.context(matplotx.styles.dufte):
    plt.plot(data["ts"], relative_inventory, marker="+")

    plt.fill_between(
        data["ts"],
        np.zeros(relative_total_w.size),
        relative_total_w,
        alpha=0.3,
    )
    # plt.fill_between(
    #     data["ts"],
    #     relative_total_w,
    #     relative_total_w + relative_mobile,
    #     alpha=0.3,
    # )
    plt.ylim(bottom=0)
    plt.xlabel("Baking time (s)")
    matplotx.ylabel_top("Relative \n inventory (%)")
    plt.tight_layout()
    plt.show()
