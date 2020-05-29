import os
import pandas as pd

bsp_files = [
    "/Users/scotthull/Documents - Scott’s MacBook Pro/PhD Research/depleted-lithosphere/adibekyan_bsp_compositions.csv",
    "/Users/scotthull/Documents - Scott’s MacBook Pro/PhD Research/depleted-lithosphere/kepler_bsp_compositions.csv"
]

morb_files = [
    "/Users/scotthull/Documents - Scott’s MacBook Pro/PhD Research/depleted-lithosphere/adibekyan_morb_compositions_f1200.csv",
    "/Users/scotthull/Documents - Scott’s MacBook Pro/PhD Research/depleted-lithosphere/adibekyan_morb_compositions_f1400.csv",
    "/Users/scotthull/Documents - Scott’s MacBook Pro/PhD Research/depleted-lithosphere/adibekyan_morb_compositions_f1600.csv",
    "/Users/scotthull/Documents - Scott’s MacBook Pro/PhD Research/depleted-lithosphere/kepler_morb_compositions_f1200.csv",
    "/Users/scotthull/Documents - Scott’s MacBook Pro/PhD Research/depleted-lithosphere/kepler_morb_compositions_f1400.csv",
    "/Users/scotthull/Documents - Scott’s MacBook Pro/PhD Research/depleted-lithosphere/kepler_morb_compositions_f1600.csv"
]

starting_masses_files = [
    "/Users/scotthull/Documents - Scott’s MacBook Pro/PhD Research/depleted-lithosphere/adibekyan_morb_starting_masses_f1200.csv",
    "/Users/scotthull/Documents - Scott’s MacBook Pro/PhD Research/depleted-lithosphere/adibekyan_morb_starting_masses_f1400.csv",
    "/Users/scotthull/Documents - Scott’s MacBook Pro/PhD Research/depleted-lithosphere/adibekyan_morb_starting_masses_f1600.csv",
    "/Users/scotthull/Documents - Scott’s MacBook Pro/PhD Research/depleted-lithosphere/kepler_morb_starting_masses_f1200.csv",
    "/Users/scotthull/Documents - Scott’s MacBook Pro/PhD Research/depleted-lithosphere/kepler_morb_starting_masses_f1400.csv",
    "/Users/scotthull/Documents - Scott’s MacBook Pro/PhD Research/depleted-lithosphere/kepler_morb_starting_masses_f1600.csv"
]

outfile_names = [
    "adibekyan_f1200_depleted_lithosphere_oxides.csv",
    "adibekyan_f1400_depleted_lithosphere_oxides.csv",
    "adibekyan_f1500_depleted_lithosphere_oxides.csv",
    "kepler_f1200_depleted_lithosphere_oxides.csv",
    "kepler_f1400_depleted_lithosphere_oxides.csv",
    "kepler_f1500_depleted_lithosphere_oxides.csv",
]


