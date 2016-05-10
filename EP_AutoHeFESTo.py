#!/usr/bin/env python

import os, shutil, subprocess, time, pipes, traceback, xlrd, sys, Timer
from subprocess import Popen, PIPE



home_dir_list = []
home_dir_list.append(os.getcwd())



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
print "_________________________________________"


def initialization():
    print "AutoHeFESTo" + "\n"
    print "Welcome to AutoHeFESTo..." + "\n"
    try:
        if "main" in os.listdir(home_dir_list[0]):
            print "'main' detected in the working directory.  HeFESTo is ready!" + "\n"
        else:
            print "'main' is NOT detected in the working directory!  HeFESTo is NOT ready and this script will NOT function properly!"
            pass
    except:
        print "\n" + "***" + "'main' is NOT detected in the working directory!  HeFESTo is NOT ready and this script will NOT function properly!" + "***" + "\n"
        pass
    print "Type 'bsp' to start the automation process or anything else to exit script..."
    print "***bsp = bulk silicate planet///morb = mid ocean ridge basalt***" + "\n"
    wait_for_begin = raw_input(">>> Please type 'bsp' or 'morb'... ")
    if wait_for_begin == 'bsp':
        print "\n" + "Performing BSP Calculations..." + "\n"
        makethedirs_bsp()
    elif wait_for_begin == 'morb':
        print "\n" + "Performing MORB Calculations..." + "\n"
        makethedirs_morb()
    else:
        print "Oops!  That's not a valid command!" + "\n"
        initialization()












#_____________________________________________________________________________________________MAKE DIRECTORIES
def makethedirs_bsp():
    if not os.path.exists(home_dir_list[0] + "/BSP_Control_Files"):
        print home_dir_list[0] + "/BSP_Control_Files' path not detected.  Creating..."
        os.makedirs(home_dir_list[0] + "/BSP_Control_Files")
    else:
        print home_dir_list[0] + "/BSP_Control_Files' path exists.  Deleting and recreating..."
        shutil.rmtree(home_dir_list[0] + "/BSP_Control_Files")
        os.makedirs(home_dir_list[0] + "/BSP_Control_Files")
    if not os.path.exists(home_dir_list[0] + "/BSP_Output_Files"):
        print home_dir_list[0] + "/BSP_Output_Files' path not detected.  Creating..."
        os.makedirs(home_dir_list[0] + "/BSP_Output_Files")
    else:
        print home_dir_list[0] + "/BSP_Output_Files' path exists.  Deleting and recreating..."
        shutil.rmtree(home_dir_list[0] + "/BSP_Output_Files")
        os.makedirs(home_dir_list[0] + "/BSP_Output_Files")
    if not os.path.exists(home_dir_list[0] + "/BSP_Output_Files/fort.66_files"):
        print home_dir_list[0] + "/BSP_Output_Files/fort.66_files' path not detected.  Creating..."
        os.makedirs(home_dir_list[0] + "/BSP_Output_Files/fort.66_files")
    else:
        print home_dir_list[0] + "/BSP_Output_Files/fort.66_files' path exists.  Deleting and recreating..."
        shutil.rmtree(home_dir_list[0] + "/BSP_Output_Files/fort.66_files")
        os.makedirs(home_dir_list[0] + "/BSP_Output_Files/fort.66_files")
    if not os.path.exists(home_dir_list[0] + "/BSP_Output_Files/fort.58_files"):
        print home_dir_list[0] + "/BSP_Output_Files/fort.58_files' path not detected.  Creating..."
        os.makedirs(home_dir_list[0] + "/BSP_Output_Files/fort.58_files")
    else:
        print home_dir_list[0] + "/BSP_Output_Files/fort.58_files' path exists.  Deleting and recreating..."
        shutil.rmtree(home_dir_list[0] + "/BSP_Output_Files/fort.58_files")
        os.makedirs(home_dir_list[0] + "/BSP_Output_Files/fort.58_files")
    if not os.path.exists(home_dir_list[0] + "/BSP_Output_Files/fort.59_files"):
        print home_dir_list[0] + "/BSP_Output_Files/fort.59_files' path not detected.  Creating..."
        os.makedirs(home_dir_list[0] + "/BSP_Output_Files/fort.59_files")
    else:
        print home_dir_list[0] + "/BSP_Output_Files/fort.59_files' path exists.  Deleting and recreating..."
        shutil.rmtree(home_dir_list[0] + "/BSP_Output_Files/fort.59_files")
        os.makedirs(home_dir_list[0] + "/BSP_Output_Files/fort.59_files")
    print "Moving on to input file creation..." + "\n"
    writeinputfiles_bsp()




