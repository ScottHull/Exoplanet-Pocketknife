import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from mpl_toolkits.axes_grid1 import make_axes_locatable
from composition import Inspect as InspectComposition
from buoyancy import Inspect as InspectBuoyancy


def pair_composition_to_buoyancy(buoyancy, composition, oxide):
    pairs = []
    for star in buoyancy.keys():
        final_buoyancy = buoyancy[star][-1]
        c = composition[star][oxide.lower()]
        pairs.append((c, final_buoyancy))
    return pairs

def pair_compositions_and_map_buoyancy(buoyancy, composition, oxide_x, oxide_y, special_star=None):
    pairs = []
    if special_star is None:
        for star in buoyancy.keys():
            final_buoyancy = buoyancy[star][-1]
            c_x = composition[star][oxide_x.lower()]
            c_y = composition[star][oxide_y.lower()]
            pairs.append((c_x, c_y, final_buoyancy))
    else:
        star = special_star
        final_buoyancy = buoyancy[star][-1]
        c_x = composition[star][oxide_x.lower()]
        c_y = composition[star][oxide_y.lower()]
        pairs.append((c_x, c_y, final_buoyancy))
    return pairs

def pair_compositions_and_map_buoyancy_relative_to_earth(buoyancy, composition, oxide_x, oxide_y, special_star=None):
    pairs = []
    earth_buoyancy = buoyancy['Sun'][-1]
    if special_star is None:
        for star in buoyancy.keys():
            final_buoyancy = buoyancy[star][-1]
            buoyancy_relative = None
            if final_buoyancy > earth_buoyancy:
                buoyancy_relative = 1  # more buoyant than earth
            else:
                buoyancy_relative = 0  # less buoyant than earth
            c_x = composition[star][oxide_x.lower()]
            c_y = composition[star][oxide_y.lower()]
            pairs.append((c_x, c_y, final_buoyancy, buoyancy_relative))
    else:
        star = special_star
        final_buoyancy = buoyancy[star][-1]
        buoyancy_relative = None
        if final_buoyancy > earth_buoyancy:
            buoyancy_relative = 1  # more buoyant than earth
        else:
            buoyancy_relative = 0  # less buoyant than earth
        c_x = composition[star][oxide_x.lower()]
        c_y = composition[star][oxide_y.lower()]
        pairs.append((c_x, c_y, final_buoyancy, buoyancy_relative))
    return pairs


compositions = InspectComposition(path="/Users/scotthull/Desktop/exoplanets/Depleted_Lithosphere_Compositions")
buoyancies = InspectBuoyancy(reg_path="/Users/scotthull/Desktop/exoplanets/Densities/BSP_MORB",
                             depleted_path="/Users/scotthull/Desktop/exoplanets/Densities/Depleted_Lithosphere")

adibekyan_f1400_1200_buoyancies = buoyancies.get_buoyancy(bsp_file=buoyancies.adibekyan_bsp_1600,
                                                          morb_file=buoyancies.adibekyan_morb_f1400_1200)
adibekyan_f1400_1400_buoyancies = buoyancies.get_buoyancy(bsp_file=buoyancies.adibekyan_bsp_1600,
                                                          morb_file=buoyancies.adibekyan_morb_f1400_1400)
adibekyan_f1600_1200_buoyancies = buoyancies.get_buoyancy(bsp_file=buoyancies.adibekyan_bsp_1600,
                                                          morb_file=buoyancies.adibekyan_morb_f1600_1200)
adibekyan_f1600_1400_buoyancies = buoyancies.get_buoyancy(bsp_file=buoyancies.adibekyan_bsp_1600,
                                                          morb_file=buoyancies.adibekyan_morb_f1600_1400)
adibekyan_f1600_1600_buoyancies = buoyancies.get_buoyancy(bsp_file=buoyancies.adibekyan_bsp_1600,
                                                          morb_file=buoyancies.adibekyan_morb_f1600_1600)

kepler_f1400_1200_buoyancies = buoyancies.get_buoyancy(bsp_file=buoyancies.kepler_bsp_1600,
                                                       morb_file=buoyancies.kepler_morb_f1400_1200)
kepler_f1400_1400_buoyancies = buoyancies.get_buoyancy(bsp_file=buoyancies.kepler_bsp_1600,
                                                       morb_file=buoyancies.kepler_morb_f1400_1400)
kepler_f1600_1200_buoyancies = buoyancies.get_buoyancy(bsp_file=buoyancies.kepler_bsp_1600,
                                                       morb_file=buoyancies.kepler_morb_f1600_1200)
