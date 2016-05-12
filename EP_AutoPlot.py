import os, shutil, time, bisect, string
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import operator
from operator import truediv




depth_trans_zone = [0, 6, 19.7, 28.9, 36.4, 43.88, 51.34, 58.81, 66.36, 73.94, 81.5, 88.97, 96.45, 103.93, 111.41,
                    118.92, 126.47, 134.01, 141.55, 149.09, 156.64, 164.18, 171.72, 179.27, 186.79, 194.27, 201.75,
                    209.23, 216.71, 224.09, 231.4, 238.7, 246.01, 253.31, 260.62, 267.9, 275.16, 282.42, 289.68,
                    296.94, 304.19, 311.41, 318.44, 325.47, 332.5, 339.53, 346.56, 353.59, 360.62, 367.66, 374.69,
                    381.72, 388.75, 395.78, 402.78, 409.72, 416.67, 423.61, 430.56, 437.5, 444.44, 451.32, 457.89,
                    464.47, 471.05, 477.63, 484.21, 490.79, 497.37, 503.75, 510, 516.25, 522.5, 528.75, 535, 541.25,
                    547.5, 553.95, 560.53, 567.11, 573.68]

mcdonough_bse_rho = [3.12293, 3.1433, 3.17531, 3.22685, 3.23507, 3.24317, 3.25117, 3.25906, 3.26686, 3.29163, 3.30443,
                     3.31523, 3.32475, 3.33344, 3.34157, 3.34933, 3.35681, 3.3641, 3.37123, 3.37824, 3.38516, 3.392,
                     3.39877, 3.40549, 3.41215, 3.41878, 3.42536, 3.43191, 3.43844, 3.44493, 3.45141, 3.45787, 3.46432,
                     3.47077, 3.47721, 3.48366, 3.49012, 3.4966, 3.50311, 3.50966, 3.51627, 3.52296, 3.53008, 3.5369,
                     3.54381, 3.55082, 3.55798, 3.56535, 3.57295, 3.58046, 3.58802, 3.5956, 3.60317, 3.61071, 3.61823,
                     3.69243, 3.74006, 3.74727, 3.7545, 3.76177, 3.76911, 3.77656, 3.78415, 3.79193, 3.79995, 3.80825,
                     3.81446, 3.81894, 3.8234, 3.82785, 3.83228, 3.83669, 3.84109, 3.84547, 3.85438, 3.8718, 3.89182,
                     3.9089, 3.91311, 3.9173, 3.92275]

gale_morb_rho = [2.96748, 2.98934, 3.02871, 3.12504, 3.2649, 3.32414, 3.40401, 3.41811, 3.43281, 3.44608, 3.45855,
                 3.47031, 3.5037, 3.51281, 3.52141, 3.52955, 3.5373, 3.54472, 3.55187, 3.55881, 3.56557, 3.57218,
                 3.57866, 3.58505, 3.59134, 3.59757, 3.60373, 3.60984, 3.6159, 3.62192, 3.62791, 3.63387, 3.6398,
                 3.64571, 3.6516, 3.65749, 3.75811, 3.7639, 3.7697, 3.77549, 3.7813, 3.78712, 3.79296, 3.79882,
                 3.80472, 3.81065, 3.81662, 3.82265, 3.82874, 3.8349, 3.84114, 3.84747, 3.85391, 3.86047, 3.86718,
                 3.87404, 3.88108, 3.88832, 3.89579, 3.90353, 3.91157, 3.91994, 3.92868, 3.93784, 3.94746, 3.95758,
                 3.96823, 3.97945, 3.99123, 4.00355, 4.01639, 4.02969, 4.04339, 4.05801, 4.07212, 4.08535, 4.09777,
                 4.10947, 4.1205, 4.13093, 4.14081]

simple_earth_bsp = [3.1399, 3.16644, 3.21129, 3.21993, 3.22843, 3.23679, 3.24503, 3.25316, 3.26117, 3.26909, 3.28169,
                    3.29415, 3.30499, 3.31476, 3.3238, 3.33232, 3.34046, 3.34832, 3.35595, 3.3634, 3.3707, 3.37788,
                    3.38495, 3.39193, 3.39884, 3.40567, 3.41244, 3.41916, 3.42582, 3.43244, 3.43902, 3.44557, 3.45208,
                    3.45857, 3.46504, 3.47149, 3.47794, 3.48438, 3.49083, 3.4973, 3.50379, 3.51032, 3.51783, 3.52856,
                    3.5352, 3.54193, 3.54876, 3.55574, 3.56291, 3.57035, 3.57813, 3.58638, 3.59525, 3.60495, 3.61577,
                    3.69282, 3.7338, 3.74885, 3.75742, 3.76575, 3.77393, 3.78203, 3.79015, 3.79837, 3.80676, 3.81424,
                    3.81873, 3.82321, 3.82768, 3.83213, 3.83656, 3.84098, 3.84538, 3.84977, 3.85831, 3.87594, 3.89625,
                    3.90832, 3.91254, 3.91675, 3.92094]


