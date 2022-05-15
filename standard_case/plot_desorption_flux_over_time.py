import numpy as np
import matplotlib.pyplot as plt
import matplotx


data_recomb = np.genfromtxt(
    "instant_recomb/derived_quantities.csv", delimiter=",", names=True
)

id_poloidal_gap = 11
id_top_pipe = 12
id_toroidal_gap = 13
id_bottom = 14
id_coolant = 10

# compute retrodesorbed flux (equal to implanted flux phi_imp)
thickness = 4e-3  # m
width = 23e-3  # m
top_area = thickness * width  # m2
retro_desorbed_flux = 1.61e22  # H/m2/s
retro_desorbed_flux *= top_area / 4  # H

t = data_recomb["ts"]  # time in s

# fluxes in H/s
flux_poloidal_gap = -data_recomb["Flux_surface_{}_solute".format(id_poloidal_gap)]
flux_toroidal_gap = -data_recomb["Flux_surface_{}_solute".format(id_toroidal_gap)]
flux_top_pipe = -data_recomb["Flux_surface_{}_solute".format(id_top_pipe)]
flux_bottom = -data_recomb["Flux_surface_{}_solute".format(id_bottom)]
flux_coolant = -data_recomb["Flux_surface_{}_solute".format(id_coolant)]
flux_retro = np.ones(t.shape) * retro_desorbed_flux

# multiply the fluxes by 4 to account for the whole MB
flux_poloidal_gap *= 4
flux_toroidal_gap *= 4
flux_top_pipe *= 4
flux_bottom *= 4
flux_retro *= 4

with plt.style.context(matplotx.styles.dufte):
    plt.plot(t, flux_toroidal_gap, label="Toroidal gap")
    plt.plot(t, flux_poloidal_gap, label="Poloidal gap")
    plt.plot(t, flux_top_pipe, label="Top pipe")
    plt.plot(t, flux_coolant, label="Coolant")
    # plt.plot(t, flux_bottom, label="Bottom")
    plt.plot(t, flux_retro, label="Top surface \n (retro-desorbed)")

    plt.yscale("log")

    matplotx.line_labels()
    matplotx.ylabel_top("Desorption \n flux (H/s)")
    plt.ticklabel_format(axis="x", style="sci", scilimits=(0, 0))
    plt.xlabel("Time (s)")
    plt.ylim(top=1e19)
    plt.xlim(left=0)
    plt.tight_layout()
    plt.show()