def makethedirs_morb():
    if not os.path.exists(home_dir_list[0] + "/MORB_Control_Files"):
        print home_dir_list[0] + "/MORB_Control_Files' path not detected.  Creating..."
        os.makedirs(home_dir_list[0] + "/MORB_Control_Files")
    else:
        print home_dir_list[0] + "/MORB_Control_Files' path exists.  Deleting and recreating..."
        shutil.rmtree(home_dir_list[0] + "/MORB_Control_Files")
        os.makedirs(home_dir_list[0] + "/MORB_Control_Files")
    print "Moving on to input file creation..." + "\n"
    if not os.path.exists(home_dir_list[0] + "/MORB_Output_Files"):
        print home_dir_list[0] + "/MORB_Output_Files' path not detected.  Creating..."
        os.makedirs(home_dir_list[0] + "/MORB_Output_Files")
    else:
        print home_dir_list[0] + "/MORB_Output_Files' path exists.  Deleting and recreating..."
        shutil.rmtree(home_dir_list[0] + "/MORB_Output_Files")
        os.makedirs(home_dir_list[0] + "/MORB_Output_Files")
    if not os.path.exists(home_dir_list[0] + "/MORB_Output_Files/fort.66_files"):
        print home_dir_list[0] + "/MORB_Output_Files/fort.66_files' path not detected.  Creating..."
        os.makedirs(home_dir_list[0] + "/MORB_Output_Files/fort.66_files")
    else:
        print home_dir_list[0] + "/MORB_Output_Files/fort.66_files' path exists.  Deleting and recreating..."
        shutil.rmtree(home_dir_list[0] + "/MORB_Output_Files/fort.66_files")
        os.makedirs(home_dir_list[0] + "/MORB_Output_Files/fort.66_files")
    if not os.path.exists(home_dir_list[0] + "/MORB_Output_Files/fort.58_files"):
        print home_dir_list[0] + "/MORB_Output_Files/fort.58_files' path not detected.  Creating..."
        os.makedirs(home_dir_list[0] + "/MORB_Output_Files/fort.58_files")
    else:
        print home_dir_list[0] + "/MORB_Output_Files/fort.58_files' path exists.  Deleting and recreating..."
        shutil.rmtree(home_dir_list[0] + "/MORB_Output_Files/fort.58_files")
        os.makedirs(home_dir_list[0] + "/MORB_Output_Files/fort.58_files")
    if not os.path.exists(home_dir_list[0] + "/MORB_Output_Files/fort.59_files"):
        print home_dir_list[0] + "/MORB_Output_Files/fort.59_files' path not detected.  Creating..."
        os.makedirs(home_dir_list[0] + "/MORB_Output_Files/fort.59_files")
    else:
        print home_dir_list[0] + "/MORB_Output_Files/fort.59_files' path exists.  Deleting and recreating..."
        shutil.rmtree(home_dir_list[0] + "/MORB_Output_Files/fort.59_files")
        os.makedirs(home_dir_list[0] + "/MORB_Output_Files/fort.59_files")
    print  "\n" + "Moving on to input file creation..." + "\n"
    writeinputfiles_morb()








