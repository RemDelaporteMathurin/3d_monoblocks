import numpy as np
import matplotlib.pyplot as plt
import matplotx

root="//wsl$/Ubuntu-20.04/home/jmougenot/3d_monoblocks/results/"

thicknesses = [4, 5, 6, 7, 8, 9, 10, 14]
avg_Ts_no_gap = []
avg_Ts_gap = []
time = 1e5
id_coolant = 10
for thickness in thicknesses:
    folder = root+"{}mm_thickness/transient/instant_recomb".format(thickness)

    data_gap = np.genfromtxt(
        "{}/derived_quantities.csv".format(folder), delimiter=",", names=True
    )
    data_no_gap = np.genfromtxt(
        "{}/no_gap/derived_quantities.csv".format(folder), delimiter=",", names=True
    )
    index = np.where(data_gap["ts"] == time)[0][0]
    if index != 0:
        raise ValueError(
            "More than one entry found in derived quantities, please adapt code."
        )
    avg_Ts_gap.append(data_gap["Average_T_surface_{}".format(id_coolant)])
    avg_Ts_no_gap.append(data_no_gap["Average_T_surface_{}".format(id_coolant)])


with plt.style.context(matplotx.styles.dufte):
    plt.plot(thicknesses, avg_Ts_gap, label="Gap")
    plt.plot(thicknesses, avg_Ts_no_gap, label="No gap")
    plt.ylim(bottom=323)
    yticks = plt.gca().get_yticks()[:]
    yticks_labels = [y for y in yticks]
    yticks_labels[0] = "Coolant temp"
    plt.yticks(yticks, yticks_labels)
    matplotx.ylabel_top("Average temperature \n cooling surface (K)")
    matplotx.line_labels()
    plt.xlabel("Thickness $e$ (mm)")
    plt.tight_layout()
    plt.show()
