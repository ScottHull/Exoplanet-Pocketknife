# python /usr/bin/env/python

# /// The Exoplanet Pocketknife
# /// Scott D. Hull, The Ohio State University 2015-2017
# /// All usage must include proper citation and a link to the Github repository
# /// https://github.com/ScottHull/Exoplanet-Pocketknife


import os, csv, time, sys, shutil, subprocess
from threading import Timer
from math import *
import pandas as pd
import matplotlib.pyplot as plt
from scipy import integrate as inte
import numpy as np
import bisect

bsp_run = False
morb_run = False

gravity = 9.8
# plate_thickness = 10.0 # This is in km!
plate_thickness = 10 * 1000 # This is in m!

na_atwt = 22.98976928
mg_atwt = 24.305
al_atwt = 26.9815386
si_atwt = 28.0855
ca_atwt = 40.078
ti_atwt = 47.867
cr_atwt = 51.9961
fe_atwt = 55.845
ni_atwt = 58.6934

na2o_molwt = 61.9785
mgo_molwt = 40.3040
al2o3_molwt = 101.9601
sio2_molwt = 60.0835
cao_molwt = 56.0770
tio2_molwt = 79.8650
cr2o3_molwt = 151.9892
feo_molwt = 71.8440
nio_molwt = 74.6924
fe2o3_molwt = 159.687

num_na2o_cations = 2
num_mgo_cations = 1
num_al2o3_cations = 2
num_sio2_cations = 1
num_cao_cations = 1
num_tio2_cations = 1
num_cr2o3_cations = 2
num_feo_cations = 1
num_nio_cations = 1
num_fe2o3_cations = 2

asplund_na = 1479108.388
asplund_mg = 33884415.61
asplund_al = 2344228.815
asplund_si = 32359365.69
asplund_ca = 2041737.945
asplund_ti = 79432.82347
asplund_cr = 436515.8322
asplund_fe = 28183829.31
asplund_ni = 1698243.652
asplund_sivsfe = asplund_si / asplund_fe
asplund_navsfe = asplund_na / asplund_fe

mcd_earth_fe = 29.6738223341739
mcd_earth_na = 0.40545783900173
mcd_earth_mg = 32.812015232308
mcd_earth_al = 3.05167459380979
mcd_earth_si = 29.6859892035662
mcd_earth_ca = 2.20951970229211
mcd_earth_ni = 1.60579436264263
mcd_earth_ti = 0.0876307681103416
mcd_earth_cr = 0.468095964095391
mc_earth_ni = 1.60579436264263
mcd_sivsfe = mcd_earth_si / mcd_earth_fe
mcd_navsfe = mcd_earth_na / mcd_earth_fe

adjust_si = mcd_sivsfe / asplund_sivsfe
adjust_na = mcd_navsfe / asplund_navsfe

modelearth_mgo = 11.84409812845
gale_mgo = 7.65154964069009
mgo_fix = gale_mgo / modelearth_mgo

depth_trans_zone = [0, 6, 19.7, 28.9, 36.4, 43.88, 51.34, 58.81, 66.36, 73.94, 81.5, 88.97, 96.45, 103.93, 111.41,
                    118.92, 126.47, 134.01, 141.55, 149.09, 156.64, 164.18, 171.72, 179.27, 186.79, 194.27, 201.75,
                    209.23, 216.71, 224.09, 231.4, 238.7, 246.01, 253.31, 260.62, 267.9, 275.16, 282.42, 289.68,
                    296.94, 304.19, 311.41, 318.44, 325.47, 332.5, 339.53, 346.56, 353.59, 360.62, 367.66, 374.69,
                    381.72, 388.75, 395.78, 402.78, 409.72, 416.67, 423.61, 430.56, 437.5, 444.44, 451.32, 457.89,
                    464.47, 471.05, 477.63, 484.21, 490.79, 497.37, 503.75, 510, 516.25, 522.5, 528.75, 535, 541.25,
                    547.5, 553.95, 560.53, 567.11, 573.68]

inputfile_list = []
home_dir = []


# star_names = []
# na_h = []
# mg_h = []
# al_h = []
# si_h = []
# ca_h = []
# ti_h = []
# cr_h = []
# fe_h = []
#
# star_index = []
# na_index = []
# mg_index = []
# al_index = []
# si_index = []
# ca_index = []
# ti_index = []
# cr_index = []
# fe_index = []
#
# na_mol_abundances = []
# mg_mol_abundances = []
# al_mol_abundances = []
# si_mol_abundances = []
# ca_mol_abundances = []
# ti_mol_abundances = []
# cr_mol_abundances = []
# fe_mol_abundances = []



def adjustsi_fct(si_pct):
    adj_si_pct = si_pct * adjust_si
    return adj_si_pct

def adjustna_fct(na_pct):
    adj_na_pct = na_pct * adjust_na
    return adj_na_pct



def createbspenvfile():
    if "BSP_Env_File" in os.listdir(os.getcwd()):
        pass
    else:
        bspenvfile = open("BSP_Env_File", 'w')
        one = "!BSP_Environment_File"
        two = "ALPHAMELTS_VERSION         MELTS"
        three = "ALPHAMELTS_MODE          isobaric"
        four = "ALPHAMELTS_MAXT 3000"
        five = "ALPHAMELTS_DELTAT        -2"
        six = "ALPHAMELTS_MINT       1020"
        seven = "ALPHAMELTS_FRACTIONATE_SOLIDS true"
        eight = "ALPHAMELTS_CELSIUS_OUTPUT true"
        nine = "ALPHAMELTS_SAVE_ALL true"
        ten = "ALPHAMELTS_SKIP_FAILURE true"
        eleven = "Suppress: alloy-liquid"

        bspenvfile.write("{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n".format(one, two, three,
                                                                               four, five, six, seven, eight, nine,
                                                                               ten, eleven))
        bspenvfile.close()

def createmorbenvfile():
    if "MORB_Env_File" in os.listdir(os.getcwd()):
        pass
    else:
        morbenvfile = open("MORB_Env_File", 'w')
        one = "!MORB_Environment_File"
        two = "ALPHAMELTS_VERSION         pMELTS"
        three = "ALPHAMELTS_MODE          isobaric"
        four = "ALPHAMELTS_MAXT 3000"
        five = "ALPHAMELTS_DELTAT        -2"
        six = "ALPHAMELTS_MINT       1000"
        seven = "ALPHAMELTS_FRACTIONATE_SOLIDS true"
        eight = "ALPHAMELTS_CELSIUS_OUTPUT true"
        nine = "ALPHAMELTS_SAVE_ALL true"
        ten = "ALPHAMELTS_SKIP_FAILURE true"
        eleven = "Suppress: alloy-liquid"

        morbenvfile.write("{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n".format(one, two, three,
                                                                                four, five, six, seven, eight, nine,
                                                                                ten, eleven))
        morbenvfile.close()




def runmelts_bsp(infile_directory, inputfilename):


    print("\n[~] Preparing alphaMELTS for BSP calculations...")

    if "{}_Completed_BSP_MELTS_Files".format(inputfilename[:-4]) in os.listdir(os.getcwd()):
        shutil.rmtree("{}_Completed_BSP_MELTS_Files".format(inputfilename[:-4]))
        os.mkdir("{}_Completed_BSP_MELTS_Files".format(inputfilename[:-4]))
    else:
        os.mkdir("{}_Completed_BSP_MELTS_Files".format(inputfilename[:-4]))

    bsp_outdir = (home_dir[0] + "/{}_Completed_BSP_MELTS_Files".format(inputfilename[:-4]))

    for i in os.listdir(infile_directory):

        os.chdir(home_dir[0])

        if "alphaMELTS_tbl.txt" in os.listdir(os.getcwd()):
            os.remove("alphaMELTS_tbl.txt")
        else:
            pass

        shutil.copy((infile_directory + "/" + str(i)), (home_dir[0] + "/" + str(i)))
        print("[~] Running BSP calculations for: {}".format(i[:-20]))
        p = subprocess.Popen(["run_alphamelts.command", "-f", "BSP_Env_File"], stdin=subprocess.PIPE)
        t = Timer(300, p.kill)
        t.start()
        print("\nTimeout timer started.  300 seconds until the loop continues...\n")
        p.communicate(input=b"\n".join([b"1", i, b"8", b"alloy-liquid", b"0", b"x", b"5", b"4", b"-1.4", b"2", b"2500", b"4200", b"4", b"1", b"0"]))
        t.cancel()

        if "alphaMELTS_tbl.txt" in os.listdir(os.getcwd()):
            oldname = "alphaMELTS_tbl.txt"
            newname = i[:-20] + "_BSP_OUTPUT"
            os.rename(oldname, newname)
            shutil.move(newname, bsp_outdir + "/{}".format(newname))
            os.remove(i)
            os.chdir(bsp_outdir)
            csv_file_name = newname + ".csv"
            with open(newname, 'r') as infile, open(csv_file_name, 'w') as outfile:
                in_txt = csv.reader(infile, delimiter=" ")
                out_csv = csv.writer(outfile)
                out_csv.writerows(in_txt)
                infile.close()
                outfile.close()
                os.remove(newname)
                print("[~] {} BSP calculation processed!".format(i[:-20]))

        else:
            print("\n[X] {} BSP calculation FAILED!".format(i[:-20]))
            pass

        if i in home_dir[0]:
            os.remove(home_dir[0] + "/{}".format(i))
        else:
            pass


    print("[~] Scraping BSP files for alloy abundances...")


    return ("{}_Completed_BSP_MELTS_Files".format(inputfilename))





def file_consolidate(path, init_path):

    os.chdir(path)

    if "EP_Consolidated_Output.csv" is os.listdir(os.getcwd()):
        os.remove("EP_Consolidated_Output.csv")
    else:
        pass
    if "EP_Consolidated_Output.csv" is os.listdir(init_path):
        os.remove(init_path + "/EP_Consolidated_Output.csv")
    else:
        pass

    outfile = open("EP_Consolidated_Output.csv", 'a')

    for i in os.listdir(os.getcwd()):
        if i != "EP_Consolidated_Output.csv":
            with open(i, 'r') as infile:
                reader = csv.reader(infile, delimiter=",")
                read_row = []
                for row in reader:
                    for p in row:
                        read_row.append(p)
                writethis = ",".join(str(z) for z in read_row)
                outfile.write("{}\n".format(writethis))
            os.remove(i)

    now_dir = os.getcwd() + "/{}".format("EP_Consolidated_Output.csv")
    now_dir2 = os.getcwd()
    to_dir = init_path + "/{}".format("EP_Consolidated_Output.csv")
    shutil.move(now_dir, to_dir)
    os.chdir(init_path)
    shutil.rmtree(now_dir2)

    print("[~] Consolidated file '{}' has been written!\n(Please see '{}' for your "
          "file!)\n".format("EP_Consolidated_Output.csv", init_path))

