import os
import pandas as pd

from depleted_calculator import Calculator, WriteFiles

# Adibekyan Files
a_bsp = pd.read_excel('C:/Users/Scott/Desktop/Depleted_Mantle_Runs_6_6_2019/Temperature_Formatted_MELTS_Output_Files/Adibekyan/BSP/Adibekyan_BSP.xlsx')
a_morb_1400 = pd.read_excel('C:/Users/Scott/Desktop/Depleted_Mantle_Runs_6_6_2019/Temperature_Formatted_MELTS_Output_Files/Adibekyan/MORB/1400/Adibekyan_MORB_1400.xlsx')
a_morb_1600 = pd.read_excel('C:/Users/Scott/Desktop/Depleted_Mantle_Runs_6_6_2019/Temperature_Formatted_MELTS_Output_Files/Adibekyan/MORB/1600/Adibekyan_MORB_1600.xlsx')
a_morb_1800 = pd.read_excel('C:/Users/Scott/Desktop/Depleted_Mantle_Runs_6_6_2019/Temperature_Formatted_MELTS_Output_Files/Adibekyan/MORB/1800/Adibekyan_MORB_1800.xlsx')
a_depleted_f1200 = pd.read_csv()
a_depleted_f1400 = pd.read_csv()
a_depleted_f1600 = pd.read_csv()

# Kepler Files
k_bsp = pd.read_excel('C:/Users/Scott/Desktop/Depleted_Mantle_Runs_6_6_2019/Temperature_Formatted_MELTS_Output_Files/Kepler/BSP/Kepler_BSP.xlsx')
k_morb_1400 = pd.read_excel('C:/Users/Scott/Desktop/Depleted_Mantle_Runs_6_6_2019/Temperature_Formatted_MELTS_Output_Files/Kepler/MORB/1400/Kepler_MORB_1400.xlsx')
k_morb_1600 = pd.read_excel('C:/Users/Scott/Desktop/Depleted_Mantle_Runs_6_6_2019/Temperature_Formatted_MELTS_Output_Files/Kepler/MORB/1600/Kepler_MORB_1600.xlsx')
k_morb_1800 = pd.read_excel('C:/Users/Scott/Desktop/Depleted_Mantle_Runs_6_6_2019/Temperature_Formatted_MELTS_Output_Files/Kepler/MORB/1800/Kepler_MORB_1800.xlsx')
k_depleted_f1200 = pd.read_csv()
k_depleted_f1400 = pd.read_csv()
k_depleted_f1600 = pd.read_csv()


# Adibekyan
a_bsp_calculator = Calculator()
a_morb_1400_calculator = Calculator()
a_morb_1600_calculator = Calculator()
a_morb_1800_calculator = Calculator()

a_morb_1400_writefiles = WriteFiles()
a_morb_1600_writefiles = WriteFiles()
a_morb_1800_writefiles = WriteFiles()


