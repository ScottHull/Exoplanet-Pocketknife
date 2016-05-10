#!/usr/bin/env python

import os, xlrd, xlwt, shutil, subprocess, time, traceback, csv
from subprocess import Popen, PIPE
from glob import glob
from threading import Timer



home_dir_list = []
home_dir_list.append(os.getcwd())


def checkforalphamelts():
    try:
        if not os.path.isfile("run_alphamelts.command"):
            print "WARNING: alphaMELTS not detected in the working directory.  This program will not function properly." + "\n"
            initialization()
        else:
            print "alphaMELTS detected!  Happy calculating!" + "\n"
            initialization()
    except:
        pass




def bspormorb():
    try:
        print "\n" + "Would you like to calculate exoplanet bulk silicate planet (bsp) or exoplanet mid-ocean ridge basalt (morb)?" + "\n"
        thischoice = raw_input("Please enter either 'bsp' or 'morb': ")
        if thischoice == "bsp":
            bsp_writefiles()
        elif thischoice == "morb":
            morb_writefiles()
        else:
            print "Oops!  That's not a valid command."
            initialization()
            pass
    except:
        pass




#----------------



print "\n"
print "\n"
print "\n"
print "\n"
print "\n"
print "\n"
print "\n"
print "\n"
print "\n"
print "\n"
print "\n"
print "\n"
print "\n"
print "\n"
print "\n"
print "\n"
print "\n"
print "If you have not already done so, please place this file in directory: home_dir_list[0] + ''" + "\n"
checkforalphamelts()
print "Welcome to the AutoMELTS.  Enter 'begin' to launch the alphaMELTS automation process..." + "\n"



#-----------------





def initialization():
    """

    :rtype :
    """
    first_choice = raw_input("Please enter 'begin': ")
    if first_choice == "begin":
        bspormorb()
    else:
        print "Oops!  That's not a valid command."
        initialization()



def bsp_writefiles():
    try:
        if not os.path.exists(home_dir_list[0] + '/BSP_MELTS_Files'):
            os.mkdir(home_dir_list[0] + '/BSP_MELTS_Files')
        else:
            print "\n"
            print "'BSP_MELTS_Files' directory already exists.  Deleting and recreating..." + "\n"
            shutil.rmtree('BSP_MELTS_Files')
            os.mkdir(home_dir_list[0] + '/BSP_MELTS_Files')
        os.path.join(home_dir_list[0] + '/BSP_MELTS_Files')
        print "\n"
        xl_workbook = xlrd.open_workbook(raw_input("Please enter your .xlsx workbook name: "), 'rb')
        print "Opening workbook..."
        sheet_names = xl_workbook.sheet_names()
        print ('Sheet Names', sheet_names)
        xl_sheet = xl_workbook.sheet_by_index(0)
        print ('Sheet name: %s' % xl_sheet.name)
        print "\n"
        num_cols = xl_sheet.ncols
        print "Writing MELTS files..."
        for j in range(xl_sheet.nrows):
            row = xl_sheet.row(j)
            #print row
            file_name = str(row[0].value)
            file_name_clipped = file_name[7:]
            melts_file = open('BSP_MELTS_Files/'+file_name_clipped.rstrip()+ '.MELTS', 'w')
            print "Writing MELTS file: " + str(file_name_clipped) + " ..."
            for i in range(num_cols):
                melts_file.write(str(row[i].value)+'\n')
            melts_file.close()
    except:
        print "Error!  Unable to write MELTS files."
        initialization()
    print "\n"
    print "MELTS files have been written.  Moving on to BSP calculations..."
    print "\n"
    run_bsp()