def logep(infile, infile_type, consol_file, init_path, library):

    if "{}_MELTS_{}_Input_Files".format(inputfile_list[0][:-4], infile_type) in os.listdir(os.getcwd()):
        shutil.rmtree("{}_MELTS_{}_Input_Files".format(inputfile_list[0][:-4], infile_type))
        os.mkdir("{}_MELTS_{}_Input_Files".format(inputfile_list[0][:-4], infile_type))
    else:
        os.mkdir("{}_MELTS_{}_Input_Files".format(inputfile_list[0][:-4], infile_type))

    if "{}_{}_ConsolidatedChemFile.csv".format(infile[:-4], infile_type) in os.listdir(os.getcwd()):
        os.remove("{}_{}_ConsolidatedChemFile.csv".format(infile[:-4], infile_type))
    else:
        pass

    chem_outfile = open("{}_{}_ConsolidatedChemFile.csv".format(infile[:-4], infile_type), 'a')

    chem_outfile.write("Star,FeO,CaO,Al2O3,Na2O,MgO,SiO2,TiO2,Cr2O3,NiO,Mass_Alloy\n")

    # try:
    with open(infile, 'r') as inputfile:
        if library is True:
            print("\n[~] Writing MELTS {} Input Files...".format(infile_type))
        else:
            print("[~] Preparing consolidated MELTS output file...")
        df = pd.DataFrame(pd.read_csv(inputfile))
        for index, row in df.iterrows():
            star_name = row['Star']

            # print(star_name)
            # print(row['[Fe/H]'])
            # print(row['[Ca/H]'])
            # print(row['[Al/H]'])
            # print(row['[Na/H]'])
            # print(row['[Mg/H]'])
            # print(row['[Si/H]'])
            # print(row['[Ti/H]'])
            # print(row['[Cr/H]'])
            # print(row['[Ni/H'])

            fe_abundance = (10 ** (row['[Fe/H]'])) * asplund_fe
            ca_abundance = (10 ** (row['[Ca/H]'])) * asplund_ca
            al_abundance = (10 ** (row['[Al/H]'])) * asplund_al
            na_abundance = (10 ** (row['[Na/H]'])) * asplund_na
            mg_abundance = (10 ** (row['[Mg/H]'])) * asplund_mg
            si_abundance = (10 ** (row['[Si/H]'])) * asplund_si
            ti_abundance = (10 ** (row['[Ti/H]'])) * asplund_ti
            cr_abundance = (10 ** (row['[Cr/H]'])) * asplund_cr
            ni_abundance = (10 ** (row['[Ni/H]'])) * asplund_ni
            total_abundances = (fe_abundance + ca_abundance + al_abundance + na_abundance + mg_abundance +
                                si_abundance + ti_abundance + cr_abundance + ni_abundance)

            # print(total_abundances)

            init_pct_fe = fe_abundance / total_abundances
            init_pct_ca = ca_abundance / total_abundances
            init_pct_al = al_abundance / total_abundances
            init_pct_na = na_abundance / total_abundances
            init_pct_mg = mg_abundance / total_abundances
            init_pct_si = si_abundance / total_abundances
            init_pct_ti = ti_abundance / total_abundances
            init_pct_cr = cr_abundance / total_abundances
            init_pct_ni = ni_abundance / total_abundances
            init_pct_sum = (init_pct_fe + init_pct_ca + init_pct_al + init_pct_na + init_pct_mg + init_pct_si +
                            init_pct_ti + init_pct_cr + init_pct_ni)

            # print(star_name)
            # print(init_pct_fe, init_pct_ca, init_pct_al, init_pct_na, init_pct_mg, init_pct_si,
            #                    init_pct_ti, init_pct_cr, init_pct_ni ,init_pct_sum)

            moles_si_remaining = adjustsi_fct(si_pct=init_pct_si)
            moles_na_remaining = adjustna_fct(na_pct=init_pct_na)

            norm_pct_sum = (init_pct_fe + init_pct_ca + init_pct_al + moles_na_remaining + init_pct_mg +
                            moles_si_remaining + init_pct_ti + init_pct_cr + init_pct_ni)

            norm_pct_fe = init_pct_fe / norm_pct_sum
            norm_pct_ca = init_pct_ca / norm_pct_sum
            norm_pct_al = init_pct_al / norm_pct_sum
            norm_pct_na = moles_na_remaining / norm_pct_sum
            norm_pct_mg = init_pct_mg / norm_pct_sum
            norm_pct_si = moles_si_remaining / norm_pct_sum
            norm_pct_ti = init_pct_ti / norm_pct_sum
            norm_pct_cr = init_pct_cr / norm_pct_sum
            norm_pct_ni = init_pct_ni / norm_pct_sum
            check_norm_sum = (
            norm_pct_fe + norm_pct_ca + norm_pct_al + norm_pct_na + norm_pct_mg + norm_pct_si +
            norm_pct_ti + norm_pct_cr + norm_pct_ni)

            wt_feo = ((norm_pct_fe * fe_atwt) * feo_molwt) / (num_feo_cations * fe_atwt)
            wt_cao = ((norm_pct_ca * ca_atwt) * cao_molwt) / (num_cao_cations * ca_atwt)
            wt_al2o3 = ((norm_pct_al * al_atwt) * al2o3_molwt) / (num_al2o3_cations * al_atwt)
            wt_na2o = ((norm_pct_na * na_atwt) * na2o_molwt) / (num_na2o_cations * na_atwt)
            wt_mgo = ((norm_pct_mg * mg_atwt) * mgo_molwt) / (num_mgo_cations * mg_atwt)
            wt_sio2 = ((norm_pct_si * si_atwt) * sio2_molwt) / (num_sio2_cations * si_atwt)
            wt_tio2 = ((norm_pct_ti * ti_atwt) * tio2_molwt) / (num_tio2_cations * ti_atwt)
            wt_cr2o3 = ((norm_pct_cr * cr_atwt) * cr2o3_molwt) / (num_cr2o3_cations * cr_atwt)
            wt_nio = ((norm_pct_ni * ni_atwt) * nio_molwt) / (num_nio_cations * ni_atwt)
            sum_oxwts = (wt_feo + wt_cao + wt_al2o3 + wt_na2o + wt_mgo + wt_sio2 + wt_tio2 + wt_cr2o3 + wt_nio)

            norm_wt_feo = (wt_feo / sum_oxwts) * 100.0
            norm_wt_cao = (wt_cao / sum_oxwts) * 100.0
            norm_wt_al2o3 = (wt_al2o3 / sum_oxwts) * 100.0
            norm_wt_na2o = (wt_na2o / sum_oxwts) * 100.0
            norm_wt_mgo = (wt_mgo / sum_oxwts) * 100.0
            norm_wt_sio2 = (wt_sio2 / sum_oxwts) * 100.0
            norm_wt_tio2 = (wt_tio2 / sum_oxwts) * 100.0
            norm_wt_cr2o3 = (wt_cr2o3 / sum_oxwts) * 100.0
            norm_wt_nio = (wt_nio / sum_oxwts) * 100.0
            norm_wt_sum_check = (norm_wt_feo + norm_wt_cao + norm_wt_al2o3 + norm_wt_na2o + norm_wt_mgo +
                                 norm_wt_sio2 + norm_wt_tio2 + norm_wt_cr2o3 + norm_wt_nio)

            # print(star_name)
            # print(norm_wt_feo, norm_wt_cao, norm_wt_al2o3, norm_wt_na2o, norm_wt_mgo, norm_wt_sio2,
            #       norm_wt_tio2, norm_wt_cr2o3, norm_wt_nio, norm_wt_sum_check)

            if (star_name + "_MELTS_{}_INFILE.txt".format(infile_type)) in os.listdir(os.getcwd()):
                os.remove(star_name + "_MELTS_{}_INFILE.txt".format(infile_type))
            else:
                pass

            melts_input_file = open(star_name + "_MELTS_{}_INFILE.txt".format(infile_type), 'w')

            title = "Title: {}".format(star_name)
            initfeo = "Initial Composition: FeO {}".format(norm_wt_feo)
            initcao = "Initial Composition: Cao {}".format(norm_wt_cao)
            inital2o3 = "Initial Composition: Al2O3 {}".format(norm_wt_al2o3)
            initna2o = "Initial Composition: Na2O {}".format(norm_wt_na2o)
            initmgo = "Initial Composition: MgO {}".format(norm_wt_mgo)
            initsio2 = "Initial Composition: SiO2 {}".format(norm_wt_sio2)
            inittio2 = "Initial Composition: TiO2 {}".format(norm_wt_tio2)
            initcr2o3 = "Initial Composition: Cr2O3 {}".format(norm_wt_cr2o3)
            initnio = "Initial Composition: NiO {}".format(norm_wt_nio)
            init_temp = 'Initial Temperature: 2000'
            final_temp = "Final Temperature: 800"
            inc_temp = "Increment Temperature: -5"
            init_press = "Initial Pressure: 500"
            final_press = "Final Pressure: 500"
            dpdt = "dp/dt: 0"
            mode = "Mode: Fractionate Solids"
            mode2 = "Mode: Isobaric"

            melts_input_file.write(
                "{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n".format(title,
                                                                                                  initfeo,
                                                                                                  initcao,
                                                                                                  inital2o3,
                                                                                                  initna2o,
                                                                                                  initmgo,
                                                                                                  initsio2,
                                                                                                  inittio2,
                                                                                                  initcr2o3,
                                                                                                  initnio,
                                                                                                  init_temp,
                                                                                                  final_temp,
                                                                                                  inc_temp,
                                                                                                  init_press,
                                                                                                  final_press,
                                                                                                  dpdt, mode,
                                                                                                  mode2))

            melts_input_file.close()

            shutil.move((os.getcwd() + "/" + star_name + "_MELTS_{}_INFILE.txt".format(infile_type)),
                        (os.getcwd() + "/{}_MELTS_{}_Input_Files/".format(inputfile_list[0][:-4], infile_type)
                         + star_name + "_MELTS_{}_INFILE.txt".format(infile_type)))

            chem_outfile.write("{},{},{},{},{},{},{},{},{},{}\n".format(star_name, norm_wt_feo, norm_wt_cao, norm_wt_al2o3,
                    norm_wt_na2o, norm_wt_mgo, norm_wt_sio2, norm_wt_tio2, norm_wt_cr2o3, norm_wt_nio))


        chem_outfile.close()

        if library is True:
            infiledir = (os.getcwd() + "/{}_MELTS_{}_Input_Files/".format(inputfile_list[0][:-4], infile_type))
            print("[~] MELTS {} Input Files Written!".format(infile_type))
            print("[~] MELTS files stored in {}".format(infiledir))
        else:
            pass
        infiledir = (os.getcwd() + "/{}_MELTS_{}_Input_Files/".format(inputfile_list[0][:-4], infile_type))
        print("[~] Launching alphaMELTS for {} Calculations...".format(infile_type))
        runmelts_bsp(infile_directory=infiledir, inputfilename=infile)

        chem_outfile.close()

        if consol_file is True:
            file_consolidate(path=infiledir, init_path=init_path)
        else:
            file_consolidate(path=infiledir, init_path=init_path)
            scrapebsp2(infiledirectory=(home_dir[0] + "/{}_Completed_BSP_MELTS_Files".format(infile[:-4])),
                       inputfilename=infile)
            bsprecalc(bspmeltsfilesdir=(home_dir[0] + "{}_Completed_BSP_MELTS_Files".format(infile[:-4])),
                      infilename=infile, alloy_mass_infile="alloy_mass.csv",
                      bsp_chem_infile="{}_{}_ConsolidatedChemFile.csv".format(infile[:-4], infile_type))

    # except:
    #     # raise Exception
    #     print("\nError!  There is likely an issue with the formatting of your input file!\n"
    #           "Please refer to the documentation for more information.\n")
    #     time.sleep(8)
    #     initialization()
    #
    # sys.exit()


