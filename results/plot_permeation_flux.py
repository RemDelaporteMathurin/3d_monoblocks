import numpy as np
import matplotlib.pyplot as plt
import matplotx

transient = True
thicknesses = [4, 5, 6, 7, 8, 9, 10, 14]
flux_w = []
flux_wo = []
time = 1e5
id_coolant = 10
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
            "{}/derived_quantities.csv".format(folder), delimiter=",", names=True
        )
        index = np.where(data["ts"] == time)[0][0]
        if index != 0:
            raise ValueError(
                "More than one entry found in derived quantities, please adapt code."
            )
        flux = (
            -data["Flux_surface_{}_solute".format(id_coolant)] * 4 / (thickness * 1e-3)
        )
        if instant_recomb:
            flux_w.append(flux)
        else:
            flux_wo.append(flux)

difference = [100 * abs(w - wo) / w for w, wo in zip(flux_w, flux_wo)]

with plt.style.context(matplotx.styles.dufte):
    fig, axs = plt.subplots(2, 1, sharex=True, figsize=(6.4, 4.8*1.2), gridspec_kw={'height_ratios': [2, 1]})
    plt.sca(axs[0])
    plt.plot(
        thicknesses,
        flux_w,
        color="tab:orange",
        label="Instantaneous \n recombination",
    )
    plt.plot(thicknesses, flux_wo, color="tab:orange", label="No recombination")
    plt.fill_between(thicknesses, flux_w, flux_wo, alpha=0.3, color="tab:orange")
    matplotx.ylabel_top("Permeation \n flux per \n unit thickness \n (H/m/s)")
    # plt.yscale("log")
    plt.ylim(bottom=0)
    matplotx.line_labels()

    plt.sca(axs[1])

    matplotx.ylabel_top("Relative \n difference (%)")
    plt.xlabel("Thickness $e$ (mm)")
    plt.plot(thicknesses, difference, color="tab:orange")
    plt.ylim(bottom=0)
    plt.xticks([4, 6, 8, 10, 12, 14])
    plt.tight_layout()
    fig.subplots_adjust(top=0.8, hspace=0.7)
    plt.savefig("permeation_flux_vs_thickness.pdf")
    plt.show()