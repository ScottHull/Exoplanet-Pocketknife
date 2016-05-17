import os, shutil, time, bisect, string
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import operator
from operator import truediv
from scipy import integrate




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

simple_earth_morb = [2.89708, 2.92792, 2.94455, 3.04297, 3.17487, 3.19574, 3.25329, 3.36196, 3.37489, 3.38665, 3.39781,
                     3.40855, 3.43322, 3.4435, 3.45364, 3.46287, 3.47109, 3.47896, 3.4865, 3.49376, 3.50079, 3.50761,
                     3.51426, 3.52077, 3.52715, 3.53344, 3.53963, 3.54574, 3.55179, 3.55777, 3.56371, 3.5696, 3.57545,
                     3.58126, 3.58704, 3.59279, 3.66547, 3.67112, 3.67676, 3.68238, 3.68799, 3.69359, 3.69919, 3.70479,
                     3.71039, 3.71601, 3.72163, 3.72728, 3.73294, 3.73864, 3.74438, 3.75015, 3.75598, 3.76188, 3.76784,
                     3.77389, 3.78003, 3.78629, 3.79267, 3.79921, 3.80591, 3.8128, 3.81991, 3.82728, 3.83492, 3.84288,
                     3.85119,3.85991, 3.86906, 3.8787, 3.88887, 3.89961, 3.91094, 3.9229, 3.9355, 3.94971, 3.97115,
                     3.99127, 4.01053, 4.02931, 4.04793]