def molepct(infile, infile_type, consol_file, init_path, library):

    if "{}_MELTS_{}_Input_Files".format(inputfile_list[0][:-4], infile_type) in os.listdir(os.getcwd()):
        shutil.rmtree("{}_MELTS_{}_Input_Files".format(inputfile_list[0][:-4], infile_type))
        os.mkdir("{}_MELTS_{}_Input_Files".format(inputfile_list[0][:-4], infile_type))
    else:
        os.mkdir("{}_MELTS_{}_Input_Files".format(inputfile_list[0][:-4], infile_type))

    if "{}_{}_ConsolidatedChemFile.csv".format(infile[:-4], infile_type) in os.listdir(os.getcwd()):
        os.remove("{}_{}_ConsolidatedChemFile.csv".format(infile[:-4], infile_type))
    else:
        pass

    chem_outfile = open("{}_{}_ConsolidatedChemFile.csv".format(infile[:-4], infile_type), 'a')

    chem_outfile.write("Star,FeO,CaO,Al2O3,Na2O,MgO,SiO2,TiO2,Cr2O3,NiO,Mass_Alloy\n")

    # try:
    with open(infile, 'r') as inputfile:
        if library is True:
            print("\n[~] Writing MELTS {} Input Files...".format(infile_type))
        else:
            print("[~] Preparing consolidated MELTS output file...")
        df = pd.DataFrame(pd.read_csv(inputfile))
        for index, row in df.iterrows():

            star_name = row['Star']

            # print(star_name)
            # print(row['[Fe/H]'])
            # print(row['[Ca/H]'])
            # print(row['[Al/H]'])
            # print(row['[Na/H]'])
            # print(row['[Mg/H]'])
            # print(row['[Si/H]'])
            # print(row['[Ti/H]'])
            # print(row['[Cr/H]'])

            # print("\n\n_________________________________________\n")
            # print(star_name)

            fe_abundance = row['Fe']
            ca_abundance = row['Ca']
            al_abundance = row['Al']
            na_abundance = row['Na']
            mg_abundance = row['Mg']
            si_abundance = row['Si']
            ti_abundance = row['Ti']
            cr_abundance = row['Cr']
            ni_abundance = row['Ni']
            total_abundances = (fe_abundance + ca_abundance + al_abundance + na_abundance + mg_abundance +
                                si_abundance + ti_abundance + cr_abundance + ni_abundance)

            # print("Input abundances:")
            # print(fe_abundance, ca_abundance, al_abundance, na_abundance, mg_abundance, si_abundance,
            #       ti_abundance, cr_abundance, ni_abundance, total_abundances)


            # print(total_abundances)

            init_pct_fe = fe_abundance / total_abundances
            init_pct_ca = ca_abundance / total_abundances
            init_pct_al = al_abundance / total_abundances
            init_pct_na = na_abundance / total_abundances
            init_pct_mg = mg_abundance / total_abundances
            init_pct_si = si_abundance / total_abundances
            init_pct_ti = ti_abundance / total_abundances
            init_pct_cr = cr_abundance / total_abundances
            init_pct_ni = ni_abundance / total_abundances
            init_pct_sum = (init_pct_fe + init_pct_ca + init_pct_al + init_pct_na + init_pct_mg + init_pct_si +
                            init_pct_ti + init_pct_cr + init_pct_ni)

            # print("Init Cation%:")
            # print(init_pct_fe, init_pct_ca, init_pct_al, init_pct_na, init_pct_mg, init_pct_si,
            #                    init_pct_ti, init_pct_cr, init_pct_sum)

            moles_si_remaining = adjustsi_fct(si_pct=init_pct_si)
            moles_na_remaining = adjustna_fct(na_pct=init_pct_na)
            #
            # print("Moles Si/Na Remaining:")
            # print(moles_si_remaining, moles_na_remaining)

            norm_pct_sum = (init_pct_fe + init_pct_ca + init_pct_al + moles_na_remaining + init_pct_mg +
                            moles_si_remaining + init_pct_ti + init_pct_cr + init_pct_ni)

            norm_pct_fe = init_pct_fe / norm_pct_sum
            norm_pct_ca = init_pct_ca / norm_pct_sum
            norm_pct_al = init_pct_al / norm_pct_sum
            norm_pct_na = moles_na_remaining / norm_pct_sum
            norm_pct_mg = init_pct_mg / norm_pct_sum
            norm_pct_si = moles_si_remaining / norm_pct_sum
            norm_pct_ti = init_pct_ti / norm_pct_sum
            norm_pct_cr = init_pct_cr / norm_pct_sum
            norm_pct_ni = init_pct_ni / norm_pct_sum
            check_norm_sum = (
            norm_pct_fe + norm_pct_ca + norm_pct_al + norm_pct_na + norm_pct_mg + norm_pct_si +
            norm_pct_ti + norm_pct_cr + norm_pct_ni)

            # print("Normalized Cation% After Si/Na Correction:")
            # print(norm_pct_fe, norm_pct_ca, norm_pct_al, norm_pct_na, norm_pct_mg, norm_pct_si, norm_pct_ti,
            #       norm_pct_cr, norm_pct_ni, norm_pct_sum)

            wt_feo = ((norm_pct_fe * fe_atwt) * feo_molwt) / (num_feo_cations * fe_atwt)
            wt_cao = ((norm_pct_ca * ca_atwt) * cao_molwt) / (num_cao_cations * ca_atwt)
            wt_al2o3 = ((norm_pct_al * al_atwt) * al2o3_molwt) / (num_al2o3_cations * al_atwt)
            wt_na2o = ((norm_pct_na * na_atwt) * na2o_molwt) / (num_na2o_cations * na_atwt)
            wt_mgo = ((norm_pct_mg * mg_atwt) * mgo_molwt) / (num_mgo_cations * mg_atwt)
            wt_sio2 = ((norm_pct_si * si_atwt) * sio2_molwt) / (num_sio2_cations * si_atwt)
            wt_tio2 = ((norm_pct_ti * ti_atwt) * tio2_molwt) / (num_tio2_cations * ti_atwt)
            wt_cr2o3 = ((norm_pct_cr * cr_atwt) * cr2o3_molwt) / (num_cr2o3_cations * cr_atwt)
            wt_nio = ((norm_pct_ni * ni_atwt) * nio_molwt) / (num_nio_cations * ni_atwt)
            sum_oxwts = (wt_feo + wt_cao + wt_al2o3 + wt_na2o + wt_mgo + wt_sio2 + wt_tio2 + wt_cr2o3 + wt_nio)

            # print("Wt Oxides:")
            # print(wt_feo, wt_cao, wt_al2o3, wt_na2o, wt_mgo, wt_sio2, wt_tio2, wt_cr2o3, wt_nio, sum_oxwts)

            norm_wt_feo = (wt_feo / sum_oxwts) * 100.0
            norm_wt_cao = (wt_cao / sum_oxwts) * 100.0
            norm_wt_al2o3 = (wt_al2o3 / sum_oxwts) * 100.0
            norm_wt_na2o = (wt_na2o / sum_oxwts) * 100.0
            norm_wt_mgo = (wt_mgo / sum_oxwts) * 100.0
            norm_wt_sio2 = (wt_sio2 / sum_oxwts) * 100.0
            norm_wt_tio2 = (wt_tio2 / sum_oxwts) * 100.0
            norm_wt_cr2o3 = (wt_cr2o3 / sum_oxwts) * 100.0
            norm_wt_nio = (wt_nio / sum_oxwts) * 100.0
            norm_wt_sum_check = (norm_wt_feo + norm_wt_cao + norm_wt_al2o3 + norm_wt_na2o + norm_wt_mgo +
                                 norm_wt_sio2 + norm_wt_tio2 + norm_wt_cr2o3 + norm_wt_nio)

            # print(star_name)
            # print(norm_wt_feo, norm_wt_cao, norm_wt_al2o3, norm_wt_na2o, norm_wt_mgo, norm_wt_sio2,
            #       norm_wt_tio2, norm_wt_cr2o3, norm_wt_nio, norm_wt_sum_check)

            if (star_name + "_MELTS_{}_INFILE.txt") in os.listdir(os.getcwd()):
                os.remove(star_name + "_MELTS_{}_INFILE.txt".format(infile_type))
            else:
                pass

            melts_input_file = open(star_name + "_MELTS_{}_INFILE.txt".format(infile_type), 'w')

            title = "Title: {}".format(star_name)
            initfeo = "Initial Composition: FeO {}".format(norm_wt_feo)
            initcao = "Initial Composition: Cao {}".format(norm_wt_cao)
            inital2o3 = "Initial Composition: Al2O3 {}".format(norm_wt_al2o3)
            initna2o = "Initial Composition: Na2O {}".format(norm_wt_na2o)
            initmgo = "Initial Composition: MgO {}".format(norm_wt_mgo)
            initsio2 = "Initial Composition: SiO2 {}".format(norm_wt_sio2)
            inittio2 = "Initial Composition: TiO2 {}".format(norm_wt_tio2)
            initcr2o3 = "Initial Composition: Cr2O3 {}".format(norm_wt_cr2o3)
            initnio = "Initial Composition: NiO {}".format(norm_wt_nio)
            init_temp = 'Initial Temperature: 2000'
            final_temp = "Final Temperature: 800"
            inc_temp = "Increment Temperature: -5"
            init_press = "Initial Pressure: 500"
            final_press = "Final Pressure: 500"
            dpdt = "dp/dt: 0"
            mode = "Mode: Fractionate Solids"
            mode2 = "Mode: Isobaric"

            melts_input_file.write(
                "{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n".format(title,
                                                                                                  initfeo,
                                                                                                  initcao,
                                                                                                  inital2o3,
                                                                                                  initna2o,
                                                                                                  initmgo,
                                                                                                  initsio2,
                                                                                                  inittio2,
                                                                                                  initcr2o3,
                                                                                                  initnio,
                                                                                                  init_temp,
                                                                                                  final_temp,
                                                                                                  inc_temp,
                                                                                                  init_press,
                                                                                                  final_press,
                                                                                                  dpdt, mode,
                                                                                                  mode2))

            chem_outfile.write(
                "{},{},{},{},{},{},{},{},{},{}\n".format(star_name, norm_wt_feo, norm_wt_cao, norm_wt_al2o3,
                                                         norm_wt_na2o, norm_wt_mgo, norm_wt_sio2, norm_wt_tio2,
                                                         norm_wt_cr2o3, norm_wt_nio))

            melts_input_file.close()

            shutil.move((os.getcwd() + "/" + star_name + "_MELTS_{}_INFILE.txt".format(infile_type)),
                        (os.getcwd() + "/{}_MELTS_{}_Input_Files/".format(inputfile_list[0][:-4], infile_type)
                         + star_name + "_MELTS_{}_INFILE.txt".format(infile_type)))

        infiledir = os.getcwd() + "/{}_MELTS_{}_Input_Files/".format(inputfile_list[0][:-4], infile_type)
        if library is True:
            print("[~] MELTS {} Input Files Written!".format(infile_type))
            print("[~] MELTS files stored in " + (os.getcwd()))
        else:
            pass
        # print("[~] Launching alphaMELTS for {} Calculations...".format(infile_type))

        infiledir = (os.getcwd() + "/{}_MELTS_{}_Input_Files/".format(inputfile_list[0][:-4], infile_type))
        print("[~] Launching alphaMELTS for {} Calculations...".format(infile_type))
        runmelts_bsp(infile_directory=infiledir, inputfilename=infile)

        chem_outfile.close()

        if consol_file is True:
            file_consolidate(path=infiledir, init_path=init_path)
        else:
            file_consolidate(path=infiledir, init_path=init_path)
            scrapebsp2(infiledirectory=(home_dir[0] + "/{}_Completed_BSP_MELTS_Files".format(infile[:-4])), inputfilename=infile)
            bsprecalc(bspmeltsfilesdir=(home_dir[0] + "{}_Completed_BSP_MELTS_Files".format(infile[:-4])),
                      infilename=infile, alloy_mass_infile="alloy_mass.csv",
                      bsp_chem_infile="{}_{}_ConsolidatedChemFile.csv".format(infile[:-4], infile_type))

    # except:
    #     raise Exception
    #     # print("\nError!  There is likely an issue with the formatting of your input file!\n"
    #     #       "Please refer to the documentation for more information.\n")
    #     time.sleep(8)
    #     initialization()


    # sys.exit()

