import os, sys, csv, glob, time


home_dir_list = []
home_dir_list.append(os.getcwd())



#header_structure0 = ['Star','Pressure','Temperature','mass','SiO2','TiO2','Al2O3','Fe2O3','Cr2O3','FeO',
#                    'MgO','NiO','CaO','Na2O', 'Alloy-Mass']

header_structure_bsp = ['Star', 'Alloy-Mass']

header_structure_morb = ["Star", 'Pressure', 'Temperature', 'mass', 'SiO2', 'TiO2', 'Al2O', 'Fe2O3', 'Cr2O3', 'FeO', 'MgO',
                         'CaO', 'Na2O']




def initialization():
    print "___________________________________________"
    print "\n\n\n\n\n\n\n\n\n\n\n\n"
    print "Would you like to parse bsp or morb files?"
    print "\n"
    x = raw_input("Please enter 'bsp' or 'morb' to begin scraping: ")
    if x == 'bsp':
        file_parse_bsp()
    elif x == 'morb':
        file_parse_morb()
    else:
        print "Oops!  That's not a valid command!"
        initialization()



def file_parse_bsp():
    if "BSP_Data.csv" in os.listdir(os.getcwd()):
        os.remove("BSP_Data.csv")
    else:
        pass
    #working_dir = os.getcwd()
    combined_output_file = open("BSP_Data.csv", "a")
    combined_output_file.write(",".join(header_structure_bsp) + "\n")
    if "temp.txt" in os.listdir(os.getcwd()):
        os.remove("temp.txt")
    else:
        pass
    for filename in glob.glob("*.csv"):
        time.sleep(0.5)
        if "temp.txt" in os.listdir(os.getcwd()):
            #os.remove("temp.txt")
            pass
        else:
            pass
        if not filename == "BSP_Data.csv":
            if enumerate(filename, 1) >= 100:
                try:
                    if "temp.txt" in os.listdir(os.getcwd()):
                        os.remove("temp.txt")
                    else:
                        pass
                except:
                    pass
                data = []
                with open(filename, "rb") as meltsfile2:
                    try:
                        reader2 = csv.reader(meltsfile2, delimiter=",")
                        reader2 = list(reader2)
                        title = reader2[0][1]
                        data.append(str(title))
                        print "\n\n" + "__________________________________________________________________" + "\n"
                        print "\n" +  "**********************************************" + "\n"+ \
                              "This is the BSP alphaMELTS output file for: " + str(title) + " ..." + "\n" + \
                              "**********************************************"
                       # for num, line in enumerate(reader2, 1):
                       #     if "Liquid" in line:
                       #         #print num
                       #         skip_row2 = num + 1
                       #         liquid_comp = reader2[skip_row2]
                       #         print ""
                       #         for item in liquid_comp:
                       #             data.append(item)
                       #     else:
                       #         pass
                    except:
                        pass
                meltsfile2.close()
                with open(filename, "rb") as meltsfile:
                    reader = csv.reader(meltsfile, delimiter=",")
                    for num, line in enumerate(reader, 1):
                        if "Phase" in line:
                            try:
                                #print num
                                skip_row = num + 1
                                #print skip_row
                                csv_list = list(reader)
                                alloy_index = csv_list[0].index("alloy-solid_0")
                                #print alloy_index
                                for row in csv_list[1:]:
                                    with open("temp.txt", "a") as tempfile:
                                        vals = []
                                        if not row == []:
                                            a = row[alloy_index]
                                            x = str(float(a))
                                            vals.append(x)
                                        else:
                                            break
                                        tempfile.write('%s\n' % vals)
                                    tempfile.close()
                                else:
                                    pass
                                somevals = []
                                with open("temp.txt", 'rb') as infile2:
                                    for row in infile2:
                                        x = float(row[2:-4])
                                        somevals.append(x)
                                    infile2.close()
                                print "\n" + "The mass of alloy generated is: " + str(sum(somevals)) + "g ..." + "\n"
                                thesum = str(float(sum(somevals)))
                                data.append(thesum)
                            except:
                                print "\n" + "There was an error while parsing this file.  Phase 'alloy-solid_0' may " \
                                             "not have been generated..." + "\n"
                                data.append("ERROR!")
                                combined_output_file.write(",".join(data) + "\n")
                                pass
                        else:
                            pass
                meltsfile.close()
                combined_output_file.write(",".join(data) + "\n")
                time.sleep(0.5)
                #print data
                print "\n"
            else:
                pass
        else:
            pass





def file_parse_morb():
    if "MORB_Data.csv" in os.listdir(os.getcwd()):
        os.remove("MORB_Data.csv")
    else:
        pass
    #working_dir = os.getcwd()
    combined_output_file = open("MORB_Data.csv", "a")
    combined_output_file.write(",".join(header_structure_morb) + "\n")
    for filename in glob.glob("*.csv"):
        if not filename == "MORB_Data.csv":
            if enumerate(filename, 1) >= 100:
                with open(filename, "rb") as meltsfile2:
                    data = []
                    try:
                        reader2 = csv.reader(meltsfile2, delimiter=",")
                        reader2 = list(reader2)
                        title = reader2[0][1]
                        data.append(str(title))
                        print "\n\n" + "__________________________________________________________________" + "\n"
                        print "\n" +  "**********************************************" + "\n"+ \
                              "This is the MORB alphaMELTS output file for: " + str(title) + " ..." + "\n" + \
                              "**********************************************"
                        for num, line in enumerate(reader2, 1):
                            if "Liquid" in line:
                                #print num
                                skip_row2 = num + 1
                                liquid_comp = reader2[skip_row2]
                                print ""
                                for item in liquid_comp:
                                    data.append(item)
                            else:
                                pass
                    except:
                        pass
                meltsfile2.close()
                print "The liquid composition at 5% melt is: " + "\n" + str(header_structure_morb) + "\n" + \
                      str(data) + "\n"
                combined_output_file.write(",".join(data) + "\n")
                time.sleep(0.5)
            else:
                pass
        else:
            pass






initialization()
