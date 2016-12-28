import os, sys, csv, glob, operator, shutil, time, string



# depth_trans_zone = [0, 6, 19.7, 28.9, 36.4, 43.88, 51.34, 58.81, 66.36, 73.94, 81.5, 88.97, 96.45, 103.93, 111.41,
#                     118.92, 126.47, 134.01, 141.55, 149.09, 156.64, 164.18, 171.72, 179.27, 186.79, 194.27, 201.75,
#                     209.23, 216.71, 224.09, 231.4, 238.7, 246.01, 253.31, 260.62, 267.9, 275.16, 282.42, 289.68,
#                     296.94, 304.19, 311.41, 318.44, 325.47, 332.5, 339.53, 346.56, 353.59, 360.62, 367.66, 374.69,
#                     381.72, 388.75, 395.78, 402.78, 409.72, 416.67, 423.61, 430.56, 437.5, 444.44, 451.32, 457.89,
#                     464.47, 471.05, 477.63, 484.21, 490.79, 497.37, 503.75, 510, 516.25, 522.5, 528.75, 535, 541.25,
#                     547.5, 553.95, 560.53, 567.11, 573.68]







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
    x = raw_input("Please enter 'bsp' or 'morb' to begin parsing, or enter 'align' to align outputs: ")
    if x == 'bsp':
        file_parse_bsp()
    elif x == 'morb':
        file_parse_morb()
    elif x == 'align':
        print "Would you like to align bsp or morb data?"
        y = raw_input("Please enter 'bsp' or 'morb', or 'universal' for data of any length: ")
        if y == 'bsp':
            bsp_align()
        elif y == 'morb':
            morb_align()
        elif y == 'universal':
            universalparse()
        else:
            print "Oops!  That's not a valid command!"
            initialization()
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
                                # skip_row = num + 1
                                csv_list = list(reader)
                                alloy_index = csv_list[0].index("alloy-solid_0")
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



def bsp_align():
    print "\n"
    if "Aligned_BSP_Outputs.csv" in os.listdir(home_dir_list[0]):
        os.remove("Aligned_BSP_Outputs.csv")
    else:
        pass
    aligned_out = open("Aligned_BSP_Outputs.csv", 'a')
    data1 = raw_input("Please enter your .csv filename: ")
    with open(data1, 'rb') as infile:
        val1 = []
        val2 = []
        val3 = []
        reader = csv.reader(infile, delimiter=",")
        for row in reader:
            try:
                val1.append(row[0].rstrip())
                val2.append(row[1].rstrip())
                val3.append(row[2])
            except:
                val2.append('-')
                val3.append('-')
                pass
        for x in val1:
            temp = []
            if x in val2:
                temp.append(x)
                ind = val2.index(temp[0])
                print "Got match: " + x + "\n"
                wr = x + "," + val3[ind]
                aligned_out.write("%s\n" % wr)
            else:
                print "Failed to find: " + x + "\n"
                wr = ""
                aligned_out.write("%s\n" % wr)
    aligned_out.close()
    print "\n\nFinished matching values!\n"




def morb_align():
    print "\n"
    if "Aligned_MORB_Outputs.csv" in os.listdir(home_dir_list[0]):
        os.remove("Aligned_MORB_Outputs.csv")
    else:
        pass
    aligned_out = open("Aligned_MORB_Outputs.csv", 'a')
    data1 = raw_input("Please enter your .csv filename: ")
    with open(data1, 'rb') as infile:
        val1 = []
        val2 = []
        val3 = []
        val4 = []
        val5 = []
        val6 = []
        val7 = []
        val8 = []
        val9 = []
        val10 = []
        val11 = []
        val12 = []
        val13 = []
        val14 = []
        reader = csv.reader(infile, delimiter=",")
        for row in reader:
            try:
                val1.append(row[0].rstrip())
                val2.append(row[1].rstrip())
                val3.append(row[2])
                val4.append(row[3])
                val5.append(row[4])
                val6.append(row[5])
                val7.append(row[6])
                val8.append(row[7])
                val9.append(row[8])
                val10.append(row[9])
                val11.append(row[10])
                val12.append(row[11])
                val13.append(row[12])
                val14.append(row[13])
            except:
                val2.append('-')
                val3.append('-')
                val4.append('-')
                val5.append('-')
                val6.append('-')
                val7.append('-')
                val8.append('-')
                val9.append('-')
                val10.append('-')
                val11.append('-')
                val12.append('-')
                val13.append('-')
                val14.append('-')
                pass
        for x in val1:
            temp = []
            if x in val2:
                temp.append(x)
                ind = val2.index(temp[0])
                print "Got match: " + x + "\n"
                wr = x + "," + val3[ind] + "," + val4[ind] + "," + val5[ind] + "," + val6[ind] + "," + val7[ind] + "," + val8[ind] + "," + val9[ind] + "," + val10[ind] + "," + val11[ind] + "," + val12[ind] + "," + val13[ind] + "," + val14[ind]
                aligned_out.write("%s\n" % wr)
            else:
                print "Failed to find: " + x + "\n"
                wr = ""
                aligned_out.write("%s\n" % wr)
    aligned_out.close()
    print "\n\nFinished matching values!\n"



def universalparse():
    if "Alligned_Outputs.csv" in os.listdir(os.curdir):
        print "\nFound 'Alligned_Outputs.csv' in working directory.  Removing...\n"
        os.remove("Alligned_Outputs.csv")
    else:
        pass
    aligned_out = open("Alligned_Outputs.csv", 'a')
    data1 = raw_input("Please enter your .csv filename: ")
    with open(data1, 'rb') as infile:
        reader = csv.reader(infile, delimiter=",")
        print "\nParsing...\n"
        time.sleep(1)
        success = []
        temp1 = []
        temp2 = []
        temp3 = []
        for row in reader:
            temp1.append(str(row[0]))
            temp2.append(str(row[1]))
            temp3.append(row[2:])
        for x in temp1:
            if x in temp2:
                success.append(x)
                ind = temp2.index(x)
                getthese = temp3[ind]
                print "Got match: " + x + "\n"
                usethese = ",".join(str(i) for i in getthese)
                wr = x + "," + usethese
                aligned_out.write("%s\n" % wr)
            else:
                print "Failed to find: " + x + "\n"
                wr = ""
                aligned_out.write("%s\n" % wr)
                pass
    aligned_out.close()
    print "\n\nFinished matching values!\n"







initialization()