def bsprecalc(bspmeltsfilesdir, infilename, alloy_mass_infile, bsp_chem_infile):



    if "{}_BSP_Composition.csv".format(infilename[:-4]) in os.listdir(home_dir[0]):
        os.remove(home_dir[0] + "/{}_BSP_Composition.csv".format(infilename[:-4]))

    bsp_chemfile = open("{}_BSP_Composition.csv".format(infilename[:-4]), 'a')
    bsp_comp_header = "Star,FeO,Na2O,MgO,Al2O3,SiO2,CaO,TiO2,Cr2O3"
    bsp_chemfile.write("{}\n".format(bsp_comp_header))


    if "bsp_debug.csv" in os.listdir(os.getcwd()):
        os.remove("bsp_debug.csv")

    bsp_debug = open("bsp_debug.csv", 'a')


    if os.path.exists(home_dir[0] + "/MELTS_MORB_Input_Files"):
        shutil.rmtree(home_dir[0] + "/MELTS_MORB_Input_Files")
    else:
        pass

    os.mkdir(home_dir[0] + "/MELTS_MORB_Input_Files")

    # need to build in the MELTS file parser to extract alloy info
    # construct it so that it extracts alloy and chemistry, and the write to file with predictable headers

    # for i in os.listdir(os.getcwd()):
    df_chem = pd.read_csv(bsp_chem_infile)
    df_alloy = pd.read_csv(alloy_mass_infile)
    for row in df_chem.index:
        try:
            # print(df_chem)
            # print(df_chem.index)
            star_name = df_chem['Star'][row]
            feo_in = df_chem['FeO'][row]
            na2o_in = df_chem['Na2O'][row]
            mgo_in = df_chem['MgO'][row]
            al2o3_in = df_chem['Al2O3'][row]
            sio2_in = df_chem['SiO2'][row]
            cao_in = df_chem['CaO'][row]
            nio_in = df_chem['NiO'][row]
            tio2_in = df_chem['TiO2'][row]
            cr2o3_in = df_chem['Cr2O3'][row]

            in1_header = "1,feo,na2o,mgo,al2o3,sio2,cao,nio,tio2,cr2o3"
            in1 = ",{},{},{},{},{},{},{},{},{}".format(feo_in, na2o_in, mgo_in, al2o3_in, sio2_in, cao_in, nio_in, tio2_in, cr2o3_in)
            bsp_debug.write("{}\n{}\n".format(in1_header, in1))

            for row in df_alloy.index:
                star_name2 = df_alloy['star'][row]
                alloy_mass = df_alloy['alloy mass'][row]

                if star_name == star_name2:

                    feo_moles = feo_in / feo_molwt
                    na2o_moles = na2o_in / na2o_molwt
                    mgo_moles = mgo_in / mgo_molwt
                    al2o3_moles = al2o3_in / al2o3_molwt
                    sio2_moles = sio2_in / sio2_molwt
                    cao_moles = cao_in / cao_molwt
                    nio_moles = nio_in / nio_molwt
                    tio2_moles = tio2_in / tio2_molwt
                    cr2o3_moles = cr2o3_in / cr2o3_molwt

                    in2_header = "2,feo,na2o,mgo,al2o3,sio2,cao,nio,tio2,cr2o3"
                    in2 = ",{},{},{},{},{},{},{},{},{}".format(feo_moles, na2o_moles, mgo_moles, al2o3_moles, sio2_moles, cao_moles, nio_moles, tio2_moles, cr2o3_moles)
                    bsp_debug.write("{}\n{}\n".format(in2_header, in2))


                    fe_moles = feo_moles * num_feo_cations
                    na_moles = na2o_moles * num_na2o_cations
                    mg_moles = mgo_moles * num_mgo_cations
                    al_moles = al2o3_moles * num_al2o3_cations
                    si_moles = sio2_moles * num_sio2_cations
                    ca_moles = cao_moles * num_cao_cations
                    ni_moles = nio_moles * num_nio_cations
                    ti_moles = tio2_moles * num_tio2_cations
                    cr_moles = cr2o3_moles * num_cr2o3_cations

                    in3_header = "3,fe,na,mg,al,si,ca,ni,ti,cr"
                    in3 = ",{},{},{},{},{},{},{},{},{}".format(fe_moles, na_moles, mg_moles, al_moles,
                            si_moles, ca_moles, ni_moles, ti_moles, cr_moles)
                    bsp_debug.write("{}\n{}\n".format(in3_header, in3))

                    fe_mass = fe_moles * fe_atwt
                    na_mass = na_moles * na_atwt
                    mg_mass = mg_moles * mg_atwt
                    al_mass = al_moles * al_atwt
                    si_mass = si_moles * si_atwt
                    ca_mass = ca_moles * ca_atwt
                    ni_mass = ni_moles * ni_atwt
                    ti_mass = ti_moles * ti_atwt
                    cr_mass = cr_moles * cr_atwt

                    in4_header = "4,fe,na,mg,al,si,ca,ni,ti,cr"
                    in4 = ",{},{},{},{},{},{},{},{},{}".format(fe_mass, na_mass, mg_mass, al_mass,
                                si_mass, ca_mass, ni_mass, ti_mass, cr_mass)
                    bsp_debug.write("{}\n{}\n".format(in4_header, in4))

                    alloy_subt_ni_mass = alloy_mass - ni_mass
                    if alloy_subt_ni_mass < 0:
                        print("Ni MASS ERROR!")
                        sys.exit()
                    else:
                        pass


                    new_mass_fe = fe_mass - alloy_subt_ni_mass

                    if new_mass_fe < 0:
                        print("Fe MASS ERROR!")
                        sys.exit()

                    remaining_moles_fe = new_mass_fe / fe_atwt
                    remaining_moles_feo = remaining_moles_fe * num_feo_cations
                    remaining_mass_feo = remaining_moles_feo * feo_molwt

                    in5_header = "5,alloy_but_ni_mass,new_mass_fe,remaining_moles_fe,remaining_moles_feo,remaining_mass_feo"
                    in5 = ",{},{},{},{},{}".format(alloy_subt_ni_mass, new_mass_fe, remaining_moles_fe, remaining_moles_feo,
                                                   remaining_mass_feo)
                    bsp_debug.write("{}\n{}\n".format(in5_header, in5))

                    unnormalized_sum = (remaining_mass_feo + na2o_in + mgo_in + al2o3_in + sio2_in + cao_in +
                                        tio2_in + cr2o3_in)

                    norm_feo = remaining_mass_feo / unnormalized_sum * 100.0
                    norm_na2o = na2o_in / unnormalized_sum * 100.0
                    norm_mgo = mgo_in / unnormalized_sum * 100.0
                    norm_al2o3 = al2o3_in / unnormalized_sum * 100.0
                    norm_sio2 = sio2_in / unnormalized_sum * 100.0
                    norm_cao = cao_in / unnormalized_sum * 100.0
                    norm_tio2 = tio2_in / unnormalized_sum * 100.0
                    norm_cr2o3 = cr2o3_in / unnormalized_sum * 100.0
                    norm_sum = norm_feo + norm_na2o + norm_mgo + norm_al2o3 + norm_sio2 + norm_cao + norm_tio2 + norm_cr2o3

                    in6_header = "6,feo,na2o,mgo,al2o3,sio2,cao,tio2,cr2o3,unnorm_sum,norm_sum"
                    in6 = ",{},{},{},{},{},{},{},{},{},{}".format(norm_feo, norm_na2o, norm_mgo, norm_al2o3,
                            norm_sio2, norm_cao, norm_tio2, norm_cr2o3, unnormalized_sum, norm_sum)
                    bsp_debug.write("{}\n{}\n".format(in6_header, in6))

                    bsp_comp = "{},{},{},{},{},{},{},{},{}".format(star_name, norm_feo, norm_na2o, norm_mgo, norm_al2o3,
                            norm_sio2, norm_cao, norm_tio2, norm_cr2o3)
                    bsp_chemfile.write("{}\n".format(bsp_comp))




                    # print(norm_feo)
                    # print(norm_sum)
                    #
                    # if norm_sum != 100.0:
                    #     print("ERROR!  NORMALIZED SUM IS NOT 100.0!")
                    #     sys.exit()

                    title = "Title: {}".format(star_name)
                    bsp_feo = "Initial Composition: FeO {}".format(norm_feo)
                    bsp_na2o = "Initial Composition: Na2O {}".format(norm_na2o)
                    bsp_mgo = "Initial Composition: MgO {}".format(norm_mgo)
                    bsp_al2o3 = "Initial Composition: Al2O3 {}".format(norm_al2o3)
                    bsp_sio2 = "Initial Composition: SiO2 {}".format(norm_sio2)
                    bsp_cao = "Initial Composition: CaO {}".format(norm_cao)
                    bsp_tio2 = "Initial Composition: TiO2 {}".format(norm_tio2)
                    bsp_cr2o3 = "Initial Composition: Cr2O3 {}".format(norm_cr2o3)
                    init_temp = 'Initial Temperature: 2000'
                    final_temp = "Final Temperature: 800"
                    inc_temp = "Increment Temperature: -5"
                    init_press = "Initial Pressure: 10000"
                    final_press = "Final Pressure: 10000"
                    dpdt = "dp/dt: 0"
                    mode = "Mode: Fractionate Solids"
                    mode2 = "Mode: Isobaric"

                    melts_morb_input_file_vars = "{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}".format(
                        title,
                        bsp_feo, bsp_na2o, bsp_mgo, bsp_al2o3, bsp_sio2, bsp_cao, bsp_tio2, bsp_cr2o3,
                        init_temp, init_temp, final_temp, inc_temp, init_press, final_press, dpdt, mode, mode2)

                    morb_outfile = open("{}_MELTS_{}_INFILE.txt".format(star_name, "MORB"), 'w')
                    morb_outfile.write(melts_morb_input_file_vars)
                    morb_outfile.close()

                    fdir = os.getcwd() + "/{}_MELTS_{}_INFILE.txt".format(star_name, "MORB")
                    tdir = home_dir[0] + "/MELTS_MORB_Input_Files/{}_MELTS_{}_INFILE.txt".format(star_name, "MORB")
                    shutil.move(fdir, tdir)
        except:
            pass

    bsp_debug.close()
    bsp_chemfile.close()

    hefestofilewriter_bsp(bulkfile=(home_dir[0] + "/{}_BSP_Composition.csv".format(infilename[:-4])), infilename=infilename)
    runmelts_morb(infile_directory=(home_dir[0] + "/MELTS_MORB_Input_Files"), inputfilename=infilename[:-4])


def runmelts_morb(infile_directory, inputfilename):

    if "{}_Completed_MORB_MELTS_Files".format(inputfilename) in os.listdir(os.getcwd()):
        shutil.rmtree("{}_Completed_MORB_MELTS_Files".format(inputfilename))
        os.mkdir("{}_Completed_MORB_MELTS_Files".format(inputfilename))
    else:
        os.mkdir("{}_Completed_MORB_MELTS_Files".format(inputfilename))

    for i in os.listdir(infile_directory):

        os.chdir(home_dir[0])

        if "alphaMELTS_tbl.txt" in os.listdir(os.getcwd()):
            os.remove("alphaMELTS_tbl.txt")
        else:
            pass

        shutil.copy((infile_directory + "/" + i), (home_dir[0] + "/" + i))
        print("[~] Running MORB calculations for: {}".format(i[:-20]))
        p = subprocess.Popen(["run_alphamelts.command", "-f", "MORB_Env_File"], stdin=subprocess.PIPE)
        t = Timer(300, p.kill)
        t.start()
        print("\nTimeout timer started.  300 seconds until the loop continues...\n")
        p.communicate(input=b"\n".join(
            [b"1", i, b"8", b"alloy-liquid", b"0", b"x", b"5", b"3", b"+0.4", b"2", b"1400", b"10000", b"10", b"1",
             b"3", b"1", b"liquid", b"1", b"0.05", b"0", b"10", b"0", b"4", b"0"]))
        t.cancel()

        if "alphaMELTS_tbl.txt" in os.listdir(os.getcwd()):
            oldname = "alphaMELTS_tbl.txt"
            newname = i[:-20] + "_MORB_OUTPUT"
            os.rename(oldname, newname)
            shutil.move(newname, home_dir[0] + "/{}_Completed_MORB_MELTS_Files".format(inputfilename))
            os.remove(i)
            os.chdir(home_dir[0] + "/{}_Completed_MORB_MELTS_Files".format(inputfilename))
            csv_file_name = newname + ".csv"
            with open(newname, 'rb') as infile, open(csv_file_name, 'wb') as outfile:
                in_txt = csv.reader(infile, delimiter=" ")
                out_csv = csv.writer(outfile)
                out_csv.writerows(in_txt)
                infile.close()
                outfile.close()
                os.remove(newname)
                print("[~] {} MORB calculation processed!".format(i[:-17]))

        else:
            print("[X] {} MORB calculation FAILED!".format(i[:-20]))
            pass

        if i in home_dir[0]:
            os.remove(home_dir[0] + "/{}".format(i))
        else:
            pass

    scrapemorb(infiledirectory=(home_dir[0] + "/{}_Completed_MORB_MELTS_Files".format(inputfilename)), infilename=inputfilename)


def scrapebsp2(infiledirectory, inputfilename):

    if "alloy_mass.csv" in os.listdir(home_dir[0]):
        os.remove(home_dir[0] + "/alloy_mass.csv")
    else:
        pass

    alloy_mass_outfile = open(home_dir[0] + "/alloy_mass.csv", 'a')

    alloy_mass_outfile.write("{},{}\n".format("star", "alloy mass"))

    os.chdir(infiledirectory)



    for i in os.listdir(os.getcwd()):
        try:
            os.chdir(infiledirectory)
            if enumerate(i, 1) >= 100:
                alloy_abundance = []
                with open(i, 'r') as infile:
                    reader = csv.reader(infile)
                    row1 = next(reader)
                    star_name = row1[1]
                    alloy_abundance.append(star_name)
                    for num, line in enumerate(reader, 1):
                        if "Phase" in line:
                            csv_list = list(reader)
                            alloy_index = csv_list[0].index("alloy-solid_0")
                            for row in csv_list[1:]:
                                if not row == []:
                                    a = row[alloy_index]
                                    x = str(float(a))
                                    alloy_abundance.append(x)
                                else:
                                    break
                        else:
                            pass
                os.chdir(home_dir[0])
                # print(alloy_abundance[1:])
                alloy_abundance_nums = []
                for z in alloy_abundance[1:]:
                    alloy_abundance_nums.append(float(z))
                alloy_abundance_sum = sum(alloy_abundance_nums)
                print("Alloy abundance for {}: {}".format(alloy_abundance[0], alloy_abundance_sum))
                alloy_mass_outfile.write("{},{}\n".format(alloy_abundance[0], alloy_abundance_sum))
        except:
            pass
        else:
            pass




def hefestofilewriter_bsp(bulkfile, infilename):

    os.chdir(home_dir[0])

    infilename = infilename[:-4]

    if os.path.exists("{}_BSP_HeFESTo_Input_Files".format(infilename)):
        shutil.rmtree("{}_BSP_HeFESTo_Input_Files".format(infilename))
    else:
        pass

    os.mkdir("{}_BSP_HeFESTo_Input_Files".format(infilename))

    bulkfile_df = pd.read_csv(bulkfile)

    for row in bulkfile_df.index:
        try:
            star = bulkfile_df["Star"][row]
            si = bulkfile_df["SiO2"][row]
            mg = bulkfile_df["MgO"][row]
            fe = bulkfile_df["FeO"][row]
            ca = bulkfile_df["CaO"][row]
            al = bulkfile_df["Al2O3"][row]
            na = bulkfile_df["Na2O"][row]

            hefesto_bsp_file = open("{}_BSP_HeFESTo_Infile.txt".format(star), 'a')

            format_of_file = "0,20,80,1600,0,-2,0\n6,2,4,2\noxides\nSi          {}      5.39386    0\nMg          {}     2.71075    0\n" \
                             "Fe          {}      .79840    0\nCa            {}      .31431    0\nAl            {}      .96680    0\n" \
                             "Na            {}      .40654    0\n1,1,1\ninv251010\n47\nphase plg\n1\nan\nab\nphase sp\n0\nsp\nhc\n" \
                             "phase opx\n1\nen\nfs\nmgts\nodi\nphase c2c\n0\nmgc2\nfec2\nphase cpx\n1\ndi\nhe\ncen\ncats\njd\n" \
                             "phase gt\n0\npy\nal\ngr\nmgmj\njdmj\nphase cpv\n0\ncapv\nphase ol\n1\nfo\nfa\nphase wa\n0\nmgwa\nfewa\n" \
                             "phase ri\n0\nmgri\nferi\nphase il\n0\nmgil\nfeil\nco\nphase pv\n0\nmgpv\nfepv\nalpv\nphase ppv\n0\nmppv\n" \
                             "fppv\nappv\nphase cf\n0\nmgcf\nfecf\nnacf\nphase mw\n0\npe\nwu\nphase qtz\n1\nqtz\nphase coes\n0\ncoes\n" \
                             "phase st\n0\nst\nphase apbo\n0\napbo\nphase ky\n0\nky\nphase neph\n0\nneph".format(si,
                                mg, fe, ca, al, na)

            hefesto_bsp_file.write(format_of_file)
            hefesto_bsp_file.close()
            fdir = home_dir[0] + "/{}".format("{}_BSP_HeFESTo_Infile.txt".format(star))
            tdir = home_dir[0] + "/{}/{}".format("{}_BSP_HeFESTo_Input_Files".format(infilename),
                                                 "{}_BSP_HeFESTo_Infile.txt".format(star))
            shutil.move(fdir, tdir)
        except:
            pass

    print("\n[~] BSP HeFESTo input files available in '{}'".format("{}_BSP_HeFESTo_Input_Files".format(infilename)))