home_dir_list = []
home_dir_list.append(os.getcwd())





def initialization():
    print "_____________________________________________________________________"
    print "\n" + "\n" + "\n" + "\n" + "\n" + "\n" + "\n" + "\n" + "\n" + "\n" + "\n" + "\n" + "\n" + "\n" + "\n" + "\n" + "\n" + "\n" + "\n"
    print "Welcome to AutoPlot!" + "\n"
    if not os.path.exists(home_dir_list[0] + "/hefesto_fort.58_bsp_outputs"):
        print "Warning!  Path 'hefesto_fort.58_bsp_outputs' not detected in the working directory!  Please create this directory and place HeFESTo fort.58 BSP files in it!" + "\n"
    else:
        pass
    if not os.path.exists(home_dir_list[0] + "/hefesto_fort.58_morb_outputs"):
        print "Warning!  Path 'hefesto_fort.58_morb_outputs' not detected in the working directory!  Please create this directory and place HeFESTo fort.58 MORB files in it!" + "\n"
    else:
        pass
    if os.path.exists(home_dir_list[0] + "/hefesto_fort.58_bsp_outputs") and os.path.exists(home_dir_list[0] + "/hefesto_fort.58_morb_outputs"):
        print "Proper fort.58 BSP/MORB directories detected in the working directory!  Happy calculating!" + "\n"
    else:
        pass
    print "Please type 'begin' to launch the automated plotting process..." + "\n"
    x = raw_input(">>>Please enter 'begin': ")
    if x == "begin":
        makethedirs()
    else:
        print "\n" + "Oops!  That's not a valid command!" + "\n"
        initialization()




