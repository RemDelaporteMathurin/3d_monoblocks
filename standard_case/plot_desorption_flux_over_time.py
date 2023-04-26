import numpy as np
import matplotlib.pyplot as plt
import matplotx

root="//wsl$/Ubuntu-20.04/home/jmougenot/3d_monoblocks/standard_case/"

data_recomb = np.genfromtxt(
    root+"instant_recomb/derived_quantities.csv", delimiter=",", names=True
)

id_coolant = 10
id_poloidal_gap_W = 11
id_poloidal_gap_Cu = 12
id_toroidal_gap = 13
id_bottom = 14
id_top_pipe = 15

# compute retrodesorbed flux (equal to implanted flux phi_imp)
thickness = 4e-3  # m
width = 23e-3  # m
top_area = thickness * width  # m2
retro_desorbed_flux = 1.61e22  # H/m2/s
retro_desorbed_flux *= top_area / 4  # H

t = data_recomb["ts"]  # time in s

# fluxes in H/s
flux_poloidal_gap = -data_recomb["Flux_surface_{}_solute".format(id_poloidal_gap_W)]-data_recomb["Flux_surface_{}_solute".format(id_poloidal_gap_Cu)]
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

colour_vessel = "tab:blue"
colour_coolant = "tab:orange"

with plt.style.context(matplotx.styles.dufte):
    plt.plot(t, flux_toroidal_gap, label="Toroidal gap", color=colour_vessel)
    plt.plot(t, flux_poloidal_gap, label="Poloidal gap", color=colour_vessel)
    plt.plot(t, flux_top_pipe, label="Top pipe", color=colour_vessel)
    plt.plot(t, flux_coolant, label="Coolant", color=colour_coolant)
    # plt.plot(t, flux_bottom, label="Bottom")
    plt.plot(
        t, flux_retro, label="Top surface \n (retro-desorbed)", color=colour_vessel
    )

    plt.xscale("log")
    plt.yscale("log")

    matplotx.line_labels()
    # plt.ticklabel_format(axis="x", style="sci", scilimits=(0, 0))
    plt.xlabel("Time (s)")
    plt.ylim(top=1e19)
    matplotx.ylabel_top("Desorption \n flux (H/s)")
    plt.tight_layout()
    plt.show()