kepler_f1600_1400_buoyancies = buoyancies.get_buoyancy(bsp_file=buoyancies.kepler_bsp_1600,
                                                       morb_file=buoyancies.kepler_morb_f1600_1400)
kepler_f1600_1600_buoyancies = buoyancies.get_buoyancy(bsp_file=buoyancies.kepler_bsp_1600,
                                                       morb_file=buoyancies.kepler_morb_f1600_1600)

adibekyan_depleted_f1400_1400_morb_1200_buoyancies = buoyancies.get_buoyancy(
    bsp_file=buoyancies.adibekyan_depleted_bsp_f1400_1400,
    morb_file=buoyancies.adibekyan_morb_f1400_1200)
adibekyan_depleted_f1400_1400_morb_1400_buoyancies = buoyancies.get_buoyancy(
    bsp_file=buoyancies.adibekyan_depleted_bsp_f1400_1400,
    morb_file=buoyancies.adibekyan_morb_f1400_1400)
adibekyan_depleted_f1600_1600_morb_1200_buoyancies = buoyancies.get_buoyancy(
    bsp_file=buoyancies.adibekyan_depleted_bsp_f1600_1600,
    morb_file=buoyancies.adibekyan_morb_f1600_1200)
adibekyan_depleted_f1600_1600_morb_1400_buoyancies = buoyancies.get_buoyancy(
    bsp_file=buoyancies.adibekyan_depleted_bsp_f1600_1600,
    morb_file=buoyancies.adibekyan_morb_f1600_1400)
adibekyan_depleted_f1600_1600_morb_1600_buoyancies = buoyancies.get_buoyancy(
    bsp_file=buoyancies.adibekyan_depleted_bsp_f1600_1600,
    morb_file=buoyancies.adibekyan_morb_f1600_1600)

kepler_depleted_f1400_1400_morb_1200_buoyancies = buoyancies.get_buoyancy(
    bsp_file=buoyancies.kepler_depleted_bsp_f1400_1400,
    morb_file=buoyancies.kepler_morb_f1400_1200)
kepler_depleted_f1400_1400_morb_1400_buoyancies = buoyancies.get_buoyancy(
    bsp_file=buoyancies.kepler_depleted_bsp_f1400_1400,
    morb_file=buoyancies.kepler_morb_f1400_1400)
kepler_depleted_f1600_1600_morb_1200_buoyancies = buoyancies.get_buoyancy(
    bsp_file=buoyancies.kepler_depleted_bsp_f1600_1600,
    morb_file=buoyancies.kepler_morb_f1600_1200)
kepler_depleted_f1600_1600_morb_1400_buoyancies = buoyancies.get_buoyancy(
    bsp_file=buoyancies.kepler_depleted_bsp_f1600_1600,
    morb_file=buoyancies.kepler_morb_f1600_1400)
kepler_depleted_f1600_1600_morb_1600_buoyancies = buoyancies.get_buoyancy(
    bsp_file=buoyancies.kepler_depleted_bsp_f1600_1600,
    morb_file=buoyancies.kepler_morb_f1600_1600)


adibekyan_f1400_depletion = compositions.get_depletion(parent_reservoir=compositions.adibekyan_bsp,
                                                          daughter_reservoir=compositions.adibekyan_morb_f1400)
adibekyan_f1600_depletion = compositions.get_depletion(parent_reservoir=compositions.adibekyan_bsp,
                                                          daughter_reservoir=compositions.adibekyan_morb_f1600)
adibekyan_depleted_f1400_depletion = compositions.get_depletion(parent_reservoir=compositions.adibekyan_depleted_bsp_f1400,
                                                          daughter_reservoir=compositions.adibekyan_morb_f1400)
adibekyan_depleted_f1600_depletion = compositions.get_depletion(parent_reservoir=compositions.adibekyan_depleted_bsp_f1600,
                                                          daughter_reservoir=compositions.adibekyan_morb_f1600)

kepler_f1400_depletion = compositions.get_depletion(parent_reservoir=compositions.kepler_bsp,
                                                          daughter_reservoir=compositions.kepler_morb_f1400)
kepler_f1600_depletion = compositions.get_depletion(parent_reservoir=compositions.kepler_bsp,
                                                          daughter_reservoir=compositions.kepler_morb_f1600)
kepler_depleted_f1400_depletion = compositions.get_depletion(parent_reservoir=compositions.kepler_depleted_bsp_f1400,
                                                          daughter_reservoir=compositions.kepler_morb_f1400)