def makethedirs():
    if "Combined_All_File.csv" in os.listdir(home_dir_list[0]):
        os.remove(home_dir_list[0] + "/Combined_All_File.csv")
    else:
        pass
    if "Combined_DeltaRho_File.csv" in os.listdir(home_dir_list[0]):
        os.remove(home_dir_list[0] + "/Combined_DeltaRho_File.csv")
    else:
        pass
    if "Combined_BSPRho_File.csv" in os.listdir(home_dir_list[0]):
        os.remove(home_dir_list[0] + "/Combined_BSPRho_File.csv")
    else:
        pass
    if "Combined_MORBRho_File.csv" in os.listdir(home_dir_list[0]):
        os.remove(home_dir_list[0] + "/Combined_MORBRho_File.csv")
    else:
        pass
    if "Combined_Depth_File.csv" in os.listdir(home_dir_list[0]):
        os.remove(home_dir_list[0] + "/Combined_Depth_File.csv")
    else:
        pass
    if "log.csv" in os.listdir(home_dir_list[0]):
        os.remove(home_dir_list[0] + "/log.csv")
    if "log.csv" in os.listdir(home_dir_list[0]):
        os.remove(home_dir_list[0] + "/log.csv")
    else:
        pass
    if "Error_Calculations.csv" in os.listdir(home_dir_list[0]):
        os.remove(home_dir_list[0] + "/Error_Calculations.csv")
    else:
        pass
    print "\n" + "\n" + "Beginning BSP Output File Parsing..." + "\n"
    time.sleep(2)
    print "\n" + "Creating 'BSP_vs_Rho_Plots' directory.." + "\n"
    if not os.path.exists(home_dir_list[0] + "/BSP_vs_Rho_Plots"):
        os.mkdir(home_dir_list[0] + "/BSP_vs_Rho_Plots")
    else:
        shutil.rmtree(home_dir_list[0] + "/BSP_vs_Rho_Plots")
        os.mkdir(home_dir_list[0] + "/BSP_vs_Rho_Plots")
    print "\n"+ "Creating directory 'CSV_Formatted'..." + "\n"
    if not os.path.exists(home_dir_list[0] + "/hefesto_fort.58_bsp_outputs/CSV_Formatted"):
        os.mkdir(home_dir_list[0] + "/hefesto_fort.58_bsp_outputs/CSV_Formatted")
    else:
        shutil.rmtree(home_dir_list[0] + "/hefesto_fort.58_bsp_outputs/CSV_Formatted")
        os.mkdir(home_dir_list[0] + "/hefesto_fort.58_bsp_outputs/CSV_Formatted")
    if not os.path.exists(home_dir_list[0] + "/hefesto_fort.58_morb_outputs/CSV_Formatted"):
        os.mkdir(home_dir_list[0] + "/hefesto_fort.58_morb_outputs/CSV_Formatted")
    else:
        shutil.rmtree(home_dir_list[0] + "/hefesto_fort.58_morb_outputs/CSV_Formatted")
        os.mkdir(home_dir_list[0] + "/hefesto_fort.58_morb_outputs/CSV_Formatted")
    if not os.path.exists(home_dir_list[0] + "/Delta_Rho_CSV_Outputs"):
        os.mkdir(home_dir_list[0] + "/Delta_Rho_CSV_Outputs")
    else:
        shutil.rmtree(home_dir_list[0] + "/Delta_Rho_CSV_Outputs")
        os.mkdir(home_dir_list[0] + "/Delta_Rho_CSV_Outputs")
    if not os.path.exists(home_dir_list[0] + "/Delta_Rho_Plots"):
        os.mkdir(home_dir_list[0] + "/Delta_Rho_Plots")
    else:
        shutil.rmtree(home_dir_list[0] + "/Delta_Rho_Plots")
        os.mkdir(home_dir_list[0] + "/Delta_Rho_Plots")
    if not os.path.exists(home_dir_list[0] + "/Error_Plots"):
        os.mkdir(home_dir_list[0] + "/Error_Plots")
    else:
        shutil.rmtree(home_dir_list[0] + "/Error_Plots")
        os.mkdir(home_dir_list[0] + "/Error_Plots")
    os.chdir(home_dir_list[0] + "/hefesto_fort.58_bsp_outputs")
    for stuff in os.listdir(home_dir_list[0] + "/hefesto_fort.58_bsp_outputs"):
        print "\n" + "___________________________________________________________________" + "\n"
        try:
            if str(stuff)+"_csvformatted.csv" in os.listdir(home_dir_list[0] + "/hefesto_fort.58_bsp_outputs"):
                os.remove(str(stuff)+"_csvformatted.csv")
            else:
                pass
            with open(stuff, "rb") as infile:
                print "\n"  "\n" + "\n" + "This is file: "+str(stuff) + "\n"
                readthefile = pd.read_fwf(infile, colspecs='infer')
                #print readthefile
                df = readthefile.iloc[:, [1, 3]]
                print df
                df.to_csv(str(stuff) + '_csvformatted.csv', sep=",", header=False, index=False)
                filename = str(stuff)+"_csvformatted.csv"
                if filename in os.listdir(home_dir_list[0] + "/hefesto_fort.58_bsp_outputs"):
                    src = home_dir_list[0] + "/hefesto_fort.58_bsp_outputs/" + str(stuff)+"_csvformatted.csv"
                    todir = home_dir_list[0] + "/hefesto_fort.58_bsp_outputs/CSV_Formatted/" + str(stuff)+"_csvformatted.csv"
                    shutil.move(src, todir)
                    pd.read_csv(filename)
                else:
                    pass
                infile.close()
        except:
            print "\n" + "*******************************"
            print "File processed: " + str(stuff) + "..."
            print "*******************************" + "\n"
    else:
        print "\n" + "\n" + "\n" + "Done with BSP Output File Analysis!" + "\n" +"\n" + "\n" + "\n"
        time.sleep(2)

    #_________________________________________________________________________________________________________________________________________________BSP ABOVE, MORB BELOW

    print "Beginning MORB Output File Parsing..." + "\n"
    time.sleep(1)
    os.chdir(home_dir_list[0] + "/hefesto_fort.58_morb_outputs")
    for stuff in os.listdir(home_dir_list[0] + "/hefesto_fort.58_morb_outputs"):
        print "\n" + "___________________________________________________________________" + "\n"
        try:
            if str(stuff)+"_csvformatted.csv" in os.listdir(home_dir_list[0] + "/hefesto_fort.58_morb_outputs"):
                os.remove(str(stuff)+"_csvformatted.csv")
            else:
                pass
            with open(stuff, "rb") as infile:
                print "\n"  "\n" + "\n" + "This is file: "+str(stuff) + "\n"
                readthefile = pd.read_fwf(infile, colspecs='infer')
                #print readthefile
                df = readthefile.iloc[:, [1, 3]]
                print df
                df.to_csv(str(stuff) + '_csvformatted.csv', sep=",", header=False, index=False)
                filename = str(stuff)+"_csvformatted.csv"
                if filename in os.listdir(home_dir_list[0] + "/hefesto_fort.58_morb_outputs"):
                    src = home_dir_list[0] + "/hefesto_fort.58_morb_outputs/" + str(stuff)+"_csvformatted.csv"
                    todir = home_dir_list[0] + "/hefesto_fort.58_morb_outputs/CSV_Formatted/" + str(stuff)+"_csvformatted.csv"
                    shutil.move(src, todir)
                    pd.read_csv(filename)
                else:
                    print "Problem with moving file: " + str(filename) + "..."
                    pass
                infile.close()
        except:
            print "\n" + "*******************************"
            print "File processed: " + str(stuff) + "..."
            print "*******************************" + "\n"
    else:
        print "\n" + "\n" + "\n" + "Done with MORB Output File Analysis!" + "\n"
        time.sleep(2)
    plotbspvsmorb()