#_______________________________________________________________________________________________________WRITE CONTROL FILES
def writeinputfiles_bsp():
    xl_workbook = xlrd.open_workbook(raw_input(">>>Please enter your workbook name: "), 'rb')
    print "\n" + "Opening workbook..." + "\n"
    xl_sheet = xl_workbook.sheet_by_index(0)
    print ('Sheet name: %s' % xl_sheet.name)
    print "\n"
    num_cols = xl_sheet.ncols
    print "Writing BSP HeFESTo control files..." + "\n"
    for j in range(xl_sheet.nrows):
        row = xl_sheet.row(j)
        file_name = str(row[0].value)
        print "~Writing HeFESTo control file: " + str(file_name) + " ..." + "\n"
        control_file = open('control.' +file_name.rstrip() + '_bsp' + ".txt", 'w')
        for i in range(1,num_cols):
            num = row[i].value
            if i <=11:
                control_file.write(str(row[i].value)+'\n')
            else:
                #print num
                test = list(str(num))[0]
                #print test
                if test.isalpha() == True:
                    control_file.write(str(row[i].value)+'\n')
                else:
                    output = int(row[i].value)
                    control_file.write(str(output)+'\n')
        control_file.close()
        filename = 'control.' +file_name.rstrip() + '_bsp' + ".txt"
        fdir = home_dir_list[0] + "/" + filename
        tdir = home_dir_list[0] + "/BSP_Control_Files/" + filename
        shutil.move(fdir, tdir)
    else:
        print "BSP HeFESTo control files written..." + "\n"
    os.chdir(home_dir_list[0])
    if "fort.66" in os.listdir(home_dir_list[0]):
        os.remove("fort.66")
    else:
        pass
    if "fort.58" in os.listdir(home_dir_list[0]):
        os.remove("fort.58")
    else:
        pass
    if "fort.59" in os.listdir(home_dir_list[0]):
        os.remove("fort.59")
    else:
        pass
    if "control" in os.listdir(home_dir_list[0]):
        os.remove("control")
    else:
        pass
    run_hefesto_bsp()





def writeinputfiles_morb():
    xl_workbook = xlrd.open_workbook(raw_input(">>>Please enter your workbook name: "), 'rb')
    print "\n" + "Opening workbook..." + "\n"
    xl_sheet = xl_workbook.sheet_by_index(0)
    print ('Sheet name: %s' % xl_sheet.name)
    print "\n"
    num_cols = xl_sheet.ncols
    print "Writing MORB HeFESTo control files..." + "\n"
    for j in range(xl_sheet.nrows):
        row = xl_sheet.row(j)
        file_name = str(row[0].value)
        print "~Writing HeFESTo control file: " + str(file_name) + " ..." + "\n"
        control_file = open('control.' +file_name.rstrip() + '_morb' + ".txt", 'w')
        for i in range(1,num_cols):
            num = row[i].value
            if i <=11:
                control_file.write(str(row[i].value)+'\n')
            else:
                #print num
                test = list(str(num))[0]
                #print test
                if test.isalpha() == True:
                    control_file.write(str(row[i].value)+'\n')
                else:
                    output = int(row[i].value)
                    control_file.write(str(output)+'\n')
        control_file.close()
        filename = 'control.' +file_name.rstrip() + '_morb' + ".txt"
        fdir = home_dir_list[0] + "/" + filename
        tdir = home_dir_list[0] + "/MORB_Control_Files/" + filename
        shutil.move(fdir, tdir)
    else:
        print "MORB HeFESTo control files written..." + "\n"
    os.chdir(home_dir_list[0])
    if "fort.66" in os.listdir(home_dir_list[0]):
        os.remove("fort.66")
    else:
        pass
    if "fort.58" in os.listdir(home_dir_list[0]):
        os.remove("fort.58")
    else:
        pass
    if "fort.59" in os.listdir(home_dir_list[0]):
        os.remove("fort.59")
    else:
        pass
    if "control" in os.listdir(home_dir_list[0]):
        os.remove("control")
    else:
        pass
    run_hefesto_morb()