kepler_depleted_f1600_depletion = compositions.get_depletion(parent_reservoir=compositions.kepler_depleted_bsp_f1600,
                                                          daughter_reservoir=compositions.kepler_morb_f1600)

# adibekyan_regular_bsp_1600_morb_f1400_1200_buoyancy = pair_composition_to_buoyancy(
#     buoyancy=adibekyan_f1400_1200_buoyancies, composition=adibekyan_f1400_depletion, oxide='sio2')
#
# ax = plt.figure().add_subplot(111)
# x = [i[0] for i in adibekyan_regular_bsp_1600_morb_f1400_1200_buoyancy]
# y = [i[1] for i in adibekyan_regular_bsp_1600_morb_f1400_1200_buoyancy]
# # determine best fit line
# coeffs = np.polyfit(x, y, 1)
# intercept = coeffs[-1]
# slope = coeffs[-2]
# xl = [min(x), max(x)]
# yl = [(slope * xx) + intercept for xx in xl]
# ax.scatter(x, y, marker="+")
# ax.plot(xl, yl, color='red', linestyle="--", label="Best Fit")
#
# ax.set_xlabel("SiO2 Depletion (%)")
# ax.set_ylabel("Buoyancy Force (N)")
# ax.grid()




adibekyan_regular_bsp_1600_morb_f1400_1200_buoyancy = pair_compositions_and_map_buoyancy(
    buoyancy=adibekyan_f1400_1200_buoyancies, composition=adibekyan_f1400_depletion, oxide_x='sio2', oxide_y="feo")
earth_regular_bsp_1600_morb_f1400_1200_buoyancy = pair_compositions_and_map_buoyancy(
    buoyancy=adibekyan_f1400_1200_buoyancies, composition=adibekyan_f1400_depletion, oxide_x='sio2', oxide_y="feo",
    special_star="Sun")

adibekyan_depleted_bsp_1600_morb_f1400_1200_buoyancy = pair_compositions_and_map_buoyancy(
    buoyancy=adibekyan_depleted_f1400_1400_morb_1200_buoyancies,
    composition=adibekyan_depleted_f1400_depletion, oxide_x='sio2', oxide_y="feo")
earth_depleted_bsp_1600_morb_f1400_1200_buoyancy = pair_compositions_and_map_buoyancy(
    buoyancy=adibekyan_depleted_f1400_1400_morb_1200_buoyancies,
    composition=adibekyan_depleted_f1400_depletion, oxide_x='sio2', oxide_y="feo", special_star="Sun")

fig = plt.figure()
ax = fig.add_subplot(111)
x = [i[0] for i in adibekyan_regular_bsp_1600_morb_f1400_1200_buoyancy]
y = [i[1] for i in adibekyan_regular_bsp_1600_morb_f1400_1200_buoyancy]
b = [i[2] for i in adibekyan_regular_bsp_1600_morb_f1400_1200_buoyancy]
undepleted_ellipse = Ellipse(xy=(((max(x) - min(x)) / 2.0), (max(y) - min(y)) / 2.0), width=abs(max(x) - min(x)),
                             height=abs(max(y) - min(y)), edgecolor='blue', lw=4, facecolor='none',
                             label="Undepleted BSP Sample")
x_depleted = [i[0] for i in adibekyan_depleted_bsp_1600_morb_f1400_1200_buoyancy]
y_depleted = [i[1] for i in adibekyan_depleted_bsp_1600_morb_f1400_1200_buoyancy]
b_depleted = [i[2] for i in adibekyan_depleted_bsp_1600_morb_f1400_1200_buoyancy]
depleted_ellipse = Ellipse(xy=(((max(x_depleted) - min(x_depleted)) / 2.0), (max(y_depleted) - min(y_depleted)) / 2.0),
                           width=abs(max(x_depleted) - min(x_depleted)), height=abs(max(y_depleted) - min(y_depleted)),
                           edgecolor='red', lw=4, facecolor='none', label="Depleted BSP Sample")
x = x + x_depleted
y = y + y_depleted
b = b + b_depleted
# determine best fit line
coeffs = np.polyfit(x, y, 1)
intercept = coeffs[-1]
slope = coeffs[-2]
xl = [min(x), max(x)]
yl = [(slope * xx) + intercept for xx in xl]
sc = ax.scatter(x, y, c=b, marker="+", cmap='viridis')
ax.scatter(earth_regular_bsp_1600_morb_f1400_1200_buoyancy[0][0], earth_regular_bsp_1600_morb_f1400_1200_buoyancy[0][1],
           marker='x', color='black', s=50, label='Sun-Derived Model (Undepleted)')