def hefestofilewriter_morb(bulkfile, infilename):

    os.chdir(home_dir[0])

    if os.path.exists("{}_MORB_HeFESTo_Input_Files".format(infilename)):
        shutil.rmtree("{}_MORB_HeFESTo_Input_Files".format(infilename))
    else:
        pass

    os.mkdir("{}_MORB_HeFESTo_Input_Files".format(infilename))

    bulkfile_df = pd.read_csv(bulkfile)

    for row in bulkfile_df.index:
        try:
            star = bulkfile_df["Star"][row]
            si = bulkfile_df["SiO2"][row]
            mg = bulkfile_df["MgO"][row]
            fe = bulkfile_df["FeO"][row]
            ca = bulkfile_df["CaO"][row]
            al = bulkfile_df["Al2O3"][row]
            na = bulkfile_df["Na2O"][row]

            hefesto_morb_file = open("{}_MORB_HeFESTo_Infile.txt".format(star), 'a')

            format_of_file = "0,20,80,1200,0,-2,0\n6,2,4,2\noxides\nSi           {}     5.33159    0\n" \
                             "Mg           {}     1.37685    0\nFe           {}      .55527    0\n" \
                             "Ca           {}     1.33440    0\nAl           {}     1.82602    0\n" \
                             "Na           {}     0.71860    0\n1,1,1\ninv251010\n47\nphase plg\n1\nan\nab\nphase sp\n0\nsp\n" \
                             "hc\nphase opx\n1\nen\nfs\nmgts\nodi\nphase c2c\n0\nmgc2\nfec2\nphase cpx\n1\ndi\nhe\ncen\ncats\n" \
                             "jd\nphase gt\n0\npy\nal\ngr\nmgmj\njdmj\nphase cpv\n0\ncapv\nphase ol\n1\nfo\nfa\nphase wa\n0\n" \
                             "mgwa\nfewa\nphase ri\n0\nmgri\nferi\nphase il\n0\nmgil\nfeil\nco\nphase pv\n0\nmgpv\nfepv\nalpv\n" \
                             "phase ppv\n0\nmppv\nfppv\nappv\nphase cf\n0\nmgcf\nfecf\nnacf\nphase mw\n0\npe\nwu\nphase qtz\n" \
                             "1\nqtz\nphase coes\n0\ncoes\nphase st\n0\nst\nphase apbo\n0\napbo\nphase ky\n0\nky\nphase neph\n" \
                             "0\nneph".format(si, mg, fe, ca, al, na)

            hefesto_morb_file.write(format_of_file)
            hefesto_morb_file.close()
            fdir = home_dir[0] + "/{}".format("{}_MORB_HeFESTo_Infile.txt".format(star))
            tdir = home_dir[0] + "/{}/{}".format("{}_MORB_HeFESTo_Input_Files".format(infilename),
                                                 "{}_MORB_HeFESTo_Infile.txt".format(star))
            shutil.move(fdir, tdir)
        except:
            pass

    print("\n[~] Crust HeFESTo input files available in '{}'".format("{}_MORB_HeFESTo_Input_Files".format(infilename)))

    consol_hefestofolders(infilename=infilename)




def consol_hefestofolders(infilename):

    print('\n[~] Consolidating HeFESTo input file folders...')

    bsp_folder = "/{}_BSP_HeFESTo_Input_Files".format(infilename)
    morb_folder = "/{}_MORB_HeFESTo_Input_Files".format(infilename)

    print("[~] Got HeFESTo BSP folder '{}'".format(bsp_folder))
    print("[~] Got HeFESTo Crust folder '{}'".format(morb_folder))

    if "{}_HeFESTo_Input_Files".format(infilename) in os.listdir(os.getcwd()):
        shutil.rmtree("{}_HeFESTo_Input_Files".format(infilename))
    else:
        pass


    consol_folder = (home_dir[0] + "/{}_HeFESTo_Input_Files".format(infilename))

    print("\n[~] Created consolidated HeFESTo input file folder: {}".format(consol_folder))

    fdir_bsp = (home_dir[0] + bsp_folder)
    fdir_morb = (home_dir[0] + morb_folder)
    tdir_bsp = consol_folder + bsp_folder
    tdir_morb = consol_folder + morb_folder

    shutil.move(fdir_bsp, tdir_bsp)
    shutil.move(fdir_morb, tdir_morb)

    print("\n[~] HeFESTo Input files are now available in {} for transfer to a HeFESTo VM".format(consol_folder))

    print("\n[~] Please move this script and folder '{}' to a working HeFESTo directory!".format(consol_folder))
    print("[~] Exiting the Exoplanet Pocketknife's active processes...")

    time.sleep(6)

    initialization()







def runhefesto(infiledir, actual_run, runname):

    os.chdir(home_dir[0])

    if actual_run is True:
    # try:
        if 'main' not in os.listdir(os.getcwd()):
            print("[X] ERROR!  HeFESTo's 'main' not detected in the working directory!\n")
            time.sleep(4)
            initialization()
        else:
            print("[~] HeFESTo detected in the working directory!\n")
            pass
        # os.chdir(home_dir[0])
        # print("\nPlease enter the name of your BSP HeFESTo input .csv sheet:")
        # hefesto_input_bsp = input(">>> ")
        # if hefesto_input_bsp in os.listdir(os.getcwd()):
        #     print("[~] {} has been found in the working directory!".format(hefesto_input_bsp))
        # else:
        #     print("[X] {} has NOT been found in the working directory!".format(hefesto_input_bsp))
        #     time.sleep(4)
        #     initialization()
        # print("\nPlease enter the name of your crust HeFESTo input .csv sheet:")
        # hefesto_input_morb = input(">>> ")
        # if hefesto_input_morb in os.listdir(os.getcwd()):
        #     print("[~] {} has been found in the working directory!".format(hefesto_input_morb))
        # else:
        #     print("[X] {} has NOT been found in the working directory!".format(hefesto_input_morb))
        #     time.sleep(4)
        #     initialization()
        #
        # if os.path.exists("HeFESTo_BSP_Input_Files"):
        #     shutil.rmtree("HeFESTo_BSP_Input_Files")
        # else:
        #     pass
        # if os.path.exists("HeFESTo_MORB_Input_Files"):
        #     shutil.rmtree("HeFESTo_MORB_Input_Files")
        # else:
        #     pass
        #
        # os.mkdir("HeFESTo_BSP_Input_Files")

        if os.path.exists(home_dir[0] + "/{}_HeFESTo_BSP_Output_Files".format(runname)):
            shutil.rmtree(home_dir[0] + "/{}_HeFESTo_BSP_Output_Files".format(runname))
        else:
            pass

        if os.path.exists(home_dir[0] + "/{}_HeFESTo_MORB_Output_Files".format(runname)):
            shutil.rmtree(home_dir[0] + "/{}_HeFESTo_MORB_Output_Files".format(runname))
        else:
            pass


        os.mkdir(home_dir[0] + "/{}_HeFESTo_BSP_Output_Files".format(runname))
        os.mkdir(home_dir[0] + "/{}_HeFESTo_BSP_Output_Files/fort.66".format(runname))
        os.mkdir(home_dir[0] + "/{}_HeFESTo_BSP_Output_Files/fort.58".format(runname))
        os.mkdir(home_dir[0] + "/{}_HeFESTo_BSP_Output_Files/fort.59".format(runname))
        os.mkdir(home_dir[0] + "/{}_HeFESTo_MORB_Output_Files".format(runname))
        os.mkdir(home_dir[0] + "/{}_HeFESTo_MORB_Output_Files/fort.66".format(runname))
        os.mkdir(home_dir[0] + "/{}_HeFESTo_MORB_Output_Files/fort.58".format(runname))
        os.mkdir(home_dir[0] + "/{}_HeFESTo_MORB_Output_Files/fort.59".format(runname))

        bsp_dir = []
        morb_dir = []
        os.chdir(infiledir)
        for i in os.listdir(os.getcwd()):
            if "BSP" in i or "bsp" in i:
                print("[~] Found BSP directory: {}".format(i))
                bsp_dir.append(i)
            elif "MORB" in i or "morb" in i:
                print("[~] Found MORB directory: {}".format(i))
                morb_dir.append(i)
            # else:
            #     print("\n[X] HeFESTo cumulative input directory not properly formatted!")
            #     initialization()

        if len(bsp_dir) > 1 or len(morb_dir) > 1:
            print("\n[X] HeFESTo cumulative input directory not properly formatted!")
            time.sleep(2)
            initialization()


        bsp_dir = home_dir[0] + "/{}/{}".format(infiledir, bsp_dir[0])
        morb_dir = home_dir[0] + "/{}/{}".format(infiledir, morb_dir[0])


        print("\b[~] Initiating HeFESTo BSP calculations...")


        for i in os.listdir(bsp_dir):

            star_name = i[:-23]

            os.chdir(home_dir[0])
            if "fort.66" in os.listdir(os.getcwd()):
                try:
                    os.remove("fort.66")
                except:
                    pass
                try:
                    shutil.rmtree("fort.66")
                except:
                    pass
            else:
                pass
            if "fort.58" in os.listdir(os.getcwd()):
                try:
                    os.remove("fort.58")
                except:
                    pass
                try:
                    shutil.rmtree("fort.58")
                except:
                    pass
            else:
                pass
            if "fort.59" in os.listdir(os.getcwd()):
                try:
                    os.remove("fort.59")
                except:
                    pass
                try:
                    shutil.rmtree("fort.59")
                except:
                    pass
            else:
                pass
            if "control" in os.listdir(os.getcwd()):
                try:
                    os.remove("control")
                except:
                    pass
                try:
                    shutil.rmtree("control")
                except:
                    pass
            else:
                pass
            os.chdir(bsp_dir)
            shutil.copy((bsp_dir + "/{}".format(i)), (home_dir[0] + "/{}".format("control")))
            print("\n[~] Performing HeFESTo BSP calculations on: {}".format(i))
            os.chdir(home_dir[0])
            argz = (home_dir[0] + "/main")
            p = subprocess.Popen(argz, stdin=None, stdout=None)
            t = Timer(800, p.kill)
            t.start()
            p.communicate()
            t.cancel()
            if "fort.66" in os.listdir(os.getcwd()):
                print("\n[~] 'fort.66' found!")
                shutil.move("fort.66", (home_dir[0] + "/{}_HeFESTo_BSP_Output_Files/fort.66/{}".format(runname, star_name + "_fort66")))
            if "fort.58" in os.listdir(os.getcwd()):
                print("\n[~] 'fort.58' found!")
                shutil.move("fort.58", (home_dir[0] + "/{}_HeFESTo_BSP_Output_Files/fort.58/{}".format(runname, star_name + "_fort58")))
            if "fort.59" in os.listdir(os.getcwd()):
                print("\n[~] 'fort.59' found!")
                shutil.move("fort.59", (home_dir[0] + "/{}_HeFESTo_BSP_Output_Files/fort.59/{}".format(runname, star_name + "_fort59")))
            if "control" in os.listdir(os.getcwd()):
                os.remove("control")

            time.sleep(2)

        print("\b[~] Initiating HeFESTo crust calculations...")


        for i in os.listdir(morb_dir):

            star_name = i[:-24]

            os.chdir(home_dir[0])
            if "fort.66" in os.listdir(home_dir[0]):
                os.remove(home_dir[0] + "/fort.66")
            if "fort.58" in os.listdir(home_dir[0]):
                os.remove(home_dir[0] + "/fort.58")
            if "fort.59" in os.listdir(home_dir[0]):
                os.remove(home_dir[0] + "/fort.59")
            if "control" in os.listdir(home_dir[0]):
                os.remove(home_dir[0] + "/control")
            os.chdir(morb_dir)
            shutil.copy((morb_dir + "/{}".format(i)), (home_dir[0] + "/{}".format("control")))
            print("\n[~] Performing HeFESTo crust calculations on: {}".format(i))
            os.chdir(home_dir[0])
            argz = (home_dir[0] + "/main")
            p = subprocess.Popen(argz, stdin=None, stdout=None)
            t = Timer(800, p.kill)
            t.start()
            p.communicate()
            t.cancel()
            try:
                if "fort.66" in os.listdir(home_dir[0]):
                    print("\n[~] 'fort.66; found!")
                    shutil.move(home_dir[0] + "/fort.66", (home_dir[0] + "/{}_HeFESTo_MORB_Output_Files/fort.66/{}".format(runname, star_name + "_fort66")))
                if "fort.58" in os.listdir(home_dir[0]):
                    print("\n[~] 'fort.58' found!")
                    shutil.move(home_dir[0] + "/fort.58", (home_dir[0] + "/{}_HeFESTo_MORB_Output_Files/fort.58/{}".format(runname, star_name + "_fort58")))
                if "fort.59" in os.listdir(home_dir[0]):
                    print("\n[~] 'fort.59 found!")
                    shutil.move(home_dir[0] + "/fort.59", (home_dir[0] + "/{}_HeFESTo_MORB_Output_Files/fort.59/{}".format(runname, star_name + "_fort59")))
                if "control" in os.listdir(home_dir[0]):
                    os.remove(home_dir[0] + "/control")
            except:
                pass
            os.chdir(home_dir[0])
            if "fort.66" in os.listdir(os.getcwd()):
                os.remove("fort.66")
            if "fort.58" in os.listdir(os.getcwd()):
                os.remove("fort.58")
            if "fort.66" in os.listdir(os.getcwd()):
                os.remove("fort.69")
            if "control" in os.listdir(os.getcwd()):
                os.remove("control")
        if os.path.exists("{}_HeFESTo_Output_Files".format(runname)):
            shutil.rmtree("{}_HeFESTo_Output_Files".format(runname))
        os.mkdir("{}_HeFESTo_Output_Files".format(runname))
        shutil.move(home_dir[0] + "/{}_HeFESTo_BSP_Output_Files".format(runname), home_dir[0] + "/{}_HeFESTo_Output_Files".format(runname))
        shutil.move(home_dir[0] + "/{}_HeFESTo_MORB_Output_Files".format(runname), home_dir[0] + "/{}_HeFESTo_Output_Files".format(runname))

        print("\n[~] HeFESTo Output Files available at '{}'".format(home_dir[0] + "/{}_HeFESTo_Output_Files".format(runname)))
        print("\n[~] Finished with HeFESTo calculations!")




            # bsp_infile_init = (home_dir[0] + "/{}".format(hefesto_input_bsp))
            # bsp_infile_to = (home_dir[0] + "/HeFESTo_BSP_Input_Files/{}".format(hefesto_input_bsp))
            # morb_infile_init = (home_dir[0] + "/{}".format(hefesto_input_morb))
            # morb_infile_to = (home_dir[0] + "/HeFESTo_MORB_Input_Files/{}".format(hefesto_input_morb))
            # shutil.copy(bsp_infile_init, bsp_infile_to)
            # shutil.copy(morb_infile_init, morb_infile_to)

            # os.chdir(bsp_dir)
            # with open(hefesto_input_bsp, 'r') as infile:
            #     reader = csv.reader(infile, delimiter=",")
            #     for row in reader:
            #         list_formatted = []
            #         for z in row:
            #             list_formatted.append(z)
            #         title = list_formatted[0].strip()
            #         output_file = open("{}_HeFESTo_BSP_nput.txt".format(title), 'a')
            #         for z in list_formatted[1:]:
            #             output_file.write("{}\n".format(z))
            #         output_file.close()
            #
            # os.chdir(home_dir[0] + "/HeFESTo_MORB_Input_Files")
            # with open(hefesto_input_morb, 'r') as infile:
            #     reader = csv.reader(infile, delimiter=",")
            #     for row in reader:
            #         list_formatted = []
            #         for z in row:
            #             list_formatted.append(z)
            #         title = list_formatted[0].strip()
            #         output_file = open("{}_HeFESTo_MORB_Input.txt".format(title), 'a')
            #         for z in list_formatted[1:]:
            #             output_file.write("{}\n".format(z))
            #         output_file.close()
            # print("[~] HeFESTo files written!\n"
            #       "Please see {} for your files!\n".format(os.getcwd()))
        # except:
        #     pass

    #     os.chdir(home_dir[0] + "/HeFESTo_BSP_Input_Files")
    #     print("[~] Launching HeFESTo simulations...")
    #     # curr_planet = ""
    #     # for i in os.listdir(os.getcwd()):
    #     # curr_planet.update(i)
    #     # print("[~] Currently simulating BSP for: {}".format(curr_planet.get()))
    #
    #
    #
    # else:
    #     try:
    #         if os.path.exists(home_dir[0] + "/HeFESTo_Inputs"):
    #             shutil.rmtree(home_dir[0] + "/HeFESTo_Inputs")
    #         else:
    #             pass
    #         os.mkdir(home_dir[0] + "/HeFESTo_Inputs")
    #         os.chdir(home_dir[0])
    #         print("\nPlease enter the name of your HeFESTo input .csv sheet:")
    #         hefesto_input = input(">>> ")
    #         if hefesto_input in os.listdir(os.getcwd()):
    #             print("[~] {} has been found in the working directory!".format(hefesto_input))
    #         else:
    #             print("[X] {} has NOT been found in the working directory!".format(hefesto_input))
    #             time.sleep(4)
    #             initialization()
    #
    #         infile_init = (home_dir[0] + "/{}".format(hefesto_input))
    #         infile_to = (home_dir[0] + "/HeFESTo_Inputs/{}".format(hefesto_input))
    #         shutil.copy(infile_init, infile_to)
    #
    #         os.chdir(home_dir[0] + "/HeFESTo_Inputs")
    #         with open(hefesto_input, 'r') as infile:
    #             reader = csv.reader(infile, delimiter=",")
    #             for row in reader:
    #                 list_formatted = []
    #                 for z in row:
    #                     list_formatted.append(z)
    #                 title = list_formatted[0].strip()
    #                 output_file = open("{}_HeFESTo_Input.txt".format(title), 'a')
    #                 for z in list_formatted[1:]:
    #                     output_file.write("{}\n".format(z))
    #                     # if z.isalpha() == True:
    #                     #     output_file.write("{}\n".format(z))
    #                     # else:
    #                     #     output_file.write("{}\n".format(z))
    #                 output_file.close()
    #         print("[~] HeFESTo files written!\n"
    #               "Please see {} for your files!\n".format(os.getcwd()))
    #     except:
    #         pass