# Adibekyan F1400
for row in a_morb_1400.index:
    star = a_morb_1400['Star'][row]
    if star in a_bsp['Star'].tolist():
        bsp_index = a_bsp['Star'].tolist().index(star)
        morb_index = a_morb_1400['Star'].tolist().index(star)
        a_bsp_calculator.calculator(
            type='bsp',
            temperature=None,
            mass_fraction=None,
            mgo=a_bsp['MgO'][bsp_index],
            sio2=a_bsp['SiO2'][bsp_index],
            feo=a_bsp['FeO'][bsp_index],
            al2o3=a_bsp['Al2O3'][bsp_index],
            na2o=a_bsp['Na2O'][bsp_index],
            cao=a_bsp['CaO'][bsp_index],
            tio2=a_bsp['TiO2'][bsp_index],
        )
        a_bsp_moles = a_bsp_calculator.calcMoles()
        a_morb_1400_calculator.calculator(
            type='morb',
            temperature=1400,
            mass_fraction=a_morb_1400['Mass'][morb_index],
            mgo=a_morb_1400['MgO'][morb_index],
            sio2=a_morb_1400['SiO2'][morb_index],
            feo=a_morb_1400['FeO'][morb_index],
            al2o3=a_morb_1400['Al2O3'][morb_index],
            na2o=a_morb_1400['Na2O'][morb_index],
            cao=a_morb_1400['CaO'][morb_index],
            tio2=a_morb_1400['TiO2'][morb_index],
        )
        a_morb_1400_moles = a_morb_1400_calculator.calcMoles()
        a_morb_1400_difference = a_morb_1400_calculator.bsp_morb_difference(moles_bsp=a_bsp_moles,
                                                                      moles_morb_extracted=a_morb_1400_moles)
        a_morb_1400_moles_pct_changes = a_morb_1400_calculator.molesPctChanges(bsp_morb_differences=a_morb_1400_difference,
                                                                         moles_bsp=a_bsp_moles)
        a_morb_1400_bsp_morb_wt = a_morb_1400_calculator.wtBSPMORB(bsp_morb_moles=a_morb_1400_difference)
        a_morb_1400_depleted_mantle_composition_wt_pct = a_morb_1400_calculator.depletedMantleCompositionWtPct(
            bsp_morb_wt=a_morb_1400_bsp_morb_wt)
        a_morb_1400_depleted_mantle_composition_cation_pct = a_morb_1400_calculator.depletedMantleCompositionCations(
            depletedMantleCompositionWtPct=a_morb_1400_depleted_mantle_composition_wt_pct)
        a_morb_1400_bsp_files = a_morb_1400_writefiles.writeFile(star=star, type='bsp', F_temperature=1400, temperatures_to_run=[1400],
                                          kwargs=a_morb_1400_depleted_mantle_composition_cation_pct)


