import numpy as np
import matplotlib.pyplot as plt
import matplotx

transient = True
thicknesses = [4, 5, 6, 7, 8, 9, 10, 14]
retention_w = []
retention_wo = []
time = 1e4
for instant_recomb in [True, False]:
    for thickness in thicknesses:
        folder = "{}mm_thickness".format(thickness)
        if transient:
            folder += "/transient"
        else:
            folder += "/steady_state"
        if instant_recomb:
            folder += "/instant_recomb"
        else:
            folder += "/no_recomb"
        data = np.genfromtxt(
            "{}/no_gap/derived_quantities.csv".format(folder), delimiter=",", names=True
        )
        index = np.where(data["ts"] == time)[0][0]
        if index != 0:
            raise ValueError(
                "More than one entry found in derived quantities, please adapt code."
            )
        retention = sum(
            [data["Total_retention_volume_{}".format(vol_id)] for vol_id in [6, 7, 8]]
        ) / (thickness * 1e-3)
        if instant_recomb:
            retention_w.append(retention)
        else:
            retention_wo.append(retention)

ratio = [w / wo for w, wo in zip(retention_w, retention_wo)]
difference = [100 * abs(w - wo) / w for w, wo in zip(retention_w, retention_wo)]

with plt.style.context(matplotx.styles.dufte):
    fig, axs = plt.subplots(2, 1, sharex=True, figsize=(6.4, 4.8 * 1.5))
    plt.sca(axs[0])
    plt.title("No CuCrZr \n extrusion")
    plt.plot(
        thicknesses,
        retention_w,
        color="tab:blue",
        label="Instantaneous \n recombination",
    )
    plt.plot(thicknesses, retention_wo, color="tab:blue", label="No recombination")
    plt.fill_between(thicknesses, retention_w, retention_wo, alpha=0.3)
    matplotx.ylabel_top("Inventory per \n unit thickness \n (H/m) \n")
    # plt.yscale("log")
    plt.ylim(bottom=0)
    matplotx.line_labels()
    plt.tight_layout()

    plt.sca(axs[1])

    matplotx.ylabel_top("Relative \n difference (%)")
    plt.xlabel("Thickness $e$ (mm)")
    plt.plot(thicknesses, difference)
    plt.ylim(bottom=0)
    plt.tight_layout()
    plt.show()