def scrapemorb(infiledirectory, infilename):

    if "{}_MORB_Consolidated_Chem_File".format(infilename) in os.listdir(home_dir[0]):
        os.remove(home_dir[0] + "/{}_MORB_Consolidated_Chem_File".format(infilename))
    else:
        pass

    morb_outfile = open((home_dir[0] + "/{}_MORB_Consolidated_Chem_File".format(infilename)), 'a') # need a header
    morb_outfile_header = "Star Name,Pressure,Temperature,mass,SiO2,TiO2,Al2O3,Fe2O3,Cr2O3,FeO,MgO,CaO,Na2O\n"
    morb_outfile.write(morb_outfile_header)


    for i in os.listdir(infiledirectory):
        try:
            print("\n[~] Scraping MORB output file: {}".format(i))
            os.chdir(infiledirectory)
            with open(i, 'r') as infile:
                star_name = []
                data = []
                reader = csv.reader(infile, delimiter=',')
                reader2 = list(reader)
                star_name.append(reader2[0][1])
                if enumerate(i, 1) >= 100:
                    for num, line in enumerate(reader2, 1):
                        if "Liquid" in line:
                            skip_row2 = num + 1
                            liquid_comp = reader2[skip_row2]
                            for item in liquid_comp:
                                data.append(item)
                        else:
                            pass
                    data_formatted = ",".join(str(z) for z in data)
                    os.chdir(home_dir[0])
                    morb_outfile.write("{},{}\n".format(star_name[0], data_formatted))
                else:
                    os.chdir(home_dir[0])
                    morb_outfile.write("{},ERROR!\n".format(star_name[0]))
        except:
            pass

    morb_outfile.close()

    os.chdir(home_dir[0])

    consol_file = (home_dir[0] + "/{}_MORB_Consolidated_Chem_File".format(infilename))
    morbrecalc(infiledirectory=infiledirectory, infilename=infilename, bulkfilename=consol_file)