def run_bsp():
    try:
        if not os.path.exists(home_dir_list[0] + "/Completed_BSP_MELTS_Files"):
            print "Creating directory: 'Completed_BSP_MELTS_Files'"
            os.mkdir(home_dir_list[0] + "/Completed_BSP_MELTS_Files")
        else:
            print "\n" + "'Completed_BSP_MELTS_Files' directory already exists.  Deleting and recreating..." + "\n"
            shutil.rmtree(home_dir_list[0] + "/Completed_BSP_MELTS_Files")
            os.mkdir(home_dir_list[0] + "/Completed_BSP_MELTS_Files")
    except:
        pass
    firstdir = home_dir_list[0] + "/BSP_Env_File"
    seconddir = home_dir_list[0] + "/BSP_MELTS_Files/BSP_Env_File"
    os.chdir(home_dir_list[0] + "/BSP_MELTS_Files")
    shutil.copy(firstdir, seconddir)
    working_dir = bhome_dir_list[0] + '/BSP_MELTS_Files'
    os.chdir(home_dir_list[0] + "/BSP_MELTS_Files")
    working_dir = bhome_dir_list[0] + '/BSP_MELTS_Files'
    def automate_bsp():
        for filename in glob(b"*.MELTS"):
            print "\n" + "**************************"
            print("Performing calculations on {filename!r}...".format(**vars()))
            print "**************************" + "\n"
            try:
                os.path.join(home_dir_list[0] + "")
                os.remove("alphaMELTS_tbl.txt")
                os.path.join(home_dir_list[0] + "/BSP_MELTS_Files")
                os.remove("alphaMELTS_tbl.txt")
            except OSError:
                print "\n" + "'alphaMELTS_tbl.txt' not in directory.  Can proceed with calculations..." + "\n"
                pass
            try:
                time.sleep(3)
                print "\n"
                print "Opening the alphaMELTS algorithm..."
                print "\n"
                p = Popen(["run_alphamelts.command", "-f", "BSP_Env_File"], cwd=working_dir, stdin=PIPE)
                print "\n" + "Timeout counter started.  200 seconds until the loop continues..." + "\n"
                t = Timer(200, p.kill)
                t.start()
                #p.communicate(input=b"\n".join([b"1", str(filename), b"8", b"alloy-liquid", b"0", b"x", b"5", b"3", b"+0.4", b"2", b"1400", b"10000", b"10", b"1", b"3", b"1", b"liquid", b"1", b"0.07", b"0", b"10", b"0", b"4", b"0"])) #these are alphamelts settings
                p.communicate(input=b"\n".join([b"1", str(filename), b"8", b"alloy-liquid", b"0", b"x", b"5", b"4", b"-1.5", b"2", b"2500", b"4200", b"4", b"1", b"0"]))
                #1 = enter MELTS file, str(filename) = enters file from directory, 8 = suppress phase, alloy-liquid = liquid alloy phase
                #0 = suppress (for stability of the program), x = exit phase suppression, 5 = select fO2, 4 = iron-wustite buffer
                #-1.6 = -1.6 log units below buffer, 4 = equilibriate, 0 = exit alphaMELTS
                t.cancel()
                print "Timeout timer cancelled..." + "\n"
                time.sleep(2)
                print "\n" + "Writing output to 'Completed_BSP_MELTS_Files' directory..." + "\n"
                oldname = "alphaMELTS_tbl.txt"
                newname = str(filename) + "_BSP_OUTPUT" + ".bsp"
                os.rename(oldname, newname)
                shutil.copy(newname, home_dir_list[0] + "/Completed_BSP_MELTS_Files")
                print "_____________________________________________________________"
            except Exception:
                traceback.print_exc()
                print "\n"
                print "Calculation failure.  alphaMELTS failed to run properly." + "\n" + \
                      "Output file may not have been written." + "\n" + "Moving on..." + "\n"
        else:
            print "There doesn't seem to be any MELTS files in the working directory.  They should end with a '.MELTS' extension."
            print "\n"
            print "Done with BSP calculations.  Moving on..."
            print "\n"
    automate_bsp()
    dataparse_bsp()





def morb_writefiles():
    try:
        if not os.path.exists(home_dir_list[0] + '/MORB_MELTS_Files'):
            os.mkdir(home_dir_list[0] + '/MORB_MELTS_Files')
        else:
            print "\n"
            print "'MORB_MELTS_Files' directory already exists.  Deleting and recreating..." + "\n"
            shutil.rmtree('MORB_MELTS_Files')
            os.mkdir(home_dir_list[0] + '/MORB_MELTS_Files')
        os.path.join(home_dir_list[0] + '/MORB_MELTS_Files')
        print "\n"
        xl_workbook = xlrd.open_workbook(raw_input("Please enter your .xlsx workbook name: "), 'rb')
        print "Opening workbook..."
        sheet_names = xl_workbook.sheet_names()
        print ('Sheet Names', sheet_names)
        xl_sheet = xl_workbook.sheet_by_index(0)
        print ('Sheet name: %s' % xl_sheet.name)
        print "\n"
        num_cols = xl_sheet.ncols
        print "Writing MELTS files..."
        for j in range(xl_sheet.nrows):
            row = xl_sheet.row(j)
            #print row
            file_name = str(row[0].value)
            file_name_clipped = file_name[7:]
            melts_file = open('MORB_MELTS_Files/'+file_name_clipped.rstrip()+ '.MELTS', 'w')
            print "Writing MELTS file: " + str(file_name_clipped) + " ..."
            for i in range(num_cols):
                melts_file.write(str(row[i].value)+'\n')
            melts_file.close()
    except:
        print "Error!  Unable to write MELTS files."
        initialization()
    print "\n"
    print "MELTS files have been written.  Moving on to MORB calculations..."
    print "\n"
    run_morb()