def plotbspvsmorb():
    combined_morb_output_file = open("Combined_MORBRho_File.csv", "a")
    print "\n" + "Looking for matches between BSP and MORB directories..." + "\n"
    time.sleep(2)
    planet_log = open("log.csv", "a")
    for filename in os.listdir(home_dir_list[0] + "/hefesto_fort.58_bsp_outputs\CSV_Formatted"):
        print "\n" + "___________________________________________________________________" + "\n"
        graphtitletemp2 = str(filename)[:-29]
        graphtitle2 = str(graphtitletemp2)[16:]
        print "\n" + "********************************"
        print "PROCESSING PLANET: " + str(graphtitle2) + "..."
        print "********************************" + "\n"
        print "\n" + "Found '" + str(filename)[:-4] + "' in BSP directory..."
        graphtitletemp = str(filename)[:-28]
        graphtitle = str(graphtitletemp)[7:]
        fileclipped = str(filename)[:-28] + "morb.txt_morb_csvformatted.csv"
        if fileclipped in os.listdir(home_dir_list[0] + "/hefesto_fort.58_morb_outputs\CSV_Formatted"):
            planet_log_success = graphtitle2 + ",Success\n"
            planet_log.write(planet_log_success)
            print "\n" + "Found '" + str(fileclipped) + "' in MORB directory..." + "\n"
            os.chdir(home_dir_list[0] + "/hefesto_fort.58_bsp_outputs\CSV_Formatted")
            try:
                print "\n" + "Opening data from " + str(filename) + "..." + "\n"
                bsp_rho_data = np.loadtxt(filename, delimiter=",", usecols=[0])
                bsp_depth = np.loadtxt(filename, delimiter=",", usecols=[1])
                print "\n" + "************************" + "\n" + "DATA FOR " + str(filename) + "\n" + "************************" + "\n"
                print "\n" + "\n" + "_______ASSIGNING BSP DATA TO LIST " + str(fileclipped) + "..."+"_______" + "\n"
                bsp_rho_list = []
                bsp_rho_list.append(bsp_rho_data)
                bsp_depth_list = []
                bsp_depth_list.append(bsp_depth)
                print "\n" + "PRINTING BSP RHO LIST FOR " + str(filename) + "..." + "\n"
                print bsp_rho_data
                print "\n" + "PRINTING BSP DEPTH LIST FOR " + str(filename) + "..." + "\n"
                print bsp_depth
                os.chdir(home_dir_list[0] + "/hefesto_fort.58_morb_outputs\CSV_Formatted")
                morb_data = np.loadtxt(fileclipped, delimiter=",", usecols=[0])
                morb_depth = np.loadtxt(fileclipped, delimiter=",", usecols=[1])
                print "\n" + "************************" + "\n" + "DATA FOR " + str(fileclipped) + "\n" + "************************" + "\n"
                print "\n" + "_______ASSIGNING MORB DATA TO LIST " + str(fileclipped) + "..." + "_______" + "\n"
                morb_rho_list = []
                morb_rho_list.append(morb_data)
                morb_depth_list = []
                morb_depth_list.append(morb_depth)
                print "\n" + "PRINTING MORB RHO LIST FOR " + str(filename) + "..." + "\n"
                print morb_data
                print "\n" + "PRINTING MORB DEPTH LIST FOR " + str(filename) + "..." + "\n"
                print morb_depth
                #deltarho = [(morb_rho_list-bsp_rho_list for morb_rho_list,bsp_rho_list in zip(morb_rho_list,bsp_rho_list))]
                #deltarho = map(sub, morb_data, bsp_rho_data)
                delta_rho_filename = str(graphtitle2)+"_deltarho.csv"
                #deltarho = list(set(morb_data) - set(bsp_rho_data))
                #deltarho = [morb_data - bsp_rho_data for morb_data, bsp_rho_data in zip(morb_data,bsp_rho_data)]
                deltarho_rows = map(operator.sub, morb_depth_list, bsp_depth_list)
                #deltarho_cols = zip(*deltarho_rows)
                try:
                    with open(delta_rho_filename, "wb") as fp:
                        for x in zip(*deltarho_rows):
                            fp.write("{0}\n".format(*x))
                        fp.close()
                except:
                    pass
                #time.sleep(0.5)
                fdir = home_dir_list[0] + "/hefesto_fort.58_morb_outputs/CSV_Formatted/" + delta_rho_filename
                gdir = home_dir_list[0] + "/Delta_Rho_CSV_Outputs/" + delta_rho_filename
                if delta_rho_filename in os.listdir(os.curdir):
                    shutil.move(fdir, gdir)
                else:
                    pass
                print "\n" + "PRINTING MORB RHO LIST FOR " + str(fileclipped) + "..." + "\n"
                print morb_data
                print "\n" + "PRINTING MORB DEPTH LIST FOR " + str(fileclipped) + "..." + "\n"
                print morb_depth
                reform_morb_data = []
                reform_morb_data.append(graphtitle2)
                reform_morb_data2 = ",".join(str(i) for i in morb_depth)
                reform_morb_data.append(reform_morb_data2)
                reform_morb_data3 = ",".join(i for i in reform_morb_data)
                combined_morb_output_file.write("%s\n" % reform_morb_data3)
                font = {'weight' : 'bold',
                        'size' : 14}
                matplotlib.rc('font', **font)
                if str(graphtitle2) + ".png" in os.listdir(home_dir_list[0] + "/hefesto_fort.58_morb_outputs\CSV_Formatted"):
                    os.remove(str(graphtitle2) + ".png")
                else:
                    pass
                plt.plot(depth_trans_zone, mcdonough_bse_rho, 'b', linestyle="--", label="Earth BSP", linewidth=3.0)
                plt.plot(depth_trans_zone, gale_morb_rho, 'b', label="Earth MORB", linewidth=3.0)
                plt.plot(bsp_rho_data, bsp_depth, '-r', linestyle="--", label="Exo-BSP", linewidth=3.0)
                plt.plot(morb_data,morb_depth, "-r", label="Exo-MORB", linewidth=3.0)
                plt.ylabel("Density (g/cc)")
                plt.xlabel("Depth (km)")
                plt.title(str(graphtitle2))
                plt.legend(loc='lower right')
                plt.xlim(xmax=570)
                plt.grid()
                plt.savefig(str(graphtitle2 + ".png"), format='png')
                plt.close()
                #plt.show()
                if str(graphtitle2) + ".png" in os.listdir(home_dir_list[0] + "/hefesto_fort.58_morb_outputs/CSV_Formatted"):
                    zdir = home_dir_list[0] + "/hefesto_fort.58_morb_outputs/CSV_Formatted/" + str(graphtitle2) + ".png"
                    tdir = home_dir_list[0] + "/BSP_vs_Rho_Plots/" + str(graphtitle2) + ".png"
                    shutil.move(zdir, tdir)
                    print "\n" + "****************************"
                    print str(graphtitle2) + ".png is available in 'BSP_vs_Rho_Plots' directory..."
                    print "****************************" + "\n"
                    #time.sleep(0.2)
                else:
                    pass
            except:
                print "\n" +"Error in opening and assigning data for " + str(filename) + " and " + str(fileclipped) + " ..." + "\n"
                pass
        else:
            print "\n" + "***"+fileclipped + " not found in MORB directory!***" + "\n"
            planet_log_fail = graphtitle2 + ",Failure\n"
            planet_log.write(planet_log_fail)
    planet_log.close()
    if "log.csv" in os.listdir(home_dir_list[0] + "/hefesto_fort.58_morb_outputs"):
        fdirr = home_dir_list[0] + "/hefesto_fort.58_morb_outputs/" + "log.csv"
        tdirr = home_dir_list[0] + "/" + "log.csv"
        shutil.move(fdirr, tdirr)
    else:
        print "'log.csv' not found!"
    combined_morb_output_file.close()
    if "Combined_MORBRho_File.csv" in os.listdir(home_dir_list[0] + "/hefesto_fort.58_morb_outputs"):
        fdir1 = home_dir_list[0] + "/hefesto_fort.58_morb_outputs/Combined_MORBRho_File.csv"
        tdir1 = home_dir_list[0] + "/Combined_MORBRho_File.csv"
        shutil.move(fdir1, tdir1)
        print "\n" + "'Combined_MORBRho_File.csv' now available!" + "\n"
    else:
        print "\n" + "Unable to find 'Combined_MORBRho_File.csv'!" + "\n"
        pass
    plotdeltarhovsbserho()