#_____________________________________________________________________________________________________RUN HEFESTO
def run_hefesto_bsp():
    for thing in os.listdir(home_dir_list[0] + "/BSP_Control_Files"):
        print "\n" + "Opening HeFESTo for " + str(thing) + "\n"
        time.sleep(2)
        if "control" in os.listdir(home_dir_list[0]):
            os.remove(home_dir_list[0] + "/control")
        else:
            pass
        if "fort.59" in os.listdir(home_dir_list[0]):
            os.remove(home_dir_list[0] + "/fort.59")
        else:
            pass
        if "fort.58" in os.listdir(home_dir_list[0]):
            os.remove(home_dir_list[0] + "/fort.58")
        else:
            pass
        if "fort.66" in os.listdir(home_dir_list[0]):
            os.remove(home_dir_list[0] + "/fort.66")
        else:
            pass
        os.chdir(home_dir_list[0] + "/BSP_Control_Files")
        print "Copying" + str(thing) + " to path" + home_dir_list[0] + "..." + "\n"
        todir = home_dir_list[0] + "/" + "control"
        copyfromdir = home_dir_list[0] + "/BSP_Control_Files/" + str(thing)
        shutil.copy(copyfromdir, todir)
        os.chdir(home_dir_list[0])
        #src = str(thing)
        #drc = "control"
        #os.rename(src, drc)
        print("Performing calculations on {thing!r} ...".format(**vars()))
        print "\n"
        print "\n" + "Opening HeFESTo for calculations on " + str(thing) + " ..." + "\n"
        print "\n"
        #working_dir = os.curdir()
        #Popen(["main"], cwd=working_dir, stdin=PIPE)
        argz = home_dir_list[0] + "/main"
        p = subprocess.Popen(argz, stdin=None, stdout=None)
        t = Timer(800, p.kill)
        print "\n" + "Timeout timer started.  800 seconds until the process is terminated and the loop continues..." + "\n"
        t.start()
        t.communicate()
        t.cancel()
        print "\n" + "Copying output files to " + home_dir_list[0] + "/BSP_Output_Files directory..." + "\n"
        try:
            os.remove("control")
        except:
            print "\n" + "Control file not found!" + "\n"
            pass
        if "fort.66" in os.listdir(home_dir_list[0]):
            print "\n" + "fort.66 found!" + "\n"
            theoutputfile66 = home_dir_list[0] + "/" + "fort.66"
            outputtodir66 = home_dir_list[0] + "/BSP_Output_Files/fort.66_files/" + "fort.66."+str(thing)+"_bsp"
            shutil.move(theoutputfile66, outputtodir66)
        else:
            print "fort.66." + str(thing) + " not found!"
            pass
        if "fort.58" in os.listdir(home_dir_list[0]):
            print "\n" + "fort.58 found!" + "\n"
            theoutputfile58 = home_dir_list[0] + "/" + "fort.58"
            outputtodir58 = home_dir_list[0] + "/BSP_Output_Files/fort.58_files/" + "fort.58."+str(thing)+"_bsp"
            shutil.move(theoutputfile58, outputtodir58)
        else:
            print "fort.58." + str(thing) + " not found!"
            pass
        if "fort.59" in os.listdir(home_dir_list[0]):
                print "\n" + "fort.59 found!" + "\n"
                theoutputfile59 = home_dir_list[0] + "/" + "fort.59"
                outputtodir59 = home_dir_list[0] + "/BSP_Output_Files/fort.59_files/" + "fort.59."+str(thing)+"_bsp"
                shutil.move(theoutputfile59, outputtodir59)
        else:
            print "fort.59." + str(thing) + " not found!"
            pass
        print "LOOP FINISHED FOR " + str(thing)
        time.sleep(2)
        #except Exception:
           # traceback.print_exc()
           # print "\n"
           # print "Calculation failure for " + str(thing) + ".  Moving on..."
           # print "\n"
    else:
        print "\n"
        print "Done with BSP HeFESTo calculations.  Exiting script..." + "\n\n\n\n"
        print "___________________________________________________________"
        print "\n"
  #  copydirs_bsp()







