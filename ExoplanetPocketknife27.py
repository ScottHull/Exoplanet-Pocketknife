# python /usr/bin/env/python

# /// The Exoplanet Pocketknife
# /// Scott D. Hull, The Ohio State University 2017
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
plate_thickness = 10.0

na_atwt = 22.9898
mg_atwt = 24.3050
al_atwt = 26.9815
si_atwt = 28.0855
ca_atwt = 40.0780
ti_atwt = 47.8670
cr_atwt = 51.9961
fe_atwt = 55.8450
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


        if consol_file is True:
            file_consolidate(path=infiledir, init_path=init_path)
        else:
            pass

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

def bsprecalc(bspmeltsfilesdir, infilename, alloy_mass_infile, bsp_chem_infile, bulkfile):

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

                fe_moles = feo_moles / num_feo_cations
                na_moles = na2o_moles / num_na2o_cations
                mg_moles = mgo_moles / num_mgo_cations
                al_moles = al2o3_moles / num_al2o3_cations
                si_moles = sio2_moles / num_sio2_cations
                ca_moles = cao_moles / num_cao_cations
                ni_moles = nio_moles / num_nio_cations
                ti_moles = tio2_moles / num_tio2_cations
                cr_moles = cr2o3_moles / num_cr2o3_cations

                fe_mass = fe_moles * fe_atwt
                na_mass = na_moles * na_atwt
                mg_mass = mg_moles * mg_atwt
                al_mass = al_moles * al_atwt
                si_mass = si_moles * si_atwt
                ca_mass = ca_moles * ca_atwt
                ni_mass = ni_moles * ni_atwt
                ti_mass = ti_moles * ti_atwt
                cr_mass = cr_moles * cr_atwt

                alloy_subt_ni_mass = alloy_mass - ni_mass
                if alloy_subt_ni_mass < 0:
                    print("NI MASS ERROR!")
                    sys.exit()
                else:
                    pass

                new_mass_fe = fe_mass - alloy_subt_ni_mass

                if new_mass_fe < 0:
                    print("FE MASS ERROR!")
                    sys.exit()

                remaining_moles_fe = new_mass_fe / fe_atwt
                remaining_moles_feo = remaining_moles_fe * num_feo_cations
                remaining_mass_feo = remaining_moles_feo * feo_molwt

                unnormalized_sum = (remaining_mass_feo + na_mass + mg_mass + al_mass + si_mass + ca_mass +
                                    ti_mass + cr_mass)

                norm_feo = remaining_mass_feo / unnormalized_sum * 100.0
                norm_na2o = na2o_in / unnormalized_sum * 100.0
                norm_mgo = mgo_in / unnormalized_sum * 100.0
                norm_al2o3 = al2o3_in / unnormalized_sum * 100.0
                norm_sio2 = sio2_in / unnormalized_sum * 100.0
                norm_cao = cao_in / unnormalized_sum * 100.0
                norm_tio2 = tio2_in / unnormalized_sum * 100.0
                norm_cr2o3 = cr2o3_in / unnormalized_sum * 100.0
                norm_sum = norm_feo + norm_na2o + norm_mgo + norm_al2o3 + norm_sio2 + norm_cao + norm_tio2 + norm_cr2o3


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

    hefestofilewriter_bsp(bulkfile=bsp_chem_infile)
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

    if "alloy_mass.csv" in os.listdir(os.getcwd()):
        os.remove("alloy_mass.csv")
    else:
        pass

    alloy_mass_outfile = open("alloy_mass.csv", 'a')

    alloy_mass_outfile.write("{},{}\n".format("star", "alloy mass"))

    os.chdir(infiledirectory)

    for i in os.listdir(os.getcwd()):
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
        else:
            pass