def plotdeltarhovsbserho():
    print "\n" + "Creating delta rho plots..." + "\n"
    combinedfile = open("Combined_All_File.csv", "a")
    combined_deltarho_file = open("Combined_DeltaRho_File.csv", "a")
    combined_bsp_rho_file = open("Combined_BSPRho_File.csv", "a")
    combined_depth_file = open("Combined_Depth_File.csv", "a")
    os.chdir(home_dir_list[0] + "/hefesto_fort.58_bsp_outputs\CSV_Formatted")
    for filename in os.listdir(home_dir_list[0] + "/hefesto_fort.58_bsp_outputs\CSV_Formatted"):
        print "\n" + "___________________________________________________________________" + "\n"
        graphtitletemp2 = str(filename)[:-29]
        graphtitle2 = str(graphtitletemp2)[16:]
        graphtitletemp = str(filename)[:-28]
        graphtitle = str(graphtitletemp)[7:]
        fileclipped = graphtitle2+"_deltarho.csv"
        print "\n" + "*******************************"
        print "Processing Planet: " + graphtitle2 + "..."
        print "*******************************" + "\n"
        print "\n" + "Found '"+str(filename)[:-4] + "' in BSP directory..."
        try:
            bsp_rho = np.loadtxt(filename, delimiter=",", usecols=[1])
            thedepths = np.loadtxt(filename, delimiter=",", usecols=[0])
        except:
            pass
        os.chdir(home_dir_list[0] + "/Delta_Rho_CSV_Outputs")
        if fileclipped in os.listdir(home_dir_list[0] + "/Delta_Rho_CSV_Outputs"):
            print "\n" + "Found files for star '" + str(graphtitle2) + "' in BSP/delta rho directories!"
            print "Found file: '" + str(fileclipped) + "' ..."
            print "Found file: '" + str(filename) + "' ..." + "\n"
            delta_rho = np.loadtxt(fileclipped, usecols=[0])
            deltarhovsbsprho = map(truediv, delta_rho, bsp_rho)
            if str(graphtitle2) + ".png" in os.listdir(home_dir_list[0] + "/hefesto_fort.58_bsp_outputs\CSV_Formatted"):
                os.remove(str(graphtitle2) + ".png")
            else:
                pass
            print "\n" + "Printing delta rho values..." + "\n"
            print delta_rho
            print "\n" + "Printing bsp rho values..." + "\n"
            print bsp_rho
            print "\n" + "Printing (delta rho / bsp rho) values..." + "\n"
            print deltarhovsbsprho
            outputs = []
            outputs.append(str(graphtitle2))
            reform_deltarhovsbsprho = ", ".join(str(i) for i in deltarhovsbsprho)
            outputs.append(reform_deltarhovsbsprho)
            reform_outputs = ", ".join(str(i) for i in outputs)
            #reformattedoutputs = outputs[1:-1]
            bsp_rho_outputs = []
            bsp_rho_outputs.append(str("---"))
            reform_bsprho = ", ".join(str(i) for i in bsp_rho)
            bsp_rho_outputs.append(reform_bsprho)
            reform_bsp_rho_outputs = ", ".join(str(i) for i in bsp_rho_outputs)
            bsp_rho_outputs2 = []
            bsp_rho_outputs2.append(str(graphtitle2))
            bsp_rho_outputs2.append(reform_bsprho)
            reform_bsp_rho_outputs2 = ", ".join(str(i) for i in bsp_rho_outputs2)
            greaterthanzero = bisect.bisect(deltarhovsbsprho, 0)
            thevalue = thedepths[greaterthanzero]
            print "\n" + "The depth of MORB override of BSP on planet " + graphtitle2 + " is: " + str(thevalue) + " km..." + "\n"
            thevalueformatted = []
            #reform_depth_outputs = ", ".join(thevalue)
            reform_depth_outputs = ", " + str(thevalue)
            thevalueformatted.append(str(graphtitle2))
            thevalueformatted.append(reform_depth_outputs)
            reform_depth_outputs = ", ".join(str(i) for i in thevalueformatted)
            depthsdepths = []
            depthsdepths.append(str("---"))
            reform_depthsdepths = ", ".join(str(i) for i in thedepths)
            depthsdepths.append(reform_depthsdepths)
            reform_depthdepth_outputs = ", ".join(str(i) for i in depthsdepths)
            combinedfile.write('%s\n%s\n%s\n' % (reform_outputs, reform_bsp_rho_outputs, reform_depthdepth_outputs))
            combined_bsp_rho_file.write('%s\n' % reform_bsp_rho_outputs2)
            combined_deltarho_file.write('%s\n' % reform_outputs)
            combined_depth_file.write('%s\n' % reform_depth_outputs)
            line_deltarho_y1 = 0.049748193831
            line_deltarho_x1 = 0
            line_deltarho_x2 = 6
            font = {'weight' : 'bold',
                    'size' : 14}
            matplotlib.rc('font', **font)
            plt.plot(bsp_rho, deltarhovsbsprho, '-b', label="Delta Rho", linewidth=2)
            plt.hlines(line_deltarho_y1, line_deltarho_x1, line_deltarho_x2, colors="r", linestyles='dashed', label="Earth-like", linewidth=2)
            plt.hlines(0, 1, 6, colors="k", linestyle="dashed",  linewidth=3)
            plt.xlabel("BSP Rho")
            plt.ylabel("Delta Rho / BSP Rho")
            plt.xlim(xmin=2.8, xmax=4.2)
            plt.text(3.6, -0.03, "Depth of MORB" + "\n" + "Override: " + str(thevalue) + " km", withdash=False)
            plt.grid()
            plt.legend(loc='lower right')
            plt.title(graphtitle2 + " [(Delta Rho / BSP Rho) vs BSP Rho]")
            #plt.show()
            plt.savefig(str(graphtitle2 + "_deltarhograph.png"), format='png')
            plt.close()
            movethisfile = graphtitle2 + "_deltarhograph.png"
            if movethisfile in os.listdir(home_dir_list[0] + "/Delta_Rho_CSV_Outputs"):
                fdir = home_dir_list[0] + "/Delta_Rho_CSV_Outputs/" + movethisfile
                tdir = home_dir_list[0] + "/Delta_Rho_Plots/" + movethisfile
                shutil.move(fdir, tdir)
                print "\n" + "*******************************"
                print movethisfile + " is now in 'Delta_Rho_Plots' directory!"
                print "*******************************" + "\n"
            else:
                print movethisfile + " not found in the directory!"
                pass
            os.chdir(home_dir_list[0] + "/hefesto_fort.58_bsp_outputs\CSV_Formatted")
        else:
            print "Problem with file: " + str(fileclipped)
            pass
    combinedfile.close()
    combined_bsp_rho_file.close()
    combined_deltarho_file.close()
    combinedfile_name = "Combined_All_File.csv"
    combined_bsp_rho_name = "Combined_BSPRho_File.csv"
    combined_deltarho_name = "Combined_DeltaRho_File.csv"
    combined_depth_file = "Combined_Depth_File.csv"
    if combinedfile_name in os.listdir(home_dir_list[0] + "/hefesto_fort.58_morb_outputs/CSV_Formatted"):
        fdir2 = home_dir_list[0] + "/hefesto_fort.58_morb_outputs/CSV_Formatted/" + combinedfile_name
        tdir2 = home_dir_list[0] + "/" + combinedfile_name
        shutil.move(fdir2, tdir2)
        print "\n" + "Comprehensive output files from calculations now available " \
              "in directory 'HeFESToPlot'" + "\n"
    else:
        pass
    if combined_bsp_rho_name in os.listdir(home_dir_list[0] + "/hefesto_fort.58_morb_outputs/CSV_Formatted"):
        fdir3 = home_dir_list[0] + "/hefesto_fort.58_morb_outputs/CSV_Formatted/" + combined_bsp_rho_name
        tdir3 = home_dir_list[0] + "/" + combined_bsp_rho_name
        shutil.move(fdir3, tdir3)
    else:
        pass
    if combined_deltarho_name in os.listdir(home_dir_list[0] + "/hefesto_fort.58_morb_outputs/CSV_Formatted"):
        fdir4 = home_dir_list[0] + "/hefesto_fort.58_morb_outputs/CSV_Formatted/" + combined_deltarho_name
        tdir4 = home_dir_list[0] + "/" + combined_deltarho_name
        shutil.move(fdir4, tdir4)
        print "\n" + "Output files from calculation [(Morb_Rho/BSP_Rho)/BSP_Rho] now available " \
              "in directory 'HeFESToPlot'" + "\n"
    else:
        pass
    if combined_depth_file in os.listdir(home_dir_list[0] + "/hefesto_fort.58_morb_outputs/CSV_Formatted"):
        fdir5 = home_dir_list[0] + "/hefesto_fort.58_morb_outputs/CSV_Formatted/" + combined_depth_file
        tdir5 = home_dir_list[0] + "/" + combined_depth_file
        shutil.move(fdir5, tdir5)
    else:
        pass
    if os.path.exists(home_dir_list[0] + "/Delta_Rho_CSV_Outputs"):
        dir1 = home_dir_list[0] + "/Delta_Rho_CSV_Outputs"
        dir2 = home_dir_list[0] + "/Delta_Rho_Plots/Delta_Rho_CSV_Outputs"
        shutil.move(dir1, dir2)
    else:
        pass
    ploterror()