for index, i in enumerate(morb_files):
    outfile_name = outfile_names[index]
    if outfile_name in os.listdir(os.getcwd()):
        os.remove(outfile_name)
    outfile = open(outfile_name, "a")
    header = ["Star", "FeO", "Na2O", "MgO", "Al2O3", "SiO2", "CaO", "TiO2", "Cr2O3"]
    header_line = ",".join(str(i) for i in header)
    outfile.write(header_line + "\n")
    bsp = None
    df = pd.read_csv(i)
    print(starting_masses_files[index])
    starting_mass = pd.read_csv(starting_masses_files[index], index_col='star')
    if "adibekyan" in i:
        # print(i)
        # print(bsp_files[0])
        # print(starting_masses_files[index])
        bsp = pd.read_csv(bsp_files[0], index_col='Star')
    else:
        # print(i)
        # print(bsp_files[0])
        # print(starting_masses_files[index])
        bsp = pd.read_csv(bsp_files[1], index_col='Star')
    for row in df.index:
        star = df['Star'][row]
        # print(star)
        try:
            bsp_mass = starting_mass['initial_mass'][star]
            bsp_feo = bsp['FeO'][star] / 100.0
            bsp_na2o = bsp['Na2O'][star] / 100.0
            bsp_mgo = bsp['MgO'][star] / 100.0
            bsp_al2o3 = bsp['Al2O3'][star] / 100.0
            bsp_sio2 = bsp['SiO2'][star] / 100.0
            bsp_cao = bsp['CaO'][star] / 100.0
            bsp_tio2 = bsp['TiO2'][star] / 100.0
            bsp_cr2o3 = bsp['Cr2O3'][star] / 100.0

            morb_mass = df['Mass'][row]
            morb_feo = df['FeO'][row] / 100.0
            print(morb_feo)
            morb_na2o = df['Na2O'][row] / 100.0
            morb_mgo = (df['MgO'][row] / 100.0) / 0.646
            morb_al2o3 = df['Al2O3'][row] / 100.0
            morb_sio2 = df['SiO2'][row] / 100.0
            morb_cao = df['CaO'][row] / 100.0
            morb_tio2 = df['TiO2'][row] / 100.0
            morb_cr2o3 = df['Cr2O3'][row] / 100.0

            morb_oxide_sum = (morb_feo + morb_na2o + morb_mgo + morb_al2o3 + morb_sio2 + morb_cao + morb_tio2 + morb_cr2o3)

            morb_feo /= morb_oxide_sum
            print(morb_feo)
            morb_na2o /= morb_oxide_sum
            morb_mgo /= morb_oxide_sum
            morb_al2o3 /= morb_oxide_sum
            morb_sio2 /= morb_oxide_sum
            morb_cao /= morb_oxide_sum
            morb_tio2 /= morb_oxide_sum
            morb_cr2o3 /= morb_oxide_sum

            morb_oxide_sum2 = (morb_feo + morb_na2o + morb_mgo + morb_al2o3 + morb_sio2 + morb_cao + morb_tio2 + morb_cr2o3)

            morb_feo_mass = morb_feo * morb_mass
            morb_na2o_mass = morb_na2o * morb_mass
            morb_mgo_mass = morb_mgo * morb_mass
            morb_al2o3_mass = morb_al2o3 * morb_mass
            morb_sio2_mass = morb_sio2 * morb_mass
            morb_cao_mass = morb_cao * morb_mass
            morb_tio2_mass = morb_tio2 * morb_mass
            morb_cr2o3_mass = morb_cr2o3 * morb_mass

            bsp_feo_mass = bsp_feo * bsp_mass
            bsp_na2o_mass = bsp_na2o * bsp_mass
            bsp_mgo_mass = bsp_mgo * bsp_mass
            bsp_al2o3_mass = bsp_al2o3 * bsp_mass
            bsp_sio2_mass = bsp_sio2 * bsp_mass
            bsp_cao_mass = bsp_cao * bsp_mass
            bsp_tio2_mass = bsp_tio2 * bsp_mass
            bsp_cr2o3_mass = bsp_cr2o3 * bsp_mass

            depleted_feo = bsp_feo_mass - morb_feo_mass
            depleted_na2o = bsp_na2o_mass - morb_na2o_mass
            depleted_mgo = bsp_mgo_mass - morb_mgo_mass
            depleted_al2o3 = bsp_al2o3_mass - morb_al2o3_mass
            depleted_sio2 = bsp_sio2_mass - morb_sio2_mass
            depleted_cao = bsp_cao_mass - morb_cao_mass
            depleted_tio2 = bsp_tio2_mass - morb_tio2_mass
            depleted_cr2o3 = bsp_cr2o3_mass - morb_cr2o3_mass

            depleted_oxide_sum = (depleted_feo + depleted_na2o + depleted_mgo + depleted_al2o3 + depleted_sio2 +
                                   depleted_cao + depleted_tio2 + depleted_cr2o3)

            depleted_feo = depleted_feo / depleted_oxide_sum * 100.0
            depleted_na2o = depleted_na2o / depleted_oxide_sum * 100.0
            depleted_mgo = depleted_mgo / depleted_oxide_sum * 100.0
            depleted_al2o3 = depleted_al2o3 / depleted_oxide_sum * 100.0
            depleted_sio2 = depleted_sio2 / depleted_oxide_sum * 100.0
            depleted_cao = depleted_cao / depleted_oxide_sum * 100.0
            depleted_tio2 = depleted_tio2 / depleted_oxide_sum * 100.0
            depleted_cr2o3 = depleted_cr2o3 / depleted_oxide_sum * 100.0

            line = ",".join(str(j) for j in [
                star, depleted_feo, depleted_na2o, depleted_mgo, depleted_al2o3, depleted_sio2, depleted_cao, depleted_tio2,
                depleted_cr2o3
            ])
            outfile.write(line + "\n")
        except:
            outfile.write(star + "\n")

    outfile.close()