def run_hefesto_morb():
    for thing in os.listdir(home_dir_list[0] + "/MORB_Control_Files"):
        print "\n" + "Opening HeFESTo for " + str(thing) + "\n"
        time.sleep(2)
        if "control" in os.listdir(home_dir_list[0]):
            os.remove(home_dir_list[0] + "/control")
        else:
            pass
        os.chdir(home_dir_list[0] + "/MORB_Control_Files")
        print "Copying" + str(thing) + " to path " + home_dir_list[0] + "..." + "\n"
        todir = home_dir_list[0] + "/" + "control"
        copyfromdir = home_dir_list[0] + "/MORB_Control_Files/" + str(thing)
        shutil.copy(copyfromdir, todir)
        os.chdir(home_dir_list[0])
        #src = str(thing)
        #drc = "control"
        #os.rename(src, drc)
        print("Performing calculations on {thing!r} ...".format(**vars()))
        print "\n"
        print "\n" + "Opening HeFESTo for calculations on " + str(thing) + " ..." + "\n"
        print "\n"
        #working_dir = os.curdir()
        #Popen(["main"], cwd=working_dir, stdin=PIPE)
        argz = home_dir_list[0] + "/main"
        p = subprocess.Popen(argz, stdin=None, stdout=None)
        t = Timer(800, p.kill)
        print "\n" + "Timeout timer started.  800 seconds until the process is terminated and the loop continues..." + "\n"
        t.start()
        t.communicate()
        t.cancel()
        print "\n" + "Copying output files to" +  home_dir_list[0]+ "/MORB_Output_Files' directory..." + "\n"
        try:
            os.remove("control")
        except:
            print "\n" + "Control file not found!" + "\n"
            pass
        if "fort.66" in os.listdir(home_dir_list[0]):
            print "\n" + "fort.66 found!" + "\n"
            theoutputfile66 = home_dir_list[0] + "/" + "fort.66"
            outputtodir66 = home_dir_list[0] + "/MORB_Output_Files/fort.66_files/" + "fort.66."+str(thing)+"_morb"
            shutil.move(theoutputfile66, outputtodir66)
        else:
            print "fort.66." + str(thing) + " not found!"
            pass
        if "fort.58" in os.listdir(home_dir_list[0]):
            print "\n" + "fort.58 found!" + "\n"
            theoutputfile58 = home_dir_list[0] + "/" + "fort.58"
            outputtodir58 = home_dir_list[0] + "/MORB_Output_Files/fort.58_files/" + "fort.58."+str(thing)+"_morb"
            shutil.move(theoutputfile58, outputtodir58)
        else:
            print "fort.58." + str(thing) + " not found!"
            pass
        if "fort.59" in os.listdir(home_dir_list[0]):
                print "\n" + "fort.59 found!" + "\n"
                theoutputfile59 = home_dir_list[0] + "/" + "fort.59"
                outputtodir59 = home_dir_list[0] + "/MORB_Output_Files/fort.59_files/" + "fort.59."+str(thing)+"_morb"
                shutil.move(theoutputfile59, outputtodir59)
        else:
            print "fort.59." + str(thing) + " not found!"
            pass
        print "LOOP FINISHED FOR " + str(thing)
        time.sleep(2)
        #except Exception:
           # traceback.print_exc()
           # print "\n"
           # print "Calculation failure for " + str(thing) + ".  Moving on..."
           # print "\n"
    else:
        print "\n"
        print "Done with MORB HeFESTo calculations.  Exiting script..." + "\n\n\n\n"
        print "___________________________________________________________"
        print "\n"



initialization()