def hefestofilewriter_bsp(bulkfile):

    os.chdir(home_dir[0])

    if os.path.exists("BSP_HeFESTo_Input_Files"):
        os.remove("BSP_HeFESTo_Input_Files")
    else:
        pass

    os.mkdir("BSP_HeFESTo_Input_Files")

    bulkfile_df = pd.read_csv(bulkfile)

    for row in bulkfile_df.index:
        star = bulkfile_df["Star"][row]
        si = bulkfile_df["SiO2"][row]
        mg = bulkfile_df["MgO"][row]
        fe = bulkfile_df["FeO"][row]
        ca = bulkfile_df["CaO"][row]
        al = bulkfile_df["Al2O3"][row]
        na = bulkfile_df["Na2O"][row]

        hefesto_bsp_file = open("{}_BSP_HeFESTO_Infile.txt".format(star))

        format_of_file = "{}\n0,20,80,1600,0,-2,0\n6,2,4,2\noxides\nSi          {}      5.39386    0\nMg          {}     2.71075    0\n" \
                         "Fe          {}      .79840    0\nCa            {}      .31431    0\nAl            {}      .96680    0\n" \
                         "Na            {}      .40654    0\n1,1,1\ninv251010\n47\nphase plg\n1\nan\nab\nphase sp\n0\nsp\nhc\n" \
                         "phase opx\n1\n\nen\nfs\nmgts\nodi\nphase c2c\n0\nmgc2\nfec2\nphase cpx\n1\ndi\n\nhe\ncen\ncats\n\njd\n" \
                         "phase gt\n0\npy\nal\ngr\nmgmj\njdmj\nphase cpv\n0\ncapv\nphase ol\n1\nfo\nfa\nphase wa\n0\nmgwa\nfewa\n" \
                         "phase ri\n0\nmgri\nferi\nphase il\n0\nmgil\nfeil\nco\nphase pv\n0\nmgpv\nfepv\nalpv\nphase ppv\n0\nmppv\n" \
                         "fppv\nappv\nphase cf\n0\nmgcf\nfecf\nnacf\nphase mw\n0\npe\nwu\nphase qtz\n1\nqtz\nphase coes\n0\ncoes\n" \
                         "phase st\n0\nst\nphase apbo\n0\napbo\nphase ky\n0\nky\nphase neph\n0\nneph".format(star, si,
                            mg, fe, ca, al, na)

        hefesto_bsp_file.write(format_of_file)
        hefesto_bsp_file.close()
        fdir = home_dir[0] + "/{}".format("{}_BSP_HeFESTO_Infile.txt".format(star))
        tdir = home_dir[0] + "/BSP_HeFESTo_Input_Files/{}".format("{}_BSP_HeFESTO_Infile.txt".format(star))
        shutil.move(fdir, tdir)


def hefestofilewriter_morb(bulkfile):

    os.chdir(home_dir[0])

    bulkfile_name = bulkfile[:-4]

    if os.path.exists("{}_MORB_HeFESTo_Input_Files".format(bulkfile_name)):
        os.remove("{}_MORB_HeFESTo_Input_Files".format(bulkfile_name))
    else:
        pass

    os.mkdir("{}_MORB_HeFESTo_Input_Files".format(bulkfile_name))

    bulkfile_df = pd.read_csv(bulkfile)

    for row in bulkfile_df.index:
        star = bulkfile_df["Star"][row]
        si = bulkfile_df["SiO2"][row]
        mg = bulkfile_df["MgO"][row]
        fe = bulkfile_df["FeO"][row]
        ca = bulkfile_df["CaO"][row]
        al = bulkfile_df["Al2O3"][row]
        na = bulkfile_df["Na2O"][row]

        hefesto_morb_file = open("{}_MORB_HeFESTO_Infile.txt".format(star))

        format_of_file = "{}\n0,20,80,1200,0,-2,0\n6,2,4,2\noxides\nSi           {}     5.33159    0\n" \
                         "Mg           {}     1.37685    0\nFe           {}      .55527    0\n" \
                         "Ca           {}     1.33440    0\nAl           {}     1.82602    0\n" \
                         "Na           {}     0.71860    0\n1,1,1\ninv251010\n47\nphase plg\n1\nan\nab\nphase sp\n0\nsp\n" \
                         "hc\nphase opx\n1\nen\nfs\nmgts\nodi\nphase c2c\n0\nmgc2\nfec2\nphase cpx\n1\ndi\nhe\ncen\ncats\n" \
                         "jd\nphase gt\n0\npy\nal\ngr\nmgmj\njdmj\nphase cpv\n0\ncapv\nphase ol\n1\nfo\nfa\nphase wa\n0\n" \
                         "mgwa\nfewa\nphase ri\n0\nmgri\nferi\nphase il\n0\nmgil\nfeil\nco\nphase pv\n0\nmgpv\nfepv\nalpv\n" \
                         "phase ppv\n0\nmppv\nfppv\nappv\nphase cf\n0\nmgcf\nfecf\nnacf\nphase mw\n0\npe\nwu\nphase qtz\n" \
                         "1\nqtz\nphase coes\n0\ncoes\nphase st\n0\nst\nphase apbo\n0\napbo\nphase ky\n0\nky\nphase neph\n" \
                         "0\nneph".format(star, si, mg, fe, ca, al, na)

        hefesto_morb_file.write(format_of_file)
        hefesto_morb_file.close()
        fdir = home_dir[0] + "/{}".format("{}_MORB_HeFESTO_Infile.txt".format(star))
        tdir = home_dir[0] + "/MORB_HeFESTo_Input_Files/{}".format("{}_MORB_HeFESTO_Infile.txt".format(star))
        shutil.move(fdir, tdir)







