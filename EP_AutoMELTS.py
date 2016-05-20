#!/usr/bin/env python
import os, xlrd, shutil, subprocess, time, csv
from subprocess import Popen, PIPE
from glob import glob
from threading import Timer

home_dir_list = []
home_dir_list.append(os.getcwd())


def initialization():
    print("___________________________________________")
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print("___________________________________________\n")
    print "AutoMELTS v2.0"
    if not os.path.isfile("run_alphaMELTS.command"):
        print("\nWARNING!  ALPHAMELTS IS NOT DETECTED IN THE WORKING DIRECTORY!\n")
        pass
    else:
        print("ALPHAMELTS DETECTED!")
        pass
    if not os.path.isfile("BSP_Env_File"):
        print("\nWARNING!  BSP_ENV_FILE IS NOT DETECTED IN THE WORKING DIRECTORY!\n")
        pass
    else:
        print("BSP_ENV_FILE DETECTED!")
        pass
    if not os.path.isfile("MORB_Env_File"):
        print("\nWARNING!  MORB_ENV_FILE IS NOT DETECTED IN THE WORKING DIRECTORY!\n")
        pass
    else:
        print("MORB_ENV_FILE DETECTED!")
        pass
    print("\n\nWelcome to AutoMELTS for Python 3!\n")
    print("Would you like to perform 'bsp' or 'morb' calculations?\n")
    x1 = raw_input("Please enter 'bsp' or 'morb': ")
    if x1 == 'bsp':
        bsp_writefiles()
    elif x1 == 'morb':
        morb_writefiles()
    else:
        print("\nOops!  That's not a valid command!\n")
        initialization()



def bsp_writefiles():
    if not os.path.exists(home_dir_list[0] + "/BSP_MELTS_Files"):
        os.mkdir(home_dir_list[0] + "/BSP_MELTS_Files")
    else:
        shutil.rmtree(home_dir_list[0] + "/BSP_MELTS_Files")
        os.mkdir(home_dir_list[0] + "/BSP_MELTS_Files")
    if not os.path.exists(home_dir_list[0] + "/Completed_BSP_MELTS_Files"):
        os.mkdir(home_dir_list[0] + "/Completed_BSP_MELTS_Files")
    else:
        shutil.rmtree(home_dir_list[0] + "/Completed_BSP_MELTS_Files")
        os.mkdir(home_dir_list[0] + "/Completed_BSP_MELTS_Files")
    if "BSP_MELTS_Success_Log.csv" in os.listdir(home_dir_list[0]):
        os.remove("BSP_MELTS_Success_Log")
    else:
        pass
    if "MORB_MELTS_Success_Log.csv" in os.listdir(home_dir_list[0]):
        os.remove("MORB_MELTS_Success_Log")
    else:
        pass
    workbook = raw_input("Please enter your .xlsx workbook filename: ")
    if os.path.isfile(workbook):
        print("\n" + workbook + " has been found in the working directory!\n")
        dir1 = home_dir_list[0] + "/" + workbook
        dir2 = home_dir_list[0] + "/BSP_MELTS_Files/" + workbook
        shutil.copy(dir1, dir2)
        os.chdir(home_dir_list[0] + "/BSP_MELTS_Files/")
        pass
    else:
        print("\n" + workbook + " has NOT been found in the working directory!\n")
        bsp_writefiles()
    xl_workbook = xlrd.open_workbook(workbook)
    sheet_names = xl_workbook.sheet_names()
    xl_sheet = xl_workbook.sheet_by_index(0)
    num_cols = xl_sheet.ncols
    print("Writing BSP MELTS files...\n")
    for j in range(xl_sheet.nrows):
        row = xl_sheet.row(j)
        #print row
        file_name = str(row[0].value)
        file_name_clipped = file_name[7:]
        melts_file = open(file_name_clipped.rstrip()+ '.MELTS', 'w')
        print("Writing MELTS file for: " + str(file_name_clipped) + "...")
        for i in range(num_cols):
            melts_file.write(str(row[i].value)+'\n')
        melts_file.close()
    os.remove(workbook)
    print("\nAll BSP MELTS files have been written!\n")
    run_bsp()


def morb_writefiles():
    if not os.path.exists(home_dir_list[0] + "/MORB_MELTS_Files"):
        os.mkdir(home_dir_list[0] + "/MORB_MELTS_Files")
    else:
        shutil.rmtree(home_dir_list[0] + "/MORB_MELTS_Files")
        os.mkdir(home_dir_list[0] + "/MORB_MELTS_Files")
    if not os.path.exists(home_dir_list[0] + "/Completed_MORB_MELTS_Files"):
        os.mkdir(home_dir_list[0] + "/Completed_MORB_MELTS_Files")
    else:
        shutil.rmtree(home_dir_list[0] + "/Completed_MORB_MELTS_Files")
        os.mkdir(home_dir_list[0] + "/Completed_MORB_MELTS_Files")
    if "MORB_MELTS_Success_Log" in os.listdir(home_dir_list[0]):
        os.remove("MORB_MELTS_Success_Log")
    else:
        pass
    workbook = raw_input("Please enter your .xlsx workbook filename: ")
    if os.path.isfile(workbook):
        print("\n" + workbook + " has been found in the working directory!\n")
        dir1 = home_dir_list[0] + "/" + workbook
        dir2 = home_dir_list[0] + "/MORB_MELTS_Files/" + workbook
        shutil.copy(dir1, dir2)
        os.chdir(home_dir_list[0] + "/MORB_MELTS_Files/")
        pass
    else:
        print("\n" + workbook + " has NOT been found in the working directory!\n")
        morb_writefiles()
    xl_workbook = xlrd.open_workbook(workbook)
    sheet_names = xl_workbook.sheet_names()
    xl_sheet = xl_workbook.sheet_by_index(0)
    num_cols = xl_sheet.ncols
    print("Writing MORB MELTS files...\n")
    for j in range(xl_sheet.nrows):
        row = xl_sheet.row(j)
        #print row
        file_name = str(row[0].value)
        file_name_clipped = file_name[7:]
        melts_file = open(file_name_clipped.rstrip()+ '.MELTS', 'w')
        print("Writing MELTS file for: " + str(file_name_clipped) + "...")
        for i in range(num_cols):
            melts_file.write(str(row[i].value)+'\n')
        melts_file.close()
    os.remove(workbook)
    print("\nAll MORB MELTS files have been written!\n")
    run_morb()


