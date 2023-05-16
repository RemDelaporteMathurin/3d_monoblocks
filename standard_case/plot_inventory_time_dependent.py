import numpy as np
import matplotlib.pyplot as plt
import matplotx

folder="//wsl$/Ubuntu-18.04/home/jmougenot/3d_monoblocks/standard_case/"

data_recomb = np.genfromtxt(
    folder+"transient/instant_recomb/derived_quantities.csv", delimiter=",", names=True
)
data_no_recomb = np.genfromtxt(
    folder+"transient/no_recomb/derived_quantities.csv", delimiter=",", names=True
)

data_recomb_s = np.genfromtxt(
    folder+"steady_state/instant_recomb/derived_quantities.csv", delimiter=",", names=True
)
data_no_recomb_s = np.genfromtxt(
    folder+"steady_state/no_recomb/derived_quantities.csv", delimiter=",", names=True
)

inventory_no_recomb = sum(
    [data_no_recomb["Total_retention_volume_{}".format(vol_id)] for vol_id in [6, 7, 8]]
)
#inventory_no_recomb *= 4  # for the whole MB

inventory_recomb = sum(
    [data_recomb["Total_retention_volume_{}".format(vol_id)] for vol_id in [6, 7, 8]]
)
#inventory_recomb *= 4  # for the whole MB

difference = [
    100 * abs(w - wo) / w for w, wo in zip(inventory_recomb, inventory_no_recomb)
]


#fig, axs = plt.subplots(2, 1, sharex=True, figsize=(6.4, 4.8*1.2), gridspec_kw={'height_ratios': [2, 1]})
#plt.sca(axs[0])

plt.plot(
    data_no_recomb["ts"],
    inventory_no_recomb,
    label="Case A: No recombination on the poloidal gap",
    color="tab:blue",
)

plt.plot(
    data_recomb["ts"],
    inventory_recomb,
    label="Case B: Instantaneous recombination",
    color="tab:orange",
)
plt.fill_between(
    data_no_recomb["ts"], inventory_no_recomb, inventory_recomb, alpha=0.2
)
plt.yscale("log")
# plt.ylim(bottom=0)
plt.ylim(1e13, 1e17)
plt.ylabel("Inventory for the 1/4 MB (H)")
plt.xscale("log")
plt.grid()
plt.xlim(1e3,1e7)
#matplotx.line_labels()
plt.legend()
plt.title('for the 4-mm MB thickness')
plt.tight_layout()
plt.savefig(folder+"temporal.png",dpi=900)


#plt.sca(axs[1])
#plt.xlabel("Time (s)")
#plt.plot(data_no_recomb["ts"], difference)
#plt.ylim(bottom=0, top=1000)
#matplotx.ylabel_top("Relative \n difference (%)")
#plt.tight_layout()
plt.show()