def runhefesto(actual_run):

    os.chdir(home_dir[0])

    if actual_run is True:
        try:
            if 'main' not in os.listdir(os.getcwd()):
                print("[X] ERROR!  HeFESTO's 'main' not detected in the working directory!\n")
                time.sleep(4)
                initialization()
            else:
                print("[~] HeFESTo detected in the working directory!\n")
                pass
            os.chdir(home_dir[0])
            print("\nPlease enter the name of your BSP HeFESTo input .csv sheet:")
            hefesto_input_bsp = input(">>> ")
            if hefesto_input_bsp in os.listdir(os.getcwd()):
                print("[~] {} has been found in the working directory!".format(hefesto_input_bsp))
            else:
                print("[X] {} has NOT been found in the working directory!".format(hefesto_input_bsp))
                time.sleep(4)
                initialization()
            print("\nPlease enter the name of your crust HeFESTo input .csv sheet:")
            hefesto_input_morb = input(">>> ")
            if hefesto_input_morb in os.listdir(os.getcwd()):
                print("[~] {} has been found in the working directory!".format(hefesto_input_morb))
            else:
                print("[X] {} has NOT been found in the working directory!".format(hefesto_input_morb))
                time.sleep(4)
                initialization()

            if os.path.exists("HeFESTO_BSP_Input_Files"):
                shutil.rmtree("HeFESTO_BSP_Input_Files")
            else:
                pass
            if os.path.exists("HeFESTO_MORB_Input_Files"):
                shutil.rmtree("HeFESTO_MORB_Input_Files")
            else:
                pass

            os.mkdir("HeFESTO_BSP_Input_Files")
            os.mkdir("HeFESTo_BSP_Output_Files")
            os.mkdir(os.getcwd() + "/HeFESTO_BSP_Output_Files/fort.66")
            os.mkdir(os.getcwd() + "/HeFESTO_BSP_Output_Files/fort.58")
            os.mkdir(os.getcwd() + "/HeFESTO_BSP_Output_Files/fort.59")
            os.mkdir("HeFESTO_MORB_Input_Files")
            os.mkdir(os.getcwd() + "/HeFESTO_MORB_Output_Files/fort.66")
            os.mkdir(os.getcwd() + "/HeFESTO_MORB_Output_Files/fort.58")
            os.mkdir(os.getcwd() + "/HeFESTO_MORB_Output_Files/fort.59")

            bsp_infile_init = (home_dir[0] + "/{}".format(hefesto_input_bsp))
            bsp_infile_to = (home_dir[0] + "/HeFESTO_BSP_Input_Files/{}".format(hefesto_input_bsp))
            morb_infile_init = (home_dir[0] + "/{}".format(hefesto_input_morb))
            morb_infile_to = (home_dir[0] + "/HeFESTO_MORB_Input_Files/{}".format(hefesto_input_morb))
            shutil.copy(bsp_infile_init, bsp_infile_to)
            shutil.copy(morb_infile_init, morb_infile_to)

            os.chdir(home_dir[0] + "/HeFESTO_BSP_Input_Files")
            with open(hefesto_input_bsp, 'r') as infile:
                reader = csv.reader(infile, delimiter=",")
                for row in reader:
                    list_formatted = []
                    for z in row:
                        list_formatted.append(z)
                    title = list_formatted[0].strip()
                    output_file = open("{}_HeFESTo_BSP_nput.txt".format(title), 'a')
                    for z in list_formatted[1:]:
                        output_file.write("{}\n".format(z))
                    output_file.close()

            os.chdir(home_dir[0] + "/HeFESTO_MORB_Input_Files")
            with open(hefesto_input_morb, 'r') as infile:
                reader = csv.reader(infile, delimiter=",")
                for row in reader:
                    list_formatted = []
                    for z in row:
                        list_formatted.append(z)
                    title = list_formatted[0].strip()
                    output_file = open("{}_HeFESTo_MORB_Input.txt".format(title), 'a')
                    for z in list_formatted[1:]:
                        output_file.write("{}\n".format(z))
                    output_file.close()
            print("[~] HeFESTo files written!\n"
                  "Please see {} for your files!\n".format(os.getcwd()))
        except:
            pass

        os.chdir(home_dir[0] + "/HeFESTO_BSP_Input_Files")
        print("[~] Launching HeFESTo simulations...")
        # curr_planet = ""
        # for i in os.listdir(os.getcwd()):
        # curr_planet.update(i)
        # print("[~] Currently simulating BSP for: {}".format(curr_planet.get()))



    else:
        try:
            if os.path.exists(home_dir[0] + "/HeFESTo_Inputs"):
                shutil.rmtree(home_dir[0] + "/HeFESTo_Inputs")
            else:
                pass
            os.mkdir(home_dir[0] + "/HeFESTo_Inputs")
            os.chdir(home_dir[0])
            print("\nPlease enter the name of your HeFESTo input .csv sheet:")
            hefesto_input = input(">>> ")
            if hefesto_input in os.listdir(os.getcwd()):
                print("[~] {} has been found in the working directory!".format(hefesto_input))
            else:
                print("[X] {} has NOT been found in the working directory!".format(hefesto_input))
                time.sleep(4)
                initialization()

            infile_init = (home_dir[0] + "/{}".format(hefesto_input))
            infile_to = (home_dir[0] + "/HeFESTO_Inputs/{}".format(hefesto_input))
            shutil.copy(infile_init, infile_to)

            os.chdir(home_dir[0] + "/HeFESTO_Inputs")
            with open(hefesto_input, 'r') as infile:
                reader = csv.reader(infile, delimiter=",")
                for row in reader:
                    list_formatted = []
                    for z in row:
                        list_formatted.append(z)
                    title = list_formatted[0].strip()
                    output_file = open("{}_HeFESTo_Input.txt".format(title), 'a')
                    for z in list_formatted[1:]:
                        output_file.write("{}\n".format(z))
                        # if z.isalpha() == True:
                        #     output_file.write("{}\n".format(z))
                        # else:
                        #     output_file.write("{}\n".format(z))
                    output_file.close()
            print("[~] HeFESTo files written!\n"
                  "Please see {} for your files!\n".format(os.getcwd()))
        except:
            pass