simple_earth_integrated_deltarho = [0, -0.457983511, -1.542959736, -2.177855918, -2.446160257, -2.555639127,
                                    -2.593449716, -2.459027679, -2.201137325, -1.932684051, -1.662998873, -1.401128917,
                                    -1.126137423, -0.835773866, -0.5444199, -0.250626327, 0.044889365, 0.339409207,
                                    0.633158702, 0.925934849, 1.217941505, 1.508231893, 1.797041022, 2.084642134,
                                    2.369407199, 2.650909376, 2.930621348, 3.208478061, 3.484458448, 3.754876934,
                                    4.020854231, 4.284582678, 4.546773448, 4.806697514, 5.06504398, 5.320392154,
                                    5.642959826, 6.033233158, 6.421119968, 6.80656509, 7.188975288, 7.567233107,
                                    7.931961546, 8.288728407, 8.638470139, 8.985415545, 9.329397436, 9.670197468,
                                    10.00751567, 10.34141464, 10.6704125, 10.99423977, 11.31189257, 11.62204921,
                                    11.92161156, 12.14372919, 12.26304297, 12.34066184, 12.40796738, 12.47135312,
                                    12.5315898, 12.5887274, 12.64124724, 12.69212081, 12.74149886, 12.79053983,
                                    12.84320916, 12.90275642, 12.96990528, 13.04315801, 13.12374276, 13.21405196,
                                    13.31503122, 13.42767175, 13.54955334, 13.67155013, 13.79110142, 13.92154482,
                                    14.07377004, 14.25071685, 14.45151495]


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
        #integrated_density()
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
    else:
        pass
    if "Error_Calculations.csv" in os.listdir(home_dir_list[0]):
        os.remove(home_dir_list[0] + "/Error_Calculations.csv")
    else:
        pass
    if "Integrated_DeltaRho.png" in os.listdir(home_dir_list[0]):
        os.remove("Integrated_DeltaRho.png")
    else:
        pass
    if "BasaltEclogite_Prob_File.csv" in os.listdir(home_dir_list[0]):
        os.remove("BasaltEclogite_Prob_File.csv")
    else:
        pass
    if "Combined_DeltaRho_Integrated_File.csv" in os.listdir(home_dir_list[0]):
        os.remove("Combined_DeltaRho_Integrated_File.csv")
    else:
        pass
    if "Max_Integrated_DeltaRho_Value.csv" in os.listdir(home_dir_list[0]):
        os.remove("Max_Integrated_DeltaRho_Value.csv")
    else:
        pass
    print "\n" + "\n" + "Beginning BSP Output File Parsing..." + "\n"
    time.sleep(2)
    print "\n" + "Creating 'Depth_vs_Rho_Plots' directory.." + "\n"
    if not os.path.exists(home_dir_list[0] + "/Depth_vs_Rho_Plots"):
        os.mkdir(home_dir_list[0] + "/Depth_vs_Rho_Plots")
    else:
        shutil.rmtree(home_dir_list[0] + "/Depth_vs_Rho_Plots")
        os.mkdir(home_dir_list[0] + "/Depth_vs_Rho_Plots")
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
    if not os.path.exists(home_dir_list[0] + "/MORB_Minus_BSP_Outputs"):
        os.mkdir(home_dir_list[0] + "/MORB_Minus_BSP_Outputs")
    else:
        shutil.rmtree(home_dir_list[0] + "/MORB_Minus_BSP_Outputs")
        os.mkdir(home_dir_list[0] + "/MORB_Minus_BSP_Outputs")
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
                delta_rho_filename = str(graphtitle2)+"_morbminusbsp.csv"
                deltarho_rows = map(operator.sub, morb_depth_list, bsp_depth_list)
                try:
                    with open(delta_rho_filename, "wb") as fp:
                        for x in zip(*deltarho_rows):
                            fp.write("{0}\n".format(*x))
                        fp.close()
                except:
                    pass
                #time.sleep(0.5)
                fdir = home_dir_list[0] + "/hefesto_fort.58_morb_outputs/CSV_Formatted/" + delta_rho_filename
                gdir = home_dir_list[0] + "/MORB_Minus_BSP_Outputs/" + delta_rho_filename
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
                plt.plot(depth_trans_zone, mcdonough_bse_rho, 'b', linestyle="--", label="McD2014 BSP", linewidth=3.0)
                plt.plot(depth_trans_zone, gale_morb_rho, 'b', label="Gale2013 MORB", linewidth=3.0)
                plt.plot(depth_trans_zone, simple_earth_bsp, 'g', linestyle="--", label="SEM BSP", linewidth=3.0)
                plt.plot(depth_trans_zone, simple_earth_morb, 'g', label="SEM MORB", linewidth=3.0)
                plt.plot(bsp_rho_data, bsp_depth, '-r', linestyle="--", label="Exo-BSP", linewidth=3.0)
                plt.plot(morb_data,morb_depth, "-r", label="Exo-MORB", linewidth=3.0)
                plt.ylabel("Density (g/cc)")
                plt.xlabel("Depth (km)")
                plt.title(str(graphtitle2))
                plt.legend(loc='lower right')
                plt.xlim(xmax=573.68)
                plt.grid()
                plt.savefig(str(graphtitle2 + ".png"), format='png')
                plt.close()
                #plt.show()
                if str(graphtitle2) + ".png" in os.listdir(home_dir_list[0] + "/hefesto_fort.58_morb_outputs/CSV_Formatted"):
                    zdir = home_dir_list[0] + "/hefesto_fort.58_morb_outputs/CSV_Formatted/" + str(graphtitle2) + ".png"
                    tdir = home_dir_list[0] + "/Depth_vs_Rho_Plots/" + str(graphtitle2) + ".png"
                    shutil.move(zdir, tdir)
                    print "\n" + "****************************"
                    print str(graphtitle2) + ".png is available in 'Depth_vs_Rho_Plots' directory..."
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
    integrated_listoflists = []
    combinedfile = open("Combined_All_File.csv", "a")
    combined_deltarho_file = open("Combined_DeltaRho_File.csv", "a")
    combined_bsp_rho_file = open("Combined_BSPRho_File.csv", "a")
    combined_depth_file = open("Combined_Depth_File.csv", "a")
    os.chdir(home_dir_list[0] + "/hefesto_fort.58_bsp_outputs\CSV_Formatted")
    for filename in os.listdir(home_dir_list[0] + "/hefesto_fort.58_bsp_outputs/CSV_Formatted"):
        print "\n" + "___________________________________________________________________" + "\n"
        graphtitletemp2 = str(filename)[:-29]
        graphtitle2 = str(graphtitletemp2)[16:]
        graphtitletemp = str(filename)[:-28]
        graphtitle = str(graphtitletemp)[7:]
        fileclipped = graphtitle2+"_morbminusbsp.csv"
        print "\n" + "*******************************"
        print "Processing Planet: " + graphtitle2 + "..."
        print "*******************************" + "\n"
        print "\n" + "Found '"+str(filename)[:-4] + "' in BSP directory..."
        #bsp_rho_list = np.genfromtxt(filename, delimiter=",", usecols=[1], autostrip=True, converters={lambda s: float(s or 0)})
        #thedepths = np.loadtxt(filename, delimiter=",", usecols=[0])
        if fileclipped in os.listdir(home_dir_list[0] + "/MORB_Minus_BSP_Outputs"):
            os.chdir(home_dir_list[0] + "/hefesto_fort.58_bsp_outputs/CSV_Formatted")
            bsp_rho_list = np.genfromtxt(filename.strip(), delimiter=",", usecols=[1], autostrip=True, dtype=float)
            thedepths = np.genfromtxt(filename.strip(), delimiter=",", usecols=[0], autostrip=True, dtype=float)
            os.chdir(home_dir_list[0] + "\MORB_Minus_BSP_Outputs")
            with open(fileclipped) as z:
                if len(z.readlines()) >= 81:
                    z.close()
                    #try:
                    print "\n" + "Found files for star '" + str(graphtitle2) + "' in BSP/delta rho directories!"
                    print "Found file: '" + str(fileclipped) + "' ..."
                    print "Found file: '" + str(filename) + "' ..." + "\n"
                    os.chdir(home_dir_list[0] + "/MORB_Minus_BSP_Outputs")
                    delta_rho = np.genfromtxt(fileclipped.strip(), dtype=float, delimiter=None, autostrip=True)
                    #delta_rho = pd.read_csv(fileclipped, usecols=[0], delimiter=",", dtype=float)
                    #delta_rho = np.genfromtxt(fileclipped, usecols=[0], autostrip=True, converters={lambda s: float(s or 0)})
                    deltarhovsbsprho = map(truediv, delta_rho, bsp_rho_list)
                    if str(graphtitle2) + ".png" in os.listdir(home_dir_list[0] + "/hefesto_fort.58_bsp_outputs\CSV_Formatted"):
                        os.remove(str(graphtitle2) + ".png")
                    else:
                        pass
                    print "\n" + "Printing delta rho values..." + "\n"
                    print delta_rho
                    print "\n" + "Printing bsp rho values..." + "\n"
                    print bsp_rho_list
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
                    reform_bsprho = ", ".join(str(i) for i in bsp_rho_list)
                    bsp_rho_outputs.append(reform_bsprho)
                    reform_bsp_rho_outputs = ", ".join(str(i) for i in bsp_rho_outputs)
                    bsp_rho_outputs2 = []
                    bsp_rho_outputs2.append(str(graphtitle2))
                    bsp_rho_outputs2.append(reform_bsprho)
                    reform_bsp_rho_outputs2 = ", ".join(str(i) for i in bsp_rho_outputs2)
                    greaterthanzero = bisect.bisect_right(deltarhovsbsprho, 0)
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
                    deltarhofile = open(str(graphtitle2) + "_deltarho.csv", 'wb')
                    deltarhofile.write(reform_outputs)
                    deltarhofile.close()
                    if str(graphtitle2) + "_deltarho.csv" in os.listdir(os.getcwd()):
                        dur1 = os.getcwd() + "/" + str(graphtitle2) + "_deltarho.csv"
                        dur2 = home_dir_list[0] + "/Delta_Rho_CSV_Outputs/" + str(graphtitle2) + "_deltarho.csv"
                        shutil.move(dur1, dur2)
                    else:
                        pass
                    line_deltarho_y1 = 0.0539198491061
                    line_deltarho_x1 = 0
                    line_deltarho_x2 = 6
                    font = {'weight' : 'bold',
                            'size' : 14}
                    matplotlib.rc('font', **font)
                    plt.plot(bsp_rho_list, deltarhovsbsprho, '-b', label="Delta Rho", linewidth=2)
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
                    if movethisfile in os.listdir(home_dir_list[0] + "/MORB_Minus_BSP_Outputs"):
                        fdir = home_dir_list[0] + "/MORB_Minus_BSP_Outputs/" + movethisfile
                        tdir = home_dir_list[0] + "/Delta_Rho_Plots/" + movethisfile
                        shutil.move(fdir, tdir)
                        print "\n" + "*******************************"
                        print movethisfile + " is now in 'Delta_Rho_Plots' directory!"
                        print "*******************************" + "\n"
                    else:
                        print movethisfile + " not found in the directory!"
                        pass
                    os.chdir(home_dir_list[0] + "/hefesto_fort.58_bsp_outputs\CSV_Formatted")
                    # except:
                    #     print "\nProblem with file: " + str(fileclipped) + ".  Small decimal or 0 value likely experienced...\n"
                    #     error_deltarho = str(graphtitle2) + ",ERROR!  SMALL DECIMAL OR 0 VALUE LIKELY EXPERIENCED!"
                    #     combined_deltarho_file.write("%s\n," % error_deltarho)
                    #     pass
                else:
                    print "\nProblem with file: " + str(fileclipped) + " ...\n"
                    pass
        else:
            print "\nProblem with file: " + str(fileclipped) + " ...\n"
            pass
    combinedfile.close()
    combined_bsp_rho_file.close()
    combined_deltarho_file.close()
    combined_depth_file.close()
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
    try:
        if os.path.exists(home_dir_list[0] + "/MORB_Minus_BSP_Outputs"):
            dir1 = home_dir_list[0] + "/MORB_Minus_BSP_Outputs"
            dir2 = home_dir_list[0] + "/Delta_Rho_Plots/MORB_Minus_BSP_Outputs"
            shutil.move(dir1, dir2)
        else:
            pass
    except:
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
            try:
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
                plt.xlim(xmax=573.68)
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
            except:
                print "\n" "Problem with file: " + str(graphtitle2) + ".  Likely got a very small or 0 value."
                err_error = str(graphtitle2) + ",ERROR!  LILEY GOT A VERY SMALL OR 0 VALUE!"
                erroroutput.write("%s\n" % err_error)
                pass
        else:
            print "Error handling files for star: " + graphtitle2 + " ..."
    erroroutput.close()
    integrated_density()