def run_bsp():
    os.chdir(home_dir_list[0])
    print("\n\nPerforming BSP MELTS calculations...\n")
    os.chdir(home_dir_list[0] + "/BSP_MELTS_Files")
    for filename2 in glob("*.MELTS"):
        print("\n___________________________________________\n")
        thefile = str(filename2)
        print("Performing calculations on: " + thefile + "\n")
        time.sleep(2)
        dir1 = home_dir_list[0] + "/BSP_MELTS_Files/" + thefile
        dir2 = home_dir_list[0] + "/" + thefile
        shutil.move(dir1, dir2)
        os.chdir(home_dir_list[0])
        working_dir = home_dir_list[0]
        try:
            print("Opening alphaMELTS...\n")
            p = Popen(["run_alphamelts.command", "-f", "BSP_Env_File"], cwd=working_dir, stdin=PIPE)
            t = Timer(300, p.kill)
            t.start()
            print("\nTimeout timer started.  300 seconds until the loop continues...\n")
            p.communicate(input=b"\n".join([b"1", thefile, b"8", b"alloy-liquid", b"0", b"x", b"5", b"4", b"-1.4", b"2", b"2500", b"4200", b"4", b"1", b"0"]))
            t.cancel()
            print("Timeout timer cancelled...\n")
            if "alphaMELTS_tbl.txt" in os.listdir(home_dir_list[0]):
                oldname = "alphaMELTS_tbl.txt"
                newname = thefile + "_BSP_OUTPUT" + ".bsp"
                os.rename(oldname, newname)
                shutil.move(newname, home_dir_list[0] + "/Completed_BSP_MELTS_Files")
                os.remove(thefile)
                os.chdir(home_dir_list[0] + "/Completed_BSP_MELTS_Files")
                csv_file_name = newname[:-4] + "_CSVformat" + ".csv"
                with open(newname, 'rb') as infile, open(csv_file_name, 'wb') as outfile:
                    in_txt = csv.reader(infile, delimiter=" ")
                    out_csv = csv.writer(outfile)
                    out_csv.writerows(in_txt)
                    infile.close()
                    outfile.close()
                    os.remove(newname)
        except Exception:
            print("Problem with file: " + thefile)
            os.remove(thefile)
            pass
        print(thefile + " has been processed...\n")
    print("\n\n\nFinished with BSP calculations.  Exiting script...\n\n\n")
    print("________________________________________\n\n")




def run_morb():
    os.chdir(home_dir_list[0])
    print("\n\nPerforming MORB MELTS calculations...\n")
    os.chdir(home_dir_list[0] + "/MORB_MELTS_Files")
    for filename2 in glob("*.MELTS"):
        print("\n___________________________________________\n")
        thefile = str(filename2)
        print("Performing calculations on: " + thefile + "\n")
        time.sleep(2)
        dir1 = home_dir_list[0] + "/MORB_MELTS_Files/" + thefile
        dir2 = home_dir_list[0] + "/" + thefile
        shutil.move(dir1, dir2)
        os.chdir(home_dir_list[0])
        working_dir = home_dir_list[0]
        try:
            print("Opening alphaMELTS...\n")
            p = Popen(["run_alphamelts.command", "-f", "MORB_Env_File"], cwd=working_dir, stdin=PIPE)
            t = Timer(300, p.kill)
            t.start()
            print("\nTimeout timer started.  300 seconds until the loop continues...\n")
            p.communicate(input=b"\n".join([b"1", thefile, b"8", b"alloy-liquid", b"0", b"x", b"5", b"3", b"+0.4", b"2", b"1400", b"10000", b"10", b"1", b"3", b"1", b"liquid", b"1", b"0.07", b"0", b"10", b"0", b"4", b"0"]))
            t.cancel()
            print("Timeout timer cancelled...\n")
            if "alphaMELTS_tbl.txt" in os.listdir(home_dir_list[0]):
                oldname = "alphaMELTS_tbl.txt"
                newname = thefile + "_MORB_OUTPUT" + ".morb"
                os.rename(oldname, newname)
                shutil.move(newname, home_dir_list[0] + "/Completed_MORB_MELTS_Files")
                os.remove(thefile)
                os.chdir(home_dir_list[0] + "/Completed_MORB_MELTS_Files")
                csv_file_name = newname[:-4] + "_CSVformat" + ".csv"
                with open(newname, 'rb') as infile, open(csv_file_name, 'wb') as outfile:
                    in_txt = csv.reader(infile, delimiter=" ")
                    out_csv = csv.writer(outfile)
                    out_csv.writerows(in_txt)
                    infile.close()
                    outfile.close()
                    os.remove(newname)
        except Exception:
            print("Problem with file: " + thefile)
            os.remove(thefile)
            pass
        print(thefile + " has been processed...\n")
    print("\n\n\nFinished with MORB calculations.  Exiting script...\n\n\n")
    print("________________________________________\n\n")








initialization()