def scrapemorb(infiledirectory, infilename):

    if "{}_MORB_Consolidated_Chem_File".format(infilename) in os.listdir(home_dir[0]):
        os.remove(home_dir[0] + "/{}_MORB_Consolidated_Chem_File".format(infilename))
    else:
        pass

    morb_outfile = open((home_dir[0] + "/{}_MORB_Consolidated_Chem_File".format(infilename)), 'a') # need a header
    morb_outfile_header = "Star Name,Pressure,Temperature,mass,SiO2,TiO2,Al2O3,Fe2O3,Cr2O3,FeO,MgO,CaO,Na2O\n"
    morb_outfile.write(morb_outfile_header)


    for i in os.listdir(infiledirectory):
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

    morb_recalc_outfile = open("{}_MORB_Recalc_Bulkfile.csv".format(infilename), 'a')
    morb_recalc_outfile_header = "Star,Pressure,Temperature,Mass,SiO2,TiO2,Al2O3,Cr2O3,FeO,MgO,CaO,Na2O,SUM\n"
    morb_recalc_outfile.write(morb_recalc_outfile_header)

    df_morb_chem = pd.read_csv(bulkfilename)
    for row in df_morb_chem.index:
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

        # fe2o3 --> feo recalc
        total_mol_fe = (fe_feo_cations + fe_fe2o3_cations)
        total_wt_fe = total_mol_fe * fe_atwt
        total_wt_feo = total_mol_fe * feo_molwt

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
        norm_wt_cao = wt_mgo_in / unnorm_sum
        norm_wt_na2o = wt_na2o_in / unnorm_sum
        norm_sum_nomgofix = (norm_wt_sio2 + norm_wt_tio2 + norm_wt_al2o3 + norm_wt_feo + norm_wt_cr2o3 + norm_wt_mgo +
                                norm_wt_cao + norm_wt_na2o)

        # mgo fix
        norm_wt_mgo_fix = norm_wt_mgo * mgo_fix
        norm_sum_mgofix = (norm_wt_sio2 + norm_wt_tio2 + norm_wt_al2o3 + norm_wt_feo + norm_wt_cr2o3 + norm_wt_mgo_fix +
                                norm_wt_cao + norm_wt_na2o)

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

        chem_to_outfile = "{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(star_name, pressure, temperature, mass, sio2_wtpct,
                                tio2_wtpct, al2o3_wtpct, cr2o3_wtpct, feo_wtpct, mgo_wtpct, cao_wtpct, na2o_wtpct, sum_wtpct)

        morb_recalc_outfile.write(chem_to_outfile)


    morb_recalc_outfile.close()









        # def file_parse_morb():
        #     if "MORB_Data.csv" in os.listdir(os.getcwd()):
        #         os.remove("MORB_Data.csv")
        #     else:
        #         pass
        #     # working_dir = os.getcwd()
        #     combined_output_file = open("MORB_Data.csv", "a")
        #     combined_output_file.write(",".join(header_structure_morb) + "\n")
        #     for filename in glob.glob("*.csv"):
        #         if not filename == "MORB_Data.csv":
        #             if enumerate(filename, 1) >= 100:
        #                 with open(filename, "rb") as meltsfile2:
        #                     data = []
        #                     try:
        #                         reader2 = csv.reader(meltsfile2, delimiter=",")
        #                         reader2 = list(reader2)
        #                         title = reader2[0][1]
        #                         data.append(str(title))
        #                         print
        #                         "\n\n" + "__________________________________________________________________" + "\n"
        #                         print
        #                         "\n" + "**********************************************" + "\n" + \
        #                         "This is the MORB alphaMELTS output file for: " + str(title) + " ..." + "\n" + \
        #                         "**********************************************"
        #                         for num, line in enumerate(reader2, 1):
        #                             if "Liquid" in line:
        #                                 # print num
        #                                 skip_row2 = num + 1
        #                                 liquid_comp = reader2[skip_row2]
        #                                 print
        #                                 ""
        #                                 for item in liquid_comp:
        #                                     data.append(item)
        #                             else:
        #                                 pass
        #                     except:
        #                         pass
        #                 meltsfile2.close()
        #                 print
        #                 "The liquid composition at 5% melt is: " + "\n" + str(header_structure_morb) + "\n" + \
        #                 str(data) + "\n"
        #                 combined_output_file.write(",".join(data) + "\n")
        #                 time.sleep(0.5)
        #             else:
        #                 pass
        #         else:
        #             pass







