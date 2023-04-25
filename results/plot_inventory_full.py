import numpy as np
import matplotlib.pyplot as plt
import matplotx

transient = True
thicknesses = [4, 5, 6, 7, 8, 9, 10, 14]
retention_w = []
retention_wo = []
retention_wp = []
retention_wo_nogap = []
time = 1e5
for instant_recomb in [0,1,2]:
    for thickness in thicknesses:
        folder = "//wsl$/Ubuntu-20.04/home/jmougenot/3d_monoblocks/results/{}mm_thickness".format(thickness)
        if transient:
            folder += "/transient"
        else:
            folder += "/steady_state"
        if instant_recomb==1:
            folder += "/instant_recomb"
        else:
            if instant_recomb==2:
                folder += "/recomb"
            else:
                folder += "/no_recomb"
        data = np.genfromtxt(
            "{}/derived_quantities.csv".format(folder), delimiter=",", names=True
        )
        if instant_recomb!=2:
            datanogap = np.genfromtxt(
            "{}/no_gap/derived_quantities.csv".format(folder), delimiter=",", names=True
            )
        index = np.where(data["ts"] == time)[0][0]
        if index != 0:
            raise ValueError(
                "More than one entry found in derived quantities, please adapt code."
            )
        retention = sum(
            [data["Total_retention_volume_{}".format(vol_id)] for vol_id in [6, 7, 8]]
            * 4
        ) / (thickness * 1e-3)
        retentionnogap = sum(
            [datanogap["Total_retention_volume_{}".format(vol_id)] for vol_id in [6, 7, 8]]
            * 4
        ) / (thickness * 1e-3)
        if instant_recomb==1:
            retention_w.append(retention)
        else:
            if instant_recomb==2:
                retention_wp.append(retention)
            else:
                retention_wo.append(retention)
                retention_wo_nogap.append(retentionnogap)

ratio = [w / wo for w, wo in zip(retention_w, retention_wo)]
difference = [100 * abs(w - wo) / w for w, wo in zip(retention_w, retention_wo)]

with plt.style.context(matplotx.styles.dufte):
    fig, axs = plt.subplots(2, 1, sharex=True, figsize=(6.4, 4.8*1.2), gridspec_kw={'height_ratios': [2, 1]})
    plt.sca(axs[0])
    plt.plot(
        thicknesses,
        retention_w,
        color="tab:blue",
        label="Instantaneous \n recombination",
    )
    plt.plot(thicknesses, retention_wo, color="tab:blue", label="No recombination")
    plt.plot(thicknesses, retention_wo_nogap, color="tab:blue", linestyle='dashed')
    plt.fill_between(thicknesses, retention_w, retention_wo, alpha=0.3)
    plt.plot(thicknesses, retention_wp, color="tab:red", label="Recombination on Cu parts")
    matplotx.ylabel_top("Inventory per \n unit thickness \n (H/m) \n")
    # plt.yscale("log")
    plt.ylim(bottom=0)
    matplotx.line_labels()
    plt.tight_layout()

    plt.sca(axs[1])

    matplotx.ylabel_top("Relative \n difference (%)")
    plt.xlabel("Thickness $e$ (mm)")
    plt.plot(thicknesses, difference)
    plt.ylim(0, 200)
    plt.tight_layout()
    plt.show()
