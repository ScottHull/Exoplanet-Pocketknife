import os
import csv
from scipy import integrate
import matplotlib.pyplot as plt

DEPTHS = [-1.0 * i for i in [0, 6, 19.7, 28.9, 36.4, 43.88, 51.34, 58.81, 66.36, 73.94, 81.5, 88.97, 96.45, 103.93, 111.41,
          118.92, 126.47, 134.01, 141.55, 149.09, 156.64, 164.18, 171.72, 179.27, 186.79, 194.27, 201.75,
          209.23, 216.71, 224.09, 231.4, 238.7, 246.01, 253.31, 260.62, 267.9, 275.16, 282.42, 289.68,
          296.94, 304.19, 311.41, 318.44, 325.47, 332.5, 339.53, 346.56, 353.59, 360.62, 367.66, 374.69,
          381.72, 388.75, 395.78, 402.78, 409.72, 416.67, 423.61, 430.56, 437.5, 444.44, 451.32, 457.89,
          464.47, 471.05, 477.63, 484.21, 490.79, 497.37, 503.75, 510, 516.25, 522.5, 528.75, 535, 541.25,
          547.5, 553.95, 560.53, 567.11, 573.68]]


class Inspect:

    def __init__(self, reg_path, depleted_path):
        super().__init__()
        self.reg_path = reg_path
        self.depleted_path = depleted_path
        self.adibekyan_bsp_1200 = None
        self.adibekyan_bsp_1400 = None
        self.adibekyan_bsp_1600 = None
        self.adibekyan_depleted_bsp_f1200_1200 = None
        self.adibekyan_depleted_bsp_f1400_1200 = None
        self.adibekyan_depleted_bsp_f1400_1400 = None
        self.adibekyan_depleted_bsp_f1600_1200 = None
        self.adibekyan_depleted_bsp_f1600_1400 = None
        self.adibekyan_depleted_bsp_f1600_1600 = None
        self.adibekyan_morb_f1200_1200 = None
        self.adibekyan_morb_f1400_1200 = None
        self.adibekyan_morb_f1400_1400 = None
        self.adibekyan_morb_f1600_1200 = None
        self.adibekyan_morb_f1600_1400 = None
        self.adibekyan_morb_f1600_1600 = None
        self.kepler_bsp_1200 = None
        self.kepler_bsp_1400 = None
        self.kepler_bsp_1600 = None
        self.kepler_depleted_bsp_f1200_1200 = None
        self.kepler_depleted_bsp_f1400_1200 = None
        self.kepler_depleted_bsp_f1400_1400 = None
        self.kepler_depleted_bsp_f1600_1200 = None
        self.kepler_depleted_bsp_f1600_1400 = None
        self.kepler_depleted_bsp_f1600_1600 = None
        self.kepler_morb_f1200_1200 = None
        self.kepler_morb_f1400_1200 = None
        self.kepler_morb_f1400_1400 = None
        self.kepler_morb_f1600_1200 = None
        self.kepler_morb_f1600_1400 = None
        self.kepler_morb_f1600_1600 = None

        self.__getfiles()

    def __return_df(self, f):
        return list(csv.reader(open(f, 'r'), delimiter=","))

    def __getfiles(self):
        files = []
        fnames = []
        for dirname, dirnames, f in os.walk(self.reg_path):
            for i in f:
                files.append(dirname + "/" + i)
                fnames.append(i)
        for index, i in enumerate(fnames):
            f = files[index]
            if "Adibekyan" in i and "BSP" in i and "1200" in i:
                self.adibekyan_bsp_1200 = self.__return_df(f=f)
            elif "Adibekyan" in i and "BSP" in i and "1400" in i:
                self.adibekyan_bsp_1400 = self.__return_df(f=f)
            elif "Adibekyan" in i and "BSP" in i and "1600" in i:
                self.adibekyan_bsp_1600 = self.__return_df(f=f)
            elif "Adibekyan" in i and "MORB" in i and "_F1200" in i and "_1200" in i:
                self.adibekyan_morb_f1200_1200 = self.__return_df(f=f)
            elif "Adibekyan" in i and "MORB" in i and "_F1400" in i and "_1200" in i:
                self.adibekyan_morb_f1400_1200 = self.__return_df(f=f)
            elif "Adibekyan" in i and "MORB" in i and "_F1400" in i and "_1400" in i:
                self.adibekyan_morb_f1400_1400 = self.__return_df(f=f)
            elif "Adibekyan" in i and "MORB" in i and "_F1600" in i and "_1200" in i:
                self.adibekyan_morb_f1600_1200 = self.__return_df(f=f)
            elif "Adibekyan" in i and "MORB" in i and "_F1600" in i and "_1400" in i:
                self.adibekyan_morb_f1600_1400 = self.__return_df(f=f)
            elif "Adibekyan" in i and "MORB" in i and "_F1600" in i and "_1600" in i:
                self.adibekyan_morb_f1600_1600 = self.__return_df(f=f)
            elif "Kepler" in i and "BSP" in i and "1200" in i:
                self.kepler_bsp_1200 = self.__return_df(f=f)
            elif "Kepler" in i and "BSP" in i and "1400" in i:
                self.kepler_bsp_1400 = self.__return_df(f=f)
            elif "Kepler" in i and "BSP" in i and "1600" in i:
                self.kepler_bsp_1600 = self.__return_df(f=f)
            elif "Kepler" in i and "MORB" in i and "_F1200" in i and "_1200" in i:
                self.kepler_morb_f1200_1200 = self.__return_df(f=f)
            elif "Kepler" in i and "MORB" in i and "_F1400" in i and "_1200" in i:
                self.kepler_morb_f1400_1200 = self.__return_df(f=f)
            elif "Kepler" in i and "MORB" in i and "_F1400" in i and "_1400" in i:
                self.kepler_morb_f1400_1400 = self.__return_df(f=f)
            elif "Kepler" in i and "MORB" in i and "_F1600" in i and "_1200" in i:
                self.kepler_morb_f1600_1200 = self.__return_df(f=f)
            elif "Kepler" in i and "MORB" in i and "_F1600" in i and "_1400" in i:
                self.kepler_morb_f1600_1400 = self.__return_df(f=f)
            elif "Kepler" in i and "MORB" in i and "_F1600" in i and "_1600" in i:
                self.kepler_morb_f1600_1600 = self.__return_df(f=f)

        files = []
        fnames = []
        for dirname, dirnames, f in os.walk(self.depleted_path):
            for i in f:
                files.append(dirname + "/" + i)
                fnames.append(i)
        for index, i in enumerate(fnames):
            f = files[index]
            if "Adibekyan" in i and "F1200" in i and "_1200" in i:
                self.adibekyan_depleted_bsp_f1200_1200 = self.__return_df(f=f)
            elif "Adibekyan" in i and "F1400" in i and "_1200" in i:
                self.adibekyan_depleted_bsp_f1400_1200 = self.__return_df(f=f)
            elif "Adibekyan" in i and "F1400" in i and "_1400" in i:
                self.adibekyan_depleted_bsp_f1400_1400 = self.__return_df(f=f)
            elif "Adibekyan" in i and "F1600" in i and "_1200" in i:
                self.adibekyan_depleted_bsp_f1600_1200 = self.__return_df(f=f)
            elif "Adibekyan" in i and "F1600" in i and "_1400" in i:
                self.adibekyan_depleted_bsp_f1600_1400 = self.__return_df(f=f)
            elif "Adibekyan" in i and "F1600" in i and "_1600" in i:
                self.adibekyan_depleted_bsp_f1600_1600 = self.__return_df(f=f)
            elif "Kepler" in i and "F1200" in i and "_1200" in i:
                self.kepler_depleted_bsp_f1200_1200 = self.__return_df(f=f)
            elif "Kepler" in i and "F1400" in i and "_1200" in i:
                self.kepler_depleted_bsp_f1400_1200 = self.__return_df(f=f)
            elif "Kepler" in i and "F1400" in i and "_1400" in i:
                self.kepler_depleted_bsp_f1400_1400 = self.__return_df(f=f)
            elif "Kepler" in i and "F1600" in i and "_1200" in i:
                self.kepler_depleted_bsp_f1600_1200 = self.__return_df(f=f)
            elif "Kepler" in i and "F1600" in i and "_1400" in i:
                self.kepler_depleted_bsp_f1600_1400 = self.__return_df(f=f)
            elif "Kepler" in i and "F1600" in i and "_1600" in i:
                self.kepler_depleted_bsp_f1600_1600 = self.__return_df(f=f)

    def __get_morb_row(self, star, morb_file):
        for row in morb_file:
            if row[0] == star:
                return row
        return []

    def __get_earth_row(self, file):
        for row in file:
            if row[0].lower() == "sun":
                return row

    def __compute_buoyancy_at_depth(self, density_differentials, plate_thickness=10 * 1000, gravity=9.8):
        buoyancies = []
        for index, i in enumerate(density_differentials):
            if index < len(density_differentials) - 1:
                sublist_density_diffs = density_differentials[0:index + 1]
                d = DEPTHS[0:index + 1]
                buoyancy_force = integrate.simps(sublist_density_diffs, d) * 1000 * 1000 * plate_thickness * gravity
                buoyancies.append(buoyancy_force)
            else:
                buoyancy_force = integrate.simps(density_differentials,
                                                 DEPTHS) * 1000 * 1000 * plate_thickness * gravity
                buoyancies.append(buoyancy_force)
        return buoyancies


    def get_buoyancy(self, bsp_file, morb_file):
        buoyancies = {}

        for bsp_row in bsp_file:
            star = bsp_row[0]
            morb_row = self.__get_morb_row(star=star, morb_file=morb_file)
            if len(bsp_row[1:]) == len(morb_row[1:]) == len(DEPTHS):
                densitity_differnces = [float(x) - float(y) for x, y in zip(morb_row[1:], bsp_row[1:])]
                buoyancy_force = self.__compute_buoyancy_at_depth(density_differentials=densitity_differnces)
                buoyancies.update({star: buoyancy_force})

        return buoyancies