import os, csv, time, sys, shutil
from operator import add
from math import *
import pandas as pd


bsp_run = False
morb_run = False

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

num_na2o_cations = 2
num_mgo_cations = 1
num_al2o3_cations = 2
num_sio2_cations = 1
num_cao_cations = 1
num_tio2_cations = 1
num_cr2o3_cations = 2
num_feo_cations = 1
num_nio_cations = 1


asplund_na = 1479108.388
asplund_mg = 33884415.61
asplund_al = 2344228.815
asplund_si = 32359365.69
asplund_ca = 2041737.945
asplund_ti = 79432.82347
asplund_cr = 436515.8322
asplund_fe = 28183829.31
asplund_ni = 1698243.652
asplund_sivsfe = asplund_si/asplund_fe
asplund_navsfe = asplund_na/asplund_fe

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
mcd_sivsfe = mcd_earth_si/mcd_earth_fe
mcd_navsfe = mcd_earth_na/mcd_earth_fe

adjust_si = mcd_sivsfe/asplund_sivsfe
adjust_na = mcd_navsfe/asplund_navsfe

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



class equations:

    def adjustsi_fct(self, si_pct):
        adj_si_pct = si_pct*adjust_si
        return adj_si_pct

    def adjustna_fct(self, na_pct):
        adj_na_pct = na_pct*adjust_na
        return adj_na_pct



class createenvfiles:

    def createbspenvfile(self):
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
            eleven = "Supress: alloy-liquid"

            bspenvfile.write("{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n".format(one, two, three,
                                four, five, six, seven, eight, nine, ten, eleven))
            bspenvfile.close()
            
    def createmorbenvfile(self):
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
            eleven = "Supress: alloy-liquid"

            morbenvfile.write("{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n".format(one, two, three,
                                four, five, six, seven, eight, nine, ten, eleven))
            morbenvfile.close()


class runmelts:

    def runmeltsbsp(self):
        pass




    def runmeltsmorb(self):
        pass



