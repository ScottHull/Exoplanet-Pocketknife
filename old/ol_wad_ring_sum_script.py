import os, csv, pandas


# header_structure = ["Star", "HeFESTo Pass/Fail?", "Olivine (fraction)", "Wadsleyite (fraction)", "Ringwoodite (fraction)", "Sum of Ol/Wa/Ring Phases"]

hefesto_stars_pass = []
hefesto_stars_fail = []

def __init__():
    print("\n_____________________________________\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print("Make sure that this file exists within a directory containing HeFESTo fort.66 files for parsing.\n")
    print("Please type 'b' to begin...")
    in1 = input(">>> ")
    if in1 == "b" or in1 == "begin":
        fort66_fileparse()
    else:
        print("\nOops!  That's not a valid command!\n")
        __init__()



def fort66_fileparse():
    if "Ol_Wa_Ring_Sums.csv" in os.listdir(os.getcwd()):
        os.remove("Ol_Wa_Ring_Sums.csv")
    else:
        pass
    outputfile = open("Ol_Wa_Ring_Sums.csv", 'a') #this output file will be created in working directory and will contain all sums with their respective star
    outputfile.write("{},{},{},{},{},{}\n".format("Star", "HeFESTo Pass/Fail?", "Olivine (fraction)", "Wadsleyite (fraction)", "Ringwoodite (fraction)", "Sum of Ol/Wa/Ring Phases"))
    for f in os.listdir(os.getcwd()):
        starname = f[16:-12]
        try:
            print("\nAnalyzing fort.66 output for star: " + starname)
            olivine_fraction_list = []
            wadsleyite_fraction_list = []
            ringwoodite_fraction_list = []
            all_sum = []
            with open(f, 'r') as infile:
                readthefile = pandas.read_fwf(infile, colspecs='infer')
                df = readthefile.iloc[:, [10, 11, 12]] #these are the columns in which ol/wad/ring always exist in HeFESTo fort.66 files.  To get sums of different phases, simply change column index.
                hefesto_stars_pass.append(starname)
                for i in df['ol']:
                    olivine_fraction_list.append(i)
                for i in df['wa']:
                    wadsleyite_fraction_list.append(i)
                for i in df['ri']:
                    ringwoodite_fraction_list.append(i)
            print("OLIVINE FRACTION: " + str(olivine_fraction_list[55])) #the 55th index of each column represents depth at 409.72km
            print("WADSLEYITE FRACTION: " + str(wadsleyite_fraction_list[55])) #the 55th index of each column represents depth at 409.72km
            print("RINGWOODITE FRACTION: " + str(ringwoodite_fraction_list[55])) #the 55th index of each column represents depth at 409.72km
            all_sum.append(olivine_fraction_list[55]) #the 55th index of each column represents depth at 409.72km
            all_sum.append(wadsleyite_fraction_list[55]) #the 55th index of each column represents depth at 409.72km
            all_sum.append(ringwoodite_fraction_list[55]) #the 55th index of each column represents depth at 409.72km
            # olivine_sum = sum(olivine_fraction_list)
            # wadsleyite_sum = sum(wadsleyite_fraction_list)
            # ringwoodite_sum = sum(ringwoodite_fraction_list)
            sum_of_phases = sum(all_sum)
            print("SUM OF OL/WA/RING PHASES: " + str(sum_of_phases))

            outputfile.write("{},{},{},{},{},{}\n".format(starname, "PASS", str(olivine_fraction_list[55]), str(wadsleyite_fraction_list[55]), str(ringwoodite_fraction_list[55]), str(sum_of_phases)))

        except:
            hefesto_stars_fail.append(starname)
            outputfile.write("{},{}\n".format(starname, "FAIL"))
            pass

    outputfile.close()




__init__()
