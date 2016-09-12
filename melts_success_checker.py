import os, csv


#create a root directory in which this file is placed.  create two more directories, titled 'bsp' and 'morb'
#put bsp and morb MELTS .csv outputs in each respective directory
#run this code
#view output file "MELTS_Success_Checker_Output.csv"

full_list_stars = []
bsp_planetsindir = []
bsp_planetshung = []
bsp_planetssuccess = []
bsp_convergencefailure = []

morb_planetsindir = []
morb_planetshung = []
morb_convergencefailure = []
morb_planetssuccess = []

output_file_header=["All Planets", "BSP Planets w/ Output Files", "BSP Planets Hung", "BSP Convergence Failure",
                    "BSP Successful Planets", "MORB Planets w/ Output Files", "MORB Planets Hung", 
                    "MORB Convergence Failure", "MORB Successful Planets"]


class bsp_analysis:

    def meltsout_bspanalysis(self):
        print("\nComparing MELTS BSP output files to the full planet list...\n")
        os.chdir(os.getcwd() + "/bsp")
        for i in os.listdir(os.getcwd()):
            planetname = i[:-31]
            bsp_planetsindir.append(planetname)
            filesize = os.path.getsize(i)
            if filesize < 2000:
                bsp_convergencefailure.append(planetname)
        print("All BSP planet output files in directory...")
        print(bsp_planetsindir)
        for i in full_list_stars:
            planetname = i
            if i not in bsp_planetsindir:
                bsp_planetshung.append(planetname)
            else:
                if i not in bsp_convergencefailure:
                    bsp_planetssuccess.append(planetname)
        print("BSP planets that hung:")
        print(bsp_planetshung)
        print("BSP planets that had convergence failure:")
        print(bsp_convergencefailure)
        os.chdir("..")


class morb_analysis:
    
    def meltsout_morbanalysis(self):
        print("\nComparing MELTS MORB output files to the full planet list...\n")
        os.chdir(os.getcwd() + "/morb")
        for i in os.listdir(os.getcwd()):
            planetname = i[:-33]
            morb_planetsindir.append(planetname)
            filesize = os.path.getsize(i)
            if filesize < 2000:
                morb_convergencefailure.append(planetname)
        print("All MORB planet output files in directory...")
        print(morb_planetsindir)
        for i in bsp_planetssuccess:
            planetname = i
            if i not in morb_planetsindir:
                morb_planetshung.append(planetname)
        print("MORB planets that hung:")
        print(morb_planetshung)
        print("MORB planets that had convergence failure:")
        print(morb_convergencefailure)
        os.chdir("..")
        for i in full_list_stars:
            planetname = i
            if i not in morb_planetshung:
                if i not in morb_convergencefailure:
                    morb_planetssuccess.append(planetname)


def __init__(self):
    print("\n_________________________________________-\n\n\n\n\n\n\n\n\n\n\n")
    print("Please put MELTS BSP output file in a folder titled 'bsp' and pMELTS MORB output files in a folder titled"
          "'morb'.\n")
    print("Please enter a .csv in current working directory of the full list of planets in the first"
          "column to check against...")
    inputfile = input(">>> ")
    with open(inputfile, 'r') as infile:
        reader = csv.reader(infile, delimiter=",")
        for row in reader:
            full_list_stars.append(row[0])
    bsp_analysis.meltsout_bspanalysis(self)
    morb_analysis.meltsout_morbanalysis(self)

__init__(self=None)

if "MELTS_Success_Checker_Output.csv" in os.listdir(os.getcwd()):
    os.remove("MELTS_Success_Checker_Output.csv")
else:
    pass

full_list_stars_formatted = ["All Planets"] + full_list_stars
bsp_planetsindir_formatted = ["BSP Planets w/ Output Files"] + bsp_planetsindir
bsp_planetshung_formatted = ["BSP Planets Hung"] + bsp_planetshung
bsp_convergencefailure_formatted = ["BSP Convergence Failure"] + bsp_convergencefailure
bsp_planetssuccess_formatted = ["BSP Successful Planets"] + bsp_planetssuccess
morb_planetsindir_formatted = ["MORB Planets w/ Output Files"] + morb_planetsindir
morb_planetshung_formatted = ["MORB Planets Hung"] + morb_planetshung
morb_convergencefailure_formatted = ["MORB Convergence Failure"] + morb_convergencefailure
morb_planetssuccess_formatted = ["MORB Successful Planets"] + morb_planetssuccess

full_list_stars_formatted2 = ",".join(z for z in full_list_stars_formatted)
bsp_planetsindir_formatted2 = ",".join(z for z in bsp_planetsindir_formatted)
bsp_planetshung_formatted2 = ",".join(z for z in bsp_planetshung_formatted)
bsp_convergencefailure_formatted2 = ",".join(z for z in bsp_convergencefailure_formatted)
bsp_planetssuccess_formatted2 = ",".join(z for z in bsp_planetssuccess_formatted)
morb_planetsindir_formatted2 = ",".join(z for z in morb_planetsindir_formatted)
morb_planetshung_formatted2 = ",".join(z for z in morb_planetshung_formatted)
morb_convergencefailure_formatted2 = ",".join(z for z in morb_convergencefailure_formatted)
morb_planetssuccess_formatted2 = ",".join(z for z in morb_planetssuccess_formatted)

output_file_header_formatted = ",".join(z for z in output_file_header)
with open("MELTS_Success_Checker_Output.csv", 'a') as outputfile:
    outputfile.write("%s\n" % full_list_stars_formatted2)
    outputfile.write("%s\n" % bsp_planetsindir_formatted2)
    outputfile.write("%s\n" % bsp_planetshung_formatted2)
    outputfile.write("%s\n" % bsp_convergencefailure_formatted2)
    outputfile.write("%s\n" % bsp_planetssuccess_formatted2)
    outputfile.write("%s\n" % morb_planetsindir_formatted2)
    outputfile.write("%s\n" % morb_planetshung_formatted2)
    outputfile.write("%s\n" % morb_convergencefailure_formatted2)
    outputfile.write("%s\n" % morb_planetssuccess_formatted2)


outputfile.close()
print("\nExiting script...\n\n\n________________________________________\n")


# print("The full list of stars: ")
# print(full_list_stars)