# class hefestooutputparser:
#
#     def fort58_parser(self):
#
#         os.chdir(home_dir[0] + "/HeFESTO_BSP_Output_Files/fort.58")
#
#         for i in os.listdir(os.getcwd()):
#             infile = pd.read_csv(i, delimiter='infer')
#             depth = ""



def integrationloop2():

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




    hefesto_bsp_out_path = home_dir[0] + "/HeFESTO_BSP_Output_Files"
    hefesto_morb_out_path = home_dir[0] + "/HeFESTO_MORB_Output_Files"

    os.chdir(hefesto_bsp_out_path)

    print("\n[~] Initiating BSP HeFESTO output file parsing...\n")

    for i in os.listdir(os.getcwd()):
        depth_list = []
        bsp_rho_list = []
        morb_rho_list = []
        os.chdir(hefesto_bsp_out_path)
        cross_depth_list = []
        if "fort.58" in str(i):
            print("[~] Found file: {}".format(i))
            with open(i, 'r') as infile:
                # print(infile)
                # star_name = i[:-4]
                star_name = i[16:-8]
                # print(star_name)
                readthefile = pd.read_fwf(infile, colspecs='infer')
                depth_df = readthefile.iloc[:, [1]]
                depth_list2 = pd.np.array(depth_df)
                for list1 in depth_list2:
                    for val in list1:
                        depth_list.append(float(val))
                bsp_rho = readthefile.iloc[:, [3]]
                bsp_rho_list2 = pd.np.array(bsp_rho)
                for list1 in bsp_rho_list2:
                    for val in list1:
                        bsp_rho_list.append(float(val))
                infile.close()
                # print(depth_df)
                # print(bsp_rho)
                os.chdir(hefesto_morb_out_path)
                for z in os.listdir(os.getcwd()):
                    if star_name in str(z):
                        with open(z, 'r') as infile:
                            readthefile = pd.read_fwf(infile, colspecs="infer")
                            morb_rho = readthefile.iloc[:, [3]]
                            morb_rho_list2 = pd.np.array(morb_rho)
                            for list1 in morb_rho_list2:
                                for val in list1:
                                    morb_rho_list.append(float(val))
                            infile.close()
        rho_diff = [a - b for a, b in
                    zip(morb_rho_list, bsp_rho_list)]  # the difference in density between BSP and crust

        crossover_index = bisect.bisect_left(rho_diff, 0)
        # print(crossover_index)
        # print(depth_list)
        if crossover_index > 0:
            cross_depth = depth_list[crossover_index]
            cross_depth_list.append(float(cross_depth))
            # print(cross_depth)
        else:
            cross_depth = 0
            cross_depth_list.append(0.0)
            # print(cross_depth)

        integrated_rho = []
        for t in range(len(rho_diff) - 1):
            x = depth_list[:(t + 2)]
            y = rho_diff[:(t + 2)]
            integrated_rho.append(inte.simps(y, x))