ax.scatter(earth_depleted_bsp_1600_morb_f1400_1200_buoyancy[0][0], earth_depleted_bsp_1600_morb_f1400_1200_buoyancy[0][1],
           marker='*', color='black', s=50, label='Sun-Derived Model (Depleted)')
ax.plot(xl, yl, color='red', linestyle="--", label="Best Fit")
ax.add_patch(undepleted_ellipse)
ax.add_patch(depleted_ellipse)
cbar = plt.colorbar(sc, ax=ax)
cbar.set_label('Buoyancy Force (N)')
ax.set_xlabel("SiO2 Depletion (%)")
ax.set_ylabel("FeO Depletion (%)")
ax.legend()
ax.grid()

# adibekyan_regular_bsp_1600_morb_f1400_1200_buoyancy = pair_compositions_and_map_buoyancy_relative_to_earth(
#     buoyancy=adibekyan_f1400_1200_buoyancies, composition=adibekyan_f1400_depletion, oxide_x='sio2', oxide_y="feo")
# earth_regular_bsp_1600_morb_f1400_1200_buoyancy = pair_compositions_and_map_buoyancy_relative_to_earth(
#     buoyancy=adibekyan_f1400_1200_buoyancies, composition=adibekyan_f1400_depletion, oxide_x='sio2', oxide_y="feo",
#     special_star="Sun")
#
# adibekyan_depleted_bsp_1600_morb_f1400_1200_buoyancy = pair_compositions_and_map_buoyancy_relative_to_earth(
#     buoyancy=adibekyan_depleted_f1400_1400_morb_1200_buoyancies,
#     composition=adibekyan_depleted_f1400_1400_morb_1200_buoyancies, oxide_x='sio2', oxide_y="feo")
# earth_depleted_bsp_1600_morb_f1400_1200_buoyancy = pair_compositions_and_map_buoyancy_relative_to_earth(
#     buoyancy=adibekyan_depleted_f1400_1400_morb_1200_buoyancies,
#     composition=adibekyan_depleted_f1400_1400_morb_1200_buoyancies, oxide_x='sio2', oxide_y="feo", special_star="Sun")

# fig = plt.figure()
# ax = fig.add_subplot(111)
# x_greater_than = [i[0] for i in adibekyan_regular_bsp_1600_morb_f1400_1200_buoyancy if i[3] == 1]
# y_greater_than = [i[1] for i in adibekyan_regular_bsp_1600_morb_f1400_1200_buoyancy if i[3] == 1]
# x_less_than = [i[0] for i in adibekyan_regular_bsp_1600_morb_f1400_1200_buoyancy if i[3] == 0]
# y_less_than = [i[1] for i in adibekyan_regular_bsp_1600_morb_f1400_1200_buoyancy if i[3] == 0]
# # determine best fit line
# coeffs_greater_than = np.polyfit(x_greater_than, y_greater_than, 1)
# intercept_greater_than = coeffs_greater_than[-1]
# slope_greater_than = coeffs_greater_than[-2]
# xl_greater_than = [min(x_greater_than), max(x_greater_than)]
# yl_greater_than = [(slope_greater_than * xx) + intercept_greater_than for xx in xl_greater_than]
# ax.scatter(x_greater_than, y_greater_than, c='red', marker="+", label="Buoyancy > Earth ({})".format(len(x_greater_than)))
# # ax.plot(xl_greater_than, yl_greater_than, color='red', linestyle="--", label="Best Fit (> Earth)")
# coeffs_less_than = np.polyfit(x_less_than, y_less_than, 1)
# intercept_less_than = coeffs_less_than[-1]
# slope_less_than = coeffs_less_than[-2]
# xl_less_than = [min(x_less_than), max(x_less_than)]
# yl_less_than = [(slope_less_than * xx) + intercept_less_than for xx in xl_less_than]
# ax.scatter(x_less_than, y_less_than, c='blue', marker="+", label="Buoyancy <= Earth ({})".format(len(x_less_than)))
# ax.scatter(earth_regular_bsp_1600_morb_f1400_1200_buoyancy[0][0], earth_regular_bsp_1600_morb_f1400_1200_buoyancy[0][1],
#            marker='x', color='black', s=50, label='Sun-Derived Model')
# # ax.plot(xl_less_than, yl_less_than, color='blue', linestyle="--", label="Best Fit (<= Earth)")
# ax.set_xlabel("SiO2 Depletion (%)")
# ax.set_ylabel("FeO Depletion (%)")
# ax.legend()
# ax.grid()




plt.show()