def run_morb():
    try:
        if not os.path.exists(home_dir_list[0] + "/Completed_MORB_MELTS_Files"):
            print "Creating directory: 'Completed_MORB_MELTS_Files'"
            os.mkdir(home_dir_list[0] + "/Completed_MORB_MELTS_Files")
        else:
            print "\n" + "'Completed_MORB_MELTS_Files' directory already exists.  Deleting and recreating..." + "\n"
            shutil.rmtree(home_dir_list[0] + "/Completed_MORB_MELTS_Files")
            os.mkdir(home_dir_list[0] + "/Completed_MORB_MELTS_Files")
    except:
        pass
    firstdir = home_dir_list[0] + "/MORB_Env_File"
    seconddir = home_dir_list[0] + "/MORB_MELTS_Files/MORB_Env_File"
    os.chdir(home_dir_list[0] + "/MORB_MELTS_Files")
    shutil.copy(firstdir, seconddir)
    working_dir = bhome_dir_list[0] + '/MORB_MELTS_Files'
    os.chdir(home_dir_list[0] + "/MORB_MELTS_Files")
    working_dir = bhome_dir_list[0] + '/MORB_MELTS_Files'
    def automate_morb():
        for filename in glob(b"*.MELTS"):
            print "\n" + "**************************"
            print("Performing calculations on {filename!r}...".format(**vars()))
            print "**************************" + "\n"
            try:
                os.path.join(home_dir_list[0] + "")
                os.remove("alphaMELTS_tbl.txt")
                os.path.join(home_dir_list[0] + "/MORB_MELTS_Files")
                os.remove("alphaMELTS_tbl.txt")
            except OSError:
                print "\n" + "'alphaMELTS_tbl.txt' not in directory.  Can proceed with calculations..." + "\n"
                pass
            try:
                time.sleep(3)
                print "\n"
                print "Opening the alphaMELTS algorithm..."
                print "\n"
                p = Popen(["run_alphamelts.command", "-f", "MORB_Env_File"], cwd=working_dir, stdin=PIPE)
                print "\n" + "Timeout counter started.  200 seconds until the loop continues..." + "\n"
                t = Timer(200, p.kill)
                t.start()
                p.communicate(input=b"\n".join([b"1", str(filename), b"8", b"alloy-liquid", b"0", b"x", b"5", b"3", b"+0.4", b"2", b"1400", b"10000", b"10", b"1", b"3", b"1", b"liquid", b"1", b"0.07", b"0", b"10", b"0", b"4", b"0"])) #these are alphamelts settings
                #p.communicate(input=b"\n".join([b"1", str(filename), b"8", b"alloy-liquid", b"0", b"x", b"5", b"4", b"-1.5", b"2", b"2500", b"4200", b"4", b"1", b"0"]))
                #1 = enter MELTS file, str(filename) = enters file from directory, 8 = suppress phase, alloy-liquid = liquid alloy phase
                #0 = suppress (for stability of the program), x = exit phase suppression, 5 = select fO2, 4 = iron-wustite buffer
                #-1.6 = -1.6 log units below buffer, 4 = equilibriate, 0 = exit alphaMELTS
                t.cancel()
                print "Timeout timer cancelled..." + "\n"
                time.sleep(2)
                print "\n" + "Writing output to 'Completed_MORB_MELTS_Files' directory..." + "\n"
                oldname = "alphaMELTS_tbl.txt"
                newname = str(filename) + "_MORB_OUTPUT" + ".morb"
                os.rename(oldname, newname)
                shutil.copy(newname, home_dir_list[0] + "/Completed_MORB_MELTS_Files")
                print "_____________________________________________________________"
            except Exception:
                traceback.print_exc()
                print "\n"
                print "Calculation failure.  alphaMELTS failed to run properly." + "\n" + \
                      "Output file may not have been written." + "\n" + "Moving on..." + "\n"
        else:
            print "There doesn't seem to be any MELTS files in the working directory.  They should end with a '.MELTS' extension."
            print "\n"
            print "Done with MORB calculations.  Moving on..."
            print "\n"
    automate_morb()
    dataparse_morb()