def initialization():
    home_dir.append(os.getcwd())
    # integrationloop2()


    createbspenvfile()
    createmorbenvfile()
    print("\n_______________________________________________\n\n\n\n\n\n\n\n\n\n")
    print("\n\n\nThe Exoplanet Pocketknife\nScott D. Hull, The Ohio State University 2015-2017\n")
    print("This code is meant to work in conjunction with the methods described in 'The Prevalence of"
          " Exoplanetary Plate Tectonics' (Unterborn et. al 2017).\nPlease refer to the article and "
          "the documentation for more information.\n"
          "\n*Any use of this code or the methods described in Unterborn et al. 2016 requires proper"
          " citation.*\n\n")
    # if "Star2Oxide_Output.csv" in os.listdir(os.getcwd()):
    #     os.remove("Star2Oxide_Output.csv")
    # else:
    #     pass
    # outputfile = open("Star2Oxide_Output.csv", 'a')
    # time.sleep(1)
    print("Enter '1' to raw_input [X/H] stellar abundances or '2' to raw_input stellar mole abundances.\nEnter 'o' for "
          "more options.\n"
          "To exit, enter 'e'.")
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
    elif option1 == 'o':
        print("\nPlease enter the letter of your choice.  Would you like to: \na. Write a single file with MELTS raw_inputs\n"
              "b. Write a library of MELTS raw_input files\nc. Write a library of HeFESTo raw_input files")
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
