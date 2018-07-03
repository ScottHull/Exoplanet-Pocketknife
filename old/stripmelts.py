import os
import shutil
import csv
import pandas as pd


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


def liqComp(infile):
    with open(infile, 'r') as infile:
        reader = csv.reader(infile)
        for row in reader:
            if 'liquid_0' in row:
                l = list(reader)
                if len(l) > 5:
                    for index, line in enumerate(l[1:]):
                        if l[index + 1] == []:
                            return l[index]
                else:
                    return []







if __name__ == "__main__":
    header = "Star,Pressure,Temperature,mass,S,H,V,Cp,viscosity,SiO2,TiO2,Al2O3,Fe2O3,Cr2O3,FeO,MgO,CaO,Na2O"
    if "logfile.csv" in os.listdir(os.getcwd()):
        os.remove("logfile.csv")
    outfile = open("logfile.csv", 'a')
    outfile.write(header + "\n")
    hefesto_fildir = os.getcwd() + '/hefesto_files'
    if os.path.exists(hefesto_fildir):
        shutil.rmtree(hefesto_fildir)
    os.mkdir(hefesto_fildir)
    for i in os.listdir(os.getcwd()):
        if "M_MORB_OUTPUT" in i:
            star = i.replace("_M_MORB_OUTPUT.csv", "")
            print(star)
            comp = liqComp(i)
            compstr = star + "," + ",".join(str(z) for z in comp)
            outfile.write(compstr + '\n')
    outfile.close()


    if "MORB_Recalc_Bulkfile.csv" in os.listdir(os.getcwd()):
        os.remove("MORB_Recalc_Bulkfile.csv")
    else:
        pass

    if "morb_debug.csv" in os.listdir(os.getcwd()):
        os.remove("morb_debug.csv")

    morb_debug = open("morb_debug.csv", 'a')

    morb_recalc_outfile = open("MORB_Recalc_Bulkfile.csv", 'a')
    morb_recalc_outfile_header = "Star,Pressure,Temperature,Mass,SiO2,TiO2,Al2O3,Cr2O3,FeO,MgO,CaO,Na2O,SUM\n"
    morb_recalc_outfile.write(morb_recalc_outfile_header)

    df_morb_chem = pd.read_csv("logfile.csv")
    for row in df_morb_chem.index:
        try:
            star_name = df_morb_chem["Star"][row]
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


    df = pd.read_csv("MORB_Recalc_Bulkfile.csv")
    for row in df.index:
        star = df["Star"][row]
        si = df["SiO2"][row]
        mg = df["MgO"][row]
        fe = df["FeO"][row]
        ca = df["CaO"][row]
        al = df["Al2O3"][row]
        na = df["Na2O"][row]
        hefesto_morb_file = open(hefesto_fildir + "/{}_MORB_HeFESTo_Infile.txt".format(star), 'a')

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
