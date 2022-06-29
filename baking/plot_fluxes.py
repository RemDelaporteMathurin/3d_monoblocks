import matplotlib.pyplot as plt
import numpy as np
import matplotx
from matplotx_proxy import label_fillbetween

id_W_top = 9
id_coolant = 10
id_poloidal_gap = 11
id_toroidal_gap = 12
id_bottom = 13
id_top_pipe = 14
TUNGSTEN_SURFACES = [id_poloidal_gap, id_toroidal_gap, id_bottom, id_W_top]

baking_temperature = 600

data = np.genfromtxt(
    "baking_temperature={:.0f}K/derived_quantities.csv".format(baking_temperature),
    delimiter=",",
    names=True,
)

total_desorption = -sum(
    [
        data["Flux_surface_{}_solute".format(surf_id)]
        for surf_id in TUNGSTEN_SURFACES + [id_coolant, id_top_pipe]
    ]
)

top_desorption = -data["Flux_surface_{}_solute".format(id_W_top)]
bot_desorption = -data["Flux_surface_{}_solute".format(id_bottom)]
toroidal_desorption = -data["Flux_surface_{}_solute".format(id_toroidal_gap)]
poloidal_desorption = -data["Flux_surface_{}_solute".format(id_poloidal_gap)]
coolant_desorption = -data["Flux_surface_{}_solute".format(id_coolant)]
top_pipe_desorption = -data["Flux_surface_{}_solute".format(id_top_pipe)]

# plt.plot(data["ts"], total_desorption)
with plt.style.context(matplotx.styles.dufte):
    plt.figure(figsize=(6.4 * 1.2, 4.8 * 1.2))
    plt.fill_between(
        data["ts"],
        poloidal_desorption,
        color="tab:blue",
        alpha=0.9,
        label="Poloidal",
    )
    plt.fill_between(
        data["ts"],
        poloidal_desorption,
        poloidal_desorption + top_desorption,
        color="tab:blue",
        alpha=0.7,
        label="Top",
    )
    plt.fill_between(
        data["ts"],
        poloidal_desorption + top_desorption,
        poloidal_desorption + top_desorption + toroidal_desorption,
        color="tab:blue",
        alpha=0.5,
        label="Toroidal gap",
    )
    plt.fill_between(
        data["ts"],
        top_desorption + poloidal_desorption + toroidal_desorption,
        top_desorption + poloidal_desorption + toroidal_desorption + coolant_desorption,
        color="tab:orange",
        alpha=0.75,
        label="Coolant",
    )
    plt.fill_between(
        data["ts"],
        top_desorption + poloidal_desorption + toroidal_desorption + coolant_desorption,
        top_desorption
        + poloidal_desorption
        + toroidal_desorption
        + coolant_desorption
        + top_pipe_desorption,
        color="tab:orange",
        alpha=0.5,
        label="Top pipe",
    )

    plt.ylim(bottom=0)
    plt.xlim(0, 1e5)

    label_fillbetween()
    matplotx.ylabel_top("Desorption flux \n")
    plt.xlabel("Baking time (s)")
    plt.tight_layout()

    plt.show()