def integrated_density():
    integrated_output_file = open("Combined_DeltaRho_Integrated_File.csv", 'a')
    be_status_file = open("BasaltEclogite_Prob_File.csv", "a")
    max_integrated_output_file = open("Max_Integrated_DeltaRho_Value.csv", 'a')
    print "\n" + "___________________________________________________________________" + "\n"
    os.chdir(home_dir_list[0] + "/Delta_Rho_CSV_Outputs")
    if "Integrated_DeltaRho.png" in os.listdir(home_dir_list[0] + "/Delta_Rho_CSV_Outputs"):
        os.remove("Integrated_DeltaRho.png")
    else:
        pass
    integrated_listoflists_BEpositive = []
    integrated_listoflists_BEnegative = []
    integrated_listoflists_BEpositive_names = []
    integrated_listoflists_BEnegative_names = []
    simpleearth_deltarhomax = float(0.0539198491061)
    print "\n\n\n\n\nPerforming integration calculations as a function of depth...\n"
    time.sleep(1)
    if "temp.csv" in os.listdir(home_dir_list[0] + "/Delta_Rho_CSV_Outputs"):
        os.remove("temp.csv")
    else:
        pass
    for filename in os.listdir(home_dir_list[0] + "/Delta_Rho_CSV_Outputs"):
        graphtitle2 = str(filename)[:-13]
        thedata = np.genfromtxt(os.path.join(home_dir_list[0], "Combined_DeltaRho_File.csv"), delimiter=',', dtype=None, autostrip=True)
        for i in thedata:
            thedata2 = list(i)
            for y in thedata2:
                if y == graphtitle2:
                    success = ",\n".join(str(t) for t in thedata2)
                    with open("temp.csv", 'wb') as tempfile:
                        tempfile.write("%s" % success)
                        tempfile.close()
                    thedata_nonlist = np.genfromtxt("temp.csv", skip_header=True, dtype=None, autostrip=True)
                    thedata_almost = list(thedata_nonlist)
                    thedata3 = [float(i[:-1].strip()) for i in thedata_almost]
                    datacheck = []
                    for value in thedata3:
                        if value >= simpleearth_deltarhomax:
                            datacheck.append(0)
                        else:
                            datacheck.append(1)
                    if 0 in datacheck:
                        integrated_listoflists_BEpositive_names.append(str(y))
                        graphtitle2 = str(filename)[:-12]
                        print "\n" + "___________________________________________________________________" + "\n"
                        print "\n" + "*******************************"
                        print "Processing Planet: " + str(y) + "..."
                        print "*******************************" + "\n"
                        print "Planet " + str(y) + " is likely for a basalt-eclogite transition!\n"
                        integrated_delta_rho = integrate.cumtrapz(thedata3, x=depth_trans_zone, initial=0)
                        integrated_listoflists_BEpositive.append(integrated_delta_rho)
                        print "Printing delta rho values...\n"
                        print thedata3
                        print "\n"
                        print "Printing integrated delta rho values as a function of depth...\n"
                        print integrated_delta_rho
                        print "\n"
                        output1 = []
                        output1.append(str(y)+",POS")
                        output2 = ",".join(str(q) for q in integrated_delta_rho)
                        output1.append(output2)
                        output3 = ",".join(str(o) for o in output1)
                        integrated_output_file.write("%s\n" % output3)
                        stat1 = []
                        stat1.append(str(y)+",POS")
                        be_status_file.write("%s\n" % str(y))
                        int_numpy_list = np.array(integrated_delta_rho)
                        max_val = np.amax(int_numpy_list)
                        list1 = []
                        list1.append(str(y) + ",POS")
                        dat1 = str(max_val)
                        list1.append(dat1)
                        dat2 = ",".join(q for q in list1)
                        max_integrated_output_file.write("%s\n" % dat2)
                        print "The maximum integrated delta rho value obtained by planet " + str(y) + " is: " + dat1
                    else:
                        integrated_listoflists_BEnegative_names.append(str(y))
                        graphtitle2 = str(filename)[:-12]
                        print "\n" + "___________________________________________________________________" + "\n"
                        print "\n" + "*******************************"
                        print "Processing Planet: " + str(y) + "..."
                        print "*******************************" + "\n"
                        print "Planet " + str(y) + " is NOT likely for a basalt-eclogite transition!\n"
                        integrated_delta_rho = integrate.cumtrapz(thedata3, x=depth_trans_zone, initial=0)
                        integrated_listoflists_BEnegative.append(integrated_delta_rho)
                        print "Printing delta rho values...\n"
                        print thedata3
                        print "\n"
                        print "Printing integrated delta rho values as a function of depth...\n"
                        print integrated_delta_rho
                        print "\n"
                        output1 = []
                        output1.append(str(y)+",NEG")
                        output2 = ",".join(str(q) for q in integrated_delta_rho)
                        output1.append(output2)
                        output3 = ",".join(str(o) for o in output1)
                        integrated_output_file.write("%s\n" % output3)
                        stat1 = []
                        stat1.append(str(y)+",NEG")
                        be_status_file.write("%s\n" % str(y))
                        int_numpy_list = np.array(integrated_delta_rho)
                        max_val = np.amax(int_numpy_list)
                        list1 = []
                        list1.append(str(y) + ",NEG")
                        dat1 = str(max_val)
                        list1.append(dat1)
                        dat2 = ",".join(q for q in list1)
                        max_integrated_output_file.write("%s\n" % dat2)
                        print "The maximum integrated delta rho value obtained by planet " + str(y) + " is: " + dat1 + "\n"
                    time.sleep(1)
                    os.remove("temp.csv")
                else:
                    pass
    integrated_output_file.close()
    max_integrated_output_file.close()
    print "\n\n\n\n"
    print "\n" + "___________________________________________________________________" + "\n"
    print "Finished integrating...\n"
    be_fav = ", ".join(str(i) for i in integrated_listoflists_BEpositive_names)
    be_unfav = ", ".join(str(i) for i in integrated_listoflists_BEnegative_names)
    print "Planets LIKELY for basalt eclogite transition:"
    print be_fav
    print "\n"
    print "Planets UNLIKELY for basalt eclogite transition:"
    print be_unfav
    print "\n"
    print "Plotting integration results.  Please wait..."
    print "\n"
    font = {'weight' : 'bold',
            'size' : 14}
    matplotlib.rc('font', **font)
    plt.figure(num=1)
    dtz = np.array(depth_trans_zone)
    label_added = False
    for i in integrated_listoflists_BEnegative:
        z2 = np.array(i)
        # print z2.shape
        # print dtz.shape
        # print "______________________"
        if not label_added:
            plt.hold(True)
            plt.plot(dtz, z2, "r", linewidth=2, label="BE-trans unlikely")
            plt.hlines(0, 1, 574, colors="k", linestyle="dashed",  linewidth=3)
            plt.title("Integrated Delta Rho vs Depth")
            plt.ylabel("Integrated Delta Rho")
            plt.xlabel("Depth")
            plt.xlim(xmax=573.68)
            plt.grid()
            label_added = True
        else:
            plt.plot(dtz, z2, "r", linewidth=2)
    label_added = False
    for i in integrated_listoflists_BEpositive:
        z2 = np.array(i)
        if not label_added:
            plt.hold(True)
            plt.plot(dtz, z2, "b", linewidth=2, label="BE-trans likely")
            plt.hlines(0, 1, 574, colors="k", linestyle="dashed",  linewidth=2)
            plt.title("Integrated Delta Rho vs Depth")
            plt.ylabel("Integrated Delta Rho")
            plt.xlabel("Depth")
            plt.xlim(xmax=573.68)
            plt.grid()
            label_added = True
        else:
            plt.plot(dtz, z2, "b", linewidth=2)
    plt.plot(dtz, simple_earth_integrated_deltarho, "g", linewidth=3, label="Simple Earth")
    plt.hlines(0, 1, 574, colors="k", linestyle="dashed",  linewidth=2)
    plt.title("Integrated Delta Rho vs Depth")
    plt.ylabel("Integrated Delta Rho")
    plt.xlabel("Depth")
    plt.xlim(xmax=573.68)
    plt.grid()
    plt.legend(loc="upper left")
    plt.savefig("Integrated_DeltaRho.png", format='png')
    plt.close()
    if "Integrated_DeltaRho.png" in os.listdir(home_dir_list[0] + "/Delta_Rho_CSV_Outputs"):
        fdir1 = home_dir_list[0] + "/Delta_Rho_CSV_Outputs/Integrated_DeltaRho.png"
        fdir2 = home_dir_list[0] + "/Integrated_DeltaRho.png"
        shutil.move(fdir1, fdir2)
        print "'Integrated_DeltaRho.png' now available in directory: " + str(home_dir_list[0])
    else:
        pass
    if "Combined_DeltaRho_Integrated_File.csv" in os.listdir(home_dir_list[0] + "/Delta_Rho_CSV_Outputs"):
        fdir1 = home_dir_list[0] + "/Delta_Rho_CSV_Outputs/Combined_DeltaRho_Integrated_File.csv"
        fdir2 = home_dir_list[0] + "/Combined_DeltaRho_Integrated_File.csv"
        shutil.move(fdir1, fdir2)
        print "'Combined_DeltaRho_Integrated_File.csv' now available in directory: " + str(home_dir_list[0])
    else:
        pass
    exitscript()



def exitscript():
    DIRR = home_dir_list[0] + "/Depth_vs_Rho_Plots"
    number_plots = len(os.walk(DIRR).next()[2])
    print "\n" + "Finished with automated plotting.  There are " + str(number_plots) + " simulated planets with plots!"
    print "Please see directory " + str(home_dir_list[0]) + " for output files."
    print "Exiting script..." + "\n" + "\n" + "\n" + "____________________________________"


initialization()