# # Adibekyan F1600
# for row in a_morb_1600.index:
#     star = a_morb_1600['Star'][row]
#     if star in a_bsp['Star'].tolist():
#         bsp_index = a_bsp['Star'].tolist().index(star)
#         morb_index = a_morb_1600['Star'].tolist().index(star)
#         a_bsp_calculator.calculator(
#             type='bsp',
#             temperature=None,
#             mass_fraction=None,
#             mgo=a_bsp['MgO'][bsp_index],
#             sio2=a_bsp['SiO2'][bsp_index],
#             feo=a_bsp['FeO'][bsp_index],
#             al2o3=a_bsp['Al2O3'][bsp_index],
#             na2o=a_bsp['Na2O'][bsp_index],
#             cao=a_bsp['CaO'][bsp_index],
#             tio2=a_bsp['TiO2'][bsp_index],
#         )
#         a_bsp_moles = a_bsp_calculator.calcMoles()
#         a_morb_1600_calculator.calculator(
#             type='morb',
#             temperature=1600,
#             mass_fraction=a_morb_1600['Mass'][morb_index],
#             mgo=a_morb_1600['MgO'][morb_index],
#             sio2=a_morb_1600['SiO2'][morb_index],
#             feo=a_morb_1600['FeO'][morb_index],
#             al2o3=a_morb_1600['Al2O3'][morb_index],
#             na2o=a_morb_1600['Na2O'][morb_index],
#             cao=a_morb_1600['CaO'][morb_index],
#             tio2=a_morb_1600['TiO2'][morb_index],
#         )
#         a_morb_1600_moles = a_morb_1600_calculator.calcMoles()
#         a_morb_1600_difference = a_morb_1600_calculator.bsp_morb_difference(moles_bsp=a_bsp_moles,
#                                                                       moles_morb_extracted=a_morb_1600_moles)
#         a_morb_1600_moles_pct_changes = a_morb_1600_calculator.molesPctChanges(bsp_morb_differences=a_morb_1600_difference,
#                                                                          moles_bsp=a_bsp_moles)
#         a_morb_1600_bsp_morb_wt = a_morb_1600_calculator.wtBSPMORB(bsp_morb_moles=a_morb_1600_difference)
#         a_morb_1600_depleted_mantle_composition_wt_pct = a_morb_1600_calculator.depletedMantleCompositionWtPct(
#             bsp_morb_wt=a_morb_1600_bsp_morb_wt)
#         a_morb_1600_depleted_mantle_composition_cation_pct = a_morb_1600_calculator.depletedMantleCompositionCations(
#             depletedMantleCompositionWtPct=a_morb_1600_depleted_mantle_composition_wt_pct)
#         a_morb_1600_bsp_files = a_morb_1600_writefiles.writeFile(star=star, type='bsp', F_temperature=1600, temperatures_to_run=[1400, 1600],
#                                           kwargs=a_morb_1600_depleted_mantle_composition_cation_pct)
#
# # Adibekyan F1800
# for row in a_morb_1800.index:
#     star = a_morb_1800['Star'][row]
#     if star in a_bsp['Star'].tolist():
#         bsp_index = a_bsp['Star'].tolist().index(star)
#         morb_index = a_morb_1800['Star'].tolist().index(star)
#         a_bsp_calculator.calculator(
#             type='bsp',
#             temperature=None,
#             mass_fraction=None,
#             mgo=a_bsp['MgO'][bsp_index],
#             sio2=a_bsp['SiO2'][bsp_index],
#             feo=a_bsp['FeO'][bsp_index],
#             al2o3=a_bsp['Al2O3'][bsp_index],
#             na2o=a_bsp['Na2O'][bsp_index],
#             cao=a_bsp['CaO'][bsp_index],
#             tio2=a_bsp['TiO2'][bsp_index],
#         )
#         a_bsp_moles = a_bsp_calculator.calcMoles()
#         a_morb_1800_calculator.calculator(
#             type='morb',
#             temperature=1800,
#             mass_fraction=a_morb_1800['Mass'][morb_index],
#             mgo=a_morb_1800['MgO'][morb_index],
#             sio2=a_morb_1800['SiO2'][morb_index],
#             feo=a_morb_1800['FeO'][morb_index],
#             al2o3=a_morb_1800['Al2O3'][morb_index],
#             na2o=a_morb_1800['Na2O'][morb_index],
#             cao=a_morb_1800['CaO'][morb_index],
#             tio2=a_morb_1800['TiO2'][morb_index],
#         )
#         a_morb_1800_moles = a_morb_1800_calculator.calcMoles()
#         a_morb_1800_difference = a_morb_1800_calculator.bsp_morb_difference(moles_bsp=a_bsp_moles,
#                                                                       moles_morb_extracted=a_morb_1800_moles)
#         a_morb_1800_moles_pct_changes = a_morb_1800_calculator.molesPctChanges(bsp_morb_differences=a_morb_1800_difference,
#                                                                          moles_bsp=a_bsp_moles)
#         a_morb_1800_bsp_morb_wt = a_morb_1800_calculator.wtBSPMORB(bsp_morb_moles=a_morb_1800_difference)
#         a_morb_1800_depleted_mantle_composition_wt_pct = a_morb_1800_calculator.depletedMantleCompositionWtPct(
#             bsp_morb_wt=a_morb_1800_bsp_morb_wt)
#         a_morb_1800_depleted_mantle_composition_cation_pct = a_morb_1800_calculator.depletedMantleCompositionCations(
#             depletedMantleCompositionWtPct=a_morb_1800_depleted_mantle_composition_wt_pct)
#         a_morb_1800_bsp_files = a_morb_1800_writefiles.writeFile(star=star, type='bsp', F_temperature=1800, temperatures_to_run=[1400, 1600, 1800],
#                                           kwargs=a_morb_1800_depleted_mantle_composition_cation_pct)
#
# # Kepler
# k_bsp_calculator = Calculator()
# k_morb_1400_calculator = Calculator()
# k_morb_1600_calculator = Calculator()
# k_morb_1800_calculator = Calculator()
#
# k_morb_1400_writefiles = WriteFiles()
# k_morb_1600_writefiles = WriteFiles()
# k_morb_1800_writefiles = WriteFiles()
#
# # Kepler BSP
#
# # Kepler F1400
# for row in k_morb_1400.index:
#     star = k_morb_1400['Star'][row]
#     if star in k_bsp['Star'].tolist():
#         bsp_index = k_bsp['Star'].tolist().index(star)
#         morb_index = k_morb_1400['Star'].tolist().index(star)
#         k_bsp_calculator.calculator(
#             type='bsp',
#             temperature=None,
#             mass_fraction=None,
#             mgo=k_bsp['MgO'][bsp_index],
#             sio2=k_bsp['SiO2'][bsp_index],
#             feo=k_bsp['FeO'][bsp_index],
#             al2o3=k_bsp['Al2O3'][bsp_index],
#             na2o=k_bsp['Na2O'][bsp_index],
#             cao=k_bsp['CaO'][bsp_index],
#             tio2=k_bsp['TiO2'][bsp_index],
#         )
#         k_bsp_moles = k_bsp_calculator.calcMoles()
#         k_morb_1400_calculator.calculator(
#             type='morb',
#             temperature=1400,
#             mass_fraction=k_morb_1400['Mass'][morb_index],
#             mgo=k_morb_1400['MgO'][morb_index],
#             sio2=k_morb_1400['SiO2'][morb_index],
#             feo=k_morb_1400['FeO'][morb_index],
#             al2o3=k_morb_1400['Al2O3'][morb_index],
#             na2o=k_morb_1400['Na2O'][morb_index],
#             cao=k_morb_1400['CaO'][morb_index],
#             tio2=k_morb_1400['TiO2'][morb_index],
#         )
#         k_morb_1400_moles = k_morb_1400_calculator.calcMoles()
#         k_morb_1400_difference = k_morb_1400_calculator.bsp_morb_difference(moles_bsp=k_bsp_moles,
#                                                                       moles_morb_extracted=k_morb_1400_moles)
#         k_morb_1400_moles_pct_changes = k_morb_1400_calculator.molesPctChanges(bsp_morb_differences=k_morb_1400_difference,
#                                                                          moles_bsp=k_bsp_moles)
#         k_morb_1400_bsp_morb_wt = k_morb_1400_calculator.wtBSPMORB(bsp_morb_moles=k_morb_1400_difference)
#         k_morb_1400_depleted_mantle_composition_wt_pct = k_morb_1400_calculator.depletedMantleCompositionWtPct(
#             bsp_morb_wt=k_morb_1400_bsp_morb_wt)
#         k_morb_1400_depleted_mantle_composition_cation_pct = k_morb_1400_calculator.depletedMantleCompositionCations(
#             depletedMantleCompositionWtPct=k_morb_1400_depleted_mantle_composition_wt_pct)
#         k_morb_1400_bsp_files = k_morb_1400_writefiles.writeFile(star=star, type='bsp', F_temperature=1400, temperatures_to_run=[1400],
#                                           kwargs=k_morb_1400_depleted_mantle_composition_cation_pct)
#
#
# # Kepler F1600
# for row in k_morb_1600.index:
#     star = k_morb_1600['Star'][row]
#     if star in k_bsp['Star'].tolist():
#         bsp_index = k_bsp['Star'].tolist().index(star)
#         morb_index = k_morb_1600['Star'].tolist().index(star)
#         k_bsp_calculator.calculator(
#             type='bsp',
#             temperature=None,
#             mass_fraction=None,
#             mgo=k_bsp['MgO'][bsp_index],
#             sio2=k_bsp['SiO2'][bsp_index],
#             feo=k_bsp['FeO'][bsp_index],
#             al2o3=k_bsp['Al2O3'][bsp_index],
#             na2o=k_bsp['Na2O'][bsp_index],
#             cao=k_bsp['CaO'][bsp_index],
#             tio2=k_bsp['TiO2'][bsp_index],
#         )
#         k_bsp_moles = k_bsp_calculator.calcMoles()
#         k_morb_1600_calculator.calculator(
#             type='morb',
#             temperature=1600,
#             mass_fraction=k_morb_1600['Mass'][morb_index],
#             mgo=k_morb_1600['MgO'][morb_index],
#             sio2=k_morb_1600['SiO2'][morb_index],
#             feo=k_morb_1600['FeO'][morb_index],
#             al2o3=k_morb_1600['Al2O3'][morb_index],
#             na2o=k_morb_1600['Na2O'][morb_index],
#             cao=k_morb_1600['CaO'][morb_index],
#             tio2=k_morb_1600['TiO2'][morb_index],
#         )
#         k_morb_1600_moles = k_morb_1600_calculator.calcMoles()
#         k_morb_1600_difference = k_morb_1600_calculator.bsp_morb_difference(moles_bsp=k_bsp_moles,
#                                                                       moles_morb_extracted=k_morb_1600_moles)
#         k_morb_1600_moles_pct_changes = k_morb_1600_calculator.molesPctChanges(bsp_morb_differences=k_morb_1600_difference,
#                                                                          moles_bsp=k_bsp_moles)
#         k_morb_1600_bsp_morb_wt = k_morb_1600_calculator.wtBSPMORB(bsp_morb_moles=k_morb_1600_difference)
#         k_morb_1600_depleted_mantle_composition_wt_pct = k_morb_1600_calculator.depletedMantleCompositionWtPct(
#             bsp_morb_wt=k_morb_1600_bsp_morb_wt)
#         k_morb_1600_depleted_mantle_composition_cation_pct = k_morb_1600_calculator.depletedMantleCompositionCations(
#             depletedMantleCompositionWtPct=k_morb_1600_depleted_mantle_composition_wt_pct)
#         k_morb_1600_bsp_files = k_morb_1600_writefiles.writeFile(star=star, type='bsp', F_temperature=1600, temperatures_to_run=[1400, 1600],
#                                           kwargs=k_morb_1600_depleted_mantle_composition_cation_pct)
#
# # Kepler F1800
# for row in k_morb_1800.index:
#     star = k_morb_1800['Star'][row]
#     if star in k_bsp['Star'].tolist():
#         bsp_index = k_bsp['Star'].tolist().index(star)
#         morb_index = k_morb_1800['Star'].tolist().index(star)
#         k_bsp_calculator.calculator(
#             type='bsp',
#             temperature=None,
#             mass_fraction=None,
#             mgo=k_bsp['MgO'][bsp_index],
#             sio2=k_bsp['SiO2'][bsp_index],
#             feo=k_bsp['FeO'][bsp_index],
#             al2o3=k_bsp['Al2O3'][bsp_index],
#             na2o=k_bsp['Na2O'][bsp_index],
#             cao=k_bsp['CaO'][bsp_index],
#             tio2=k_bsp['TiO2'][bsp_index],
#         )
#         k_bsp_moles = k_bsp_calculator.calcMoles()
#         k_morb_1800_calculator.calculator(
#             type='morb',
#             temperature=1800,
#             mass_fraction=k_morb_1800['Mass'][morb_index],
#             mgo=k_morb_1800['MgO'][morb_index],
#             sio2=k_morb_1800['SiO2'][morb_index],
#             feo=k_morb_1800['FeO'][morb_index],
#             al2o3=k_morb_1800['Al2O3'][morb_index],
#             na2o=k_morb_1800['Na2O'][morb_index],
#             cao=k_morb_1800['CaO'][morb_index],
#             tio2=k_morb_1800['TiO2'][morb_index],
#         )
#         k_morb_1800_moles = k_morb_1800_calculator.calcMoles()
#         k_morb_1800_difference = k_morb_1800_calculator.bsp_morb_difference(moles_bsp=k_bsp_moles,
#                                                                       moles_morb_extracted=k_morb_1800_moles)
#         k_morb_1800_moles_pct_changes = k_morb_1800_calculator.molesPctChanges(bsp_morb_differences=k_morb_1800_difference,
#                                                                          moles_bsp=k_bsp_moles)
#         k_morb_1800_bsp_morb_wt = k_morb_1800_calculator.wtBSPMORB(bsp_morb_moles=k_morb_1800_difference)
#         k_morb_1800_depleted_mantle_composition_wt_pct = k_morb_1800_calculator.depletedMantleCompositionWtPct(
#             bsp_morb_wt=k_morb_1800_bsp_morb_wt)
#         k_morb_1800_depleted_mantle_composition_cation_pct = k_morb_1800_calculator.depletedMantleCompositionCations(
#             depletedMantleCompositionWtPct=k_morb_1800_depleted_mantle_composition_wt_pct)
#         k_morb_1800_bsp_files = k_morb_1800_writefiles.writeFile(star=star, type='bsp', F_temperature=1800, temperatures_to_run=[1400, 1600, 1800],
#                                           kwargs=k_morb_1800_depleted_mantle_composition_cation_pct)