def dataparse_bsp():
    print "Creating '.csv' formatted files..." + "\n"
    os.chdir(home_dir_list[0] + "/Completed_BSP_MELTS_Files")
    for filez in glob("*.bsp"):
        os.chdir(home_dir_list[0] + "/Completed_BSP_MELTS_Files")
        csv_file_name = filez[:-4] + "_CSVformat" + ".csv"
        with open(filez, "rb") as infile, open(csv_file_name, "wb") as outfile:
            in_txt = csv.reader(infile, delimiter = " ")
            out_csv = csv.writer(outfile)
            out_csv.writerows(in_txt)
    os.chdir(home_dir_list[0] + "/Completed_BSP_MELTS_Files")
    try:
        if not os.path.exists(home_dir_list[0] + "/Completed_BSP_Files/CSV_Formatted"):
            print "Creating directory: 'CSV_Formatted'"
            os.mkdir(home_dir_list[0] + "/Completed_BSP_MELTS_Files/CSV_Formatted")
        else:
            print "\n" + "'CSV_Formatted' directory in 'Completed_BSP_MELTS_Files' already exists.  " \
                         "Deleting and recreating..." + "\n"
            shutil.rmtree(home_dir_list[0] + "/Completed_BSP_MELTS_Files/CSV_Formatted")
            os.mkdir(home_dir_list[0] + "/Completed_BSP_MELTS_Files/CSV_Formatted")
    except:
        pass
    for file in glob("*.csv"):
        shutil.copy(file, home_dir_list[0] + "/Completed_BSP_MELTS_Files/CSV_Formatted")
    print "\n" + "CSV formatted files now available in directory 'CSV_Formatted.'"   \
                 "Cleaning 'Completed_BSPt_MELTS_Files'..." + "\n"
    print "Calculations and file management complete.  Exiting script.  Thank you!" + "\n"
    print "_____________________________________________________________"
    print "\n" + "\n" + "\n" + "\n"
    os.chdir(home_dir_list[0] + "/Completed_BSP_MELTS_Files")
    for file in glob("*.csv"):
        os.remove(file)




def dataparse_morb():
    print "Creating '.csv' formatted files..." + "\n"
    os.chdir(home_dir_list[0] + "/Completed_MORB_MELTS_Files")
    for filez in glob("*.morb"):
        os.chdir(home_dir_list[0] + "/Completed_MORB_MELTS_Files")
        csv_file_name = filez[:-4] + "_CSVformat" + ".csv"
        with open(filez, "rb") as infile, open(csv_file_name, "wb") as outfile:
            in_txt = csv.reader(infile, delimiter = " ")
            out_csv = csv.writer(outfile)
            out_csv.writerows(in_txt)
    os.chdir(home_dir_list[0] + "/Completed_MORB_MELTS_Files")
    try:
        if not os.path.exists(home_dir_list[0] + "/Completed_MORB_Files/CSV_Formatted"):
            print "Creating directory: 'CSV_Formatted'"
            os.mkdir(home_dir_list[0] + "/Completed_MORB_MELTS_Files/CSV_Formatted")
        else:
            print "\n" + "'CSV_Formatted' directory in 'Completed_MORB_MELTS_Files' already exists.  " \
                         "Deleting and recreating..." + "\n"
            shutil.rmtree(home_dir_list[0] + "/Completed_MORB_MELTS_Files/CSV_Formatted")
            os.mkdir(home_dir_list[0] + "/Completed_MORB_MELTS_Files/CSV_Formatted")
    except:
        pass
    for file in glob("*.csv"):
        shutil.copy(file, home_dir_list[0] + "/Completed_MORB_MELTS_Files/CSV_Formatted")
    print "\n" + "CSV formatted files now available in directory 'CSV_Formatted.'"   \
                 "Cleaning 'Completed_MORBt_MELTS_Files'..." + "\n"
    print "Calculations and file management complete.  Exiting script.  Thank you!" + "\n"
    print "_____________________________________________________________"
    print "\n" + "\n" + "\n" + "\n"
    os.chdir(home_dir_list[0] + "/Completed_MORB_MELTS_Files")
    for file in glob("*.csv"):
        os.remove(file)





initialization()