def morbrecalc(infiledirectory, infilename, bulkfilename):

    os.chdir(home_dir[0])

    if "{}_MORB_Recalc_Bulkfile.csv".format(infilename) in os.listdir(os.getcwd()):
        os.remove("{}_MORB_Recalc_Bulkfile.csv".format(infilename))
    else:
        pass

    if "morb_debug.csv" in os.listdir(os.getcwd()):
        os.remove("morb_debug.csv")

    morb_debug = open("morb_debug.csv", 'a')

    morb_recalc_outfile = open("{}_MORB_Recalc_Bulkfile.csv".format(infilename), 'a')
    morb_recalc_outfile_header = "Star,Pressure,Temperature,Mass,SiO2,TiO2,Al2O3,Cr2O3,FeO,MgO,CaO,Na2O,SUM\n"
    morb_recalc_outfile.write(morb_recalc_outfile_header)

    df_morb_chem = pd.read_csv(bulkfilename)
    for row in df_morb_chem.index:
        try:
            star_name = df_morb_chem["Star Name"][row]
            pressure = float(df_morb_chem["Pressure"][row])
            temperature = float(df_morb_chem["Temperature"][row])
            mass = float(df_morb_chem["mass"][row])
            sio2_in = float(df_morb_chem["SiO2"][row])
            tio2_in = float(df_morb_chem["TiO2"][row])
            al2o3_in = float(df_morb_chem["Al2O3"][row])
            fe2o3_in = float(df_morb_chem["Fe2O3"][row])
            cr2o3_in = float(df_morb_chem["Cr2O3"][row])
            feo_in = float(df_morb_chem["FeO"][row])
            mgo_in = float(df_morb_chem["MgO"][row])
            cao_in = float(df_morb_chem["CaO"][row])
            na2o_in = float(df_morb_chem["Na2O"][row])
            chem_in_sum = (sio2_in + tio2_in + al2o3_in + fe2o3_in + cr2o3_in + feo_in + mgo_in + cao_in + na2o_in)

            md1_header = "1,sio2,tio2,al2o3,fe2o3,cr2o3,cr2o3,feo,mgo,cao,na2o"
            md1 = ",{},{},{},{},{},{},{},{},{}".format(sio2_in, tio2_in, al2o3_in, fe2o3_in,
                                cr2o3_in, feo_in, mgo_in, cao_in, na2o_in)
            morb_debug.write("{}\n{}\n".format(md1_header, md1))


            wt_sio2_in = (sio2_in/100.0) * mass
            wt_tio2_in = (tio2_in / 100.0) * mass
            wt_al2o3_in = (al2o3_in / 100.0) * mass
            wt_fe2o3_in = (fe2o3_in / 100.0) * mass
            wt_cr2o3_in = (cr2o3_in / 100.0) * mass
            wt_feo_in = (feo_in / 100.0) * mass
            wt_mgo_in = (mgo_in / 100.0) * mass
            wt_cao_in = (cao_in / 100.0) * mass
            wt_na2o_in = (na2o_in / 100.0) * mass
            sum_wt_in = (wt_sio2_in + wt_tio2_in + wt_al2o3_in + wt_fe2o3_in + wt_cr2o3_in + wt_feo_in +
                         wt_mgo_in + wt_cao_in + wt_na2o_in)

            md2_header = "2,sio2,tio2,al2o3,fe2o3,cr2o3,feo,mgo,cao,na2o"
            md2 = ",{},{},{},{},{},{},{},{},{}".format(wt_sio2_in, wt_tio2_in, wt_al2o3_in, wt_fe2o3_in,
                        wt_cr2o3_in, wt_feo_in, wt_mgo_in, wt_cao_in, wt_na2o_in)
            morb_debug.write("{}\n{}\n".format(md2_header, md2))

            sio2_moles = wt_sio2_in / sio2_molwt
            tio2_moles = wt_tio2_in / tio2_molwt
            al2o3_moles = wt_al2o3_in / al2o3_molwt
            fe2o3_moles = wt_fe2o3_in / fe2o3_molwt
            cr2o3_moles = wt_cr2o3_in / cr2o3_molwt
            feo_moles = wt_feo_in / feo_molwt
            mgo_moles = wt_mgo_in / mgo_molwt
            cao_moles = wt_cao_in / cao_molwt
            na2o_moles = wt_na2o_in / na2o_molwt
            sum_oxide_moles = (sio2_moles + tio2_moles + al2o3_moles + fe2o3_moles + cr2o3_moles + feo_moles +
                               mgo_moles + cao_moles + na2o_moles)

            md3_header = "3,sio2,tio2,al2o3,fe2o3,feo,mgo,cao,na2o"
            md3 = ",{},{},{},{},{},{},{},{},{}".format(sio2_moles, tio2_moles, al2o3_moles, fe2o3_moles,
                    cr2o3_moles, feo_moles, mgo_moles, cao_moles, na2o_moles)
            morb_debug.write("{}\n{}\n".format(md3_header, md3))

            si_cations = sio2_moles * num_sio2_cations
            ti_cations = tio2_moles * num_tio2_cations
            al_cations = al2o3_moles * num_al2o3_cations
            fe_fe2o3_cations = fe2o3_moles * num_fe2o3_cations
            cr_cations = cr2o3_moles * num_cr2o3_cations
            fe_feo_cations = feo_moles * num_feo_cations
            mg_cations = mgo_moles * num_mgo_cations
            ca_cations = cao_moles * num_cao_cations
            na_cations = na2o_moles * num_na2o_cations
            sum_cations = (si_cations + ti_cations + al_cations + fe_fe2o3_cations + cr_cations + fe_feo_cations + mg_cations +
                              ca_cations + na_cations)

            md4_header = "4,si,ti,al,fe,cr,fe,mg,ca,na,sum"
            md4 = ",{},{},{},{},{},{},{},{},{},{}".format(si_cations, ti_cations, al_cations, fe_fe2o3_cations, cr_cations,
                    fe_feo_cations, mg_cations, na_cations, na_cations, sum_cations)
            morb_debug.write("{}\n{}\n".format(md4_header, md4))

            # fe2o3 --> feo recalc
            total_mol_fe = (fe_feo_cations + fe_fe2o3_cations)
            total_wt_fe = total_mol_fe * fe_atwt
            total_wt_feo = total_mol_fe * feo_molwt

            md5_header = "5,total_mol_fe,total_wt_fe,total_wt_feo"
            md5 = ",{},{},{}".format(total_mol_fe, total_wt_fe, total_wt_feo)
            morb_debug.write("{}\n{}\n".format(md5_header, md5))



            # unnormalized wt%
            unnorm_sum = (wt_sio2_in + wt_tio2_in + wt_al2o3_in + total_wt_feo +
                          wt_cr2o3_in + wt_mgo_in + wt_cao_in + wt_na2o_in)

            # normalized oxide wt% w/o mgo fix
            norm_wt_sio2 = wt_sio2_in / unnorm_sum
            norm_wt_tio2 = wt_tio2_in / unnorm_sum
            norm_wt_al2o3 = wt_al2o3_in / unnorm_sum
            norm_wt_feo = total_wt_feo / unnorm_sum
            norm_wt_cr2o3 = wt_cr2o3_in / unnorm_sum
            norm_wt_mgo = wt_mgo_in / unnorm_sum
            norm_wt_cao = wt_cao_in / unnorm_sum
            norm_wt_na2o = wt_na2o_in / unnorm_sum
            norm_sum_nomgofix = (norm_wt_sio2 + norm_wt_tio2 + norm_wt_al2o3 + norm_wt_feo + norm_wt_cr2o3 + norm_wt_mgo +
                                    norm_wt_cao + norm_wt_na2o)

            md6_header = "6,sio2,tio2,al2o3,feo,cr2o3,mgo,cao,na2o,sum"
            md6 = ",{},{},{},{},{},{},{},{},{}".format(norm_wt_sio2, norm_wt_tio2, norm_wt_al2o3,
                    norm_wt_feo, norm_wt_cr2o3, norm_wt_mgo, norm_wt_cao, norm_wt_na2o, norm_sum_nomgofix)
            morb_debug.write("{}\n{}\n".format(md6_header, md6))

            # mgo fix
            norm_wt_mgo_fix = norm_wt_mgo * mgo_fix
            norm_sum_mgofix = (norm_wt_sio2 + norm_wt_tio2 + norm_wt_al2o3 + norm_wt_feo + norm_wt_cr2o3 + norm_wt_mgo_fix +
                                    norm_wt_cao + norm_wt_na2o)

            md7_header = "7,mgo_fix,norm_wt_mgo_fx,norm_sum_mgofix"
            md7 = ",{},{},{}".format(mgo_fix, norm_wt_mgo_fix, norm_sum_mgofix)
            morb_debug.write("{}\n{}\n".format(md7_header, md7))

            # normaized oxide wt% abundances --- what we want!

            sio2_wtpct = (norm_wt_sio2 / norm_sum_mgofix) * 100
            tio2_wtpct = (norm_wt_tio2 / norm_sum_mgofix) * 100
            al2o3_wtpct = (norm_wt_al2o3 / norm_sum_mgofix) * 100
            feo_wtpct = (norm_wt_feo / norm_sum_mgofix) * 100
            cr2o3_wtpct = (norm_wt_cr2o3 / norm_sum_mgofix) * 100
            mgo_wtpct = (norm_wt_mgo_fix / norm_sum_mgofix) * 100
            cao_wtpct = (norm_wt_cao / norm_sum_mgofix) * 100
            na2o_wtpct = (norm_wt_na2o / norm_sum_mgofix) * 100
            sum_wtpct = (sio2_wtpct + tio2_wtpct + al2o3_wtpct + feo_wtpct + cr2o3_wtpct + mgo_wtpct + cao_wtpct + na2o_wtpct)

            md8_header = "8,sio2,tio2,al2o3,feo,cr2o3,mgo,cao,na2o,sum"
            md8 = ",{},{},{},{},{},{},{},{},{}".format(sio2_wtpct, tio2_wtpct, al2o3_wtpct, feo_wtpct,
                            cr2o3_wtpct, mgo_wtpct, cao_wtpct, na2o_wtpct, sum_wtpct)
            morb_debug.write("{}\n{}\n".format(md8_header, md8))

            chem_to_outfile = "{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(star_name, pressure, temperature, mass, sio2_wtpct,
                                    tio2_wtpct, al2o3_wtpct, cr2o3_wtpct, feo_wtpct, mgo_wtpct, cao_wtpct, na2o_wtpct, sum_wtpct)

            morb_recalc_outfile.write(chem_to_outfile)

        except:
            pass


    morb_debug.close()
    morb_recalc_outfile.close()

    hefestofilewriter_morb(bulkfile="{}_MORB_Recalc_Bulkfile.csv".format(infilename), infilename=infilename)







def integrationloop2(hefestodir, runname):

    # standard_depths = []
    #
    # model_sun_bsp_rho = [3.1399, 3.16644, 3.21129, 3.21993, 3.22843, 3.23679, 3.24503, 3.25316, 3.26117, 3.26909, 3.28169, 3.29415,
    #      3.30499, 3.31476, 3.3238, 3.33232, 3.34046, 3.34832, 3.35595, 3.3634, 3.3707, 3.37788, 3.38495, 3.39193,
    #      3.39884, 3.40567, 3.41244, 3.41916, 3.42582, 3.43244, 3.43902, 3.44557, 3.45208, 3.45857, 3.46504, 3.47149,
    #      3.47794, 3.48438, 3.49083, 3.4973, 3.50379, 3.51032, 3.51783, 3.52856, 3.5352, 3.54193, 3.54876, 3.55574,
    #      3.56291, 3.57035, 3.57813, 3.58638, 3.59525, 3.60495, 3.61577, 3.69282, 3.7338, 3.74885, 3.75742, 3.76575,
    #      3.77393, 3.78203, 3.79015, 3.79837, 3.80676, 3.81424, 3.81873, 3.82321, 3.82768, 3.83213, 3.83656, 3.84098,
    #      3.84538, 3.84977, 3.85831, 3.87594, 3.89625, 3.90832, 3.91254, 3.91675, 3.92094]
    #
    # model_sun_crust_rho = [2.89708, 2.92792, 2.94455, 3.04297, 3.17487, 3.19574, 3.25329, 3.36196, 3.37489,
    #                        3.38665, 3.39781, 3.40855, 3.43322, 3.4435, 3.45364, 3.46287, 3.47109, 3.47896, 3.4865,
    #                        3.49376, 3.50079, 3.50761, 3.51426, 3.52077, 3.52715, 3.53344, 3.53963, 3.54574,	3.55179,
    #                        3.55777,	3.56371, 3.5696, 3.57545, 3.58126, 3.58704,	3.59279, 3.66547, 3.67112, 3.67676,
    #                        3.68238, 3.68799, 3.69359, 3.69919, 3.70479,	3.71039, 3.71601, 3.72163, 3.72728,	3.73294,
    #                        3.73864,	3.74438, 3.75015, 3.75598, 3.76188,	3.76784, 3.77389, 3.78003, 3.78629,	3.79267,
    #                        3.79921,	3.80591, 3.8128, 3.81991, 3.82728, 3.83492,	3.84288, 3.85119, 3.85991, 3.86906,
    #                        3.8787, 3.88887,	3.89961, 3.91094, 3.9229, 3.9355, 3.94971, 3.97115,	3.99127, 4.01053,
    #                        4.02931,	4.04793]
    #
    # model_sun_delta_rho = [a - b for a, b in zip(model_sun_crust_rho, model_sun_bsp_rho)]
    #
    # lit_sun_bsp_rho = []
    #
    # lit_sun_crust_rho = [2.96748, 2.98934, 3.02871, 3.12504, 3.2649, 3.32414, 3.40401, 3.41811, 3.43281, 3.44608,
    #                      3.45855, 3.47031, 3.5037, 3.51281,	3.52141, 3.52955, 3.5373, 3.54472, 3.55187, 3.55881, 3.56557,
    #                      3.57218, 3.57866, 3.58505,	3.59134, 3.59757, 3.60373, 3.60984,	3.6159, 3.62192, 3.62791,
    #                      3.63387, 3.6398, 3.64571, 3.6516, 3.65749, 3.75811, 3.7639, 3.7697, 3.77549, 3.7813, 3.78712,
    #                      3.79296, 3.79882, 3.80472, 3.81065, 3.81662, 3.82265, 3.82874, 3.8349, 3.84114, 3.84747, 3.85391,
    #                      3.86047, 3.86718, 3.87404, 3.88108, 3.88832, 3.89579, 3.90353, 3.91157, 3.91994, 3.92868, 3.93784,
    #                      3.94746, 3.95758, 3.96823,	3.97945, 3.99123, 4.00355, 4.01639,	4.02969, 4.04339, 4.05801,
    #                      4.07212, 4.08535, 4.09777, 4.10947, 4.1205, 4.13093, 4.14081]



    print("\n")

    hefesto_dir = home_dir[0] + "/" + hefestodir

    output_folder = home_dir[0] + "/{}_Buoyancy_Outputs".format(runname)

    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    else:
        pass

    os.mkdir(output_folder)

    bsp_and_morb_dir = [] # BSP dir at index 0, MORB dir at index 1

    for i in os.listdir(hefesto_dir):
        if "BSP" in str(i):
            bsp_and_morb_dir.append(str(hefesto_dir + "/" + i + "/fort.58"))
        elif "MORB" in str(i):
            bsp_and_morb_dir.append(str(hefesto_dir + "/" + i + "/fort.58"))

    if len(bsp_and_morb_dir) != 2:
        print("\n[X] The directory '{}' is not formatted properly!".format(hefesto_dir))
        time.sleep(2)
        initialization()
    else:
        print("\n[~] Found BSP HeFESTo File directory: '{}'!".format(bsp_and_morb_dir[0]))
        print("[~] Found MORB HeFESTo File directory: '{}'!".format(bsp_and_morb_dir[1]))

    if "{}_Integrated_Values.csv".format(runname) in os.listdir(home_dir[0]):
        os.remove("{}_Integrated_Values.csv".format(runname))

    integrated_output_file = open("{}_Integrated_Values.csv".format(runname), 'a')
    integrated_output_file.write("Star,Net Buoyant Force,{}".format(",".join(str(i) for i in depth_trans_zone)))


    print("\n[~] Initiating HeFESTo output file parsing...")


    # planet_grav = (6.674*10**-11) * (planet_mass / planet_radius**2)

    for i in os.listdir(bsp_and_morb_dir[0]):
        star_name = i.replace("fort.58.control.", "").replace("_fort.58", "").replace("_bsp.txt_bsp", "").replace("fort.58_", "").replace("_fort58", "")
        try:
            for z in os.listdir(bsp_and_morb_dir[1]):
                starname_morb = z.replace("fort.58.control.", "").replace("fort.58_", "").replace("_morb.txt_morb", "").replace("_fort.58", "").replace("_fort58", "")
                if star_name ==starname_morb:
                    print("\n\n[~] Matched BSP and MORB files for star: {}".format(star_name))
                    os.chdir(bsp_and_morb_dir[0])
                    with open(i, 'r') as bsp_infile:
                        os.chdir(bsp_and_morb_dir[1])
                        with open(z, 'r') as morb_infile:
                            bsp_readfile = pd.read_fwf(bsp_infile, colspecs='infer')
                            morb_readfile = pd.read_fwf(morb_infile, colspecs='infer')
                            bsp_df = bsp_readfile.iloc[:, [1, 3]]
                            morb_df = morb_readfile.iloc[:, [1, 3]]
                            depths = []
                            bsp_rho = []
                            morb_rho = []
                            morb_minus_bsp_rho = []
                            integrated_values = []
                            for y in bsp_df['depth']:
                                depths.append(float(y))
                            for y in bsp_df['rho']:
                                bsp_rho.append(float(y))
                            for y in morb_df['rho']:
                                morb_rho.append(float(y))
                            bsp_infile.close()
                            morb_infile.close()
                            cur_index = 0
                            for q in morb_rho:
                                corresponding_bsp = bsp_rho[cur_index]
                                morb_minus_bsp_rho.append(corresponding_bsp - q)
                                # morb_minus_bsp_rho.append(q - corresponding_bsp)
                                cur_index += 1
                            # print("\nDEPTHS")
                            # print(depths)
                            # print("\nBSPRHO")
                            # print(bsp_rho)
                            # print("\nMORBRHO")
                            # print(morb_rho)
                            # print("\nDELTARHO")
                            # print(morb_minus_bsp_rho)
                            for t in range(len(morb_minus_bsp_rho) - 1):
                                x = depths[:(t + 2)]
                                y = morb_minus_bsp_rho[:(t + 2)]
                                # integrated_values.append(inte.simps(y, x))
                                integrated_values.append((inte.simps(y, x) * 1000 * 1000 * plate_thickness * gravity)) # Multiply by 1000 to account for g/cm^3 -> kg/m^3, and by 1000 again for depth km -> m.
                            # print("\nINTEVALS")
                            # print(integrated_values)
                            print("[~] Calculated a net buoyancy force of {} for star {}!".format(integrated_values[-1], star_name))
                            os.chdir(home_dir[0])
                            integrated_vals_formatted = ",".join(str(i) for i in integrated_values)
                            integrated_output_file.write("\n{},{},{}".format(star_name, str(integrated_values[-1]), integrated_vals_formatted))
        except:
            integrated_output_file.write("\n{},{}".format(star_name, "FAILURE"))
            print("[X] Failed to calculate a net buoyancy force for star {}!".format(star_name))

    integrated_output_file.close()
    print("\n[~] Net buoyant force output file '{}' available in '{}'!".format("{}_Integrated_Values.csv".format(runname), home_dir[0]))


    def visualize_outputs(integrated_output_file, runname):


        os.chdir(home_dir[0])

        print("\n[~] Preparing to plot integrated buoyancy force results...")

        if os.path.exists("{}_Buoyancy_Force_Graphs".format(runname)):
            shutil.rmtree("{}_Buoyancy_Force_Graphs".format(runname))

        os.mkdir("{}_Buoyancy_Force_Graphs".format(runname))

        loop_num = 1

        integrated_output_file_df = pd.read_csv(integrated_output_file)
        for row in integrated_output_file_df.index:
            try:
                integrated_buoyant_vals = []
                star_name = integrated_output_file_df['Star'][row]
                print("\n[~] Plotting integrated buoyancy force results for star: {}".format(star_name))
                if "{}.png".format(star_name) in os.listdir(home_dir[0]):
                    os.remove(home_dir[0] + "/{}_Buoyancy_Force_Graphs/{}.png".format(runname, star_name))
                buoyant_force = integrated_output_file_df['Net Buoyant Force'][row]
                with open(integrated_output_file, 'r') as inte_output:
                    reader = csv.reader(inte_output)
                    for i, row in enumerate(reader):
                        if i == loop_num:
                            for z in row[2:]:
                                integrated_buoyant_vals.append(float(z))
                loop_num += 1
                inte_output.close()
                plt.plot(depth_trans_zone[1:], integrated_buoyant_vals)
                plt.title("{} Net Buoyant Forces".format(star_name))
                plt.xlabel("Depth (km)")
                plt.ylabel("Buoyant Force (N/m)")
                plt.xlim(0, 574)
                plt.grid()
                plt.savefig("{}.png".format(star_name), format='png')
                plt.close()
                fdir = home_dir[0] + "/{}.png".format(star_name)
                tdir = home_dir[0] + "/{}_Buoyancy_Force_Graphs/{}.png".format(runname, star_name)
                shutil.move(fdir, tdir)
                print("[~] Buoyant force plot for star {} available in directory '{}'!".format(star_name, tdir))
            except:
                print("[X] Failed to build a plot for star {}!".format(star_name))

        print("\n[~] Thank you for using the Exoplanet Pocketknife!\n[~] Returning to main menu...")
        time.sleep(2)
        initialization()


    def decideplot():
        print("\n[~] Would you like to graph the integrated buoyancy force results?\nPlease enter 'y' or 'n' for 'yes' or 'no', respectively")
        plot_input = raw_input(">>> ")
        if plot_input == 'y':
            visualize_outputs(integrated_output_file="{}_Integrated_Values.csv".format(runname), runname=runname)
        elif plot_input == 'n':
            print("\n[~] Thank you for using the Exoplanet Pocketknife!\nReturning to the main menu...")
            time.sleep(2)
            initialization()
        else:
            print("\n[X] Oops!  That's not a valid command!")
            time.sleep(2)
            decideplot()

    decideplot()