def ploterror():
    print "\n" + "Creating percent error plots and comprehensive percent error output file..." + "\n"
    os.chdir(home_dir_list[0])
    erroroutput = open("Error_Calculations.csv", "a")
    os.chdir(home_dir_list[0] + "/hefesto_fort.58_bsp_outputs\CSV_Formatted")
    for filename in os.listdir(home_dir_list[0] + "/hefesto_fort.58_bsp_outputs\CSV_Formatted"):
        print "\n" + "___________________________________________________________________" + "\n"
        graphtitletemp2 = str(filename)[:-29]
        graphtitle2 = str(graphtitletemp2)[16:]
        print "\n" + "********************************"
        print "PROCESSING PLANET: " + str(graphtitle2) + "..."
        print "********************************" + "\n"
        print "\n" + "Found '" + str(filename)[:-4] + "' in BSP directory..."
        graphtitletemp = str(filename)[:-28]
        graphtitle = str(graphtitletemp)[7:]
        fileclipped = str(filename)[:-28] + "morb.txt_morb_csvformatted.csv"
        if fileclipped in os.listdir(home_dir_list[0] + "/hefesto_fort.58_morb_outputs\CSV_Formatted"):
            print "\n" + "Found '" + str(filename)[:-4] + "' in MORB directory..."
            os.chdir(home_dir_list[0] + "/hefesto_fort.58_bsp_outputs\CSV_Formatted")
            bsp_rho = np.loadtxt(filename, delimiter=",", usecols=[1])
            os.chdir(home_dir_list[0] + "/hefesto_fort.58_morb_outputs\CSV_Formatted")
            morb_rho = np.loadtxt(fileclipped, delimiter=",", usecols=[1])
            diff_bsp = map(operator.sub, bsp_rho, mcdonough_bse_rho)
            diff_morb = map(operator.sub, morb_rho, gale_morb_rho)
            error_bsp = map(truediv, diff_bsp, mcdonough_bse_rho)
            error_morb = map(truediv, diff_morb, gale_morb_rho)
            reformatted_diff_bsp = []
            reformatted_diff_morb = []
            reformatted_diff_bsp.append(str(graphtitle2))
            reformatted_diff_bsp.append("BSP:")
            reformatted_diff_morb.append("----")
            reformatted_diff_morb.append("MORB:")
            bspedit = ",".join(str(i) for i in error_bsp)
            morbedit = ",".join(str(i) for i in error_morb)
            reformatted_diff_bsp.append(bspedit)
            reformatted_diff_morb.append(morbedit)
            reformatted_diff_bsp2 = ",".join(str(i) for i in reformatted_diff_bsp)
            reformatted_diff_morb2 = ",".join(str(i) for i in reformatted_diff_morb)
          #  for i in error_bsp:
           #     reformatted_diff_bsp.append(i)
          #  reformatted_diff_morb.append("----, MORB:")
      #      for i in error_morb:
       #         reformatted_diff_morb.append(i)
            print "\n" + "Printing BSP percent error..." + "\n"
            print error_bsp
            print "\n" + "Printing MORB percent error..." + "\n"
            print error_morb
            font = {'weight' : 'bold',
                    'size' : 14}
            matplotlib.rc('font', **font)
            plt.plot(depth_trans_zone, error_bsp, '-b', label="BSP Error", linewidth=2)
            plt.plot(depth_trans_zone, error_morb, '-r', label="MORB Error", linewidth=2)
            plt.hlines(0, 1, 574, colors="k", linestyle="dashed",  linewidth=3)
            plt.xlabel("Depth")
            plt.ylabel("Percent Error")
            plt.grid()
            plt.legend(loc='upper right')
            plt.title(graphtitle2 + " Error")
            #plt.show()
            plt.savefig(str(graphtitle2) + "_error.png", format='png')
            plt.close()
            time.sleep(.02)
            graphname = str(graphtitle2) + "_error.png"
            if graphname in os.listdir(home_dir_list[0] + "/hefesto_fort.58_morb_outputs\CSV_Formatted"):
                fdir = home_dir_list[0] + "/hefesto_fort.58_morb_outputs/CSV_Formatted/" + graphname
                tdir = home_dir_list[0] + "/Error_Plots/" + graphname
                shutil.move(fdir, tdir)
                print "\n" + graphname + " now available in 'Error_Plots' directory!" + "\n"
            else:
                print "\n" + graphname + " not found!"
                pass
            os.chdir(home_dir_list[0])
            erroroutput.write("%s\n%s\n" % (reformatted_diff_bsp2, reformatted_diff_morb2))
        else:
            print "Error handling files for star: " + graphtitle2 + " ..."
    erroroutput.close()
    exitscript()










def exitscript():
    DIRR = home_dir_list[0] + "/BSP_vs_Rho_Plots"
    number_plots = len(os.walk(DIRR).next()[2])
    print "\n" + "Finished with automated plotting.  There are " + str(number_plots) + " simulated planets with plots!  Exiting script..." + "\n" + "\n" + "\n" + "____________________________________"


initialization()