class readinputs: #FIX WITH NICKEL

    def logep(self, infile):

        if "{}_MELTS_BSP_Input_Files".format(inputfile_list[0][:-4]) in os.listdir(os.getcwd()):
            shutil.rmtree("{}_MELTS_BSP_Input_Files".format(inputfile_list[0][:-4]))
            os.mkdir("{}_MELTS_BSP_Input_Files".format(inputfile_list[0][:-4]))
        else:
            os.mkdir("{}_MELTS_BSP_Input_Files".format(inputfile_list[0][:-4]))


        with open(infile, 'r') as inputfile:
            print("\n[~] Writing MELTS BSP Input Files...")
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

                fe_abundance = (10**(row['[Fe/H]']))*asplund_fe
                ca_abundance = (10**(row['[Ca/H]']))*asplund_ca
                al_abundance = (10**(row['[Al/H]']))*asplund_al
                na_abundance = (10**(row['[Na/H]']))*asplund_na
                mg_abundance = (10**(row['[Mg/H]']))*asplund_mg
                si_abundance = (10**(row['[Si/H]']))*asplund_si
                ti_abundance = (10**(row['[Ti/H]']))*asplund_ti
                cr_abundance = (10**(row['[Cr/H]']))*asplund_cr
                ni_abundance = (10**(row['[Ni/H]']))*asplund_ni
                total_abundances = (fe_abundance + ca_abundance + al_abundance + na_abundance + mg_abundance +
                                    si_abundance + ti_abundance + cr_abundance + ni_abundance)

                # print(total_abundances)

                init_pct_fe = fe_abundance/total_abundances
                init_pct_ca = ca_abundance/total_abundances
                init_pct_al = al_abundance/total_abundances
                init_pct_na = na_abundance/total_abundances
                init_pct_mg = mg_abundance/total_abundances
                init_pct_si = si_abundance/total_abundances
                init_pct_ti = ti_abundance/total_abundances
                init_pct_cr = cr_abundance/total_abundances
                init_pct_ni = ni_abundance/total_abundances
                init_pct_sum = (init_pct_fe + init_pct_ca + init_pct_al + init_pct_na + init_pct_mg + init_pct_si +
                                   init_pct_ti + init_pct_cr + init_pct_ni)

                # print(star_name)
                # print(init_pct_fe, init_pct_ca, init_pct_al, init_pct_na, init_pct_mg, init_pct_si,
                #                    init_pct_ti, init_pct_cr, init_pct_ni ,init_pct_sum)

                moles_si_remaining = equations.adjustsi_fct(equations, si_pct=init_pct_si)
                moles_na_remaining = equations.adjustna_fct(equations, na_pct=init_pct_na)

                norm_pct_sum = (init_pct_fe + init_pct_ca + init_pct_al + moles_na_remaining + init_pct_mg +
                                moles_si_remaining + init_pct_ti + init_pct_cr + init_pct_ni)
                
                norm_pct_fe = init_pct_fe/norm_pct_sum
                norm_pct_ca = init_pct_ca/norm_pct_sum
                norm_pct_al = init_pct_al/norm_pct_sum
                norm_pct_na = moles_na_remaining/norm_pct_sum
                norm_pct_mg = init_pct_mg/norm_pct_sum
                norm_pct_si = moles_si_remaining/norm_pct_sum
                norm_pct_ti = init_pct_ti/norm_pct_sum
                norm_pct_cr = init_pct_cr/norm_pct_sum
                norm_pct_ni = init_pct_ni/norm_pct_sum
                check_norm_sum = (norm_pct_fe + norm_pct_ca + norm_pct_al + norm_pct_na + norm_pct_mg + norm_pct_si +
                                  norm_pct_ti + norm_pct_cr + norm_pct_ni)

                wt_feo = ((norm_pct_fe*fe_atwt)*feo_molwt)/(num_feo_cations*fe_atwt)
                wt_cao = ((norm_pct_ca*ca_atwt)*cao_molwt)/(num_cao_cations*ca_atwt)
                wt_al2o3 = ((norm_pct_al*al_atwt)*al2o3_molwt)/(num_al2o3_cations*al_atwt)
                wt_na2o = ((norm_pct_na*na_atwt)*na2o_molwt)/(num_na2o_cations*na_atwt)
                wt_mgo = ((norm_pct_mg*mg_atwt)*mgo_molwt)/(num_mgo_cations*mg_atwt)
                wt_sio2 = ((norm_pct_si*si_atwt)*sio2_molwt)/(num_sio2_cations*si_atwt)
                wt_tio2 = ((norm_pct_ti*ti_atwt)*tio2_molwt)/(num_tio2_cations*ti_atwt)
                wt_cr2o3 = ((norm_pct_cr*cr_atwt)*cr2o3_molwt)/(num_cr2o3_cations*cr_atwt)
                wt_nio = ((norm_pct_ni*ni_atwt)*nio_molwt)/(num_nio_cations*ni_atwt)
                sum_oxwts = (wt_feo + wt_cao + wt_al2o3 + wt_na2o + wt_mgo + wt_sio2 + wt_tio2 + wt_cr2o3 + wt_nio)

                norm_wt_feo = (wt_feo/sum_oxwts)*100
                norm_wt_cao = (wt_cao/sum_oxwts)*100
                norm_wt_al2o3 = (wt_al2o3/sum_oxwts)*100
                norm_wt_na2o = (wt_na2o/sum_oxwts)*100
                norm_wt_mgo = (wt_mgo/sum_oxwts)*100
                norm_wt_sio2 = (wt_sio2/sum_oxwts)*100
                norm_wt_tio2 = (wt_tio2/sum_oxwts)*100
                norm_wt_cr2o3 = (wt_cr2o3/sum_oxwts)*100
                norm_wt_nio = (wt_nio/sum_oxwts)*100
                norm_wt_sum_check = (norm_wt_feo + norm_wt_cao + norm_wt_al2o3 + norm_wt_na2o + norm_wt_mgo +
                                     norm_wt_sio2 + norm_wt_tio2 + norm_wt_cr2o3 + norm_wt_nio)

                # print(star_name)
                # print(norm_wt_feo, norm_wt_cao, norm_wt_al2o3, norm_wt_na2o, norm_wt_mgo, norm_wt_sio2,
                #       norm_wt_tio2, norm_wt_cr2o3, norm_wt_nio, norm_wt_sum_check)

                if (star_name + "_MELTS_BSP_INFILE.txt") in os.listdir(os.getcwd()):
                    os.remove(star_name + "_MELTS_BSP_INFILE.txt")
                else:
                    pass

                melts_input_file = open(star_name + "_MELTS_BSP_INFILE.txt", 'w')

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

                melts_input_file.write("{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n".format(title,
                        initfeo, initcao, inital2o3, initna2o, initmgo, initsio2, inittio2, initcr2o3,
                            initnio, init_temp, final_temp, inc_temp, init_press, final_press, dpdt, mode, mode2))

                melts_input_file.close()

                shutil.move((os.getcwd() + "/" + star_name + "_MELTS_BSP_INFILE.txt"),
                            (os.getcwd()+"/{}_MELTS_BSP_Input_Files/".format(inputfile_list[0][:-4])
                                          + star_name + "_MELTS_BSP_INFILE.txt"))

            print("{~} MELTS BSP Input Files Written!")
            print("{~} Launching alphaMELTS for BSP Calculations...")




        sys.exit()







    def molepct(self, infile):

        if "{}_MELTS_BSP_Input_Files".format(inputfile_list[0][:-4]) in os.listdir(os.getcwd()):
            shutil.rmtree("{}_MELTS_BSP_Input_Files".format(inputfile_list[0][:-4]))
            os.mkdir("{}_MELTS_BSP_Input_Files".format(inputfile_list[0][:-4]))
        else:
            os.mkdir("{}_MELTS_BSP_Input_Files".format(inputfile_list[0][:-4]))


        with open(infile, 'r') as inputfile:
            print("\n[~] Writing MELTS BSP Input Files...")
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

                init_pct_fe = fe_abundance/total_abundances
                init_pct_ca = ca_abundance/total_abundances
                init_pct_al = al_abundance/total_abundances
                init_pct_na = na_abundance/total_abundances
                init_pct_mg = mg_abundance/total_abundances
                init_pct_si = si_abundance/total_abundances
                init_pct_ti = ti_abundance/total_abundances
                init_pct_cr = cr_abundance/total_abundances
                init_pct_ni = ni_abundance/total_abundances
                init_pct_sum = (init_pct_fe + init_pct_ca + init_pct_al + init_pct_na + init_pct_mg + init_pct_si +
                                   init_pct_ti + init_pct_cr + init_pct_ni)

                # print("Init Cation%:")
                # print(init_pct_fe, init_pct_ca, init_pct_al, init_pct_na, init_pct_mg, init_pct_si,
                #                    init_pct_ti, init_pct_cr, init_pct_sum)

                moles_si_remaining = equations.adjustsi_fct(equations, si_pct=init_pct_si)
                moles_na_remaining = equations.adjustna_fct(equations, na_pct=init_pct_na)
                #
                # print("Moles Si/Na Remaining:")
                # print(moles_si_remaining, moles_na_remaining)

                norm_pct_sum = (init_pct_fe + init_pct_ca + init_pct_al + moles_na_remaining + init_pct_mg +
                                moles_si_remaining + init_pct_ti + init_pct_cr + init_pct_ni)

                norm_pct_fe = init_pct_fe/norm_pct_sum
                norm_pct_ca = init_pct_ca/norm_pct_sum
                norm_pct_al = init_pct_al/norm_pct_sum
                norm_pct_na = moles_na_remaining/norm_pct_sum
                norm_pct_mg = init_pct_mg/norm_pct_sum
                norm_pct_si = moles_si_remaining/norm_pct_sum
                norm_pct_ti = init_pct_ti/norm_pct_sum
                norm_pct_cr = init_pct_cr/norm_pct_sum
                norm_pct_ni = init_pct_ni/norm_pct_sum
                check_norm_sum = (norm_pct_fe + norm_pct_ca + norm_pct_al + norm_pct_na + norm_pct_mg + norm_pct_si +
                                  norm_pct_ti + norm_pct_cr + norm_pct_ni)

                # print("Normalized Cation% After Si/Na Correction:")
                # print(norm_pct_fe, norm_pct_ca, norm_pct_al, norm_pct_na, norm_pct_mg, norm_pct_si, norm_pct_ti,
                #       norm_pct_cr, norm_pct_ni, norm_pct_sum)

                wt_feo = ((norm_pct_fe*fe_atwt)*feo_molwt)/(num_feo_cations*fe_atwt)
                wt_cao = ((norm_pct_ca*ca_atwt)*cao_molwt)/(num_cao_cations*ca_atwt)
                wt_al2o3 = ((norm_pct_al*al_atwt)*al2o3_molwt)/(num_al2o3_cations*al_atwt)
                wt_na2o = ((norm_pct_na*na_atwt)*na2o_molwt)/(num_na2o_cations*na_atwt)
                wt_mgo = ((norm_pct_mg*mg_atwt)*mgo_molwt)/(num_mgo_cations*mg_atwt)
                wt_sio2 = ((norm_pct_si*si_atwt)*sio2_molwt)/(num_sio2_cations*si_atwt)
                wt_tio2 = ((norm_pct_ti*ti_atwt)*tio2_molwt)/(num_tio2_cations*ti_atwt)
                wt_cr2o3 = ((norm_pct_cr*cr_atwt)*cr2o3_molwt)/(num_cr2o3_cations*cr_atwt)
                wt_nio = ((norm_pct_ni*ni_atwt)*nio_molwt)/(num_nio_cations*ni_atwt)
                sum_oxwts = (wt_feo + wt_cao + wt_al2o3 + wt_na2o + wt_mgo + wt_sio2 + wt_tio2 + wt_cr2o3 + wt_nio)

                # print("Wt Oxides:")
                # print(wt_feo, wt_cao, wt_al2o3, wt_na2o, wt_mgo, wt_sio2, wt_tio2, wt_cr2o3, wt_nio, sum_oxwts)

                norm_wt_feo = (wt_feo/sum_oxwts)*100
                norm_wt_cao = (wt_cao/sum_oxwts)*100
                norm_wt_al2o3 = (wt_al2o3/sum_oxwts)*100
                norm_wt_na2o = (wt_na2o/sum_oxwts)*100
                norm_wt_mgo = (wt_mgo/sum_oxwts)*100
                norm_wt_sio2 = (wt_sio2/sum_oxwts)*100
                norm_wt_tio2 = (wt_tio2/sum_oxwts)*100
                norm_wt_cr2o3 = (wt_cr2o3/sum_oxwts)*100
                norm_wt_nio = (wt_nio/sum_oxwts)*100
                norm_wt_sum_check = (norm_wt_feo + norm_wt_cao + norm_wt_al2o3 + norm_wt_na2o + norm_wt_mgo +
                                     norm_wt_sio2 + norm_wt_tio2 + norm_wt_cr2o3 + norm_wt_nio)

                # print(star_name)
                # print(norm_wt_feo, norm_wt_cao, norm_wt_al2o3, norm_wt_na2o, norm_wt_mgo, norm_wt_sio2,
                #       norm_wt_tio2, norm_wt_cr2o3, norm_wt_nio, norm_wt_sum_check)

                if (star_name + "_MELTS_BSP_INFILE.txt") in os.listdir(os.getcwd()):
                    os.remove(star_name + "_MELTS_BSP_INFILE.txt")
                else:
                    pass

                melts_input_file = open(star_name + "_MELTS_BSP_INFILE.txt", 'w')

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

                melts_input_file.write("{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n".format(title,
                        initfeo, initcao, inital2o3, initna2o, initmgo, initsio2, inittio2, initcr2o3,
                            initnio, init_temp, final_temp, inc_temp, init_press, final_press, dpdt, mode, mode2))

                melts_input_file.close()

                shutil.move((os.getcwd() + "/" + star_name + "_MELTS_BSP_INFILE.txt"),
                            (os.getcwd()+"/{}_MELTS_BSP_Input_Files/".format(inputfile_list[0][:-4])
                                          + star_name + "_MELTS_BSP_INFILE.txt"))

            print("{~} MELTS BSP Input Files Written!")
            print("{~} Launching alphaMELTS for BSP Calculations...")




        sys.exit()