def initialization():
    home_dir.append(os.getcwd())
    # integrationloop2()


    createbspenvfile()
    createmorbenvfile()
    print("\n_______________________________________________\n\n\n\n\n\n\n\n\n\n")
    print("\n\n\nThe Exoplanet Pocketknife\nScott D. Hull, The Ohio State University 2015-2017\n")
    print("This software is meant to work in conjunction with the methods described in 'The Prevalence of"
          " Exoplanetary Plate Tectonics' (Unterborn et. al 2017).\nPlease refer to the article and "
          "the documentation for more information.\n"
          "\n*Any use of this software or the methods described in Unterborn et al. 2017 requires proper"
          " citation.*\n\n")
    # if "Star2Oxide_Output.csv" in os.listdir(os.getcwd()):
    #     os.remove("Star2Oxide_Output.csv")
    # else:
    #     pass
    # outputfile = open("Star2Oxide_Output.csv", 'a')
    # time.sleep(1)
    print("Enter:\n"
          "'1' to raw_input [X/H] stellar abundances\n"
          "'2' to raw_input stellar mole abundances\n"
          "'3' to launch HeFESTo calculations\n"
          "'4' to perform buoyancy force calculations & visualize\n"
          "'o' for more options\n"
          "'e' to exit the Exoplanet Pocketknife\n")
    option1 = str(raw_input(">>> "))
    if option1 == '1':
        if "run_alphamelts.command" in os.listdir(os.getcwd()):
            print("\nPlease enter your .csv formatted raw_input file with [X/H] stellar abundances:")
            infile = str(raw_input(">>> "))
            if infile in os.listdir(os.getcwd()):
                print("\n[~] {} has been found in the working directory!".format(infile))
                inputfile_list.append(infile)
                # time.sleep(1)
                logep(infile, infile_type='BSP', consol_file=False, init_path=(os.getcwd()), library=True)
            else:
                print("\n{} has NOT been found in the working directory!".format(infile))
                initialization()
        else:
            print("\n[X] 'run_alphamelts.command' is not in the working directory!")
            time.sleep(2)
            initialization()
    elif option1 == '2':
        print("\nPlease enter your .csv formatted raw_input file with stellar mole abundances:")
        infile = str(raw_input(">>> "))
        if "run_alphamelts.command" in os.listdir(os.getcwd()):
            if infile in os.listdir(os.getcwd()):
                print("\n[~] {} has been found in the working directory!".format(infile))
                inputfile_list.append(infile)
                # time.sleep(1)
                molepct(infile, infile_type='BSP', consol_file=False, init_path=(os.getcwd()) ,library=True)
            else:
                print("\n{} has NOT been found in the working directory!".format(infile))
                initialization()
        else:
            print("\n[X] 'run_alphamelts.command' is not in the working directory!")
            time.sleep(2)
            initialization()
    elif option1 == "3":
        print("Please enter the name of the HeFESTo cumulative input file directory")
        option3 = str(raw_input(">>> "))
        print("What would you like to name this run?")
        option4 = str(raw_input(">>> "))
        if os.path.exists(home_dir[0] + "/{}".format(option3)):
            runhefesto(infiledir=option3, actual_run=True, runname=option4)
        else:
            print("\n[X] '{}' does not exist in working directory: "
                  "'{}'!".format((home_dir[0] + "/{}".format(option3)), home_dir[0]))
            time.sleep(2)
            pass
    elif option1 == "4":
        print("\nPlease enter the name of your HeFESTo Output File directory...")
        option5 = raw_input(">>> ")
        if not os.path.exists(option5):
            print("That directory does not exist in the working directory!")
            time.sleep(2)
            initialization()
        realform_dir = home_dir[0] + "/" + option5
        # if len(os.listdir(realform_dir)) != 2:
            # print("\n[X] Warning!  The HeFESTo directory '{}' is not properly formatted! (Length != 2, but is length {})".format(realform_dir, len(os.listdir(realform_dir))))
            # for i in os.listdir(realform_dir):
            #     print(i)
            # time.sleep(2)
            # initialization()
        print("What would you like to name this run?")
        option6 = raw_input(">>> ")
        integrationloop2(hefestodir=option5, runname=option6)
    elif option1 == 'o':
        print("\nPlease enter the letter of your choice.  Would you like to: \na. Write a single file with MELTS raw_inputs\n"
              "b. Write a library of MELTS raw_input files\nc. Write a library of HeFESTo raw input files\n"
              "d. Go back\n")
        raw_input_help = raw_input(">>> ")
        if raw_input_help == 'a':
            print("\nEnter '1' to raw_input [X/H] stellar abundances or '2' to raw_input stellar mole abundances.")
            raw_input_help2 = str(raw_input(">>> "))
            if raw_input_help2 == "1":
                print("\nPlease enter your .csv formatted raw_input file with [X/H] stellar abundances:")
                infile = str(raw_input(">>> "))
                if infile in os.listdir(os.getcwd()):
                    print("\n[~] {} has been found in the working directory!".format(infile))
                    inputfile_list.append(infile)
                    # time.sleep(1)
                    logep(infile, infile_type='file', consol_file=True, init_path=(os.getcwd()), library=False)
                else:
                    print("{} has NOT been found in the working directory!\n".format(infile))
                    time.sleep(1)
                    initialization()
            elif raw_input_help2 == "2":
                print("\nPlease enter your .csv formatted raw_input file with stellar mole abundances:")
                infile = str(raw_input(">>> "))
                if infile in os.listdir(os.getcwd()):
                    print("\n[~] {} has been found in the working directory!".format(infile))
                    inputfile_list.append(infile)
                    # time.sleep(1)
                    molepct(infile, infile_type='file', consol_file=True, init_path=(os.getcwd()), library=False)
                else:
                    print("\n{} has NOT been found in the working directory!".format(infile))
                    initialization()
            else:
                print("\n[X] Oops!  That's not a valid command!\n")
                time.sleep(1)
                initialization()
        elif raw_input_help == 'b':
            print("\nEnter '1' to raw_input [X/H] stellar abundances or '2' to raw_input stellar mole abundances.")
            raw_input_help2 = str(raw_input(">>> "))
            if raw_input_help2 == "1":
                print("\nPlease enter your .csv formatted raw_input file with [X/H] stellar abundances:")
                infile = raw_input(">>> ")
                if infile in os.listdir(os.getcwd()):
                    print("\n[~] {} has been found in the working directory!".format(infile))
                    inputfile_list.append(infile)
                    # time.sleep(1)
                    logep(infile, infile_type='file', consol_file=False, init_path=(os.getcwd()), library=True)
                else:
                    print("{} has NOT been found in the working directory!\n".format(infile))
                    time.sleep(1)
                    initialization()
            elif raw_input_help2 == "2":
                print("\nPlease enter your .csv formatted raw_input file with stellar mole abundances:")
                infile = str(raw_input(">>> "))
                if infile in os.listdir(os.getcwd()):
                    print("\n[~] {} has been found in the working directory!".format(infile))
                    inputfile_list.append(infile)
                    # time.sleep(1)
                    molepct(infile, infile_type='file', consol_file=False, init_path=(os.getcwd()), library=True)
                else:
                    print("\n{} has NOT been found in the working directory!".format(infile))
                    initialization()
            else:
                print("\n[X] Oops!  That's not a valid command!\n")
                time.sleep(1)
                initialization()
        elif raw_input_help == 'c':
            runhefesto(actual_run=False)
        elif raw_input_help == 'd':
            initialization()
        else:
            print("\n[X] Oops!  That's not a valid command!\n")
            time.sleep(1)
            initialization()
    elif option1 == 'e':
        print("\nThank you for using the Exoplanet Pocketknife!\n")
        print("\n___________________________________________\n")
        sys.exit()
    else:
        print("\n[X] Oops!  {} is not a valid command!\n".format(option1))
        time.sleep(1)
        initialization()


initialization()