def __init__():

    home_dir.append(os.getcwd())
    createenvfiles.createbspenvfile(createenvfiles)
    createenvfiles.createmorbenvfile(createenvfiles)
    print("\n\n\nThe Exoplanet Pocketknife\nScott D. Hull, The Ohio State University 2016\n\n")
    # if "Star2Oxide_Output.csv" in os.listdir(os.getcwd()):
    #     os.remove("Star2Oxide_Output.csv")
    # else:
    #     pass
    # outputfile = open("Star2Oxide_Output.csv", 'a')
    # time.sleep(1)
    print("Enter '1' to input [X/H] stellar abundances or '2' to input mole% stellar abundances?")
    option1 = input(">>> ")
    if option1 == '1':
        print("\nPleaes enter your .csv formmated input file with [X/H] stellar abundances:")
        infile = input(">>> ")
        if infile in os.listdir(os.getcwd()):
            print("\n{} has been found in the working directory!".format(infile))
            inputfile_list.append(infile)
            # time.sleep(1)
            readinputs.logep(readinputs, infile)
        else:
            print("\n{} has NOT been found in the working directory!".format(infile))
            __init__()
    if option1 == '2':
        print("\nPleaes enter your .csv formmated input file with mole$ stellar abundances:")
        infile = input(">>> ")
        if infile in os.listdir(os.getcwd()):
            print("\n{} has been found in the working directory!".format(infile))
            inputfile_list.append(infile)
            # time.sleep(1)
            readinputs.molepct(readinputs, infile)
        else:
            print("\n{} has NOT been found in the working directory!".format(infile))
            __init__()
    else:
        print("\nOops!  That's not a valid command!\n")
        time.sleep(1)
        __init__()











__init__()
